import csv
import matplotlib.pyplot as plt
import itertools
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime as dt
import datetime

filepath = 'C:\\Users\\Donald Robbins\\Desktop\\Python Files\\hello_ds\\Daylio Project\\daylio_export_'

with open(f'{filepath}2021_12_01.csv',encoding = 'utf8') as f:
    data = csv.reader(f)
    entry = {} #full_date,date,weekday,time,mood,activties,note,month,year
    for rank,row in enumerate(data):
        if rank == 0:
            continue
        entry[rank] = {'full_date':row[0],'date':row[1],'weekday':row[2],'time':row[3],'mood':row[4],\
            'activities':row[5],'note':row[7]}
#-----------------------------------------------------------------------------------------------------------
for i in entry:
    entry[i]['activities'] = entry[i]['activities'].split(' | ')
    entry[i]['date'] = entry[i]['date'].split(' ')
    entry[i]['full_date_list'] = entry[i]['full_date'].split('-')
   
for i in entry:
    if entry[i]['mood'] == 'rad':
        moodScore = 5
    elif entry[i]['mood'] == 'almost Rad':
        moodScore = 4.5
    elif entry[i]['mood'] == 'good':
        moodScore = 4
    elif entry[i]['mood'] == 'Solid':
        moodScore = 3
    elif entry[i]['mood'] == 'okay':
        moodScore = 2
    elif entry[i]['mood'] == 'meh':
        moodScore = 1
    elif entry[i]['mood'] == 'bad':
        moodScore = 0
    else:
        print("Error with moodScore: " + entry[i]['mood'])
    entry[i]['moodScore'] = moodScore
 

for i in entry:
    entry[i]['month'] = entry[i]['date'][0]
    entry[i]['year'] = int(entry[i]['full_date_list'][0])
    
#-------------------------------------------------------------------------------
#Year Select
yearRegistered = 2019
countYear = yearRegistered
today = dt.today()
dateM = str(dt(today.year, today.month, 1))
year = int(dateM[0:4])
yearList = []
while year >= countYear:
    yearList.append(countYear)
    countYear += 1
yearList.reverse()
year = st.selectbox("Choose Year",yearList)

#------------------------------------------------------------------------------------
activities = []
numOfDays = 0
for i in entry:
    if entry[i]['year'] == year:
        numOfDays += 1
        for act in entry[i]['activities']:
            if act not in activities:
                activities.append(act)
monthList = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#-------------------------------------------------------------------------------------
#Containers
firstFrame = st.beta_container()
moodFrame = st.beta_container()
dayOfWeekFrame = st.beta_container()
bestDayFrame = st.beta_container()
activityFrame = st.beta_container()
noteFrame = st.beta_container()
exerciseFrame = st.beta_container()
#-------------------------------------------------------------------------------------
with firstFrame:
    st.title(f"Welcome to your {year} Yearly Report")
def getAvgMood4Year(year):
    moodScore = 0
    totalDays = 0
    for i in entry:
        if entry[i]['year'] == year:
            totalDays += 1
            moodScore += entry[i]['moodScore']
    avgMood = moodScore / totalDays
    return avgMood
def getMonthMood(month):
    moodList = []
    moodScore = 0
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
            moodList.append(entry[i]['mood'])
            moodScore += entry[i]['moodScore']
    numOfDays = len(moodList)
    
    averageMood = float(format(moodScore / numOfDays,'.2f'))
    moodDict = {'bad':0,'meh':0,'okay':0,'Solid':0,'good':0,'almost Rad':0,'rad':0}
    for i in moodList:
        moodDict[i] += 1
    return averageMood
