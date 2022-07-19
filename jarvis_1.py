import datetime
import os
import random
import smtplib
import sys
import time
import webbrowser
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
import PyPDF2
import cv2
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import wikipedia
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import QTimer, QTime, QDate, Qt
from PySide2.QtGui import QMovie
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import loadUiType
from requests import get
from jarvisUi import Ui_jarvisUi

'''Defining engine for voices'''
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login('akshitakanther2000@gmail.com', 'Nk31107#')
    server.sendmail('akshitakanther2000@gmail.com', to, content)
    server.close()


def pdf_reader():
    book = open('D:\\Email Validation in JavaScript.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total no. of pages in this pdf {pages}")
    speak("please enter the page no. from which i have to read")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)


# function for converting text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def send_whatsapp_message(number, message):
    pywhatkit.sendwhatmsg_instantly(f"+91{number}", message)


# to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good morning")
    elif hour > 12 and hour < 16:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("Hello, I am Jarvis . Please tell me how can i help you")


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.start()

    '''function for user input and convert voice into text'''

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=4, phrase_time_limit=5)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")
        except Exception as e:
            speak("Say that again please...")
            return "none"
        return query

    def start(self):
        wish()
        while True:
            # if 1:
            self.query = self.takecommand().lower()

            if "open notepad" in self.query:
                npath = "C:\\windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif "close notepad" in self.query:
                speak("okay , closing notepad")
                os.system("taskkill /f /im notepad.exe")

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "open adobe reader" in self.query:
                npath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Reader XI"
                os.startfile(npath)

            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "play music" in self.query:
                music_dir = "C:\\Users\\hp\\Music\\4K YouTube to MP3"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                '''for song in songs:
                    if song.endswith('.mp3'):'''
                os.startfile(os.path.join(music_dir, rd))

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("searching wikipedia...")
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to wikipedia")
                speak(results)

            elif 'what is your name' in self.query:
                speak("My name is Jarvis.")

            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "open google" in self.query:
                speak("what should i search on google")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")

            elif "take screenshot" in self.query or "take a screenshot" in self.query:
                speak("Please tell me the name for this screenshot file")
                name = self.takecommand().lower()
                speak("please hold the screen for few seconds i am taking screenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("Screenshot is taken successfully")

            elif 'volume up' in self.query:
                pyautogui.press("volumeup")

            elif 'volume down' in self.query:
                pyautogui.press("volumedown")

            elif 'volume mute' in self.query or 'mute' in self.query:
                pyautogui.press("volumemute")

            elif 'what is the time' in self.query:
                Time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f'The time is {Time}')

            elif 'play song on youtube' in self.query or 'song youtube' in self.query:
                speak("What should i play on youtube?")
                answer = self.takecommand()
                pywhatkit.playonyt(answer)
                speak(f'Playing {answer}')

            elif 'hello' in self.query or 'hi' in self.query:
                speak('Hello! how can i help you?')
                answer = self.takecommand()

            elif 'what can you do for me' in self.query:
                speak('I can play music, search, tell news, switch the window, take screenshot etc.')

            elif "send whatsapp message" in self.query:
                speak('On what number should I send the message ? Please enter in the console: ')
                number = input("Enter the number: ")
                speak("What is the message ?")
                message = self.takecommand().lower()
                send_whatsapp_message(number, message)
                speak("I've sent the message.")

            elif "exit" in self.query:
                speak("thanks for using me , have a good day.")
                sys.exit()

            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif 'switch the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif 'close the window' in self.query:
                speak("closing the window")
                pyautogui.hotkey('alt', 'f4')

            elif 'minimise the windows ' in self.query or 'minimise the window' in self.query:
                speak("minimizing window")
                pyautogui.hotkey('Win', 'd')

            elif 'maximize the windows' in self.query or 'maximize the window' in self.query:
                speak("maximizing windows")
                pyautogui.hotkey('Win', 'd')

            elif 'read pdf' in self.query:
                pdf_reader()

            elif 'timer' in self.query or 'stopwatch' in self.query:
                speak("For how many minutes?")
                timing = self.takecommand()
                timing = timing.replace('minutes', '')
                timing = timing.replace('minute', '')
                timing = timing.replace('for', '')
                timing = float(timing)
                timing = timing * 60
                speak(f'I will remind you in {timing} seconds')
                time.sleep(timing)
                speak('Your time has been finished')

            elif 'tell me news' in self.query:
                speak("source: bbc")
                self.query = {"source": "bbc-news",
                              "sortBy": "top",
                              "apiKey": "0bf70eba94704ad8957968d257856abb"}  # Enter your apikey watch video to know how to get apikey
                main_url = "https://newsapi.org/v1/articles?"
                res = requests.get(main_url, params=self.query)
                open_bbc_page = res.json()
                article = open_bbc_page["articles"]
                results = []

                for ar in article:
                    results.append(ar["title"])

                for i in range(len(results)):
                    print(i + 1)
                    speak(results[i])

            elif 'send mail' in self.query or 'send email' in self.query or 'send gmail' in self.query:
                try:
                    speak("What should I say?")
                    content = self.takecommand()
                    to = 'akshitakanther18.set@modyuniversity.ac.in'
                    sendEmail(to, content)
                    speak('Email has been sent!')
                except Exception as e:
                    print(e)
                    speak("Sorry, I am not able to send this email")


startExecution = MainThread()
FROM_MAIN_ = loadUiType(os.path.join(os.path.dirname(__file__), "./jarvisUi.ui"))


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../../Downloads/man1.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../Downloads/man2.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
