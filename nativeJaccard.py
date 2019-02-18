#   This file implements the native/naive Jaccard similarity algorithm
#   to find similarities within a large dataset of lines

def main():

    # stores questions into a list with the qid in lines[0] and the question in lines[1]
    questionFile = input("Please specify an input file to find similarites in: (eg: question_4k.tsv)\n")
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

    # Get threshold from user (0.6 for question 1)
    threshold = float(input("Please enter a threshold (eg: 0.6)\n"))

    for qid, words in questions.items():
        similarqid = findSims(questions, words, threshold)
        if len(similarqid) > 0:
            print(qid, similarqid)


def findSims(questions, words1, threshold):
    similarqid = []

    # Looking through item2
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
        if (intersect / union) > threshold:
            similarqid.append(qid)
    return similarqid

if __name__ == "__main__":
    main() 