import json,sys
C='../../../data/corpora/'
L={
'weisse-evangelische-geschichte-1838':[
 ("Weisse names the Papias witness","weisse-1838-i","des Bifhofs Papias von Hierapolis"),
 ("Weisse reads the Logia as a collection of sayings","weisse-1838-i","Erläuterungen der Logia des Herren"),
 ("Weisse: a collection only of speeches and sayings","weisse-1838-i","eine Sammlung nur von Reden und Aus")],
'holtzmann-synoptische-evangelien-1863':[
 ("Holtzmann's table of contents: the reconstruction of source A, his narrative Urmarcus","holtzmann-1863","AufsteUung  der  Quelle  A"),
 ("Holtzmann: a life of Jesus drawn from source A","holtzmann-1863","Lebensbild  Jesu  nach  der  Quelle  A"),
 ("Holtzmann: the composition of Mark, source A (Urmarcus)","holtzmann-1863","Quelle  A  (Urmarcus)"),
 ("Holtzmann: the collection of sayings as a second foundation","holtzmann-1863","Grundlage  der  Spruchsammlung")],
'wernle-synoptische-frage-1899':[
 ("Wernle names the source Q and calls it hypothetical","wernle-1899","Die — hypothetische — Quelle sei mit Q bezeichnet."),
 ("Wernle: the apocalypse beneath Mark 13, reconstructed","wernle-1899","zu Grunde liegende Apokalypse noch gekannt")],
'weiss-alteste-evangelium-1903':[
 ("J. Weiss: Mark the oldest gospel, no longer a hypothesis","weiss-1903","dass unser zweites das älteste Evangelium sei, ist keine Hypo"),
 ("J. Weiss: no longer a source, already a reservoir","weiss-1903","nicht mehr Quelle, sondern schon Sammelbecken.")],
'wellhausen-einleitung-1905':[
 ("Wellhausen: the source one designates Q","wellhausen-1905","Quelle,  die  man  mit  Q  bezeichnet")],
'harnack-spruche-und-reden-1907':[
 ("Harnack's subtitle: the second source of Matthew and Luke","harnack-1907","DIE ZWEITE QUELLE DES MATTHÄUS UND LUKAS"),
 ("Harnack: that one can establish the text of Q","harnack-1907","Text von Q feststellen kann")],
'streeter-four-gospels-1925':[
 ("Streeter: the hypothetical source referred to by general consent as Q","streeter-1925","hypothetical source is now by general consent referred to as"),
 ("Streeter: the Four Document Hypothesis","streeter-1925","The Four Document Hypothesis")],
}
for c,ls in L.items():
    f=f'spec35-{c}.json'; d=json.load(open(f)); out=[]
    for lab,item,find in ls:
        t=open(C+c+f'/text/{item}.ocr.txt',encoding='utf-8').read()
        n=t.count(find); assert n>=1,(c,find); out.append({"label":lab,"text":f"text/{item}.ocr.txt","find":find})
        print(c,n,find[:40])
    d['loci']=out; json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
