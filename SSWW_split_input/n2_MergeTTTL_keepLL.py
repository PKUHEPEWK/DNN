from ROOT import TFile, TH1D, TH1F, TCanvas, TColor, TGaxis, TPad, gBenchmark, TTree
import os, sys
import numpy

sys.path.append("..")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class New_tree(object):
    def __init__(self,infile):
        self._infile = infile

    def Generate(self, tag="testtest"):
        PATH_included_root = read_file_name_root(self._infile)[2]
        f = TFile(PATH_included_root,"READ")
        outName = os.getcwd() + "/" + tag +".root"
        print("Targeting output ROOT file name :",outName)
        tree = f.Get("tree")
        Entry = tree.GetEntries(); print("Total Entry Number :",Entry)

        lep1pt = numpy.array([0],'d'); lep1eta = numpy.array([0],'d'); lep1phi = numpy.array([0],'d');
        lep2pt = numpy.array([0],'d'); lep2eta = numpy.array([0],'d'); lep2phi = numpy.array([0],'d');
        jet1pt = numpy.array([0],'d'); jet1eta = numpy.array([0],'d'); jet1phi = numpy.array([0],'d'); jet1M = numpy.array([0],'d');
        jet2pt = numpy.array([0],'d'); jet2eta = numpy.array([0],'d'); jet2phi = numpy.array([0],'d'); jet2M = numpy.array([0],'d');
        MET = numpy.array([0],'d'); lep1PID = numpy.array([0],'d'); lep2PID = numpy.array([0],'d');
        Mjj = numpy.array([0],'d'); dr_ll_jj = numpy.array([0],'d'); dphijj = numpy.array([0],'d'); 
        zeppen_lep1 = numpy.array([0],'d'); zeppen_lep2 = numpy.array([0],'d');
        METphi = numpy.array([0],'d'); detajj = numpy.array([0],'d'); Mll = numpy.array([0],'d'); RpT = numpy.array([0],'d');
        LL_Helicity = numpy.array([0],'d'); #TL_Helicity = numpy.array([0],'d'); TT_Helicity = numpy.array([0],'d');
        TTTL_Helicity = numpy.array([0],'d');

        fout = TFile(outName,"RECREATE")
        tree_w = TTree("tree","tree")
        tree.SetBranchAddress("lep1pt",lep1pt); tree_w.Branch("lep1pt",lep1pt,"lep1pt/D")
        tree.SetBranchAddress("lep1eta",lep1eta); tree_w.Branch("lep1eta", lep1eta,"lep1eta/D")
        tree.SetBranchAddress("lep1phi",lep1phi); tree_w.Branch("lep1phi", lep1phi,"lep1phi/D")
        tree.SetBranchAddress("lep2pt",lep2pt); tree_w.Branch("lep2pt", lep2pt,"lep2pt/D")
        tree.SetBranchAddress("lep2eta",lep2eta); tree_w.Branch("lep2eta", lep2eta,"lep2eta/D")
        tree.SetBranchAddress("lep2phi",lep2phi); tree_w.Branch("lep2phi", lep2phi,"lep2phi/D")
        tree.SetBranchAddress("jet1pt",jet1pt); tree_w.Branch("jet1pt", jet1pt,"jet1pt/D")
        tree.SetBranchAddress("jet1eta",jet1eta); tree_w.Branch("jet1eta", jet1eta,"jet1eta/D")
        tree.SetBranchAddress("jet1phi",jet1phi); tree_w.Branch("jet1phi", jet1phi,"jet1phi/D")
        tree.SetBranchAddress("jet1M",jet1M); tree_w.Branch("jet1M", jet1M,"jet1M/D")
        tree.SetBranchAddress("jet2pt",jet2pt); tree_w.Branch("jet2pt", jet2pt,"jet2pt/D")
        tree.SetBranchAddress("jet2eta",jet2eta); tree_w.Branch("jet2eta", jet2eta,"jet2eta/D")
        tree.SetBranchAddress("jet2phi",jet2phi); tree_w.Branch("jet2phi", jet2phi,"jet2phi/D")
        tree.SetBranchAddress("jet2M",jet2M); tree_w.Branch("jet2M", jet2M,"jet2M/D")
        tree.SetBranchAddress("MET",MET); tree_w.Branch("MET", MET,"MET/D")
        tree.SetBranchAddress("lep1PID",lep1PID); tree_w.Branch("lep1PID", lep1PID,"lep1PID/D")
        tree.SetBranchAddress("lep2PID",lep2PID); tree_w.Branch("lep2PID", lep2PID,"lep2PID/D")
        tree.SetBranchAddress("Mjj",Mjj); tree_w.Branch("Mjj", Mjj,"Mjj/D")
        tree.SetBranchAddress("dr_ll_jj",dr_ll_jj); tree_w.Branch("dr_ll_jj", dr_ll_jj,"dr_ll_jj/D")
        tree.SetBranchAddress("dphijj",dphijj); tree_w.Branch("dphijj", dphijj,"dphijj/D")
        tree.SetBranchAddress("zeppen_lep1",zeppen_lep1); tree_w.Branch("zeppen_lep1", zeppen_lep1,"zeppen_lep1/D")
        tree.SetBranchAddress("zeppen_lep2",zeppen_lep2); tree_w.Branch("zeppen_lep2", zeppen_lep2,"zeppen_lep2/D")
        tree.SetBranchAddress("METphi",METphi); tree_w.Branch("METphi", METphi,"METphi/D")
        tree.SetBranchAddress("detajj",detajj); tree_w.Branch("detajj", detajj,"detajj/D")
        tree.SetBranchAddress("Mll",Mll); tree_w.Branch("Mll", Mll,"Mll/D")
        tree.SetBranchAddress("RpT",RpT); tree_w.Branch("RpT", RpT,"RpT/D")
        tree.SetBranchAddress("LL_Helicity",LL_Helicity); tree_w.Branch("LL_Helicity", LL_Helicity,"LL_Helicity/D")
        #tree.SetBranchAddress("TL_Helicity",TL_Helicity); 
        tree_w.Branch("TTTL_Helicity", TTTL_Helicity,"TTTL_Helicity/D")
        #tree.SetBranchAddress("TT_Helicity",TT_Helicity); #tree_w.Branch("", numpy.array([0],'d'),"/D")
        #tree.SetBranchAddress("",numpy.array([0],'d')); tree_w.Branch("", numpy.array([0],'d'),"/D")


        for i in range(Entry):
            if i%10000==0: print("Now looping", i," of Total",Entry); #print LL_Helicity
            tree.GetEntry(i)
            if(LL_Helicity[0] == 0.0): TTTL_Helicity[0] = 1.0
            tree_w.Fill()
        tree_w.Write()
        fout.Close()



def main():
    infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_input/SS_120M.root"
    #infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_input/small_test_Ntuple.root"
    Test = New_tree(infile)
    Test.Generate(tag="TTTL_LL")

if __name__=="__main__":
    main()
