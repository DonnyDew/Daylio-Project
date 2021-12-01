import csv
import matplotlib.pyplot as plt
import itertools

filepath = 'C:\\Users\\Donald Robbins\\Desktop\\Python Files\\hello_ds\\Daylio Project\\daylio_export_'
with open(f'{filepath}2021_06_11.csv',encoding = 'utf8') as f:
    data = csv.reader(f)
    entry = {} #full_date,date,weekday,time,mood,activties,note,month,year
    for rank,row in enumerate(data):
        if rank == 0:
            continue
        entry[rank] = {'full_date':row[0],'date':row[1],'weekday':row[2],'time':row[3],'mood':row[4],\
            'activities':row[5],'note':row[7]}

for i in entry:
    entry[i]['activities'] = entry[i]['activities'].split(' | ')
    entry[i]['date'] = entry[i]['date'].split(' ')
    entry[i]['full_date_list'] = entry[i]['full_date'].split('-')
activitiesN = []    
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
    entry[i]['year'] = entry[i]['full_date_list'][0]
    activitiesN.append(entry[i]['activities'])
activitiesL = []
for section in activitiesN:
    for act in section:
        activitiesL.append(act)
activities = list(set(activitiesL))
activities.remove('')

def num_activities(activity):
    count = 0
    entryRank = []
    for i in entry:
        if activity in entry[i]['activities']:
            count += 1
            entryRank.append(i)
    
    cur_count = 1
    max_count = 0
    for i in range(len(entryRank)-1):
        if entryRank[i] == entryRank[i+1]-1:
            cur_count += 1
            if cur_count > max_count:
                max_count = cur_count
        else:
            cur_count = 1
    print("The total number of activties is:", count)
    print("The most consecutive days in a row is:",max_count)
def note_search(note):
    count = 0
    dates = []
    for i in entry:
        if note.lower() in entry[i]['note'].lower():
            count += 1
            dates.append(entry[i]['full_date'])
    
    print(note,"occured",count,"times")
    print("Here are the dates:",dates)
def Dew_File_Writier():
    csvfile= open('Dew Data.csv','w',newline='',encoding='utf8')
    fieldnames = ['date','weekday','time','mood','activities']
    writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()
    for i in entry:
        if 'Mountain Dew' in entry[i]['activities']:
                writer.writerow({
                    'date':entry[i]['date'],
                    'weekday':entry[i]['weekday'],
                    'time':entry[i]['time'],
                    'mood':entry[i]['mood'],
                    'activities':entry[i]['activities']
                    })
    csvfile.close()
