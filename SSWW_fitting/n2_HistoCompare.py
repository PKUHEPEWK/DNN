## This is for comparing histo shape of PseudoData, TTTL, and LL 
from ROOT import *
import sys, os, math
import numpy as np
sys.path.append("/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/func")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class HistoCompare:
    def __init__(self, fileList):
        self.filelist = fileList
        self.namelist = [read_file_name_root(i)[0] for i in fileList]
        #print(self.namelist)
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
            legend = TLegend(0.8,0.8,1.1,1.0) 
            name = str(Hist_list[0][i].GetName())+"_Compare.pdf"
            for j in range(len(Hist_list)): # files nums
                Scale_factor = 1.0/float(Hist_list[j][i].GetEntries()); #print(Scale_factor)
                Hist_list[j][i].Scale(Scale_factor)
                if j==0: 
                    Hist_list[j][i].SetStats(0); 
                    Hist_list[j][i].SetLineColor(j+1)
                    Hist_list[j][i].GetXaxis().SetTitle(str(Hist_list[0][i].GetName()))
                    Hist_list[j][i].GetYaxis().SetTitle("Proportion")
                    Hist_list[j][i].Draw("h")
                    legend.AddEntry(Hist_list[j][i],self.namelist[j]) #FIXME
                else: Hist_list[j][i].SetLineColor(j+1)  ;Hist_list[j][i].Draw("hsame"); legend.AddEntry(Hist_list[j][i],self.namelist[j]);
            legend.Draw()
            cv.SaveAs(name)
            del cv

        for i in range(len(Hist_list[0])):  # histo nums on each file
            cv = TCanvas("cv","cv",1200,900);
            cv.SetLogy()
            legend = TLegend(0.8,0.8,1.1,1.0)
            name = str(Hist_list[0][i].GetName())+"_Compare_log.pdf"
            for j in range(len(Hist_list)): # files nums
                #Scale_factor = 1.0/float(Hist_list[j][i].GetEntries()); #print(Scale_factor)
                #Hist_list[j][i].Scale(Scale_factor)
                if j==0:
                    Hist_list[j][i].SetStats(0);
                    Hist_list[j][i].SetLineColor(j+1)
                    Hist_list[j][i].GetXaxis().SetTitle(str(Hist_list[0][i].GetName()))
                    Hist_list[j][i].GetYaxis().SetTitle("Proportion")
                    Hist_list[j][i].Draw("h")
                    legend.AddEntry(Hist_list[j][i],self.namelist[j]) #FIXME
                else: Hist_list[j][i].SetLineColor(j+1)  ;Hist_list[j][i].Draw("hsame"); legend.AddEntry(Hist_list[j][i],self.namelist[j]);
            legend.Draw()
            cv.SaveAs(name)
            del cv



def main():
    infileList = ("/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/Template_for_n2/LL_120M.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/Template_for_n2/TTTL_120M.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/PseudoDATA_for_n2/PseudoDATA_DECAY.root")  ## DECAY Package involved DATA. TODO
#    infileList = ("/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/Template_for_n2/LL_120M.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/Template_for_n2/TTTL_120M.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/PseudoDATA_for_n2/PseudoDATA_noDECAY.root") ## No DECAY Package involved DATA. TODO
   
#    infileList = ("/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/Template_for_n2/LL_120M.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/Template_for_n2/TTTL_120M.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/PseudoDATA_for_n2/PseudoDATA_DECAY.root","/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/PseudoDATA_for_n2/PseudoDATA_noDECAY.root") ## Both DECAY & no_DECAY Packages involved. TODO
    HistoCom = HistoCompare(infileList)
    HistoCom.CompareHistoROOT_general()


if __name__ == "__main__":
    main()


