from sklearn import preprocessing
from sklearn.svm import LinearSVC
from sklearn import preprocessing
import pdb

def svm_classify(train_image_feats, train_labels, test_image_feats):

    svm = LinearSVC(C= 10, class_weight=None, dual=True, fit_intercept=True,
                    intercept_scaling=1, loss='squared_hinge', max_iter= 500,
                    multi_class='ovr', penalty='l2', random_state=0, tol= 0.00005,
                    verbose=0)
    svm.fit(train_image_feats, train_labels)
    pred_label = svm.predict(test_image_feats)

    return pred_label
