import nltk
import indexDataStructures as ds
import customFunctions as cf
import PySimpleGUI as sg
import gui
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')

if __name__=='__main__':
    """
    The first part is to make/read the positional index. Since it contains more info
    than the inverted index(contains position along with the doc), it can be used to
    create the inverted index
    We only pass the docs once due to this
    After this the code is for the gui logic
    """
    posIndex=ds.PositionalIndex()#positional index object
    ps = PorterStemmer()
    val=cf.readFromLocal()#try to read stored index
    if(val!=None):#if we can read it
        posIndex.index=val

    else:#make new index if we cant read the old one/does not exist
        files=['1','2','3','7','8','9','11','12','13','14','15','16','17','18','21','22','23','24','25','26']
        for i in files:#parse each file and insert into index one file at a time
            content= cf.getFileContent('./ResearchPapers/'+i+'.txt')#read the file
            stopWords= cf.getFileContent('Stopword-List.txt') #get a preset stopword list
            stopWords=word_tokenize(stopWords) #toeknize the stopwords
            cleanedWords=cf.tokenizeAndClean(content,stopWords) # clean the tokens(numbers/punctuations/special characters/stop words)
            for key in cleanedWords.keys():#store the cleaned words in the index
                word=ps.stem(key)#porter stemmer
                posIndex.insert(word,i,cleanedWords[key])#insert into index
        
        cf.saveToLocal(posIndex.index)#save the positional index to local disk
    
    #create the inverted index using positional index
    invIndex=ds.InvertedIndex()
    invIndex.createIndex(posIndex.index)

    """
    Now both indexes are ready so we get to the gui part and taking the input from the user
    """
    sg.theme('DarkAmber')
    window = sg.Window('Information Retrieval', gui.layout, element_justification='center', scaling=1.5)#create window
    while True:                      # Event Loop to process "events" and get the "values" of the inputs
        event, values = window.read()
        if event == sg.WIN_CLOSED:   # if user closes window or event=='cancel'
            break
        elif event=="-run_boolean-" and values["-query_boolean-"]:  #boolean query button pressed and box not empty
            terms,operators=cf.procBooleanQuery(values['-query_boolean-'])#convert string query to two array of terms and opertaors
            ans=invIndex.getDocs(terms,operators)#get the result of the query
            """
            ans has the final result(array of documents)
            the bottom lines are for formatting and printing the result in the ouput window
            same is the case for the next elif statement
            """
            ansString=""
            if(ans!=None and len(ans)>=1):
                arr=[]
                for i in ans:
                    arr.append(int(i))
                arr.sort()
                for i in arr:
                    ansString+=str(i)+", "
                ansString=ansString[:-2]
            resultText=f"For Query: {values['-query_boolean-']}\nDocuments: {ansString}"
            sg.popup(resultText,title="Query Result")

        elif event=="-run_proximity-" and values["-query_proximity-"]:  #proximity button pressed and box not empty
            #instead of operators, we have proximit(k) over here
            terms,k=cf.procProximityQuery(values['-query_proximity-'])
            ans=posIndex.getValidDocs(terms,k)
            ansString=""
            if(ans!=None and len(ans)>=1):
                arr=[]
                for i in ans:
                    arr.append(int(i))
                arr.sort()
                for i in arr:
                    ansString+=str(i)+", "
                ansString=ansString[:-2]
            resultText=f"For Query: {values['-query_proximity-']}\nDocuments: {ansString}"
            sg.popup(resultText,title="Query Result")

    #close the window when we come out of the loop
    window.close()


















    # val=posIndex.getValidDocs(['past','research'],3)
    # print(val)
    # print(len(posIndex.index))
    # # print(posIndex.index)
    # # for key in posIndex.index.keys():
    # #   print(f"{key} : {posIndex.index[key]}")

    # # print(len(posIndex.index))


    # print(f"cancer,learning \t{invIndex.getDocs([ps.stem('cancer'),ps.stem('learning')],['and'])}")
    # print(f"model\t {invIndex.getDocs([ps.stem('model')],['not'])}")
    # print(f"transformer AND model {invIndex.getDocs([ps.stem('transformer'),ps.stem('model')],['and'])}")
    # print(f"transformer OR model  {invIndex.getDocs([ps.stem('transformer'),ps.stem('model')],['or'])}")
    # print(f"heart AND attack {invIndex.getDocs([ps.stem('heart'),ps.stem('attack')],['and'])}")
    # print(f"heart \t {invIndex.getDocs([ps.stem('heart')],[])}")
    # print(f"feature AND selection AND redundency {invIndex.getDocs([ps.stem('feature'),ps.stem('selection'),ps.stem('redundency')],['and','and'])}")
    # print(f"feature AND selection AND classification  {invIndex.getDocs([ps.stem('feature'),ps.stem('selection'),ps.stem('classification')],['and','and'])}")
    # print(f"NOT classification  AND NOT feature {invIndex.getDocs([ps.stem('classification'),ps.stem('feature')],['not','and','not'])}")
    # print(f"tubing \t{invIndex.getDocs([ps.stem('tubing')],[])}")