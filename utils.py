
import urllib.parse

def joinWordsToMakeString(wordList):
    str = ''
    for word in wordList:
        str = str + word + ' '
    return str.strip()

def decodeUrls(urlString):
    return (urllib.parse.unquote(urlString))
    