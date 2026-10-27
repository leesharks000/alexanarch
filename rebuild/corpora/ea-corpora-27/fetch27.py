import json,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from seat import fetch
import urllib.parse
I=json.load(open(pathlib.Path(__file__).with_name('items.json')))
root=pathlib.Path(sys.argv[1])
for corpus,items in I.items():
    for it in items:
        if it['kind']=='ia':
            for fn in it['files']:
                fetch(f"https://archive.org/download/{it['identifier']}/{urllib.parse.quote(fn)}",root/corpus/'original'/it['identifier']/fn)
        else:
            fetch(it['url'],root/corpus/'original'/it['path'])
        print('ok',corpus,it['slug'],flush=True)
print('FETCHDONE')
