# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 13:02:41 2015

Copyright 2015 Nicolo' Navarin

This file is part of scikit-learn-graph.

scikit-learn-graph is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

scikit-learn-graph is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with scikit-learn-graph.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from skgraph.kernel.ODDSTGraphKernel import ODDSTGraphKernel
from skgraph.kernel.ODDSTOrthogonalizedGraphKernel import ODDSTOrthogonalizedGraphKernel
from skgraph.kernel.ODDSTRandomSplitGraphKernel import ODDSTRandomSplitGraphKernel

from skgraph.datasets import load_graph_datasets
from sklearn import datasets


if __name__=='__main__':
    if len(sys.argv)<1:
        sys.exit("python ODDKernel_example.py dataset r l filename kernel")
    dataset=sys.argv[1]
    max_radius=int(sys.argv[2])
    la=float(sys.argv[3])
    #when kernel is STRandomSplit, lambda is in fact the seed of the random split. Lambda is fixed to 1
    #hashs=int(sys.argv[3])
    njobs=1
    name=str(sys.argv[4])
    kernel=sys.argv[5]
    
    if dataset=="CAS":
        print "Loading bursi(CAS) dataset"        
        g_it=load_graph_datasets.load_graphs_bursi()
    elif dataset=="GDD":
        print "Loading GDD dataset"        
        g_it=load_graph_datasets.load_graphs_GDD()
    elif dataset=="CPDB":
        print "Loading CPDB dataset"        
        g_it=load_graph_datasets.load_graphs_CPDB()
    elif dataset=="AIDS":
        print "Loading AIDS dataset"        
        g_it=load_graph_datasets.load_graphs_AIDS()
    elif dataset=="NCI1":
        print "Loading NCI1 dataset"        
        g_it=load_graph_datasets.load_graphs_NCI1()
    else:
        print "Unknown dataset name"
     

    if kernel=="ST":
        ODDkernel=ODDSTGraphKernel(r=max_radius,l=la)
    elif kernel=="STOrthogonalized":
        ODDkernel=ODDSTOrthogonalizedGraphKernel(r=max_radius,l=la)
    elif kernel=="STRandomSplit":
        ODDkernel=ODDSTRandomSplitGraphKernel(r=max_radius,l=1,rs=la)
       
    GM_list=ODDkernel.computeKernelMatrixTrain(g_it.graphs) #Parallel ,njobs
    for mat in xrange(len(GM_list)):
        GMsvm=[]    
        for i in xrange(len(GM_list[mat])):
            GMsvm.append([])
            GMsvm[i]=[i+1]
            GMsvm[i].extend(GM_list[mat][i])
        print "Saving Gram matrix"
        #datasets.dump_svmlight_file(GMsvm,g_it.target, name+".svmlight")
        datasets.dump_svmlight_file(GMsvm,g_it.target, name+".height"+str(mat)+".svmlight")
    #print GM