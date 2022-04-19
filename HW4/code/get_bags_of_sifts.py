from PIL import Image
import numpy as np
from scipy.spatial import distance
import pickle
import scipy.spatial.distance as distance
from cyvlfeat.sift.dsift import dsift
from time import time
import pdb

def get_bags_of_sifts(image_paths):

    image_feats=[]
    vocab=pickle.load(open('vocab.pkl', 'rb'))

    for image_path in image_paths:
        img = np.asarray(Image.open(image_path),dtype='float32')
        frames, descriptors = dsift(img, step=[5,5], fast=True)
        distance_matrix = distance.cdist(descriptors,vocab,'euclidean')
        feature_idx = np.argmin(distance_matrix,axis=1)
        unique, counts = np.unique(feature_idx, return_counts=True)
        counter = dict(zip(unique, counts))

        histogram = np.zeros(vocab.shape[0])
        for idx, count in counter.items():
            histogram[idx] = count
        histogram = histogram/histogram.sum()

        image_feats.append(histogram)
        print(image_path)
    image_feats = np.asarray(image_feats)

    return image_feats
