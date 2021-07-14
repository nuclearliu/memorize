#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import numpy as np
import time
import cet6word
import pickle

def getWords():
    words = []
    with open("六级核心词.txt", "r") as f:
        for line in f:
            words.append(line[:-1])
    return words


def saveDict(words):
    print("Generating dictionary...")
    words = set(words)
    total = len(words)
    print("We haven {} words in total".format(total))
    finished = 0.0;
    dictionary = []
    print("0%...", end="")
    for word in words:
        instruct = "wd " + word
        info = os.popen(instruct).readlines()
        w = cet6word.Word(word, info)
        dictionary.append(w)
        finished += 1
        if finished != total:
            print("{:.2f}%...".format(finished/total * 100), end="")
        else:
            print("100%")
    fn = "res/cet6core.pkl"
    print("Saving dictionary to as " + fn + "\n...")
    with open(fn, "wb") as f:
        for word in dictionary:
            pickle.dump(word, f)
    print("Done!\n")
    return dictionary


def readDict():
    fn = "res/cet6core.pkl"
    f = open(fn, "rb")
    dictionary = []
    while 1:
        try:
            word = pickle.load(f)
            dictionary.append(word)
        except:
            break
    f.close()
    return dictionary





if __name__ == "__main__":
    # words = getWords()
    # saveDict(words)
    dictionary = readDict()
    for word in dictionary:
        print(word.content, end="")
    # wordsToBeReviewed = []
    # wordsNotLearned = []
    # for word in dictionary:

