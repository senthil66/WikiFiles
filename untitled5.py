from nltk import tokenize
from operator import itemgetter
import math
import bs4 as bs
import urllib.request
import re
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

search_keywords=[]
scrapped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Sachin_Tendulkar')
article = scrapped_data .read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

#print(article_text)   
 
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(article_text)
#print(sentence_list)

stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1
            
maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 20:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#print(sentence_scores)

import heapq
summary_sentences = heapq.nlargest(50, sentence_scores, key=sentence_scores.get)

doc = ' '.join(summary_sentences)
#print(summary_sentences, sep = "\n")

#print(type(summary_sentences))
#for s in summary_sentences:
    #print(s)
    
text_tokens = word_tokenize(doc)

#cword = [word for word in text_tokens if not word in stopwords.words()]

#print(type(doc))

val=1
for sen in summary_sentences:
    #print(val,sen)
    val+=1
    
total_words = doc.split()
total_word_length = len(total_words)
#print(total_word_length)

total_sentences = tokenize.sent_tokenize(doc)
total_sent_len = len(total_sentences)
#print(total_sent_len)

tf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in tf_score:
            tf_score[each_word] += 1
        else:
            tf_score[each_word] = 1

# Dividing by total_word_length for each dictionary element
tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
#print(tf_score)

def check_sent(word, sentences): 
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))
idf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in idf_score:
            idf_score[each_word] = check_sent(each_word, total_sentences)
        else:
            idf_score[each_word] = 1

# Performing a log and divide
idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

#print(idf_score)

tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
#print(tf_idf_score)

def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result

dic=get_top_n(tf_idf_score, 75)

file1 = open('keyw.txt', 'w')
for v in dic:
    if len(v) > 3:
        wiki = TextBlob(str(v))
        for e,val in wiki.tags:
            if(val == 'NN' or val == 'NNS' or val == 'NNPS' or val == 'NNP'):
                search_keywords.append(e)
    
for s in search_keywords:
    file1.writelines(s+"\n")
file1.close()
 
#print(search_keywords)
file1 = open('qns.txt', 'w')
for sentence in summary_sentences:
        vz=sum(1 for word in search_keywords if word in sentence)
        if  (int(vz))>=2 and(int(vz))<=4:
            file1.write(sentence + "\n")
file1.close()