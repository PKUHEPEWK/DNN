## Create Histo ROOT files, and also This is for comparing histo shape of PseudoData, TTTL, and LL 
## includeing "n2_HistoCompare.py" fuction
from ROOT import *
import sys, os, math
import numpy as np
sys.path.append("/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/func")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class HistProduction:
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

    def MakeHistoROOT_general(self,binNum=20, histoName=["Mjj","lep1pt"]):
        tfile_list = self.Read_Data_n_MC()[0]
        Hist_list = []
        for i in range(len(tfile_list)):
            Tree = tfile_list[i].Get("tree")
            Entries = Tree.GetEntries(); #print(Entries)
            Name = self.Read_Data_n_MC()[1][i]
            outfile = TFile(Name+"_hist.root","RECREATE")
            Hist_list.append(read_file_name_root(Name+"_hist.root")[2])

            #BinMinMax_list = []
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

            print("Bin Range of histograms :", BinMinMax_list)

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


    def MakeHistoROOT(self,binNum=20, histoName=["Mjj","lep1pt"]):
        tfile_list = self.Read_Data_n_MC()[0]
        #print(tfile_list)
        Hist_list = []
   
        BinMinMax_list = [] 
        for i in range(len(tfile_list)):  # Specify Histogram bin-range, bin-num.. ROTATE on all files
            Tree = tfile_list[i].Get("tree")
            Entries = Tree.GetEntries(); #print(Entries)
            #Name = self.Read_Data_n_MC()[1][i]
            #outfile = TFile(Name+"_hist.root","RECREATE")
            #Hist_list.append(read_file_name_root(Name+"_hist.root")[2])

            temp_BinMinMax_list = []
            for jj in range(Entries):
                Tree.GetEntry(jj)
                for kk,hName in enumerate(histoName):
                    BranchName = "Tree." + hName
                    if(jj==0):
                        minval=eval(BranchName); maxval=eval(BranchName);
                        temp_list=[minval,maxval]
                        temp_BinMinMax_list.append(temp_list)
                    else:
                        if(eval(BranchName)<temp_BinMinMax_list[kk][0]):  temp_BinMinMax_list[kk][0] = eval(BranchName)
                        if(eval(BranchName)>temp_BinMinMax_list[kk][1]):  temp_BinMinMax_list[kk][1] = eval(BranchName)
            print("Temp Bin Range of histograms :", temp_BinMinMax_list)
            if i == 0 : BinMinMax_list = list(temp_BinMinMax_list)
            else:
                for num1 in range(len(BinMinMax_list)):
                    for num2 in range(len(BinMinMax_list[num1])):
                        if((num2==0) & (BinMinMax_list[num1][num2] > temp_BinMinMax_list[num1][num2])):
                            BinMinMax_list[num1][num2] = temp_BinMinMax_list[num1][num2]
                        elif((num2==1) & (BinMinMax_list[num1][num2] < temp_BinMinMax_list[num1][num2])):
                            BinMinMax_list[num1][num2] = temp_BinMinMax_list[num1][num2]
        print("Final Bin Range of histograms :", BinMinMax_list)
        del Tree

        ################################################### CREATE FILE ################################################
        for i in range(len(tfile_list)): 
            JHisto_list = []
            Tree = tfile_list[i].Get("tree")
            Entries = Tree.GetEntries();
            #print(BinMinMax_list) ##
            Name = self.Read_Data_n_MC()[1][i]
            outfile = TFile(Name+"_hist.root","RECREATE")
            Hist_list.append(read_file_name_root(Name+"_hist.root")[2])
            for num, hName2 in enumerate(histoName):
                #print(BinMinMax_list[num][1], BinMinMax_list[num][0])  ##
                RANGE = BinMinMax_list[num][1] - BinMinMax_list[num][0]
                temp_hist = TH1D(hName2,hName2,binNum,BinMinMax_list[num][0]-RANGE/8,BinMinMax_list[num][1]+RANGE/8)
                JHisto_list.append(temp_hist)
            #del BinMinMax_list

            print "Filling Histogram :",Name
            for j in range(Entries):
                Tree.GetEntry(j)
                Entries = Tree.GetEntries();
                for kk,hName in enumerate(histoName):
                    BranchName = "Tree." + hName
                    JHisto_list[kk].Fill(eval(BranchName))
                ### FIXME remove if just interate ROOT files
                #try:
                #    if((Tree.LL_Helicity)==1.0): JHisto_list[LastNum].Fill(0)
                #    elif((Tree.TL_Helicity)==1.0) : JHisto_list[LastNum].Fill(0.5)
                #    elif((Tree.TT_Helicity)==1.0) : JHisto_list[LastNum].Fill(1)
                #except Exception:
                #    JHisto_list[LastNum].Fill(-1)
                ###
            del JHisto_list
            outfile.Write()
            outfile.Close()

        #del JHisto_list
        del BinMinMax_list
        for i in range(len(tfile_list)):
            tfile_list[i].Close()
        Hist_tuple = tuple(Hist_list)
        del Hist_list
        return Hist_tuple