def getMoodChart():
    moodList = []
    moodDic = {}
    for i in monthList:
        try:
            avgMood = getMonthMood(i)
            moodList.append(avgMood)
            moodDic[i] = avgMood
        except ZeroDivisionError:
            moodList.append(0)
            moodDic[i] = 0
    fig = go.Figure([go.Bar(x=monthList,y=moodList,text=moodList,textposition='auto',marker_color='#17BECF')])
    fig.update_layout(xaxis_title="Months",
    font = dict(
        family="Courier New, monospace",
        size=14,
        color="orangered"))
    moodList.sort()
    for i in range(0,len(moodList)):
        if moodList[i] != 0:
            lowIndex = i #This is to not have the lowest month be one with 0 (which is a month that hasn't happened yet)
            break
    lowest = []
    highest = []
    for k,v in moodDic.items():
        if v == moodList[lowIndex]:
            lowest.append(f"{k}-{v}")
        if v == moodList[11]:
            highest.append(f"{k}-{v}")
    return [fig,highest,lowest]
MoodChartData = getMoodChart()
moodChart = MoodChartData[0]
bestMonths = MoodChartData[1]
worstMonths = MoodChartData[2]
averageMood = float (format(getAvgMood4Year(year),'.2f'))

with moodFrame:
    st.write(moodChart)
    st.subheader(f"The year mood average for {year} is {averageMood}")
    moodcol1,moodcol2 = st.beta_columns(2)
    moodcol1.subheader("Best month(s): ")
    moodcol2.subheader(' '.join(map(str,bestMonths)))

    moodcol3,moodcol4 = st.beta_columns(2)
    moodcol3.subheader("Worst month(s): ")
    moodcol4.subheader(' '.join(map(str,worstMonths)))