def Best_Day_of_Week_college_or_home(year,collegeOrHome):
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dayCount = [0,0,0,0,0,0,0]
    dayScore = [0,0,0,0,0,0,0]
    moodMap = {'rad':5,'almost Rad':4.5,'good':4,'Solid':3.5,'okay':3,'meh':2,'bad':1}
    for i in entry:
        if year in entry[i]['year']:
            if collegeOrHome in entry[i]['activities']:
                for iday,day in enumerate(weekdays):
                    if day in entry[i]['weekday']:
                        dayCount[iday] += 1
                        dayScore[iday] += moodMap[entry[i]['mood']]
                   
    for iday in range(7):
        if dayCount[iday] == 0:
            dayCount[iday] = 1
    
    bottom_edges = [1,2,3,4,5,6,7]
    heights = []
    for score,count in zip(dayScore,dayCount):
        heights.append(score/count)
    plt.bar(bottom_edges,heights,color=('r','orange','y','g','mediumblue','cornflowerblue','darkviolet'))
    plt.title(f'Average Mood by Day During {collegeOrHome}in {year}')
    plt.xlabel('Days of Week')
    plt.ylabel('Average Mood')

    plt.xticks([1,2,3,4,5,6,7],
                ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun'])
    plt.yticks([1,2,3,3.5,4,5],
                ['Bad','Meh','okay','solid','good','rad'])
    for (x,y) in zip(bottom_edges,heights):
        plt.text(x,y,format(y,'.2f'))
    plt.show()
def Best_Day_of_Week(year):
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dayCount = [0,0,0,0,0,0,0]
    dayScore = [0,0,0,0,0,0,0]
    moodMap = {'rad':5,'almost Rad':4.5,'good':4,'Solid':3.5,'okay':3,'meh':2,'bad':1}
    for i in entry:
        if year in entry[i]['year']:
            for iday,day in enumerate(weekdays):
                if day in entry[i]['weekday']:
                    dayCount[iday] += 1
                    dayScore[iday] += moodMap[entry[i]['mood']]
                   
    for iday in range(7):
        if dayCount[iday] == 0:
            dayCount[iday] = 1
    
    bottom_edges = [1,2,3,4,5,6,7]
    heights = []
    for score,count in zip(dayScore,dayCount):
        heights.append(score/count)
    plt.bar(bottom_edges,heights,color=('r','orange','y','g','mediumblue','cornflowerblue','darkviolet'))
    plt.title('Average Mood by Day')
    plt.xlabel('Days of Week')
    plt.ylabel('Average Mood')

    plt.xticks([1,2,3,4,5,6,7],
                ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun'])
    plt.yticks([1,2,3,4,5],
                ['Bad','Meh','okay','good','rad'])
    for (x,y) in zip(bottom_edges,heights):
        plt.text(x,y,format(y,'.2f'))
    plt.show()
def Best_Day_by_act(activity):
    weekdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    dayCount = [0,0,0,0,0,0,0]
    dayScore = [0,0,0,0,0,0,0]
    moodMap = {'rad':5,'good':4,'okay':3,'meh':2,'bad':1}
    for i in entry:
        if activity in entry[i]['activities']:
            for iday,day in enumerate(weekdays):
                if day in entry[i]['weekday'] and (activity in entry[i]['activities']):
                    dayCount[iday] += 1
                    dayScore[iday] += moodMap[entry[i]['mood']]
                   
    for iday in range(7):
        if dayCount[iday] == 0:
            dayCount[iday] = 1
    
    bottom_edges = [1,2,3,4,5,6,7]
    heights = []
    for score,count in zip(dayScore,dayCount):
        heights.append(score/count)
    
    plt.bar(bottom_edges,heights,color=('r','orange','y','g','mediumblue','cornflowerblue','darkviolet'))
    plt.title(F'Average Mood for {activity} by Day')
    plt.xlabel('Days of Week')
    plt.ylabel('Average Mood')

    plt.xticks([1,2,3,4,5,6,7],
                ['Sun','Mon','Tues','Wed','Thurs','Fri','Sat'])
    plt.yticks([1,2,3,4,5],
                ['Bad','Meh','okay','good','rad'])
    for (x,y) in zip(bottom_edges,heights):
        plt.text(x,y,format(y,'.2f'))
        
    plt.show()
def Best_Month(year):
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthCount = [0,0,0,0,0,0,0,0,0,0,0,0]
    monthScore = [0,0,0,0,0,0,0,0,0,0,0,0]
    moodMap = {'rad':5,'almost Rad':4.5,'good':4,'Solid':3.5,'okay':3,'meh':2,'bad':1}
    for i in entry:
        if year in entry[i]['year']:
            for imonth,month in enumerate(months):
                if month in entry[i]['month']:
                    monthCount[imonth] += 1
                    monthScore[imonth] += moodMap[entry[i]['mood']]
    for imonth in range(12):
        if monthCount[imonth] == 0:
            monthCount[imonth] = 1
    bottom_edges = [1,2,3,4,5,6,7,8,9,10,11,12]
    heights = []
    for score,count in zip(monthScore,monthCount):
        heights.append(score/count)
    plt.bar(bottom_edges,heights,color=('r','orange','y','g','mediumblue','cornflowerblue','darkviolet'))
    plt.title('Average Mood by Month')
    plt.xlabel('Months')
    plt.ylabel('Average Mood')

    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],
                ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    plt.yticks([1,2,3,4,5],
                ['Bad','Meh','okay','good','rad'])
    

    for (x,y) in zip(bottom_edges,heights):
        plt.text(x,y,format(y,'.2f'))
    plt.show()
    
    count = 0
    for i in heights:
        count += i
    heights.sort()
    Len = len(heights)
    if Len % 2 == 0:
        median1 = heights[Len//2]
        median2 = heights[Len//2-1]
        median = (median1 + median2) / 2
    else:
        median = heights[Len//2]    
    medMoodYear = format(median,'.2f')
    
    avgMoodYear = format(count / len(heights),'.2f')
    print("The average mood for the year " + str(year) + " is " + str(avgMoodYear))
    print("The median mood for the year " + str(year) + " is " + str(medMoodYear))

def Best_Month_by_act(year,activity):
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthCount = [0,0,0,0,0,0,0,0,0,0,0,0]
    monthScore = [0,0,0,0,0,0,0,0,0,0,0,0]
    moodMap = {'rad':5,'good':4,'okay':3,'meh':2,'bad':1}
    for i in entry:
        if activity in entry[i]['activities']:
            if year in entry[i]['year']:
                for imonth,month in enumerate(months):
                    if month in entry[i]['month']:
                        monthCount[imonth] += 1
                        monthScore[imonth] += moodMap[entry[i]['mood']]
    for imonth in range(12):
        if monthCount[imonth] == 0:
            monthCount[imonth] = 1
    bottom_edges = [1,2,3,4,5,6,7,8,9,10,11,12]
    heights = []
    for score,count in zip(monthScore,monthCount):
        heights.append(score/count)
    plt.bar(bottom_edges,heights,color=('r','orange','y','g','mediumblue','cornflowerblue','darkviolet'))
    plt.title(F'Average Mood for {activity} by Day')
    plt.xlabel('Months')
    plt.ylabel('Average Mood')

    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],
                ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    plt.yticks([1,2,3,4,5],
                ['Bad','Meh','okay','good','rad'])
    

    for (x,y) in zip(bottom_edges,heights):
        plt.text(x,y,format(y,'.2f'))
    plt.show()
def Act_Count_per_month(year,activity):
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthCount = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in entry:
        if activity in entry[i]['activities']:
            if year in entry[i]['year']:
                for imonth,month in enumerate(months):
                    if month in entry[i]['month']:
                        monthCount[imonth] += 1
    bottom_edges = [1,2,3,4,5,6,7,8,9,10,11,12]
    heights = monthCount
    plt.bar(bottom_edges,heights,color=('r','orange','y','g','mediumblue','cornflowerblue','darkviolet'))
    plt.title(F'Number of {activity} by Month')
    plt.xlabel('Months')
    plt.ylabel('Total')

    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],
                ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    for (x,y) in zip(bottom_edges,heights):
        plt.text(x,y,format(y,'.2f'))
    plt.show()
def pushUp_n_planks():
    count = 0
    for i in entry:
        if 'chest / core' in entry[i]['activities']:
            count += 1
    num_pushUps = count / 2
    num_planks = count / 2
    lPushUps = format(num_pushUps * 100, ',.0f')
    uPushUps = format(num_pushUps * 160,',.0f')
    aplanks = num_planks * 4
    aplanks_hrs = format(aplanks // 60, '.0f')
    aplanks_mins = format(aplanks % 60, '.0f')
    print("I have done between " + str(lPushUps) + " and " + str(uPushUps) + " pushups")
    print ("I have done about " + aplanks_hrs + " hours and " + aplanks_mins + " minutes worth of planks")
def best_of_days(streak = 7):
    scores = []
    for i in entry:
        try:
            cur_score = 0
            for n in range(streak):
                cur_score += entry[i+n]['moodScore']
            
            intial_date = entry[i+streak-1]['full_date']
            final_date = entry[i]['full_date']
            scores.append((cur_score,intial_date,final_date))
        except KeyError as e:
            break    
    scores.sort()        
    print("The highest score across " + str(streak) + " days is: " + format(scores[-1][0],'.0f'))
    print("This occured from " + scores[-1][1] + " to " + scores[-1][2])
    print()
    print("The  2nd highest score across " + str(streak) + " days is: " + str(scores[-2][0]))
    print("This occured from " + scores[-2][1] + " to " + scores[-2][2])
    print()
    print("The 3rd highest score across " + str(streak) + " days is: " + str(scores[-3][0]))
    print("This occured from " + scores[-3][1] + " to " + scores[-3][2]) 
    print()
    print("The worst score across " + str(streak) + " days is: " + str(scores[0][0]))
    print("This occured from " + scores[0][1] + " to " + scores[0][2])
    print("The lowest day is " + format((scores[0][0]/scores[-1][0]),'.2%') + " of the highest day") 



#print(entry[1])
Best_Month('2020')






       


        
        











 

    
    






            


  


