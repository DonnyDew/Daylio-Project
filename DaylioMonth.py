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

with open(f'{filepath}2021_06_30.csv',encoding = 'utf8') as f:
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
        moodScore = 3.5
    elif entry[i]['mood'] == 'okay':
        moodScore = 3
    elif entry[i]['mood'] == 'meh':
        moodScore = 2
    elif entry[i]['mood'] == 'bad':
        moodScore = 1
    else:
        print("Error with moodScore: " + entry[i]['mood'])
    entry[i]['moodScore'] = moodScore
 

for i in entry:
    entry[i]['month'] = entry[i]['date'][0]
    entry[i]['year'] = int(entry[i]['full_date_list'][0])
    

#-------------------------------------------------------------------------------
#Month Select
monthList = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
month = st.selectbox("Choose month",monthList)
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

#Beta Containers
moodFrame = st.beta_container()
dayOfWeekFrame = st.beta_container()
bestDayFrame = st.beta_container()
activityFrame = st.beta_container()
pixelPlotFrame = st.beta_container()
noteFrame = st.beta_container()
exerciseFrame = st.beta_container()

activities = []
for i in entry:
    if entry[i]['month'] == month and entry[i]['year'] == year:
        for act in entry[i]['activities']:
            if act not in activities:
                activities.append(act)


#-------------------------------------------------------------------------------------------
    
def getMonthMood():
    moodList = []
    moodScore = 0
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
            moodList.append(entry[i]['mood'])
            moodScore += entry[i]['moodScore']
    numOfDays = len(moodList)
    
    averageMood = format(moodScore / numOfDays,'.2f')
    moodDict = {'bad':0,'meh':0,'okay':0,'Solid':0,'good':0,'almost Rad':0,'rad':0}
    for i in moodList:
        moodDict[i] += 1
    x= []
    y = []
    for k,v in moodDict.items():
        x.append(k)
        y.append(v)
    fig = go.Figure([go.Bar(x=x,y=y)])
    return [averageMood,numOfDays,fig]
getMonthMoodData = getMonthMood()
averageMood = float(getMonthMoodData[0])
numOfDays = int(getMonthMoodData[1])
moodChart = getMonthMoodData[2]

with moodFrame:
    st.title("Mood Tally Chart")
    st.write(moodChart)
    st.subheader(f"Average Mood: {averageMood}")