class HistoCompare:
    def __init__(self, fileList):
        self.filelist = fileList
        #print(self.filelist)

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
        del return_list1; del return_list2
        return_tuple = tuple(return_list)
        del return_list
        #print(return_tuple)
        return return_tuple

    def CompareHistoROOT_general(self):
        tfile_list = self.Read_Data_n_MC()[0]
        Hist_list = []
        for i in range(len(tfile_list)):
            dirlist = tfile_list[i].GetListOfKeys()
            ITER = dirlist.MakeIterator()
            key = ITER.Next()
            temp_list = []
            while key:
                temp_list.append(key.ReadObj())
                key = ITER.Next()
            Hist_list.append(temp_list)
        #print(Hist_list)

        for i in range(len(Hist_list[0])):  # histo nums on each file
            cv = TCanvas("cv","cv",1200,900);
            name = str(Hist_list[0][i].GetName())+"_Compare.pdf"
            for j in range(len(Hist_list)): # files nums
                Scale_factor = 1.0/float(Hist_list[j][i].GetEntries()); #print(Scale_factor)
                Hist_list[j][i].Scale(Scale_factor)
                if j==0:
                    Hist_list[j][i].SetStats(0);
                    Hist_list[j][i].SetLineColor(j+1)
                    Hist_list[j][i].Draw("h")
                else: Hist_list[j][i].SetLineColor(j+1)  ;Hist_list[j][i].Draw("hsame")
            cv.SaveAs(name)
            del cv




def main():

    Infile_list = ("/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/PseudoDATA/Ntuple_delphes_VBSsignal.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/PseudoDATA/Ntuple_PseudoDATA_DECAY.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/forFitting_SS_120M_LL.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/forFitting_SS_120M_TTTL.root")
#    Infile_list = ("/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/PseudoDATA/Ntuple_PseudoDATA_DECAY.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/forFitting_SS_120M_LL.root")
    histoName = ["Mjj","lep1pt","lep2pt","jet1pt","jet2pt","dphijj","MET","dr_ll_jj","zeppen_lep1","zeppen_lep2"] #"lep1pt"  #FIXME TODO

    HistP = HistProduction(Infile_list)
    Hist_files = HistP.MakeHistoROOT(binNum=20,histoName=histoName)  # FIXME Turn this on if histo production required.
    print(Hist_files)

    HistoCom = HistoCompare(Hist_files)
    HistoCom.CompareHistoROOT_general() 

    '''
    OUTFILE1 = read_file_name_root(Infile_list[1]);
    OUTFILE1 = os.path.dirname(os.path.realpath(__file__))+"/"+OUTFILE1[0]+"_hist.root"
    print(OUTFILE1)
    if os.path.exists(OUTFILE1) is False:
        HistP = HistProduction(Infile_list)
        Hist_files = HistP.MakeHistoROOT(binNum=20,histoName=histoName)  # FIXME Turn this on if histo production required.
        print(Hist_files)
    else:
        print("**Part of the file exist, at least. Not producing ROOT files. To Next step..")
    '''



if __name__=="__main__":
    main()

