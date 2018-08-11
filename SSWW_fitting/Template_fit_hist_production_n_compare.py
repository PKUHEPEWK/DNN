from ROOT import *
import sys, os, math
import numpy as np
sys.path.append("/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/func")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class FractionFitter:
    def __init__(self,fileList):
        self.filelist = fileList 
        #pass

    def Read_Data_n_MC(self):
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

    def MakeHistoROOT(self,binNum=20, histoName=["Mjj","lep1pt"]):
        tfile_list = self.Read_Data_n_MC()[0]
        Hist_list = []

        #for hName in histoName:

        for i in range(len(tfile_list)):
            Tree = tfile_list[i].Get("tree")
            Entries = Tree.GetEntries(); #print(Entries)
            Name = self.Read_Data_n_MC()[1][i]
            outfile = TFile(Name+"_hist.root","RECREATE")
            Hist_list.append(read_file_name_root(Name+"_hist.root")[2])

            BinMinMax_list = []
            for jj in range(Entries):
                Tree.GetEntry(jj)
                for kk,hName in enumerate(histoName):
                    BranchName = "Tree." + hName
                    if(jj==0): 
                        minval=eval(BranchName); maxval=eval(BranchName);
                        temp_list=[minval,maxval]
                        BinMinMax_list.append(temp_list)
                    else:
                        if(eval(BranchName)<BinMinMax_list[kk][0]):  BinMinMax_list[kk][0] = eval(BranchName)
                        if(eval(BranchName)>BinMinMax_list[kk][1]):  BinMinMax_list[kk][1] = eval(BranchName)

            print("DFASdfasdfs", BinMinMax_list)                

            JHisto_list = []
            for num, hName2 in enumerate(histoName):    
                RANGE = BinMinMax_list[num][1] - BinMinMax_list[num][0]
                temp_hist = TH1D(hName2,hName2,binNum,BinMinMax_list[num][0]-RANGE/8,BinMinMax_list[num][1]+RANGE/8)
                JHisto_list.append(temp_hist)
            del BinMinMax_list

            print "Filling Histogram :",Name
            for j in range(Entries):
                Tree.GetEntry(j)
                for kk,hName in enumerate(histoName):
                    BranchName = "Tree." + hName
                    JHisto_list[kk].Fill(eval(BranchName))
            outfile.Write()
            outfile.Close()
        del JHisto_list

        for i in range(len(tfile_list)):
            tfile_list[i].Close()
        Hist_tuple = tuple(Hist_list)
        del Hist_list
        return Hist_tuple

    '''
    def Perform_fit(self,Histogram_list):
        tfile = TFile(Histogram_list[0],"READ"); temp_histogram = tfile.Get("Mjj"); data = temp_histogram

        mc = TObjArray(3)
        tfile1 = TFile(Histogram_list[1],"READ"); temp_histogram1 = tfile1.Get("Mjj"); mc.Add(temp_histogram1)
        tfile2 = TFile(Histogram_list[2],"READ"); temp_histogram2 = tfile2.Get("Mjj"); mc.Add(temp_histogram2)
        tfile3 = TFile(Histogram_list[3],"READ"); temp_histogram3 = tfile3.Get("Mjj"); mc.Add(temp_histogram3)
        print(data)
        print(mc)
        mc.Print()
        #fit = TFractionFitter(data,mc)  ## this seems not stable...
    '''    


def main():
#    Infile_list = ["../PseudoData/Ntuple_delphes_VBSsignal.root","../Template/Ntuple_LL_1k.root","../Template/Ntuple_TL_1k.root","../Template/Ntuple_TT_1k.root"]
    Infile_list = ("/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/PseudoData/Ntuple_delphes_decay_VBSsignal_NoWDecay.root","/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/Ntuple_delphes_decay_VBS_SS_WW_LL_template.root","/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/Ntuple_delphes_decay_VBS_SS_WW_TL_template.root","/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/Ntuple_delphes_decay_VBS_SS_WW_TT_template.root")

    histoName = ["Mjj","lep1pt","lep2pt","jet1pt","jet2pt","dphijj","MET","dr_ll_jj","zeppen_lep1" ] #"lep1pt"  #FIXME TODO

    Fit_test = FractionFitter(Infile_list)
    Hist_files = Fit_test.MakeHistoROOT(binNum=20,histoName=histoName)
    print(Hist_files)
    #Fit_test.Perform_fit(Hist_files)

if __name__=="__main__":
    main()