def bestDayofWeek():
    dayScore = {'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0,'Sunday':0}
    dayCount = {'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0,'Sunday':0}
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
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
        if entry[i]['month'] == month and entry[i+streak-1]['month'] == month and entry[i]['year'] == year and entry[i+streak-1]['year'] == year:
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
    st.subheader("Best Week")
    bestDayData = best_of_days()
    bestDay = bestDayData[0]
    worstDay = bestDayData[-1]
    st.write(f"In {month} the best 7 days were between: {bestDay[1]}-{bestDay[2]}")
    st.write(f"The average score in this period was {bestDay[0]} compared to the average month mood of {averageMood}")
    st.subheader("Worst Week")
    st.write(f"In {month} the worst 7 days were between: {worstDay[1]}-{worstDay[2]}")
    st.write(f"The average score in this period was {worstDay[0]} compared to the average month mood of {averageMood}")
def getImpact(activity):
    monthScore = 0
    timesWithAct = 0
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
            if activity in entry[i]['activities']:
                timesWithAct += 1
                monthScore += entry[i]['moodScore']
    
    activityAvg = float(format(monthScore/timesWithAct,'.2f'))
    impact = activityAvg / averageMood
    impactChange = impact - 1
    
    return format(impactChange,'.2%')
def getActivityTable():
    monthActDic = {}
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
            for act in entry[i]['activities']:
                if act in monthActDic:
                    monthActDic[act]["Count"] += 1
                else:
                    monthActDic[act] = {"Count":1,"Impact":0}
    for act in monthActDic:
        monthActDic[act]["Impact"] = getImpact(act)
    act = []
    count = []
    impact = []
    for key in monthActDic:
        act.append(key)
        count.append(monthActDic[key]["Count"])
        impact.append(monthActDic[key]["Impact"])
    Data = {"Act":act,"Count":count,"Impact":impact}
    actTable = pd.DataFrame(Data)
    return actTable
with activityFrame:
    st.title("Activity Table")
    st.write(getActivityTable())
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
def pixelPlot(activity,decision):
    myDict = {}
        
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
            if int(entry[i]['date'][1]) == 1:
                firstWeekDay = entry[i]['weekday']
            if decision == 'Y':        
                if activity in entry[i]['activities']:
                    myDict[entry[i]['date'][1]] = entry[i]['mood']
                        
                else:
                    myDict[entry[i]['date'][1]] = "none"
            else:
                myDict[entry[i]['date'][1]] = entry[i]['mood']
    
    myList = []
    moodList = []
    for k,v in myDict.items():
        moodList.append(v)
    moodList.reverse()
        
    daysOfWeek = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        
    for i in range(0,len(daysOfWeek)):
        if daysOfWeek[i] == firstWeekDay:
            weekPosition = i
    
        
    for i in range(0,42):
        if i < weekPosition:
            value = [255,255,255]
            moodList.insert(0,0)
        else:
            try:
                if moodList[i] == 'none':
                    value = [192,192,192]
                elif moodList[i] == 'bad':
                    valuei = [64,64,64]
                elif moodList[i] == 'meh':
                    value = [0,76,153]
                elif moodList[i] == 'okay':
                    value = [178,102,255]
                elif moodList[i] == 'Solid':
                    value = [0,255,0]
                elif moodList[i] == 'good':
                    value = [0,153,0]
                elif moodList[i]== 'almost Rad':
                    value = [255,153,51]
                elif moodList[i] =='rad':
                    value = [255,128,0]
            except IndexError:
                value = [255,255,255]
        myList.append(value)
    
    myList1 = chunks(myList,7)
    
    img_rgb = np.array(list(myList1),dtype=np.uint8)
        
        
    fig = px.imshow(img_rgb,color_continuous_scale=px.colors.sequential.RdBu,labels=dict(x="Day of Week"))
    fig.update_xaxes(side="top",ticktext=daysOfWeek,tickvals=[0,1,2,3,4,5,6])
    if decision == 'Y':
        fig.update_xaxes(title=f"{activity} Frequency Pixel Chart")
    else:
        fig.update_xaxes(title="Whole Month Frequency Pixel Chart")
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
        font = dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    return fig
with pixelPlotFrame:
    st.title("Pixel Plot")
    st.write(pixelPlot(None,"N"))
    pixelAct = st.selectbox("Choose an activity",activities)
    st.write(pixelPlot(pixelAct,"Y"))    
        
def noteCount(keyword):
    count = 0
    dateList = []
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
            if keyword.lower() in entry[i]['note'].lower():
                count += 1
                dateList.append(entry[i]['date'][1])
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
        notecol1.write(f"{noteItem} appeared in these dates of {month}: ")
        notecol2.write(', '.join(map(str,noteCountData[2])))

def pushUpPlankCount(pushup,plank):
    #Pushup and Plank should be user input on how many pushups and how long for planks in minutes
    pushUpCount = 0
    plankCount = 0
    for i in entry:
        if entry[i]['month'] == month and entry[i]['year'] == year:
            if 'chest / core' in entry[i]['activities']:
                pushUpCount += pushup
                plankCount += plank
    return [pushUpCount,plankCount]

with exerciseFrame:
    st.title("Push-Ups and Planks")
    pushups = st.number_input("Enter average number of push-ups",step=5)
    planks = st.number_input("Enter average plank in minutes",step=1)
    exerciseData = pushUpPlankCount(pushups,planks)
    st.subheader("Push-ups")
    st.write(f"{exerciseData[0]} push-ups were done this month")
    st.subheader("Planks")
    st.write(f"{exerciseData[1]} minutes of planks were done this month")
    







    
    



