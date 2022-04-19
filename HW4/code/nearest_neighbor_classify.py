from __future__ import print_function

import numpy as np
import scipy.spatial.distance as distance

def nearest_neighbor_classify(train_image_feats, train_labels, test_image_feats):

    distance_mtx = distance.cdist(test_image_feats, train_image_feats)
    nn_index = np.argmin(distance_mtx, axis=1)
    test_predicts = [train_labels[i] for i in nn_index]

    return test_predicts
