
import itertools
import numpy as np


def smith_waterman(a, b, match_score=3, gap_score=2):
    H = np.zeros(shape=(len(a)+1, len(b)+1))

    for i, j in itertools.product(range(1, H.shape[0]), range(1, H.shape[1])):
        align = H[i-1, j-1] + (match_score if a[i-1] == b[j-1] else - match_score)
        gapA = H[i-1, j] - gap_score
        gapB = H[i, j-1] - gap_score

        H[i, j] = max(align, gapA, gapB, 0)
    
    score = np.max(H)
    ind = np.unravel_index(H.argmax(), H.shape)

    alignmentA = ""
    alignmentB = ""

    while score > 0:
        i, j = ind

        newIndA = (i-1, j-1)
        newIndB = (i-1, j)
        newIndC = (i, j-1)

        scoreA = H[newIndA]
        scoreB = H[newIndB]
        scoreC = H[newIndC]

        nextScore = max([scoreA, scoreB, scoreC])
        maxScoreIndex = np.argmax([scoreA, scoreB, scoreC])

        if maxScoreIndex == 0:
            nextInd = newIndA
            alignmentA += a[i-1]
            alignmentB += b[j-1]
        elif maxScoreIndex == 1:
            nextInd = newIndB
            alignmentA += a[i-1]
            alignmentB += "-"
        elif maxScoreIndex == 2:
            nextInd = newIndC
            alignmentA += "-"
            alignmentB += b[j-1]
        
        score = nextScore
        ind = nextInd

    correct = 0

    for a,b in zip(alignmentA, alignmentB):
        if a == b:
            correct += 1

    percentageAlignment = correct / len(alignmentA)
    
    return alignmentA[::-1], alignmentB[::-1], percentageAlignment