from ROOT import *
from math import sqrt
import sys, os, math
#from root_numpy import *
import numpy as np
sys.path.append("/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/func")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class Asimov_Dataset:
    def __init__(self,infileLL,infileTTTL):
        self.tfileLL = TFile(infileLL,"READ")
        self.tfileTTTL = TFile(infileTTTL,"READ")
        return

    def Make_AsimovData(self,NLLTarget,NTTTLTarget,BinNum=20):
        TreeLL = self.tfileLL.Get("tree"); TreeTTTL = self.tfileTTTL.Get("tree")
        EntriesLL = TreeLL.GetEntries(); print("Total Entry of Tree LL :",EntriesLL)
        EntriesTTTL = TreeTTTL.GetEntries(); print("Total Entry of Tree TTTL :",EntriesTTTL)
        LL_scale = NLLTarget/EntriesLL; TTTL_scale = NTTTLTarget/EntriesTTTL
        print("Scale Factor on each LL event :",LL_scale); print("Scale Factor on each TTTL event :",TTTL_scale)

        #cv = TCanvas("cv","cv",1200,900);
        OF = TFile("Asimov_Dataset_forDNN_Raw4p0M_Mjj1200.root","RECREATE")
        Asimov_hist = TH1D("Asimov_data","Asimov_data",BinNum,0,1)
        hist_LL = TH1D("LL_LL","LL_LL",BinNum,0,1)
        hist_TTTL = TH1D("TTTL_LL","TTTL_LL",BinNum,0,1)

        print("Rotation on TreeLL, Filling Histogram")
        for i in range(EntriesLL):
            if i%50000==0: print("Now looping", i," of Total",EntriesLL);
            TreeLL.GetEntry(i)
            Asimov_hist.Fill(eval("TreeLL.LL"),LL_scale)
            hist_LL.Fill(eval("TreeLL.LL"))

        print("Rotation on TreeTTTL, Filling Histogram")
        for i in range(EntriesTTTL):
            if i%50000==0: print("Now looping", i," of Total",EntriesTTTL);
            TreeTTTL.GetEntry(i)
            Asimov_hist.Fill(eval("TreeTTTL.LL"),TTTL_scale)
            hist_TTTL.Fill(eval("TreeTTTL.LL"))

        print("Resetting error-bar on each bin")
        for i in range(BinNum):
            temp_content_error = sqrt(Asimov_hist.GetBinContent(i+1))
            Asimov_hist.SetBinError(i+1, temp_content_error)

        OF.Write()
        OF.Close()
        return

    def Append_MC(self):
        
        return


def main():
    #infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/Raw_20181112_TrainENum1800000/LayerNum_5+Node_500+BatchSize_100/TEST_TRAIN_ROOT"  #FIXME
    infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/Raw_20181115_TrainENum2600000/LayerNum_10+Node_150+BatchSize_10/TEST_TRAIN_ROOT_Mjj1200"

    infileLL = infile + "/SS_4p0M_cut_LL_Mjj1200_tree.root"
    infileTTTL = infile + "/SS_4p0M_cut_TTTL_Mjj1200_tree.root"
    BinNum = 20                           #FIXME
    XSec = 0.17864 #pb                   #FIXME
    Lumi = 3000000  #pb-1 == 10^-3 *fb-1  #FIXME
    eff_sel = 0.015944 * 0.739                     #FIXME
    eff_LL = 0.04503                      #FIXME

    NTotTarget = XSec*Lumi*eff_sel;
    NLLTarget = NTotTarget*eff_LL; NTTTLTarget = NTotTarget*(1-eff_LL)
    print("Targetting LL Event number :",NLLTarget)
    print("Targetting TTTL Event number :",NTTTLTarget)

    Asimov = Asimov_Dataset(infileLL=infileLL,infileTTTL=infileTTTL)
    Asimov.Make_AsimovData(NLLTarget,NTTTLTarget,BinNum)



if __name__=="__main__":
    main()




