import csv
from collections import Counter
import streamlit as st
import pandas as pd
import numpy as np
filepath = 'C:\\Users\\Donald Robbins\\Desktop\\Python Files\\hello_ds\\Daylio Project\\daylio_export_'

def sortDictbyValue(dictionary):
    sorted_keys = sorted(dictionary,reverse = True,key=lambda x: (dictionary[x]))
    tempDict = {}
    for i in sorted_keys:
        tempDict[i] = ""
    tempDict2 = {}
    for (k,v),(k2,v2) in zip(dictionary.items(),tempDict.items()):
        tempDict2[k2] = dictionary[k2]
    return tempDict2

words = ""
with open(f'{filepath}2022_03_06.csv',encoding = 'utf8') as f:
    data = csv.reader(f)
    for row in data:
        #if row[0][0:4] == "2021" or row[0][0:4] == "2022":
            words += row[7]

deleteThese = [",","!","|",".","\"","\'",";","(",")","/",">","<",":","+","-","?","=","🥺","😂","😐","😉","😬",
            "💛", "😳","😍", "😡","😊","🤭","😊","😀","😵‍","💫", "🙁","🥵","🥳","😑","😄","💀","🤨","😔",
            "🦀","#","❄️","🐐","👀","“"]
words = ''.join([i for i in words if not i.isdigit()])
for item in deleteThese:
    words = words.replace(item,"")
words = words.replace('"','')
words = Counter(words.split(" "))
words = sortDictbyValue(words)
words.pop("")
wordList = []
valueList = []
for k,v in words.items():
    wordList.append(k)
    valueList.append(v)
numList = []
for i in range(0,4570):
    numList.append(i)
wordsData = {"Word":wordList,"Count":valueList}
wordsDF = pd.DataFrame(wordsData)
wordsDF.index = np.arange(1,len(wordsDF)+1)
myFrame = st.beta_container()
with myFrame:
    st.title("Word Counter")
    st.write(wordsDF)
    st.write("This table shows the amount of times a certain word has come up in my entries.")
    st.write("This includes entries from Nov 2019 - March 2022.")
    


    