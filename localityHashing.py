#   This file implements the locality sensitive hashing algorithm
#   to find similarities within a large dataset of lines

from fnv import *
import uuid
import time
import numpy as np

threshold = 0.6
s = 14  # num hash tables
r = 6   # minhash signature size
p = 15373875993579943603 # 64-bit prime num

def main():

    # stores questions into a list with the qid in lines[0] and the question in lines[1]
    questionFile = input("\nPlease specify an input file to find similarites in: (eg: question_4k.tsv)\n")
    lines = [line.rstrip('\n').split('\t') for line in open(questionFile, encoding="utf-8")]
    
    # stores all sets of words in a dictionary indexed by its qid
    numquestions = 0
    questions = {}
    i = 0
    for question in lines:
        # skips first line
        if i == 0:
            i += 1
            continue
        # accepts only properly formatted questions
        elif len(question) != 2:
            continue
        questions[question[0]] = question[1].split(' ')
        numquestions += 1
    
    # creating indexable random numbers for hashing
    seta = []
    setb = []
    for i in range(r):
        seta.append(uuid.uuid4().int & (1<<64)-1)
        setb.append(uuid.uuid4().int & (1<<64)-1)
    
    # build dataset of hashtables
    Dataset = []
    minHashes = np.empty((s,numquestions,r))
    for i in range(s):
        hashtable = {}
        k = 0
        for qid, words in questions.items():
            minSig = np.empty(r)
            for j in range(r):
                minHash = p+1
                for word in words:
                    hc = hashFunc(word, seta[j], setb[j])
                    if hc < minHash:
                        minHash = hc
                minHashes[i,k,j] = minHash
            temp = ''.join(str(x) for x in minHashes[i,k])
            if temp not in hashtable:
                hashtable[temp] = [qid] * 1
            elif qid not in hashtable[temp]:
                hashtable[temp].append(qid)
            k += 1
        Dataset.append(hashtable)

    print()
    print("qid\tsimilar-qids")
    k = 0
    for qid, words in questions.items():
        similarSet = []
        for i in range(s):
            hashtable = Dataset[i]

            for newqid in hashtable[''.join(str(x) for x in minHashes[i,k])]:
                if newqid != qid:
                    if newqid not in similarSet:
                        if findSims(questions[qid], questions[newqid]):
                            similarSet.append(newqid)
        k += 1
        print("%s\t" %qid, end='')
        print(','.join(similarSet))
        
    
    
        

def hashFunc(word,a,b):
    x = hash(word.encode('utf-8'), bits=64)
    hc = (a*x+b) % p
    return hc

def findSims(words1, words2):

    # Naive Jaccard Algorithm
    # loops through all words and divides intersect of words1 and words2 by the union
    # and adds the qid to similarqid[] if the answer > threshold
    intersect = 0
    union = len(words1)
    for word in words2:
        if word in words1:
            intersect += 1
            continue
        union += 1
    if (intersect / union) >= threshold:
        return True
    return False

if __name__ == "__main__":
    main()