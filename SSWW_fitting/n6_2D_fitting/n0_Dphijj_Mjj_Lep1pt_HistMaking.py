from ROOT import *
from math import sqrt
import sys, os, math
#from root_numpy import *
import numpy as np
sys.path.append("/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/func")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class TwoD_Histos:
    def __init__(self,infileLL,infileTTTL):
        self.tfileLL = TFile(infileLL,"READ")
        self.tfileTTTL = TFile(infileTTTL,"READ")
        return

    def Make_AsimovData_MjjDphijj(self,NLLTarget,NTTTLTarget):
        TreeLL = self.tfileLL.Get("tree"); TreeTTTL = self.tfileTTTL.Get("tree")
        EntriesLL = TreeLL.GetEntries(); print("Total Entry of Tree LL :",EntriesLL)
        EntriesTTTL = TreeTTTL.GetEntries(); print("Total Entry of Tree TTTL :",EntriesTTTL)

        OF = TFile("TwoD_Histos_MjjDphijj.root","RECREATE")

        ## Beginning of 'MjjDphijj'
        MjjDphijj_lowMjj_Asimov = TH1D("MjjDphijj_lowMjj_Asimov","MjjDphijj_lowMjj_Asimov",30,-0.5,3.5);
        MjjDphijj_highMjj_Asimov = TH1D("MjjDphijj_highMjj_Asimov","MjjDphijj_highMjj_Asimov",30,-0.5,3.5);
        MjjDphijj_LL_lowMjj = TH1D("MjjDphijj_LL_lowMjj","MjjDphijj_LL_lowMjj",30,-0.5,3.5);
        MjjDphijj_LL_highMjj = TH1D("MjjDphijj_LL_highMjj","MjjDphijj_LL_highMjj",30,-0.5,3.5);
        MjjDphijj_TTTL_lowMjj = TH1D("MjjDphijj_TTTL_lowMjj","MjjDphijj_TTTL_lowMjj",30,-0.5,3.5);
        MjjDphijj_TTTL_highMjj = TH1D("MjjDphijj_TTTL_highMjj","MjjDphijj_TTTL_highMjj",30,-0.5,3.5);

        print("Rotation on MjjDphijj TreeLL, Counting Event for scaling")
        lowMjjLL_num = 0; highMjjLL_num = 0;
        for i in range(EntriesLL):
            if i%50000==0: print("Now looping", i," of Total",EntriesLL);
            TreeLL.GetEntry(i)
            if((eval("TreeLL.Mjj")>=800) & (eval("TreeLL.Mjj")<=1400)):
                lowMjjLL_num = lowMjjLL_num + 1
            elif eval("TreeLL.Mjj")>1400:
                highMjjLL_num = highMjjLL_num + 1
        MjjDphijj_LL_LowTarget = NLLTarget * float(lowMjjLL_num)/EntriesLL
        MjjDphijj_LL_HighTarget = NLLTarget * float(highMjjLL_num)/EntriesLL
        MjjDphijj_LL_scale_low = MjjDphijj_LL_LowTarget/lowMjjLL_num
        MjjDphijj_LL_scale_high = MjjDphijj_LL_HighTarget/highMjjLL_num
        
        print("Rotation on MjjDphijj TreeLL, Filling Histogram")
        for i in range(EntriesLL):
            if i%50000==0: print("Now looping", i," of Total",EntriesLL);
            TreeLL.GetEntry(i)
            if((eval("TreeLL.Mjj")>=800) & (eval("TreeLL.Mjj")<=1400)):
                MjjDphijj_lowMjj_Asimov.Fill(eval("TreeLL.dphijj"),MjjDphijj_LL_scale_low)
                MjjDphijj_LL_lowMjj.Fill(eval("TreeLL.dphijj"))
            elif eval("TreeLL.Mjj")>1400:
                MjjDphijj_highMjj_Asimov.Fill(eval("TreeLL.dphijj"),MjjDphijj_LL_scale_high)
                MjjDphijj_LL_highMjj.Fill(eval("TreeLL.dphijj"))
            else:
                print("Mjj must be smaller than 800, this is error")
                continue

        print("Rotation on MjjDphijj TreeTTTL, Counting Event for scaling")
        lowMjjTTTL_num = 0; highMjjTTTL_num = 0;
        for i in range(EntriesTTTL):
            if i%50000==0: print("Now looping", i," of Total",EntriesTTTL);
            TreeTTTL.GetEntry(i)
            if((eval("TreeTTTL.Mjj")>=800) & (eval("TreeTTTL.Mjj")<=1400)):
                lowMjjTTTL_num = lowMjjTTTL_num + 1
            elif eval("TreeTTTL.Mjj")>1400:
                highMjjTTTL_num = highMjjTTTL_num + 1
        MjjDphijj_TTTL_LowTarget = NTTTLTarget * float(lowMjjTTTL_num)/EntriesTTTL
        MjjDphijj_TTTL_HighTarget = NTTTLTarget * float(highMjjTTTL_num)/EntriesTTTL
        MjjDphijj_TTTL_scale_low = MjjDphijj_TTTL_LowTarget/lowMjjTTTL_num
        MjjDphijj_TTTL_scale_high = MjjDphijj_TTTL_HighTarget/highMjjTTTL_num

        print("Rotation on MjjDphijj TreeTTTL, Filling Histogram")
        for i in range(EntriesTTTL):
            if i%50000==0: print("Now looping", i," of Total",EntriesTTTL);
            TreeTTTL.GetEntry(i)
            if((eval("TreeTTTL.Mjj")>=800) & (eval("TreeTTTL.Mjj")<=1400)):
                MjjDphijj_lowMjj_Asimov.Fill(eval("TreeTTTL.dphijj"),MjjDphijj_TTTL_scale_low)
                MjjDphijj_TTTL_lowMjj.Fill(eval("TreeTTTL.dphijj"))
            elif eval("TreeTTTL.Mjj")>1400:
                MjjDphijj_highMjj_Asimov.Fill(eval("TreeTTTL.dphijj"),MjjDphijj_TTTL_scale_high)
                MjjDphijj_TTTL_highMjj.Fill(eval("TreeTTTL.dphijj"))
        print("Resetting error-bar on each bin")
        for i in range(30):
            temp_content_error = sqrt(MjjDphijj_lowMjj_Asimov.GetBinContent(i+1))
            MjjDphijj_lowMjj_Asimov.SetBinError(i+1, temp_content_error)
            temp_content_error = sqrt(MjjDphijj_highMjj_Asimov.GetBinContent(i+1))
            MjjDphijj_highMjj_Asimov.SetBinError(i+1, temp_content_error)
        ## End of 'MjjDphijj'

        OF.Write()
        OF.Close()
        return



    def Make_AsimovData_lep1ptDphijj(self,NLLTarget,NTTTLTarget):
        TreeLL = self.tfileLL.Get("tree"); TreeTTTL = self.tfileTTTL.Get("tree")
        EntriesLL = TreeLL.GetEntries(); print("Total Entry of Tree LL :",EntriesLL)
        EntriesTTTL = TreeTTTL.GetEntries(); print("Total Entry of Tree TTTL :",EntriesTTTL)

        OF = TFile("TwoD_Histos_lep1ptDphijj.root","RECREATE")

        ## Beginning of 'lep1ptDphijj'
        lep1ptDphijj_lowlep1pt_Asimov = TH1D("lep1ptDphijj_lowlep1pt_Asimov","lep1ptDphijj_lowlep1pt_Asimov",30,-0.5,3.5);
        lep1ptDphijj_highlep1pt_Asimov = TH1D("lep1ptDphijj_highlep1pt_Asimov","lep1ptDphijj_highlep1pt_Asimov",30,-0.5,3.5);
        lep1ptDphijj_LL_lowlep1pt = TH1D("lep1ptDphijj_LL_lowlep1pt","lep1ptDphijj_LL_lowlep1pt",30,-0.5,3.5);
        lep1ptDphijj_LL_highlep1pt = TH1D("lep1ptDphijj_LL_highlep1pt","lep1ptDphijj_LL_highlep1pt",30,-0.5,3.5);
        lep1ptDphijj_TTTL_lowlep1pt = TH1D("lep1ptDphijj_TTTL_lowlep1pt","lep1ptDphijj_TTTL_lowlep1pt",30,-0.5,3.5);
        lep1ptDphijj_TTTL_highlep1pt = TH1D("lep1ptDphijj_TTTL_highlep1pt","lep1ptDphijj_TTTL_highlep1pt",30,-0.5,3.5);

        print("Rotation on lep1ptDphijj TreeLL, Counting Event for scaling")
        lowlep1ptLL_num = 0; highlep1ptLL_num = 0;
        for i in range(EntriesLL):
            if i%50000==0: print("Now looping", i," of Total",EntriesLL);
            TreeLL.GetEntry(i)
            if((eval("TreeLL.lep1pt")>=0) & (eval("TreeLL.lep1pt")<=200)):
                lowlep1ptLL_num = lowlep1ptLL_num + 1
            elif eval("TreeLL.lep1pt")>200:
                highlep1ptLL_num = highlep1ptLL_num + 1
        lep1ptDphijj_LL_LowTarget = NLLTarget * float(lowlep1ptLL_num)/EntriesLL
        lep1ptDphijj_LL_HighTarget = NLLTarget * float(highlep1ptLL_num)/EntriesLL
        lep1ptDphijj_LL_scale_low = lep1ptDphijj_LL_LowTarget/lowlep1ptLL_num
        lep1ptDphijj_LL_scale_high = lep1ptDphijj_LL_HighTarget/highlep1ptLL_num

        print("Rotation on lep1ptDphijj TreeLL, Filling Histogram")
        for i in range(EntriesLL):
            if i%50000==0: print("Now looping", i," of Total",EntriesLL);
            TreeLL.GetEntry(i)
            if((eval("TreeLL.lep1pt")>=0) & (eval("TreeLL.lep1pt")<=200)):
                lep1ptDphijj_lowlep1pt_Asimov.Fill(eval("TreeLL.dphijj"),lep1ptDphijj_LL_scale_low)
                lep1ptDphijj_LL_lowlep1pt.Fill(eval("TreeLL.dphijj"))
            elif eval("TreeLL.lep1pt")>200:
                lep1ptDphijj_highlep1pt_Asimov.Fill(eval("TreeLL.dphijj"),lep1ptDphijj_LL_scale_high)
                lep1ptDphijj_LL_highlep1pt.Fill(eval("TreeLL.dphijj"))
            else:
                print(" this is error")
                continue

        print("Rotation on lep1ptDphijj TreeTTTL, Counting Event for scaling")
        lowlep1ptTTTL_num = 0; highlep1ptTTTL_num = 0;
        for i in range(EntriesTTTL):
            if i%50000==0: print("Now looping", i," of Total",EntriesTTTL);
            TreeTTTL.GetEntry(i)
            if((eval("TreeTTTL.lep1pt")>=0) & (eval("TreeTTTL.lep1pt")<=200)):
                lowlep1ptTTTL_num = lowlep1ptTTTL_num + 1
            elif eval("TreeTTTL.lep1pt")>200:
                highlep1ptTTTL_num = highlep1ptTTTL_num + 1
        lep1ptDphijj_TTTL_LowTarget = NTTTLTarget * float(lowlep1ptTTTL_num)/EntriesTTTL
        lep1ptDphijj_TTTL_HighTarget = NTTTLTarget * float(highlep1ptTTTL_num)/EntriesTTTL
        lep1ptDphijj_TTTL_scale_low = lep1ptDphijj_TTTL_LowTarget/lowlep1ptTTTL_num
        lep1ptDphijj_TTTL_scale_high = lep1ptDphijj_TTTL_HighTarget/highlep1ptTTTL_num

        print("Rotation on lep1ptDphijj TreeTTTL, Filling Histogram")
        for i in range(EntriesTTTL):
            if i%50000==0: print("Now looping", i," of Total",EntriesTTTL);
            TreeTTTL.GetEntry(i)
            if((eval("TreeTTTL.lep1pt")>=0) & (eval("TreeTTTL.lep1pt")<=200)):
                lep1ptDphijj_lowlep1pt_Asimov.Fill(eval("TreeTTTL.dphijj"),lep1ptDphijj_TTTL_scale_low)
                lep1ptDphijj_TTTL_lowlep1pt.Fill(eval("TreeTTTL.dphijj"))
            elif eval("TreeTTTL.lep1pt")>200:
                lep1ptDphijj_highlep1pt_Asimov.Fill(eval("TreeTTTL.dphijj"),lep1ptDphijj_TTTL_scale_high)
                lep1ptDphijj_TTTL_highlep1pt.Fill(eval("TreeTTTL.dphijj"))
        print("Resetting error-bar on each bin")
        for i in range(30):
            temp_content_error = sqrt(lep1ptDphijj_lowlep1pt_Asimov.GetBinContent(i+1))
            lep1ptDphijj_lowlep1pt_Asimov.SetBinError(i+1, temp_content_error)
            temp_content_error = sqrt(lep1ptDphijj_highlep1pt_Asimov.GetBinContent(i+1))
            lep1ptDphijj_highlep1pt_Asimov.SetBinError(i+1, temp_content_error)



        OF.Write()
        OF.Close()
        return



def main():
    infileLL = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_LL_TTTL_compare/SS_250M_cut_LL.root" #FIXME
    infileTTTL = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_LL_TTTL_compare/SS_250M_cut_TTTL.root" #FIXME
    XSec = 0.17864 #pb                   #FIXME
    Lumi = 3000000  #pb-1 == 10^-3 *fb-1  #FIXME
    eff_sel = 0.015944                      #FIXME
    eff_LL = 0.04503                      #FIXME

    NTotTarget = XSec*Lumi*eff_sel;
    NLLTarget = NTotTarget*eff_LL; NTTTLTarget = NTotTarget*(1-eff_LL)
    print("Targetting LL Event number :",NLLTarget)
    print("Targetting TTTL Event number :",NTTTLTarget)

    TwoD = TwoD_Histos(infileLL=infileLL,infileTTTL=infileTTTL)
    #TwoD.Make_AsimovData_MjjDphijj(NLLTarget,NTTTLTarget)
    TwoD.Make_AsimovData_lep1ptDphijj(NLLTarget,NTTTLTarget)


if __name__=="__main__":
    main()


