import numpy as np
from scipy.spatial.distance import cdist

def SIFTMatcher(descriptor1, descriptor2, THRESH=0.49):

    match = []
    dist_matrices = cdist(descriptor1, descriptor2, 'sqeuclidean')
    for idx1, dist_list in enumerate(dist_matrices):

        # find 2 minimum pairs
        smallest = [-1, 999999999]
        second_smallest = [-1, 999999999]
        for idx2, dist in enumerate(dist_list):
            dist = np.sqrt(dist)
            if dist < smallest[1]:
                second_smallest = smallest
                smallest = [idx2, dist]
            elif dist < second_smallest[1]:
                second_smallest = [idx2, dist]

        # check if the smallest pair is a match
        if smallest[1] < THRESH * second_smallest[1]:
            match.append([idx1, smallest[0]])

    return np.asarray(match)
