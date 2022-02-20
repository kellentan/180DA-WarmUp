# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 16:09:31 2022

@author: Kellen Cheng
"""

import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("What ingredients would you like to pickup?")
    audio = r.listen(source)
    
try:
    ingredients = r.recognize_sphinx(audio).split()
    ingredients = ",".join(ingredients)
    print("You have successfully picked up " + ingredients)
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))