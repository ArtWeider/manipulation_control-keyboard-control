'''import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone(device_index=1) as source:
    print("Скажите что-нибудь ...")
    audio = r.listen(source)

query = r.recognize_google(audio, language="ru-RU")
print("Вы сказали: " + query.lower())'''

import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

main = None

opts = {
    "tbr": (),
    "cmds": {
        'park': ('парковка', 'вернуться', 'припарковаться'),
        "pointToRobot": ('точку к манипулятору', 'точку к роботу'),
        'robotToPoint': ('манипулятор к точке', 'робот к точке'),
        'pause': ('пауза', 'паузу'),
        'stop': ('стоп', 'остановить', 'прекратить'),
        'sponge': ('взять губку', 'схватить губку'),
        'bolt': ('взять болт', 'схватить болт'),
        'marker': ('взять маркер', 'схватить маркер')

    }
}

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()

        cmd = voice

        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])

    except sr.UnknownValueError: pass
    except sr.RequestError as e: pass


def recognize_cmd(cmd):
    print(cmd)
    RC = {'cmd': '', 'percent': 0}
    cmd = cmd.split(' ')
    for key, value in opts['cmds'].items():
        for x in value:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent'] and vrt > 50:

                RC['cmd'] = key
                RC['percent'] = vrt

    print(RC['cmd'])
    return RC

def execute_cmd(cmd):
    if cmd == 'park':
        print('Парковка')
        main.manipulatorController.stopPlaying()
        main.manipulatorController.forceSend("P")

    elif cmd == 'pointToRobot':
        print('Точку к манипулятору')
        main.pointMenuWidget.onPointToRobotPressed()


    elif cmd == 'robotToPoint':
        print('Манипулятор к точке')
        main.pointMenuWidget.onRobotToPoint()

    elif cmd == 'pause':
        print('Пауза')
        main.manipulatorController.pause()

    elif cmd == 'stop':
        print('Стоп')
        main.manipulatorController.stopPlaying()



with m as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(m, callback)


