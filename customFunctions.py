import nltk
import re
import string
import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')

#to read the reasearch papers/stopword file
def getFileContent(fileLocation):#ResearchPapers/1.txt
  fileContent=""
  if os.path.exists(fileLocation):
    with open(fileLocation,'r',encoding='latin-1') as f:
      fileContent=f.read()
    return fileContent
  else:
    return ""
  
#save the positional index to hardrive in .pickle format
def saveToLocal(proxIndex):
  with open('./Index.pickle','wb') as f:
    pickle.dump(proxIndex,f)
  return True

"""
if the file exists read that and return the index
since the set is static we dont need to check for the update status of the file
"""
def readFromLocal():
  if os.path.exists('./Index.pickle'):
    with open('./Index.pickle','rb') as f:
      proxIndex=pickle.load(f)
    return proxIndex
  return None

  
ps = PorterStemmer()
#convert the string into two array of operands and operatiors
def procBooleanQuery(query):
  query=query.split(" ")
  terms=[]
  operators=[]
  for i in query:
    i=i.lower()
    if(i=='not' or i=='and' or i=='not'):
      operators.append(i)
    elif(i!=''):#to avoid and empty string generated due to extra/random spaces
      terms.append(ps.stem(i))
  return terms,operators


#convert the string into an array of operands/terms and the proximity
def procProximityQuery(query):
  query=query.split(" ")
  terms=[]
  k=1#if the query doesnt contain the proximity we assume 1
  for i in query:
    i=i.lower()
    if(i.isalpha()):
      terms.append(ps.stem(i))
    elif(i!=''):#to avoid and empty string generated due to extra/random spaces
      k=int(i[1:])
  return terms,k


def tokenizeAndClean(fileContent, stopWords):
  tokens = word_tokenize(fileContent) #run the tokenizer for the words
  uselessWords=['by','me','etc','or','but','not','and']#additional list of words
  i=0
  #to go over the terms and run basic modification
  while i<len(tokens):#for case folding+puchtuation
    token=tokens[i]
    token=token.lower()#case fold
    #split words with puctuation into mulitiple words and include them in the tokken set
    words = re.sub('['+string.punctuation+']', ' ', token)#replace puctutation with space
    words=words.split(' ')#break into words and add to the token lists at the right pace
    tokens.pop(i)
    tokens=tokens[:i]+words[:]+tokens[i:]#put them in the right position to maintian proximity index
    i+=1


  i=0
  #get rid of the numbers and deal with words with numbers by breaking into smaller words
  while i<len(tokens):
    token=tokens[i]
    #handle words with numbers/numbers
    if re.search(r'\w*\d\w*', token):  #the token contains any numbers
      word=""
      words=[]
      k=0
      for j in token:#split into smaller words for further processing
        if(not j.isdigit()):#store words and discard numbers
          word+=j
        elif (word!=""):
          words.append(word)
          word=""
          k+=1

      if(word!=""):#make sure there isnt a word in temp variable
        words.append(word)
        k+=1
     
      tokens.pop(i)#delete the current token to replace with the new words
      tokens=tokens[:i]+words[:]+tokens[i:]#add the words in the correct place to maintain position
      i+=k
      # tokens.extend(words)
      continue
    else:
      tokens[i]=token
      i+=1

  i=0
  while i<len(tokens):
    token=tokens[i]
    #handle words with special characters
    if re.search(r'\w*[!@#\$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]\w*', token):#the word contains a special char
      token = re.sub(r'[!@#\$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', ' ', token)#remove the char
      words=token.split(' ')#split into smaller words
      tokens.pop(i)
      tokens=tokens[:i]+words[:]+tokens[i:]#put them in the right position to maintian proximity index
    if re.search(r'\w*[\x91-\x99]\w*', token):#do the same for escape character?(like quotes etc)
      words = re.sub(r'[\x91-\x99]', ' ', token)
      words=words.split(' ')
      tokens.pop(i)
      tokens=tokens[:i]+words[:]+tokens[i:]
    i+=1


  #after modifiying the the tokens we run them though the filter
  cleanedTokens={}
  index=0#to maintain the position
  for token in tokens:#process the tokens/clean
    #the token is a stop word or custom made useless word
    flag=False
    for stopword in stopWords: 
      if(stopword==token):
        flag=True
    for uselessword in uselessWords:
      if(uselessword==token):
        flag=True

    if(flag):#the word belongs to either of the mentioned lists
      index+=1
      continue
    
    elif (len(token)<=1): #the token is a single charachter or empty string(special case/exception)
      index+=1
      continue
   
    #if it passes all previous filters then place it in the dictionary
    if(token in cleanedTokens):#already present in the dictionary
      arr=cleanedTokens[token]
      arr.append(index)
      cleanedTokens[token]=arr
    else:
      cleanedTokens[token]=[index]
    index+=1
  return cleanedTokens

  # print('Length After: ' + str(len(tokens)))
  # print(tokens)
#   return tokens

# content = getFileContent('ResearchPapers/12.txt')
# stopWords= getFileContent('Stopword-List.txt') #get a preset list
# stopWords=word_tokenize(stopWords)

# cleanedWords=tokenizeAndClean(content,stopWords)
# # print(name)
# print(cleanedWords)