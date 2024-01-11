from datetime import date
from datetime import datetime ,timedelta, time
from time import sleep
import calendar
import tkinter as tk
from tkinter import ttk
import keyboard
import pandas as pd
import subprocess
import csv
import pandas

def speak(text):
    try:
        subprocess.run(["espeak", text])
    except Exception as e:
        print(f"Error while speaking: {e}")

df = pd.read_csv('app.csv')
def process_scanned_barcode(scanned_barcode , st , tt , sections ,start_time ,end_time):
    count = 0
    arr=[]
    if scanned_barcode in df['Barcode'].astype(str).values:
    
        card_data = df[df['Barcode'].astype(str) == scanned_barcode].to_dict(orient='records')[0]
        print(card_data , st , tt)
        if  card_data['Section'] == sections :
            
            if st <=  int(card_data['USN'][7:]) <= tt and int(card_data['USN'][7:]) not in arr :
                arr.append(int(card_data['USN'][7:]))
                count+=1

                display_result(f"Scanned Barcode: {scanned_barcode}\nCard Data:\n" + "\n".join([f"{key}: {value}" for key, value in card_data.items()]))
                speak("present")
       

        if datetime.now().time() > end_time :
            filename = f'{sections}{datetime.now().time()}.csv'
            with open(filename, 'w', newline="") as file:
                csvwriter = csv.writer(file) 
                csvwriter.writerow("rollnos") 
                for ss in arr :
                    csvwriter.writerows(ss)
                        
    else:
        speak("invalid card")
def on_scan(event , st , tt , sections , start_time ,end_time):
    if event.event_type == keyboard.KEY_DOWN:
        key = event.name
        if key =='j' :
            pass
        if key and key.isnumeric():
       
            current_barcode.append(key)

        elif key == 'enter' and current_barcode:
           
            scanned_barcode = ''.join(current_barcode)
            process_scanned_barcode(scanned_barcode , st , tt , sections , start_time ,end_time)
            current_barcode.clear()
        if key =='j' :
            pass
def display_result(result_text):
    result_label.config(text=result_text)

current_barcode = []

day = ["monday","tuesday","wednesday","thursday","friday",]

routine  ={ 'monday' : [ {"08:30 - 10:30" : {"sub" :"ds" ,
                                             "sec"  : "d",
                                             "year" :2 ,
                                             "roll" : (1,34)}   } ,

                          {"10:50 - 12:50" : {"sub" :"python" ,
                                             "sec"  : "a",
                                             "year" :1 ,
                                             "roll" : (33,66)}   } ,

                          {"02:40 - 04:30" : {"sub" :"java" ,
                                             "sec"  : "d",
                                             "year" :2 ,
                                             "roll" : (1,31)}   } ,] ,


            'thursday' : [ {"08:30 - 10:30" : {"sub" :"adev" ,
                                             "sec"  : "j",
                                             "year" :3 ,
                                             "roll" : (36,73)}   } ,

                          {"10:50 - 12:50" : {"sub" :"webdev" ,
                                             "sec"  : "g",
                                             "year" : 3,
                                             "roll" : (1, 32)}   } ,

                          {"01:00 - 02:30" : {"sub" :"ds" ,
                                             "sec"  : "d",
                                             "year" : 2 ,
                                             "roll" : (35,34)}   } ,] ,
} 
count = 0
cday = calendar.day_name[date.today().weekday()]
h = routine[cday.lower()]


if cday.lower() in day :
    for i in range(0,3) :
        for keys, values in h[i].items() :
            st_time = datetime.strptime(keys[0:5],"%I:%M") + timedelta(minutes=6)
            tt = st_time.strftime("%I:%M")
            start_time = time(int(keys[0:2]), int(keys[3:5]) )
            end_time = time(int(tt[0:2]) , int(tt[3:5]))
            print( start_time , end_time , datetime.now().time())

            while start_time <= datetime.now().time() <= end_time  :
                if count == 0 :
                    print(f"Today is {cday} \nTime is {datetime.now().strftime('%I:%M')}\nSlot is {keys}\nSubject : {h[i][keys]['sub']}")
                    print(f"""Students of year {h[i][keys]['year']} , Sec {h[i][keys]['sec'].upper()}.\nroll no from {h[i][keys]['roll'][0]} to roll no {h[i][keys]['roll'][1]} are required in lab""")
               
 
    

                global result_label
                sleep(2)
                keyboard.hook(lambda event: on_scan( event , h[i][keys]['roll'][0], h[i][keys]['roll'][1], h[i][keys]['sec'].upper() , start_time ,end_time) )
                print(datetime.now().time() , end_time , datetime.now().time()>= end_time)
                if datetime.now().time() >= end_time :
                    print("code running")
                    process_scanned_barcode(1111, h[i][keys]['roll'][0], h[i][keys]['roll'][1], h[i][keys]['sec'].upper() , start_time , end_time)
                    exit(0)
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

                count = 1
    count = 0
                 
                 

                 



