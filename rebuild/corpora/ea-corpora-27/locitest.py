import sys,json,pathlib,re
root=pathlib.Path('/home/claude/stage27')
C=json.load(open(sys.argv[1]))
for corpus,lst in C.items():
    for path,find in lst:
        t=" ".join((root/corpus/'original'/path).read_text(encoding='utf-8',errors='replace').split())
        print('OK ' if " ".join(find.split()) in t else 'NO ',corpus,path.split('/')[-1],'|',find)
