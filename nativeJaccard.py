#   This file implements the native/naive Jaccard similarity algorithm
#   to find similarities within a large dataset of lines

import time

def main():

	threshold = 0.6

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

	print()
    print("qid\tsimilar-qids")
	
	starttime = time.time()

    # finds similar questions and prints
    for qid, words in questions.items():
        similarqid = findSims(questions, words, threshold)
        print("%s\t" % qid, end="")
        print(','.join(similarqid))
	
	print("\ntotal execution time is: %s seconds\n" % (time.time() - starttime))


def findSims(questions, words1, threshold):
    similarqid = []

    # Naive Jaccard Algorithm
    # loops through all words and divides intersect of words1 and words2 by the union
    # and adds the qid to similarqid[] if the answer > threshold
    for qid,words2 in questions.items():
        if words2 == words1:
            continue
        intersect = 0
        union = len(words1)
        for word in words2:
            if word in words1:
                intersect += 1
                continue
            union += 1
        if (intersect / union) >= threshold:
            similarqid.append(qid)
    return similarqid

if __name__ == "__main__":
    main() 