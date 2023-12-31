import requests
import re
import pygame.mixer
import time
import os
import pdfreader
from pdfreader import PDFDocument,SimplePDFViewer
from bs4 import BeautifulSoup
from gtts import gTTS
from threading import Thread
from tkinter import (Tk,IntVar,Label,Radiobutton,Button,Entry,Scale,DISABLED,BooleanVar,StringVar,NORMAL,DoubleVar,filedialog as fd)

if(not os.path.exists("tmp")):
    os.mkdir('tmp')
pygame.mixer.init(frequency=36500)

display = Tk()
display.geometry("400x375")
display.resizable(height=0, width=0)
int_variable=IntVar()
url_var=StringVar()
volume_var = DoubleVar()



def expand():
    display.geometry("400x500")
    mode_value=int_variable.get()
    if(mode_value==1 or mode_value==2):
        url=url_var.get()
        y=Thread(target=read,args=[url,])
        y.start()
    elif(mode_value==3):
        x,y,j=book_command()
        y.delete(0,j)
        z=Thread(target=reading_for_text,args=[x,])
        z.start()
    else:
        print("Some error occured")

def web_art():
        Label(display,text="Enter url").grid(row=5,column=1,pady=(70,0))
        Entry(display,textvariable=url_var)
def book_command():
    try:
        Label(display,text="Select file").grid(row=5,column=1,pady=(70,0))
        x=fd.askopenfilename()
        real_name=x
        name=real_name.split("/")[-1]
        book_entry=Entry(display,textvariable=url_var)
        book_entry.insert(0,name)

        book_entry.grid(row=5,column=2,pady=(70,0))
        print(real_name.replace("/","\\"))
        file_name = open(real_name.replace("/","\\"), "rb")
        viewer = SimplePDFViewer(file_name)
        book_name=len(real_name.replace("/","\\"))
        text_list=[]
        for _ in viewer: 
            viewer.render()
            x="".join(viewer.canvas.strings).strip().encode("ascii","ignore").decode()
            if(x!=""):
                text_list.append(x)
        read_from=4
        read_till=5
        text_list=text_list[read_from:read_till+1]
        return text_list,book_entry,book_name
    except Exception:
        print("Please Select a file")


 
def change_volume(x):
    volume_level=volume_slider.get()/10
    pygame.mixer.music.set_volume(volume_level)
#parsing the required data from website 
def parse_text(content):
    soup=BeautifulSoup(content,"html.parser")
    all_p_tags=soup.find_all("p")

    return all_p_tags

#Generating speech from the list of strings and saving it as audio files 
def generate_speech(text_to_read):
    for i in range(len(text_to_read)):
        formato="\[[\d]*]"
        text_to_read[i]=re.sub(formato,"",text_to_read[i])
        tts=gTTS(text_to_read[i])
        tts.save(f"tmp_{i+1}.mp3")

#Playing the audio file using pygame mixer module
def play_audio(file_name):
    sound=pygame.mixer.Sound(file_name)
    playing_sound=sound.play()
    while(playing_sound.get_busy()):
        print("playing...")
        time.sleep(1)
    print("wait...")

#Deleting all the audio files after playing the audio
def clean_up():
    for audio_file in os.listdir():
        os.remove(audio_file)
    print("--All audio files deleted")
    exit()



def restrict():
    display.geometry("400x375")
    clean_up()
    pygame.mixer.stop()

def pause():
    pygame.mixer.pause()

#Starting a thread to download/ to generate speech and then reading it
def reading_for_text(text_to_read):
    try:
        y=Thread(target=generate_speech,args=(text_to_read,))
        y.start()
        for j in range(1,len(text_to_read)+1):
            current_audio_file=f"tmp_{j}.mp3"
            next_audio_file=f"tmp_{j+1}.mp3"
            while(next_audio_file not in os.listdir()):
                if(j==len(text_to_read)):
                    print("--downloading file")
                    time.sleep(6)
                    break
                else:
                    time.sleep(1)
                    print("checking if next file is available")
            play_audio(current_audio_file)
        print("--Reading completed")
        clean_up()
        display.geometry("400x375")
    except Exception:
        print("Reading completed")
        clean_up()


def play():
    pygame.mixer.unpause()


if __name__=="__main__":
    def read(url):
        format_url="^(https|http):\/\/[\w\d]*\.[\w\d]+\.[\w]{2,10}.*"
        if(bool(re.findall(format_url,url))):
            print("--Correct url format")
        else:
            print("--Incorrect url , Enter the url again")
        try:
            request=requests.get(url)
            content=request.text
            print("--Website url working")
        except Exception as ex:
            print("Website error ",ex)
        all_p_tags=parse_text(content)
        text_to_read=[]
        text_to_read = [x.text.strip().encode("ascii","ignore").decode() for x in all_p_tags if x.text.strip()!=""]
        text_to_read=text_to_read[:3]
        reading_for_text(text_to_read)
        
#Main gui code block
    Label(display,text="Nimble reader",font="Aerial").grid(row=1,column=2)
    Label(display,text="version v-1.0").grid(row=2,column=2,pady=(0,60))
    mode=Label(display,text="Mode : ").grid(row=3,column=0,padx=(20,15))
    website=Radiobutton(display,text="Website",variable=int_variable,value="1",command=web_art).grid(row=3,column=1,pady=(2,0))
    article=Radiobutton(display,text="Article",variable=int_variable,value="2",command=web_art).grid(row=3,column=2,pady=(2,0))
    book=Radiobutton(display,text="Books",variable=int_variable,value="3",command=book_command).grid(row=3,column=3,pady=(2,0))
    Label(display,text="URL").grid(row=5,column=1,pady=(70,0))
    url_entry=Entry(display,textvariable=url_var).grid(row=5,column=2,pady=(70,0))
    read_button=Button(text="Read Aloud",relief="ridge",pady=5,padx=12,font=("Aerial",10),background="#99ffff",activebackground="#80ffff",command=expand).grid(row=6,column=2,pady=(90,0))
    close_button=Button(text="x",relief="flat",pady=5,padx=9,font=("Aerial",10),background="#ff4d4d",activebackground="#ff3333",command=restrict).grid(row=6,column=3,pady=(90,0),padx=(25,0))
    Label(display,text="Reading...",font=("",11)).grid(row=7,column=1,pady=(30,0))
    play_button=Button(text="\u23F5",relief="flat",pady=0,padx=0,font=("Aerial",14),command=play,background="#99ffff",activebackground="#99ffff",foreground="#404040").place(x=175,y=425)
    pause_button=Button(text="| |",relief="flat",pady=0,padx=2,font=("Aerial",14),command=pause,background="#99ffff",foreground="#404040",activebackground="#80ffff").place(x=225,y=425)
    volume_slider=Scale(display,orient="horizontal",length=70,from_=0,to=10,command=change_volume,variable=volume_var)
    volume_slider.set(0)
    volume_slider.place(x=275,y=422)
    display.mainloop()
    