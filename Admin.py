from tkinter import *
from tkinter import messagebox
import sounddevice
from scipy.io.wavfile import write
import soundfile
from tkinter import filedialog
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import speech_recognition as sr

class AdminHome:
    def __init__(self,master):
        self.master=master
        self.duration=StringVar()
        self.fpath=StringVar()
        self.lbl_text=StringVar()

        self.lbl_text.set("waiting")
        #master1 = Toplevel()
        master.title("Admin Home")
        master.state("zoomed")
        large_font = ('Verdana', 25)

        lbl_2 = Label(master, text="Duration", height=2, width=20, font=large_font).place(x=700, y=10)
        dur = Entry(master,textvariable=self.duration, width=3, font=large_font).place(x=1000, y=20)
        #dur = Entry(master, text="Select a Voice...", width=20, font=large_font).place(x=400, y=20)
        sbmitbtn = Button(master, text="RECORD VOICE", height = 2, width = 20,font=large_font,command=self.recordvoice ).place(x=700, y=75)
        lbl = Label(master, text="Select a Voice...", height=2, width=20, font=large_font).place(x=700, y=200)
        voice_emotion = Label(master,textvariable=self.lbl_text, text="Emotion...", height=2, width=20, font=large_font).place(x=100, y=200)
        txt = Entry(master,textvariable=self.fpath, width=20, font=large_font).place(x=700, y=300)
        browse = Button(master, text="Browse",  font=large_font,command=self.browsefunc).place(x=1150, y=300)
        emotion = Button(master, text="VIEW EMOTION", height=2, width=20, font=large_font,command=self.viewemotion).place(x=700, y=400)
        ext = Button(master, text="Exit", height=2, width=20, font=large_font,command=master.destroy).place(x=700, y=550)
        master.mainloop()

    def recordvoice(self):
        print("record")
        tme = int(self.duration.get().strip())
        print("Time:", tme)
        fs = 44100
        # second = int(input("Enter time duration in seconds: "))
        print("Recording.....n")
        # record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
        record_voice = sounddevice.rec(int(tme * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        write("out.wav", fs, record_voice)
        print("Finished.....nPlease check your ou1tput file")
        data, samplerate = soundfile.read('out.wav')
        soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
        messagebox.showinfo("Record", "Voice recording finished...")

    def browsefunc(self):
        print("browse here")
        # data = self.fpath.get().strip()
        # print("Path entry...:",data)
        # global voice_emotion
        try:
            filename = str(filedialog.askopenfilename())
            print("Filepath:", filename)
            self.fpath.set(filename)
            # self.lbl_text.set("hai.... bye...")
        except:
            messagebox.showinfo("Alert", "only wave files supported...")

    def viewemotion(self):
        print("started...")
        path = self.fpath.get().strip()
        print(path)

        # Initialize recognizer class
        r = sr.Recognizer()

        try:
            # Reading audio file
            with sr.AudioFile(path) as source:
                audio_text = r.record(source)  # Use record() instead of listen()

            # Convert speech to text
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)

            paragraph = text

            lines_list = tokenize.sent_tokenize(paragraph)
            print(lines_list)

            NEG = NEU = POS = 0

            sid = SentimentIntensityAnalyzer()  # Initialize once, outside loop
            for sentence in lines_list:
                ss = sid.polarity_scores(sentence)
                print(f"Sentence: {sentence}, Scores: {ss}")

                NEG += ss.get("neg", 0)
                NEU += ss.get("neu", 0)
                POS += ss.get("pos", 0)

            if NEG > max(NEU, POS):
                print(f"Negative Emotion {NEG * 100:.2f}%")
            elif POS > max(NEG, NEU):
                print(f"Positive Emotion {POS * 100:.2f}%")
            else:
                print(f"Neutral Emotion {NEU * 100:.2f}%")

        except Exception as e:
            print(f"Error: {e}")
# cp=Tk()
# w=AdminHome(cp)
