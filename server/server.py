from waitress import serve
from flask import Flask, request
from flask_cors import CORS
from gtts import gTTS
import os, playsound
from pygame import mixer, _sdl2 as devicer
import nltk
import time

nltk.download('words')

from nltk.corpus import words
app = Flask(__name__)
CORS(app)

# TrieNode object
class TrieNode:
    def __init__(self):
        self.children = {}
        self.wordEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    # add word to trie 
    def addWord(self, word):
        curr = self.root
        for c in word:
            if c not in curr.children.keys():
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.wordEnd = True

    # check if a word is in the trie
    def search(self, word):
        curr = self.root
        for c in word:
            if c not in curr.children.keys():
                return False
            curr = curr.children[c]
        return curr.wordEnd
    
    # return the closest word to the input word
    def getClosestWord(self, word):
        currMinDist = [float("inf")]
        currMinWord = [""]

        def dfs(curr, currWord):
            if curr.wordEnd:
                dist = minimumDistance(currWord, word)
                if dist < currMinDist[0]:
                    print((currWord, word))
                    currMinDist[0] = dist 
                    currMinWord[0] = currWord 
            
            for char, child in curr.children.items():
                dfs(child, currWord + char)
        curr = self.root
        currStr = ""
        
        for i in range(len(word)):
            if word[i] not in curr.children.keys():
                dfs(curr, currStr)
                return currMinWord[0]
            curr = curr.children[word[i]]
            currStr += word[i]
        dfs(curr, currStr)
        return currMinWord[0]

        
            


englishWords = words.words()
wordSet = set(englishWords)
print("LENGTH: " + str(len(englishWords)))

trie = Trie()
for word in englishWords:
    trie.addWord(word)

# iterate through all english words, find miminum distance between current word nd target word, update if necessary
def findClosestWord(word):
    if word in wordSet:
        return word 
    currMinDistance = minimumDistance(word, englishWords[0])
    closestWord = englishWords[0]
    for w in englishWords:
        dist = minimumDistance(word, w)
        if dist < currMinDistance:
            currMinDistance = dist
            closestWord = w
    return closestWord


# Given two words, find the minimum edit distance between them. Edits include insertions, deletions, and replacements
"horse", "hor"
def minimumDistance(word1, word2):
    matrix = [[0 for _ in range(len(word2) + 1)] for _ in range(len(word1) + 1)]
    for i in range(len(word1)):
        matrix[i][-1] = len(word1) - i
        
    for i in range(len(word2)):
        matrix[-1][i] = len(word2) - i

    for i in range(len(word1) - 1, -1, -1):
        for j in range(len(word2) - 1, -1, -1):
            if word1[i] == word2[j]:
                matrix[i][j] = matrix[i + 1][j + 1]
            else:
                matrix[i][j] = 1 + min(matrix[i + 1][j], matrix[i][j + 1], matrix[i + 1][j + 1])
        
    return matrix[0][0]

@app.route('/autocorrect', methods = ['POST'])
def autocorrect():
    data = request.get_json()
    text = data["text"]
    print("RECEIVED " + text)
    # distance algorithm
    # start1 = time.time()
    # closestWord = findClosestWord(text)
    # end1 = time.time()
    # print("CLOSEST WORD(DISTANCE ALGO) " + closestWord + " reached in " + str(end1 - start1))

    #trie search
    if text in wordSet:
        return {"text" : text}
    else:
        start = time.time()
        res = trie.getClosestWord(text)
        end = time.time()
        print("CLOSEST WORD(TRIE) " + res + " reached in " + str(end - start))
        return {"text" : res}

@app.route('/text-to-speech', methods = ['POST'])
def textToSpeech():
    '''
        data passed in {'text': text data}
    '''
    data = request.get_json()
    text = data["text"]
    fileName = convertToAudio(text)
    playAudio(fileName)
    os.remove(fileName)
    return {}

def convertToAudio(text):
    tts = gTTS(text=text, lang="en", slow=False)
    fileName = text + ".mp3"
    tts.save(fileName)
    return fileName

def playAudio(fileName):
    mixer.init(devicename = 'VB-Cable')
    mixer.music.load(fileName)
    mixer.music.play()
    while mixer.music.get_busy(): 
        pass
    mixer.quit()
    return 

if __name__ == "__main__":
    print("RUNNING")
    serve(app, host='0.0.0.0', port=14366)



