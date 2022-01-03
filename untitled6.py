file1 = open("qns.txt","r+") 
doc=file1.read()
con=doc
file1.close()

file1 = open("keyw.txt","r+") 
keys=file1.read()
file1.close()


res = keys.split()

newString=""
def format_sentence(sentence,k) :
    strs=" "
    sentenceSplit = filter(None, sentence.split("."))
    for s in sentenceSplit:
        st=str(s.strip() + ".")
        newString = st.replace(k,'-------')
        strs+=newString
    return strs

#print(type(keys))
#print(keys.split())

for k in keys.split():
    doc=format_sentence(doc,k)
print(doc)
print("\n")
print(keys.split())
print("\n")
print(con)