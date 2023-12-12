from time import sleep
import random

#Add Phidgets Library 
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
from gtts import gTTS
import os.path

redLED = DigitalOutput()
redLED.setHubPort(1)
redLED.setIsHubPortDevice(True)
redLED.openWaitForAttachment(1000)
#Create Green
greenLED = DigitalOutput()
greenLED.setHubPort(4)
greenLED.setIsHubPortDevice(True)
greenLED.openWaitForAttachment(1000)
#Create GreenButton
greenButton = DigitalInput()
greenButton.setHubPort(5)
greenButton.setIsHubPortDevice(True)
greenButton.openWaitForAttachment(1000)
#Create RedButton
redButton = DigitalInput()
redButton.setHubPort(0)
redButton.setIsHubPortDevice(True)
redButton.openWaitForAttachment(1000)

mixer.init() #Initialzing pyamge mixer

def wait(Number):
    sleep(Number)

maxCount = 10
gameRunning = True
redPressed = False
greenPressed = False
greenCount = 0
redCount = 0

def SpeakText(Text,WaitFor):
    #FileName = "TTS/"+str(Text)+".mp3"
    FileName = "TTS/test.mp3"
    #if True or not os.path.isfile(FileName):
    tts = gTTS(Text, lang='en')
    tts.save(FileName)
    ##playsound(FileName)
    mixer.music.load(FileName) #Loading Music File
    mixer.music.play() #Playing Music with Pygame
    mixer.music.set_volume(10)
    while mixer.music.get_busy() == True and WaitFor == True:
        wait(0.1)

RedName = "Dr. J"
GreenName = "Dr. J2"

def Won():
    greenLED.setState(False)
    redLED.setState(False)
    Winner = ""
    if greenCount >= maxCount:
        Winner = "Green"
    elif redCount >= maxCount:
        Winner = "Red"
    if Winner != "":
        global gameRunning
        gameRunning = False
        TextToSpeak = "Nothing"
        if Winner == "Red":
           TextToSpeak = RedName+" has won with 10 clicks! "+GreenName+" had "+str(greenCount)+" clicks, :( "
        else:
            TextToSpeak = GreenName+" has won with 10 clicks! "+RedName+" had "+str(redCount)+" clicks, :( try harder next time"
        print(TextToSpeak)
        SpeakText(TextToSpeak, False)
        for i in range(5):
            if Winner == "Green":
                greenLED.setState(True)
            else:
                redLED.setState(True)
            wait(0.1)
            if Winner == "Green":
                greenLED.setState(False)
            else:
                redLED.setState(False)
            wait(0.1)
print('Started')
for i in range(2,0,-1):
    SpeakText(str(i),False)
    wait(1)
wait(random.randint(1,3))
SpeakText("GO!",False)
wait(0.1)
greenLED.setState(True)
redLED.setState(True)

while (gameRunning):
    if(redButton.getState() and not redPressed):
        redPressed = True
        redCount+=1
        print(redCount)
        Won()
    elif not redButton.getState() and redPressed:
        redPressed = False
        
    if(greenButton.getState() and not greenPressed):
        greenPressed = True
        greenCount+=1
        print(greenCount)
        Won()
    elif not greenButton.getState() and greenPressed:
        greenPressed = False
