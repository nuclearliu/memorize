#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import numpy as np
import time
import cet6word
import pickle
import random

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
    print("Saving dictionary as " + fn + "\n...")
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


def waitForEnter(prompt=""):
    sys.stdout.flush()
    instr = input(prompt)
    while instr != "":
        instr = input(prompt)


def review(words):
    i = 1
    miss = []
    for word in words:
        if word.mastered:
            continue
        print("review: {}/{}".format(i, len(words)))
        print(word.content, end="")
        print(word.pronunciation, end="")
        for line in word.translation:
            print(line, end="")
        word.reviewCount += 1
        sys.stdout.flush()
        instr = input().strip() # if still remember, press enter, if too easy, enter "pass"
        if instr == "":
            word.toBeReviewed = False
        elif instr == "pass":
            word.toBeReviewed = False
            word.alreadyLearned = True
            word.mastered = True
            print("")
        else:
            miss.append(word)
        i += 1
    print("")
    check(miss)


def learnNew(words):
    print("Here are today's words")
    i = 1
    for word in words:
        print("new word: {}/{}".format(i, len(words)))
        word.getInfo()
        word.alreadyLearned = True
        word.toBeReviewed = True
        sys.stdout.flush()
        instr = input()
        if instr == "pass":
            word.mastered = True
            word.toBeReviewed = False
            print("")
        elif instr == "":
            pass
        i += 1


def check(words):
    done = []
    miss = []
    total = 0
    for word in words:
        if not word.mastered:
            total += 1
    if total != 0:
        waitForEnter("Do some test?")
    while len(done) < total:
        target = total - len(done)
        i = 1
        for word in words:
            if word in done or word.mastered:
                continue
            print("test: {}/{}".format(i, target))
            for line in word.translation:
                print(line, end="")
            answer = input("\nanswer:{}".format(word.word[0]))
            if word.word[0] + answer == word.word:
                print("Correct!")
                done.append(word)
            else:
                print("The answer is {}".format(word.content)[:-1])
                print("Try again later")
                miss.append(word)
                word.incorrectCount += 1
            waitForEnter()
            i += 1
        # print(info)
    miss = set(miss)
    return miss


if __name__ == "__main__":
    # words = getWords()
    # saveDict(words)
    dictionary = readDict()
    # 单词计划
    schedule = 3
    # for word in dictionary:
    #     print(word.content, end="")
    wordsToBeReviewed = []
    wordsNotLearned = []
    wordsToBeLearned = []
    for word in dictionary:
        if word.toBeReviewed and not word.mastered:
            wordsToBeReviewed.append(word)
        elif not word.alreadyLearned and not word.mastered:
            wordsNotLearned.append(word)
    if len(wordsNotLearned) > schedule:
        wordsToBeLearned = random.sample(wordsNotLearned, schedule)
    else:
        schedule = len(wordsNotLearned)
        wordsToBeLearned = wordsNotLearned

    # status report
    print("total: {} words".format(len(dictionary)))
    print("already learned: {} words".format(len(dictionary) - len(wordsNotLearned)))
    print("your schedule: {} words a day".format(schedule))

    # review & learn & check
    waitForEnter("Start today's learning? (press enter)")
    review(wordsToBeReviewed)
    learnNew(wordsToBeLearned)
    miss = check(wordsToBeLearned)

    # modify cet6core.pkl
    fn = "res/cet6core.pkl"
    with open(fn, "wb") as f:
        for word in dictionary:
            pickle.dump(word, f)

    # summary
    waitForEnter("Get today's report?")
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)
    print("Today you learned {} words:".format(len(wordsToBeLearned)))
    i = 0
    for word in wordsToBeLearned:
        print(word.word + "\t", end="")
        i = i + 1
        if i == 4:
            print("")
            i = 0
    if i != 0:
        print("")
    if len(miss) > 0:
        print("\nYou may want to review these words:")
        for word in miss:
            print(word.word + "\t", end="")
        print("\n")