from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
# from pdf2image import convert_from_path
import pyrebase
import os
from PyPDF2 import PdfFileReader
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\Supraja\\Downloads\\Evaluation\\Evaluation.json"

global grade

#Firebase connection
def someFunc(request):
    
    def isUsefulWord(text):
        stop_words = set(stopwords.words('english'))
       # word_tokens = word_tokenize(text)
       # filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
       #for w in word_tokens:
        for w in text:
            if w not in stop_words:
                #return true
                filtered_sentence.append(w)
        return filtered_sentence

    """"To detect the input image ocr in GCP"""
    def detect_document(content):
        from google.cloud import vision
        from google.cloud.vision import types
        client = vision.ImageAnnotatorClient()
        #print(content)
        image = vision.types.Image(content=content)
        response = client.document_text_detection(image=image)
        texts = response.full_text_annotation.text
        answer = texts.split()
        anslist = isUsefulWord(answer)
        # texts = response.text_annotations
       # print("Answer:",anslist)
        return anslist

    def read_keywords():
        pdfFileObj = open('C:\\Users\\Supraja\\Downloads\\_Keys\\key1.pdf','rb')
        #print(pdfFileObj)
        pdfReader = PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        notes = pageObj.extractText()
        #print(notes)
        keywords = notes.split()
        #print(keywords)
        keylist = isUsefulWord(keywords)
        #print("Keywords:",keylist)
        return keylist


        """""Compares pdf key and ocr'd image - answer"""  
    def compareans(anslist,keylist):
        matches = [item for item in keylist if item in anslist]
       # print("Matched:",matches)
        return matches
        #calculatemarks(len(matches),len(keylist))
    
        """"Calculates marks for each answer based on matches"""
    def calculateMarks(matches,keylen):
        
        print("Matches:",matches)
        print("Keylength:",keylen)
        totalmarks = 13
        Marks = (matches/keylen)*totalmarks
        #print("Total marks:"+str(Marks))
        #print("Total marks:"+str((obtained/given)*totalmarks))
        return(Marks)

    def getGrade(Total):
        if Total > 90:
            return "A"
        elif (Total > 80) and (Total < 91):
            return "B"
        elif (Total > 70) and (Total < 81):
            return "C"
        elif (Total > 60) and (Total < 71):
            return "D"
        elif (Total > 50) and (Total < 61):    
            return "E"
        else:      
            return "RA"

        """"Calculates Grade based on total marks"""
        
        

    inputPath = r"C:\\Users\\Supraja\\Downloads\\_Answers\\"
    #print("works")
    print(os.listdir(inputPath))
    listFiles = []
    listFiles = os.listdir(inputPath)
    result = []
    Tot = 0
    keyList = read_keywords()

    for i in listFiles:
        inputImagePath = inputPath+i
           # print(inputImagePath)
        with open(inputImagePath, 'rb') as image_file:
            content = image_file.read()
            ansList = detect_document(content)
            matches = compareans(ansList,keyList)
            Mark = calculateMarks(len(matches),len(keyList))
            Tot = Tot + Mark
            print("Total Marks:"+str(Tot))
            
            print("="*40)

    Grade = getGrade(Tot)
    #print(Grade)
    return JsonResponse({"Grade":Grade})
    if Grade == A:
        return JsonResponse({"Remarks":"You have a sound knowledge on the subject and particular topics. Keep it up."})
    elif Grade == B:
        return JsonResponse({"Remarks":"You seem to have a good understanding on various topics, yet need to concentrate on specific concepts."})
    elif Grade == C:
        return JsonResponse({"Remarks":"Lacks in various crucial topics. More understanding is required to reach a sound knowledge."})
    elif Grade == D:
        return JsonResponse({"Remarks":"More effort is required to reach the levels of understanding the subject. Practice more on important concepts."})
    elif Grade == E:    
        return JsonResponse({"Remarks":"Need to improve much and practice better."})
    else:      
        return JsonResponse({"Remarks":"FAIL"})
        
    
    
    # Create your views here.
    config = {
        'apiKey': "AIzaSyAhPVxF8PZZ06_Vi3qFitmgs9NJvMmelRc",
        'authDomain': "fir-connectivity-57d5b.firebaseapp.com",
        'databaseURL': "https://fir-connectivity-57d5b.firebaseio.com",
        'projectId': "fir-connectivity-57d5b",
        'storageBucket': "fir-connectivity-57d5b.appspot.com",
        'messagingSenderId': "990842322372"
      }
    #firebase.initializeApp(config)
    firebase = pyrebase.initialize_app(config)
    print("Works")
    #return JsonResponse({"Grade":""})



