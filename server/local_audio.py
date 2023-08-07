import requests as rq
import os, playsound

#https://www.youtube.com/watch?v=bUfUKtJqaxQ For Socket explanation

flaskURL = 'http://localhost:14366/'
def speakText(input_text):
    headers = {'Content-Type': 'application/json'}
    data = {'text': input_text.rstrip()}
    response = rq.post(f"{flaskURL}/text-to-speech", json=data, headers = headers)
    playsound.playsound(response.text)

input_text = input("Enter text to say: ")
speakText(input_text)


