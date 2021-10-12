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
    "tbr": ('скажи'),
    "cmds": {
        'park': ('парковка', 'вернуться'),
        'radio': ('включи музыку', 'воспроизведи радио', 'включи радио'),
        'stupid1': ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()
        print("[log] Разпознано: " + voice)


        cmd = voice


        for x in opts['tbr']:
            cmd.replace(x, '').strip()

        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print('[log] Голос не распознан!')
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    cmd = cmd.split(' ')
    for key, value in opts['cmds'].items():
        for word in cmd:
            for x in value:
                vrt = fuzz.ratio(word, x)
                if vrt > RC['percent'] and vrt > 50:
                    RC['cmd'] = key
                    RC['percent'] = vrt


    return RC

def execute_cmd(cmd):
    if cmd == 'park':
        main.manipulatorController.toSend = 'P'
        main.manipulatorController.send(False)

    elif cmd == 'radio':
        print('radio')

    elif cmd == 'stupid1':
        print('i am stupid')

    else:
        print('unknown command')


with m as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(m, callback)


