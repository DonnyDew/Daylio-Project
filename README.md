# Daylio Reports
This project aims to give a monthly/yearly report of the data given from the Daylio App.

## What is Daylio
Daylio is a sudo-journal where you can enter activities,moods, and notes.

## CSV Files
The data comes from downloading a csv file from the Daylio app. I included a fake entry csv file to show what it would look like.
I am not including any of my actual files due to privacy.
## This project is personalized
Daylio is very customizable so if you downloaded your entries into a csv and entered it into this program
errors would likely occur
Here is a run down on how I use Daylio so people can modify
* I have 1 Daylio Entry every single day
* I have 7 moods: (bad,meh,okay,solid,good,almost Rad,rad)
* I have my own custom activities made but the only feature as of now dependent on a custom one is pushups/planks

* The variable `yearRegistered` should be changed unless it is 2019
* The file path also needs to change to your computer

## Daylio Month Features
**Program runs by running program and then entering to console `streamlit run` and then tab until you find the file**
* Enter any month that there is data
* Mood tally chart
* Average Mood (numerically)
* Best Day of Week Bar Chart
* Best and worst 7 day streak (Occurence and mood score)
* Activity Table with impact on mood
* A pixel plot on moods color coded in a calendar format
* Pixel plot by activity which is the same as previous but if activity didn't occur it is grayed out
This gives a visual representation on the frequency of the activity and the moods
* Note Search of any keyword (cap friendly)
* Push-Up and Plank counter based on the activity `chest / core`

## Daylio Year Features
* Enter any year (only the years there's data for will show up)
* Monthly Mood Average Bar Chart
* Yearly average mood
* Best and Worst month
* Best Day of Week Bar Chart
* Best and worst 7 day streak across year
* Activity Table with it's % impact on mood
* Note Search
* Push-Up and Plank counter

## Concluding Notes
This program is most likely not user ready after download due to the customizablity to Daylio. I hope this program
can be of help for making your own program or just altering this one :)



