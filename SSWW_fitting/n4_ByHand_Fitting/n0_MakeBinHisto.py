from ROOT import *
import sys, os, math
import numpy as np
sys.path.append("/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/func")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class MakeBinHisto:

    def __init__(self, fileList, bin_setting):
        self.filelist = fileList
        self.bin_setting = bin_setting   #[bin_num, init, final]

    def Read_ROOTs(self): ## This returns (["Read TFile ROOTs"],["File names without '.root'"])
        return_list = []
        return_list1 = []
        return_list2 = []
        for i in range(len(self.filelist)):
            tfile = TFile(read_file_name_root(self.filelist[i])[2],"READ")
            return_list1.append(tfile)
            return_list2.append(read_file_name_root(self.filelist[i])[0])
        return_list.append(return_list1)
        return_list.append(return_list2)
        #print(return_list1)
        #print(return_list2)
        del return_list1; del return_list2
        return_tuple = tuple(return_list)
        del return_list
        return return_tuple

    def MakeHistoROOT(self,BranchName="lep1pt"):
        tfile_list = self.Read_ROOTs()[0]
        TreeLL = tfile_list[0].Get("tree")
        TreeTTTL = tfile_list[1].Get("tree")
        TreePseudoData = tfile_list[2].Get("tree")
        EntriesLL = TreeLL.GetEntries();
        EntriesTTTL = TreeTTTL.GetEntries();
        EntriesPseudoData = TreePseudoData.GetEntries();            

        outfile = TFile(BranchName+".root","RECREATE")
        HistoLL = TH1D("LL","LL",self.bin_setting[0],self.bin_setting[1],self.bin_setting[2])
        HistoTTTL = TH1D("TTTL","TTTL",self.bin_setting[0],self.bin_setting[1],self.bin_setting[2])
        HistoPseudoData = TH1D("PseudoData","PseudoData",self.bin_setting[0],self.bin_setting[1],self.bin_setting[2])

        print("LL Total Entry :", EntriesLL)
        for jj in range(EntriesLL):
            if(jj%10000==0): print("Now looping ",jj,"/",EntriesLL)
            TreeLL.GetEntry(jj)
            HistoLL.Fill(eval("TreeLL."+BranchName))
        print("TTTL Total Entry :", EntriesTTTL)
        for jj in range(EntriesTTTL):
            if(jj%10000==0): print("Now looping ",jj,"/",EntriesTTTL)
            TreeTTTL.GetEntry(jj)
            HistoTTTL.Fill(eval("TreeTTTL."+BranchName)) 
        print("PseudoData Total Entry :", EntriesPseudoData)
        for jj in range(EntriesPseudoData):
            if(jj%10000==0): print("Now looping ",jj,"/",EntriesPseudoData)
            TreePseudoData.GetEntry(jj)
            HistoPseudoData.Fill(eval("TreePseudoData."+BranchName))
        outfile.Write()
        outfile.Close()
#        cv = TCanvas("cv","cv",1200,900);


def main():
    print("Preliminary")
#    infile = ["../n1_2p5m_result_30bins/PseudoDATA_3ab_hist.root","../n1_2p5m_result_30bins/SS_2p5M_cut_LL_hist.root","../n1_2p5m_result_30bins/SS_2p5M_cut_TTTL_hist.root"] #FIXME
    infile = ["/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/SS_2p5M_cut_LL.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/SS_2p5M_cut_TTTL.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/PseudoDATA/PseudoDATA_3ab.root"] #FIXME
    bin_setting = [20,0,500] #FIXME
    BranchName = "lep1pt" #FIXME

    Exe = MakeBinHisto(infile,bin_setting)
    Exe.MakeHistoROOT(BranchName=BranchName) 


if __name__=="__main__":
    main()

