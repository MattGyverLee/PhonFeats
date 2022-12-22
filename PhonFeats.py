import panphon;
import os
import copy
#from ..minphonfeat import featuremin as minphonfeat
English = u"pʰ p b b̥ tʰ t ɾ d d̥ ɾ kʰ k ɡ ɡ̥̊ t̠ʃ d̠ʒ f v θ ð s z ʃ ʒ h m n ɾ ŋ l ɫ ɹ j w ɪ ɛ æ ɑ oʊ ʊ uː ʉː ʌ ɚː ə aɪ ɔɪ aʊ"
Simple = u"a e i o u m n l b p"
EngSegs = ["pʰ","p","b","b̥","tʰ","t","ɾ","d","d̥","ɾ","kʰ","k","ɡ","ɡ̥̊","t̠ʃ","d̠ʒ","f","v","θ","ð","s","z","ʃ","ʒ","h","m","n","ɾ","ŋ","l","ɫ","ɹ","j","w","ɪ","ɛ","æ","ɑ","oʊ","ʊ","uː","ʉː","ʌ","ɚː","ə","aɪ","ɔɪ","aʊ"]

simpleSegs = Simple.split(" ")

word = English
#word = u"p b m n"
segs = EngSegs

ft = panphon.FeatureTable()
SpaceSegs = English.split(" ")



""" for seg in segs:
    if ft.seg_known() """


if ft.validate_word(word): 
    print("String is valid IPA");
    if "a" in word:
        print(u"Did you mean 'ɑ' (U+0251), the open/low back unrounded vowel?")
else:
    print("String is invalid IPA");
    for l in word:
        if not ft.validate_word(l):
            print (" The phone '"+l+"' is invalid IPA.")
            if l == "g":
                print(u"  Did you mean ɡ (U+0261)?")
for seg in ft.segs_safe(word):
    if seg != " ":
        print(seg)
        print (ft.fts(seg))

print("")

#print ("syl son cons cont delrel lat nas strid voi sg cg ant cor distr lab hi lo back round velaric tense long hitone hireg") 
panphon_features = ["syl","son","cons","cont","delrel","lat","nas","strid","voi","sg","cg","ant","cor","distr","lab","hi","lo","back","round","velaric","tense","long","hitone","hireg"]
tab = "\t"
print("ipa\t" + tab.join(panphon_features))
vecTable = {}
with open('phontable.txt', 'w', encoding='UTF-8') as f:
    f.write("\t" + tab.join(panphon_features)+"\r\n")
    #vecTable.append(["labels",panphon_features])
    vecTable.update({"feats": panphon_features})
    for seg in ft.segs_safe(word):
        if seg != " ":
            # This is the table-form
            vec = ft.segment_to_vector(seg)
            print(seg + "\t" + tab.join(vec))
            f.write(seg + "\t" + tab.join(vec) + "\r\n")
            vecTable.update({seg: vec})


delIdx = []
for i in range(0,len(panphon_features)):
    
    diff = False
    val = ""
    for key in vecTable:
        if key != "feats":
            if (vecTable[key][i] != val):
                if val == "":
                    # set initial value
                    val = vecTable[key][i]
                else:
                    diff = True
                    break 
    else:
        print("Discarding: " + panphon_features[i] + " from minimal table.")
        delIdx.append(i)
        
vecTableMin = copy.deepcopy(vecTable)
#for j in range(len(panphon_features),0,-1):
delIdx.sort(reverse = True)
for idx in delIdx:
    for key in vecTable:       
        del vecTableMin[key][idx]

with open('phontablemin.txt', 'w', encoding='UTF-8') as f:
    for key in vecTableMin:
        if key == "feats":
            f.write("\t" + tab.join(vecTableMin[key])+"\r\n")
        else: 
            f.write(key + "\t" + tab.join(vecTableMin[key])+"\r\n")
    
comma = ","               
#alpha = comma.join(segs)
alpha = "m,n"
cmd = "python ../minphonfeat/featuremin.py phontablemin.txt " + alpha

os.system(cmd)


