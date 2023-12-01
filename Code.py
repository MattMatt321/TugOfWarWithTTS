from time import sleep

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

def Won():
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
           TextToSpeak = "Red has won with 10 clicks! Green had "+str(greenCount)+" clicks, :( "
        else:
            TextToSpeak = "Green has won with 10 clicks! Red had "+str(redCount)+" clicks, :( "
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
for i in range(3,0,-1):
    SpeakText(str(i),False)
    wait(1)
SpeakText("GO!",False)
wait(0.1)
while (gameRunning == True):
    if(redButton.getState() and redPressed == False):
        redPressed = True
        redCount+=1
        Won()
    elif redButton.getState() == False and redPressed == True:
        redPressed = False
    if(greenButton.getState() and greenPressed == False):
        greenPressed = True
        greenCount+=1
        Won()
    elif greenButton.getState() == False and greenPressed == True:
        greenPressed = False




