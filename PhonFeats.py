import panphon;
import panphon.distance
import os
import copy
#from ..minphonfeat import featuremin as minphonfeat
segs = []
with open('input/testInventory.txt', "r", encoding="utf-8") as f:
    lines = [line for line in f]
    segs = str(lines[0].strip()).split(" ")

ft = panphon.FeatureTable()

for seg in segs:
    if len(ft.segs_safe(seg)) > 1:
        print (" The phone '" + seg + "' is too complex.")
    elif not ft.seg_known(seg):
        print (" The phone '"+ seg +"' is invalid IPA.")
        if seg == "g":
            print(u"  Did you mean ɡ (U+0261)?")
    if "a" in seg:
        print(u"You wrote 'a'. Did you mean 'ɑ' (U+0251), the open/low back unrounded vowel?")
    

print("")

#print ("syl son cons cont delrel lat nas strid voi sg cg ant cor distr lab hi lo back round velaric tense long hitone hireg") 
panphon_features = ["syl","son","cons","cont","delrel","lat","nas","strid","voi","sg","cg","ant","cor","distr","lab","hi","lo","back","round","velaric","tense","long","hitone","hireg"]
tab = "\t"
print("ipa\t" + tab.join(panphon_features))
vecTable = {}
if not os.path.exists("output"):
    os.makedirs("output")
with open('output/phontablemax.txt', 'w', encoding='UTF-8') as f:
    f.write("\t" + tab.join(panphon_features)+"\n")
    #vecTable.append(["labels",panphon_features])
    vecTable.update({"feats": panphon_features})
    for seg in segs:
        if seg != " ":
            # This is the table-form
            vec = ft.segment_to_vector(seg)
            print(seg + "\t" + tab.join(vec))
            f.write(seg + "\t" + tab.join(vec) + "\n")
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
        print("Discarding '" + panphon_features[i] + "' from minimal table.")
        delIdx.append(i)
        
vecTableMin = copy.deepcopy(vecTable)
#for j in range(len(panphon_features),0,-1):
delIdx.sort(reverse = True)
for idx in delIdx:
    for key in vecTable:       
        del vecTableMin[key][idx]

with open('output/phontablemin.txt', 'w', encoding='UTF-8') as f:
    for key in vecTableMin:
        if key == "feats":
            f.write("\t" + tab.join(vecTableMin[key])+"\n")
            print("\t" + tab.join(vecTableMin[key])+"\n")
        else: 
            f.write(key + "\t" + tab.join(vecTableMin[key])+"\n")
            print(key + "\t" + tab.join(vecTableMin[key])+"\n")
distinct = True

for key in vecTableMin:       
        for compareKey in vecTableMin:
            if key != "feats" and compareKey != "feats" and key != compareKey:
                if vecTableMin[key] == vecTableMin[compareKey]:
                    print("'" + key + "' and '" + compareKey + "' are not distinct!")

compare = []
dst = panphon.distance.Distance()
xs = list(vecTableMin.keys())
compare.append(xs)
for x in vecTableMin:
    if x != "feats":
        vals = []
        for y in vecTableMin:
            if y != "feats":
                if dst.weighted_feature_edit_distance(x,y) != 0:
                    vals.append(dst.weighted_feature_edit_distance(x,y))
                else: 
                    vals.append("-")
        vals.insert(0, x)
        compare.append(vals)
        
with open('output/phondistmin.txt', 'w', encoding='UTF-8') as f:
    for l in compare:
        ls = [str(l) for l in l]
        f.write(tab.join(ls)+"\n")
# print(compare)


comma = ","               
#alpha = comma.join(segs)
# alpha = "m,n"
alpha = "ɪ,ɛ,æ,ɑ,ʊ,uː,ʉː,ʌ,ə"
cmd = "python featuremin.py output/phontablemin.txt " + alpha

os.system(cmd)



