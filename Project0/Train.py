import pandas as pnd
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfile as aof
from PIL import ImageTk
import pyodbc as pd
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
import random as ran
import base64
import pickle
import os

#Training Malcious URL(Accuracy not shown here)
def my_tokenizer_url(x):
    tokens_by_slash=str(x.encode('utf-8')).split('/')
    total_tokens=[]
    for i in tokens_by_slash:
        tokesn_by_hyphen=str(i).split('-')
        tokens_by_dot=[]
        for j in range(0,len(tokesn_by_hyphen)):
            tokens_by_dot=str(tokesn_by_hyphen[j]).split('.')
        total_tokens=total_tokens+tokens_by_dot
        total_tokens=list(set(total_tokens))
    if 'com' in total_tokens:
        total_tokens.remove('com')
    if 'www' in total_tokens:
        total_tokens.remove('www')
    return total_tokens    
def malicious_url():
    df=pnd.read_csv("C:/Project/DataSet/urldata.csv")
    df.head()
    Y=df['label']
    url=df['url']
    vectorizer=TfidfVectorizer(my_tokenizer_url)
    X=vectorizer.fit_transform(url)        
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    logit=LogisticRegression()	
    logit.fit(X_train, Y_train)
    print('Accuracy:', logit.score(X_test, Y_test)*100)
    with open('finalized_model0.sav', 'wb') as f:
        pickle.dump(logit, f)
    vocab=vectorizer.fit(X_train)
    with open('vectorizer0.pickle', 'wb') as f:
        pickle.dump(vocab, f)

#Training Spam Mail(Accuracy printed in the terminal)
def sp_mail():
    df=pnd.read_csv('C:/Project/DataSet/final_dataset.csv')
    stop_words=set(stopwords.words('english'))
    df['text']=df['text'].apply(lambda x: ' '.join([ word for word in word_tokenize(x)  if not word in stop_words]))
    y=df['label_num']
    X=df['text']
    new_df=pnd.concat([y, X], axis=1)
    clean_dataset='C:/Project/DataSet/clean_dataset.csv'
    new_df.to_csv(clean_dataset, index=False)
    df=pnd.read_csv('C:/Project/DataSet/clean_dataset.csv')
    y=df['label_num']
    X=df['text']
    X_train, X_test , y_train, y_test=train_test_split(X,y,test_size=0.2, random_state=1)
    cVect=CountVectorizer()
    #cVect.fit(X_train)
    feature_train=cVect.fit_transform(X_train)
    lr=LogisticRegression()
    model=lr.fit(feature_train, y_train)
    test_dtv=cVect.transform(X_test).toarray()
    pred=lr.predict(test_dtv)
    print('Accuracy:', accuracy_score(y_test, pred)*100)
    with open('finalized_model1.sav', 'wb') as f:
        pickle.dump(model, f)
    vocab=cVect.fit(X_train)
    with open('vectorizer.pickle', 'wb') as f:
        pickle.dump(vocab, f)

malicious_url()
sp_mail()