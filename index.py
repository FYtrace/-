#!/usr/bin/env python
# coding=utf-8

import jieba
import linecache

def build_dict (wordlist, line):
    for word in wordlist:
        if word not in dict:
            dict[word] = []
        dict[word].append(line)

def splitSentence (inputFile, outputFile):
    fin = open(inputFile, "r")
    fout = open(outputFile, "w+")

    i = 1 
    for eachLine in fin:
        if i % 4 != 2:
            i += 1
            line = eachLine.strip().decode('utf-8')
            fout.write(line.strip().encode('utf-8')+'\n')
            continue
        line = eachLine.strip().decode('utf-8')
        wordList = list(jieba.cut(line))
        outStr = ''
        build_dict(wordList,i)
        for word in wordList:
            outStr += word
            outStr += ' '
        fout.write(outStr.strip().encode('utf-8'))
        fout.write("\n")
        i += 1
    fin.close()
    fout.close()

def search (dict):
    input = raw_input("please input the key words : ").decode('utf-8')
    total = len(dict[input]) 
    print "\n\ntotal search answer is: %d\n"%(total)
    for i in dict[input]:
        print linecache.getline("jd.txt", i)
        print linecache.getline("jd.txt", i+1)
        print linecache.getline("jd.txt", i+2)
        print u"------------------------------------"

    



dict = {}
splitSentence('jd.txt', 'jd.out.txt')
search (dict)
