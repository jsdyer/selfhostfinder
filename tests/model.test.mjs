import test from 'node:test';import assert from 'node:assert/strict';import {selectProjects,validateSaved,safeURL,csv} from '../web/model.mjs';
const p=(id,name,archived=false)=>({id,name,description:'Feed library',categories:['Feeds'],platforms:['Docker'],licences:['MIT'],archived,updated:'2026-01-01'});
test('filters arbitrary new projects and preserves input',()=>{const rows=[p('a','Alpha'),p('new','New reader'),p('z','Archived',true)];assert.deepEqual(selectProjects(rows,{query:'reader',platform:'Docker',active:true}).map(p=>p.id),['new']);assert.equal(rows.length,3);assert.equal(selectProjects(rows,{saved:true},['new']).length,1);assert.equal(selectProjects(rows,{active:true}).length,2);});
test('storage rejects invalid IDs and deduplicates',()=>assert.deepEqual(validateSaved(['a','a',{},'<script>','new']),['a','new']));
test('untrusted links are restricted',()=>{assert.equal(safeURL('javascript:alert(1)'),null);assert.equal(safeURL('https://user:secret@evil.test'),null);});
test('CSV quotes fields and guards formulas',()=>assert.match(csv([{...p('a','=CMD()'),website:'https://example.org',source:null}]),/"'=CMD\(\)"/));
