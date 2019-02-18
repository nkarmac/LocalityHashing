#   This file implements the locality sensitive hashing algorithm
#   to find similarities within a large dataset of lines

from fnv import *
import uuid
import time

threshold = 0.6
s = 14  # num hash tables
r = 6   # minhash signature size
p = 15373875993579943603 # 64-bit prime num
htsize = 10000000 # hashtable size

def main():

    # stores questions into a list with the qid in lines[0] and the question in lines[1]
    questionFile = input("\nPlease specify an input file to find similarites in: (eg: question_4k.tsv)\n")
    lines = [line.rstrip('\n').split('\t') for line in open(questionFile, encoding="utf-8")]
    

    # stores all sets of words in a dictionary indexed by its qid
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
    
    # creating indexable random numbers for hashing
    seta = []
    setb = []
    for i in range(s):
        seta.append(uuid.uuid4().int & (1<<64)-1)
        setb.append(uuid.uuid4().int & (1<<64)-1)
    
    # build dataset of hashtables
    Dataset = []
    for i in range(s):
        hashtable = [None] * htsize

        for qid, words in questions.items():
            signature = []
            for i in range(r):
                minHash = p+1
                for word in words:
                    hc = hashFunc(word, seta[i], setb[i])
                    if hc < minHash:
                        minHash = hc
                signature.append(str(minHash))
            sigint = int(''.join(signature))
            temp = hashtable[sigint % htsize]
            if temp == None:
                hashtable[sigint % htsize] = [qid] * 1
            elif qid not in temp:
                hashtable[sigint % htsize].append(qid)
        Dataset.append(hashtable)

    bigSetBaby = {}
    for qid, words in questions.items():
        similarSet = []
        for i in range(s):
            hashtable = Dataset[i]

            signature = []
            for i in range(r):
                minHash = p+1
                for word in words:
                    hc = hashFunc(word, seta[i], setb[i])
                    if hc < minHash:
                        minHash = hc
                signature.append(str(minHash))
            sigint = int(''.join(signature))
            temp = hashtable[sigint % htsize]

            for newqid in temp:
                if newqid != qid:
                    if newqid not in similarSet:
                        if findSims(questions[qid], questions[newqid]):
                            similarSet.append(newqid)
        bigSetBaby[qid] = similarSet
    
    print()
    print("qid\tsimilar-qids")

    for qid, similarWords in bigSetBaby.items():
        print("%s\t" %qid, end='')
        print(','.join(similarWords))
    
    
        

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