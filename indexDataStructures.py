"""
These are the two classes for the two indexes
"""


class PositionalIndex:
  def  __init__ (self):
    self.index={}#dictionary


  def insert(self,term: str, docID: int, positions: list):
    positions=set(sorted(positions))#sort the positions and make set
    if (term not in self.index):#to insert a new term in dictionary
      self.index[term]={docID:positions}
      return

    if (docID not in self.index[term]):#new docment for a term(already in dict)
      """
      get the previous entries of the term and insert the new doc into theses
      then sort the entries and insert into dictionary
      """
      tempDict=self.index[term]
      tempDict[docID]=positions
      tempDict=dict(sorted(tempDict.items()))
      self.index[term]=tempDict
      return

    """
    we insert a new position for a a given documnet for a given term
    we get the old positions for the documnet and insert the new positions
    then sort these positions and update the dictionary
    """
    tempPositions=self.index[term].get(docID)
    tempPositions.update(positions)
    tempPositions=set(sorted(tempPositions))
    self.index[term][docID]=tempPositions#insert new position for an existing term and doc
    


  def getAllDocs(self, term:str):#return all the docs for for a given term
    if(term in self.index):
      return self.index[term]
    else:
      return None


  def checkDifference(self, arr1,arr2,proximity:int):
    arr1=list(arr1)
    arr2=list(arr2)
    arr1.sort()
    arr2.sort()
    p1=0
    p2=0
    correctPos=set()#to store all the correct positions
    while(p1<len(arr1) and p2<len(arr2)):
      val1=arr1[p1]
      val2=arr2[p2]
      if(val1==val2):#both are equal which cant be possible for a given doc
        p1+=1
        p2+=1
      elif(val1<val2):
        diff=val2-val1
        if(diff<=proximity):
          correctPos.add(val2)
          p2+=1
        else:
          p1+=1
      else:
        p2+=1
    return correctPos


  def getValidDocs(self, terms:list, proximity:int=1)->list:
    docs=[]
    for term in terms:#get all the documents for all the terms
      doc=self.getAllDocs(term)
      if(doc!=None):
        docs.append(doc)
      
      

    if(len(docs)<1):
      return []

    result=[]
    for key in docs[0].keys():#store the first set of docs to compare with the rest
      result.append(key)

    length=len(result)
    tempResult=docs[0]
    docs.pop(0)

    for doc in docs:#compare all docs
      check=doc
      i=0
      while(i<length):
        docID=result[i]
        if(docID in check):#if both sets of words have the same docs we check the the positions
          arr1=tempResult[docID]
          arr2=check[docID]
          correctPos=self.checkDifference(arr1,arr2,proximity)#we call the function to check the position

          if(len(correctPos)<1):#if no match we update list and move forward
            tempResult.pop(docID)
            if docID in check:
             check.pop(docID)
            result.pop(i)
            length-=1
          else:#match found so we store the result and search for more
            """
            here we store the last correct positions so that we can compare n terms
            t1, t2-> result of t2 is stored so we can do
            t2(previous result), t3 -> we then store t3 and so on
            this helps reduce/eleminate false positives
            """
            tempResult[docID]=set(sorted(correctPos))
            i+=1
        else:#if the docs dont match we update list and move forward
          tempResult.pop(docID)
          result.pop(i)
          length-=1
    return result


class InvertedIndex:
  def __init__(self):
    self.index={}
    self.universalSet=set()#universel set of documnets for not operations

  def createIndex(self,positionalIndex):
    """
    we create inverted index using positional index.
    we first creat/read positional index and the positional index has all the info we need to create the inve index
    """
    for key in positionalIndex.keys():#simply iterate and store keys,docs only
      docs=[]
      for doc in positionalIndex[key].keys():
        docs.append(doc)
      self.index[key]=set(docs)
      self.universalSet.update(docs)
    # print(self.index)


  def getDocs(self, terms, operators):
    docs=[]
    i=0
    flag=False
    """
    the first loop here makes a single string and deals with all the 'not-terms'
    the string created is in the format t1 and t2 or t3 ...
    """
    for term in terms:#for all the query terms
        docTerm=set([])#incase the term doesnt exist we use an empty set
        if(term in self.index):
            docTerm=self.index[term]

        #not operator appers before a term so we deal with it first. Universal - term
        if(i<len(operators) and operators[i].lower()=='not'):
            docs.append(self.universalSet.difference(docTerm))
            flag=True
            i+=1

        if(i==0):#special case for appending the documnet
            docs.append(docTerm)
            flag=True

        if(i<len(operators)):#append the operator and the term(if appropriate)
            docs.append(operators[i].lower())
            i+=1
            if(flag):
                flag=False
                continue
        if(not flag):
            docs.append(docTerm)


    #incase of null set/no docs
    if(len(docs)<1):
      return None
    result=set(docs[0])
    docs.pop(0)
    i=0
    """
    here we go over the newly created string and create the resultant doc set
    we use set operaions intersection(and) and or(union)
    this is where the empty set for invalid terms comes in handy
    """
    while(i<len(docs)):
      if(i+1>=len(docs)):
        docs.append(set([]))
      if(docs[i]=='and'):
        result.intersection_update(docs[i+1])
        i+=2
      else:
        result=result.union(docs[i+1])
        i+=2
    return result

