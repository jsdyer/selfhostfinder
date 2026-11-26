import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from collect import normalize,url
class CollectTests(unittest.TestCase):
 def test_new_application_and_missing_activity(self):
  r=normalize('new-app',{'name':'New App','website_url':'https://example.org','licenses':['MIT'],'platforms':['Docker'],'tags':['New category']},{})
  self.assertEqual(r['id'],'new-app');self.assertIsNone(r['updated']);self.assertIsNone(r['requirements']);self.assertFalse(r['archived'])
 def test_unsafe_urls(self):
  self.assertIsNone(url('javascript:alert(1)'));self.assertIsNone(url('https://user@example.org'))
 def test_invalid_input_rejected(self):
  with self.assertRaises(ValueError):normalize('bad',{'name':'Bad','website_url':'javascript:x'},{})
