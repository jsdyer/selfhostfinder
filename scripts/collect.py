"""Normalize a pinned checkout of awesome-selfhosted-data; no per-project requests."""
import argparse,json,re,subprocess,shutil
from datetime import date,datetime,timezone
from pathlib import Path
from urllib.parse import urlsplit
import yaml
ROOT=Path(__file__).resolve().parents[1]
def url(v):
    if not isinstance(v,str):return None
    p=urlsplit(v)
    return v if p.scheme in ('https','http') and p.hostname and not p.username and not any(c.isspace() for c in v) else None
def day(v):
    if isinstance(v,date):return v.isoformat()
    if isinstance(v,str):
        try:return date.fromisoformat(v).isoformat()
        except ValueError:pass
    return None
def normalize(slug,item,recipes):
    if not isinstance(item,dict) or not isinstance(item.get('name'),str) or not url(item.get('website_url')):raise ValueError('Invalid software record: '+slug)
    def strings(key):
        value=item.get(key,[])
        if not isinstance(value,list) or not all(isinstance(x,str) for x in value):raise ValueError('Invalid '+key+': '+slug)
        return sorted(set(value))
    release=item.get('current_release') or {}
    return {'id':slug,'name':item['name'],'description':str(item.get('description','')),'website':url(item.get('website_url')),'source':url(item.get('source_code_url')),'demo':url(item.get('demo_url')),'licences':strings('licenses'),'platforms':strings('platforms'),'categories':strings('tags'),'updated':day(item.get('updated_at')),'archived':item.get('archived') is True,'release':str(release.get('tag','')),'release_date':day(release.get('published_at')),'recipe':recipes.get(slug),'requirements':None}
def collect(source):
    config=json.loads((ROOT/'config/catalogue.json').read_text())
    sha=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
    commit_date=subprocess.check_output(['git','-C',str(source),'show','-s','--format=%cI','HEAD'],text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}',sha):raise ValueError('Invalid source revision')
    rows=[]
    for path in sorted((source/'software').glob('*.yml')):
        item=normalize(path.stem,yaml.safe_load(path.read_text()),config['recipe_ids'])
        if not(config['exclude_archived'] and item['archived']):rows.append(item)
    if not rows:raise ValueError('Empty catalogue; keeping previous edition')
    ids=[r['id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate project identifiers')
    out={'schema':'coolcode.selfhostfinder.v1','checked_at':datetime.now(timezone.utc).isoformat(),'source':config['repository'],'source_commit':sha,'source_committed_at':commit_date,'licence':'CC BY-SA 3.0','adaptation':'Fields selected, renamed and normalized from the community catalogue. Requirements are not supplied or inferred.','projects':rows}
    dest=ROOT/'web/data';dest.mkdir(exist_ok=True)
    tmp=dest/'catalogue.json.tmp';tmp.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n');tmp.replace(dest/'catalogue.json')
    for name in ['LICENSE','AUTHORS']:shutil.copyfile(source/name,dest/(name+'.txt'))
    print(f'Captured {len(rows)} projects at source commit {sha}')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',required=True,type=Path);collect(p.parse_args().source_dir)