def bestDayofWeek():
    dayScore = {'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0,'Sunday':0}
    dayCount = {'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0,'Sunday':0}
    for i in entry:
        if entry[i]['year'] == year:
            dayScore[entry[i]['weekday']] += entry[i]['moodScore']
            dayCount[entry[i]['weekday']] += 1
    y = []
    x = []
    dayDict = {}
    for (k,v),(k2,v2) in zip(dayScore.items(),dayCount.items()):
        y.append(float(format(v/v2,'.3f')))
        x.append(k)
        dayDict[k] = float(format(v/v2,'.3f'))
    fig = go.Figure([go.Bar(x=x,y=y)])
    #Find best and worst day of week
    y.sort()
    lowest = []
    highest = []
    for k,v in dayDict.items():
        if v == y[0]:
            lowest.append(k)
        if v== y[6]:
            highest.append(k)   
    
    return [fig,highest,lowest]
bestDayofWeekData = bestDayofWeek()
dayOfWeekChart = bestDayofWeekData[0]
theBestDayOfWeek = bestDayofWeekData[1]
worstDayOfWeek = bestDayofWeekData[2]
with dayOfWeekFrame:
    st.title("Best Day of the Week Chart")
    st.write(dayOfWeekChart)
    
    daycol1,daycol2 = st.beta_columns(2)
    daycol1.subheader("Best Day of Week: ")
    daycol2.subheader(' '.join(map(str,theBestDayOfWeek)))
    
    daycol3,daycol4 = st.beta_columns(2)
    daycol3.subheader("Worst Day of Week: ")
    daycol4.subheader(' '.join(map(str,worstDayOfWeek)))
def best_of_days(streak=7):
    scores = []
    for i in entry:
        if entry[i]['year'] == year and entry[i+streak-1]['year'] == year:
            try:
                cur_score = 0
                for n in range(streak):
                    cur_score += (entry[i+n]['moodScore']/streak)
                
                intial_date = entry[i+streak-1]['full_date_list'][1]+ "/"+entry[i+streak-1]['full_date_list'][2]+"/"+ \
                                entry[i+streak-1]['full_date_list'][0][-2:]
                final_date = entry[i]['full_date_list'][1] + "/"+entry[i]['full_date_list'][2]+"/"+entry[i]['full_date_list'][0][-2:]
                scores.append((format(cur_score,'.2f'),intial_date,final_date))
            except KeyError as e:
                break    
    scores.sort(reverse = True)
    return scores
with bestDayFrame:
    st.title("The Best of Days")
    bestDayData = best_of_days()
    bestDay = bestDayData[0]
    secondBestDay = bestDayData[1]
    thirdBestDay = bestDayData[2]
    worstDay = bestDayData[-1]
    secondWorstDay = bestDayData[-2]
    thirdWorstDay = bestDayData[-3]
    st.subheader("Best Week")
    st.write(f"In {year} the best 7 days were between: {bestDay[1]}-{bestDay[2]}")
    st.write(f"The average score in this period was {bestDay[0]} compared to the average month mood of {averageMood}")
    
    st.subheader("Other good weeks")
    for i in range(1,10):
        st.write(f"{bestDayData[i][1]}-{bestDayData[i][2]} with average score of {bestDayData[i][0]}")
    
    st.subheader("Worst Week")
    st.write(f"In {year} the worst 7 days were between: {worstDay[1]}-{worstDay[2]}")
    st.write(f"The average score in this period was {worstDay[0]} compared to the average month mood of {averageMood}")
    
    st.subheader("Other bad weeks")
    for i in range(-2,-11,-1):
        st.write(f"{bestDayData[i][1]}-{bestDayData[i][2]} with average score of {bestDayData[i][0]}")
def getImpact(activity):
    monthScore = 0
    timesWithAct = 0
    for i in entry:
        if entry[i]['year'] == year:
            if activity in entry[i]['activities']:
                timesWithAct += 1
                monthScore += entry[i]['moodScore']
    activityAvg = monthScore/timesWithAct
    impact = activityAvg / averageMood
    impactChange = format((impact - 1) * 100,'.2f')
    return float(impactChange)
def getActivityTable():
    yearActDic = {}
    for i in entry:
        if entry[i]['year'] == year:
            for act in entry[i]['activities']:
                if act in yearActDic:
                    yearActDic[act]["Count"] += 1
                else:
                    yearActDic[act] = {"Count":1,"Impact":0}
    
    for act in yearActDic:
        yearActDic[act]["Impact"] = getImpact(act)
    
    act = []
    count = []
    impact = []
    for key in yearActDic:
        act.append(key)
        count.append(yearActDic[key]["Count"])
        impact.append(yearActDic[key]["Impact"])
    
    Data = {"Act":act,"Count":count,"Impact":impact}
    actTable = pd.DataFrame(Data)
    return actTable
with activityFrame:
    st.title("Activity Table")
    st.write(getActivityTable())
def noteCount(keyword):
    count = 0
    dateList = []
    for i in entry:
        if entry[i]['year'] == year:
            if keyword.lower() in entry[i]['note'].lower():
                count += 1
                dateList.append(entry[i]['date'][0]+ "-"+entry[i]['date'][1])
    dateList.reverse()
    percentNote = format((count / numOfDays),'.2%')
    
    return [count,percentNote,dateList]
with noteFrame:
    st.title("Note Search")
    noteItem = st.text_input("Enter note to search")
    if noteItem != "":
        noteCountData = noteCount(noteItem)
        st.subheader(f"{noteItem} appeared {noteCountData[0]} times which is {noteCountData[1]} of entries")
        notecol1,notecol2 = st.beta_columns(2)
        notecol1.write(f"{noteItem} appeared in these dates of {year}: ")
        notecol2.write(', '.join(map(str,noteCountData[2])))

def pushUpPlankCount(pushup):
    #Pushup and Plank should be user input on how many pushups and how long for planks in minutes
    pushUpCount = 0
    for i in entry:
        if entry[i]['year'] == year:
            if 'chest / core' in entry[i]['activities']:
                pushUpCount += pushup
    return pushUpCount
with exerciseFrame:
    st.title("Push-Ups and Planks")
    pushups = st.number_input("Enter average number of push-ups",step=5)
    st.subheader("Push-ups")
    st.write(f"{pushUpPlankCount(pushups)} push-ups were done this year")
    
