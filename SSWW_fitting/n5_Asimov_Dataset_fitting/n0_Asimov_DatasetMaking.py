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
        OF = TFile("Asimov_Dataset.root","RECREATE")
        lep1pt_hist = TH1D("lep1pt_data","lep1pt_data",BinNum,20,650);
        dphijj_hist = TH1D("dphijj_data","dphijj_data",BinNum,-0.5,3.5);
        detajj_hist = TH1D("detajj_data","detajj_data",BinNum,2,10);
        jet1pt_hist = TH1D("jet1pt_data","jet1pt_data",BinNum,20,800);
        lep1pt_hist_LL = TH1D("lep1pt_LL","lep1pt_LL",BinNum,20,650);
        dphijj_hist_LL = TH1D("dphijj_LL","dphijj_LL",BinNum,-0.5,3.5);
        detajj_hist_LL = TH1D("detajj_LL","detajj_LL",BinNum,2,10);
        jet1pt_hist_LL = TH1D("jet1pt_LL","jet1pt_LL",BinNum,20,800);
        lep1pt_hist_TTTL = TH1D("lep1pt_TTTL","lep1pt_TTTL",BinNum,20,650);
        dphijj_hist_TTTL = TH1D("dphijj_TTTL","dphijj_TTTL",BinNum,-0.5,3.5);
        detajj_hist_TTTL = TH1D("detajj_TTTL","detajj_TTTL",BinNum,2,10);
        jet1pt_hist_TTTL = TH1D("jet1pt_TTTL","jet1pt_TTTL",BinNum,20,800);

        '''
        LL_lep1pt_array = tree2array(TreeLL, branches='lep1pt')
        LL_lep1pt_array_min = np.amin(LL_lep1pt_array); LL_lep1pt_array_max = np.amax(LL_lep1pt_array);
        LL_dphijj_array = tree2array(TreeLL, branches='dphijj')
        LL_dphijj_array_min = np.amin(LL_dphijj_array); LL_dphijj_array_max = np.amax(LL_dphijj_array);

        TTTL_lep1pt_array = tree2array(TreeTTTL, branches='lep1pt')
        TTTL_lep1pt_array_min = np.amin(TTTL_lep1pt_array); TTTL_lep1pt_array_max = np.amax(TTTL_lep1pt_array);
        LL_lep1pt_array = tree2array(TreeLL, branches='lep1pt')
        LL_lep1pt_array_min = np.amin(LL_lep1pt_array); LL_lep1pt_array_max = np.amax(LL_lep1pt_array);
        '''

        print("Rotation on TreeLL, Filling Histogram")
        for i in range(EntriesLL):
            if i%50000==0: print("Now looping", i," of Total",EntriesLL);
            TreeLL.GetEntry(i)
            lep1pt_hist.Fill(eval("TreeLL.lep1pt"),LL_scale)
            dphijj_hist.Fill(eval("TreeLL.dphijj"),LL_scale)
            detajj_hist.Fill(eval("TreeLL.detajj"),LL_scale)
            jet1pt_hist.Fill(eval("TreeLL.jet1pt"),LL_scale)
            lep1pt_hist_LL.Fill(eval("TreeLL.lep1pt"))
            dphijj_hist_LL.Fill(eval("TreeLL.dphijj"))
            detajj_hist_LL.Fill(eval("TreeLL.detajj"))
            jet1pt_hist_LL.Fill(eval("TreeLL.jet1pt"))
        
        print("Rotation on TreeTTTL, Filling Histogram")
        for i in range(EntriesTTTL):
            if i%50000==0: print("Now looping", i," of Total",EntriesTTTL);
            TreeTTTL.GetEntry(i)
            lep1pt_hist.Fill(eval("TreeTTTL.lep1pt"),TTTL_scale)
            dphijj_hist.Fill(eval("TreeTTTL.dphijj"),TTTL_scale) 
            detajj_hist.Fill(eval("TreeTTTL.detajj"),TTTL_scale)
            jet1pt_hist.Fill(eval("TreeTTTL.jet1pt"),TTTL_scale)
            lep1pt_hist_TTTL.Fill(eval("TreeTTTL.lep1pt"))
            dphijj_hist_TTTL.Fill(eval("TreeTTTL.dphijj"))
            detajj_hist_TTTL.Fill(eval("TreeTTTL.detajj"))
            jet1pt_hist_TTTL.Fill(eval("TreeTTTL.jet1pt"))
        
        print("Resetting error-bar on each bin")
        for i in range(BinNum):
            temp_content_error = sqrt(lep1pt_hist.GetBinContent(i+1))
            lep1pt_hist.SetBinError(i+1, temp_content_error)
            temp_content_error = sqrt(dphijj_hist.GetBinContent(i+1))
            dphijj_hist.SetBinError(i+1, temp_content_error)
            temp_content_error = sqrt(detajj_hist.GetBinContent(i+1))
            detajj_hist.SetBinError(i+1, temp_content_error)
            temp_content_error = sqrt(jet1pt_hist.GetBinContent(i+1))
            jet1pt_hist.SetBinError(i+1, temp_content_error)

        OF.Write()
        OF.Close()
        return

    def Append_MC(self):
        
        return


def main():
    infileLL = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_LL_TTTL_compare/SS_250M_cut_LL.root" #FIXME
    infileTTTL = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_LL_TTTL_compare/SS_250M_cut_TTTL.root" #FIXME
    BinNum = 20                           #FIXME
    XSec = 0.17864 #pb                   #FIXME
    Lumi = 3000000  #pb-1 == 10^-3 *fb-1  #FIXME
    eff_sel = 0.015944                      #FIXME
    eff_LL = 0.04503                      #FIXME

    NTotTarget = XSec*Lumi*eff_sel;
    NLLTarget = NTotTarget*eff_LL; NTTTLTarget = NTotTarget*(1-eff_LL)
    print("Targetting LL Event number :",NLLTarget)
    print("Targetting TTTL Event number :",NTTTLTarget)

    Asimov = Asimov_Dataset(infileLL=infileLL,infileTTTL=infileTTTL)
    Asimov.Make_AsimovData(NLLTarget,NTTTLTarget,BinNum)



if __name__=="__main__":
    main()




