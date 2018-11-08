from ROOT import *
import sys, os, math
import numpy as np
from array import array
from root_numpy import root2array, tree2array, array2root, array2tree

def ROC_List_Maker(dirname='./',dirnameNN='./', verbose=0):
    ROC_list = list()
    LL_filename = dirname+"/TEST_ROOT_LL_tree.root"
    TTTL_filename = dirname +"/TEST_ROOT_TTTL_tree.root"
    LL_TFile = TFile(LL_filename,"READ")
    TTTL_TFile = TFile(TTTL_filename,"READ")
    LL_LL_Tree = LL_TFile.Get("tree")
    TTTL_LL_Tree = TTTL_TFile.Get("tree")

    DNN_list = list()
    LL_Entry = LL_LL_Tree.GetEntries(); print("DNN LL Entry :",LL_Entry)
    TTTL_Entry = TTTL_LL_Tree.GetEntries(); print("DNN TTTL Entry :",TTTL_Entry)
    DNN_LL_array = tree2array(LL_LL_Tree, branches='LL');DNN_LL_array.sort()
    DNN_TTTL_array = tree2array(TTTL_LL_Tree, branches='LL');DNN_TTTL_array.sort()
    DNN_list.append([0,1]); pbr=0;
    for i,val in enumerate(DNN_LL_array):
        if(i+1==int(0.1*LL_Entry) & (pbr==0)):
            pbr=1; 


def main():
    dirname = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum1000000/LayerNum_7+Node_150+BatchSize_10/TEST_TRAIN_ROOT" #FIXME
#    dirname = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181026_TrainENum1500000/LayerNum_7+Node_300+BatchSize_10/TEST_TRAIN_ROOT"
    dirnameNN = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum700000/LayerNum_1+Node_150+BatchSize_10/TEST_TRAIN_ROOT" #FIXME
    verbose = 1  #FIXME

    Roc_list = ROC_List_Maker(dirname=dirname,dirnameNN=dirnameNN,verbose=verbose)




if __name__=="__main__":
    main()

