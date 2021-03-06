import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '',''))
import numpy as np
#from skgraph import datasets
from sklearn import svm
#from skgraph.ioskgraph import *
from math import sqrt
import sys
from sklearn.metrics import roc_auc_score

#"sys.path.append('..\\..\\Multiple Kernel Learning\\Framework')"
if len(sys.argv)<4:
    sys.exit("python cross_validation_from_matrix_norm.py inputMatrix.libsvm C outfile")

c=float(sys.argv[2])

##TODO read from libsvm format
from sklearn.datasets import load_svmlight_file
km, target_array = load_svmlight_file(sys.argv[1])
#print km
#tolgo indice
kmgood=km[:,1:].todense()
gram=km[:,1:].todense()
for i in xrange(len(target_array)):
    for j in xrange(0,len(target_array)):
        #AUC cross validationprint i,j,kmgood[i,j],kmgood[i,i],kmgood[j,j]
        gram[i,j]=kmgood[i,j]/sqrt(kmgood[i,i]*kmgood[j,j])
#print gram
from sklearn import cross_validation
for rs in range(42,53):
    f=open(str(sys.argv[3]+".seed"+str(rs)+".c"+str(c)),'w')

    
    kf = cross_validation.StratifiedKFold(target_array, n_folds=10, shuffle=True,random_state=rs)
    #print kf    
    #remove column zero because
    #first entry of each line is the index
    
    #gram=km[:,1:].todense()
    f.write("Total examples "+str(len(gram))+"\n")
    f.write("CV\t test_AUROC\n")
    #print gram
    # normalization
    #for i in range(len(gram)):
    #    for j in range(len(gram)):
    #        gram[i,j]=gram[i,j]/sqrt(gram[i,i]+gram[j,j])
    
    sc=[]
    for train_index, test_index in kf:
        #print("TRAIN:", train_index, "TEST:", test_index)
    
        #generated train and test lists, incuding indices of the examples in training/test
        #for the specific fold. Indices starts from 0 now
        
        clf = svm.SVC(C=c, kernel='precomputed',probability=True)
        train_gram = [] #[[] for x in xrange(0,len(train))]
        test_gram = []# [[] for x in xrange(0,len(test))]
          
        #generate train matrix and test matrix
        index=-1    
        for row in gram:
            index+=1
            if index in train_index:
                train_gram.append([gram[index,i] for i in train_index])
            else:
                test_gram.append([gram[index,i] for i in train_index])
    
    
    
        #print gram
        X_train, X_test, y_train, y_test = np.array(train_gram), np.array(test_gram), target_array[train_index], target_array[test_index]
        #COMPUTE INNERKFOLD
        kf = cross_validation.StratifiedKFold(y_train, n_folds=10, shuffle=True,random_state=rs)
        inner_scores= cross_validation.cross_val_score(
        clf, X_train, y_train, cv=kf, scoring='roc_auc')
        #print "inner scores", inner_scores
        print "Inner AUROC: %0.4f (+/- %0.4f)" % (inner_scores.mean(), inner_scores.std() / 2)

        f.write(str(inner_scores.mean())+"\t")

    
        clf.fit(X_train, y_train)
    
        # predict on test examples
        y_test_predicted=clf.predict_proba(X_test)
        #print y_test_predicted
        sc.append(roc_auc_score(y_test, y_test_predicted[:,1]))
        f.write(str(roc_auc_score(y_test, y_test_predicted[:,1]))+"\n")

    f.close()
scores=np.array(sc)
print "AUROC: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() / 2)
    
