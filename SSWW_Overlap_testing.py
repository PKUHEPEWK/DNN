import numpy as np
import os
from ROOT import TFile, TTree, TCut, TH1F
from root_numpy import fill_hist
from root_numpy import root2array, tree2array, array2root, array2tree

def Check_Overlap(infile):
    InFile = TFile(infile,"READ")
    tree = InFile.Get('tree')
    tree.Print()

    lep1pt_      = tree2array(tree, branches='lep1pt')
    lep1eta_     = tree2array(tree, branches='lep1eta')
    lep1phi_     = tree2array(tree, branches='lep1phi')
    lep2pt_      = tree2array(tree, branches='lep2pt')
    lep2eta_     = tree2array(tree, branches='lep2eta')
    lep2phi_     = tree2array(tree, branches='lep2phi')
    jet1pt_      = tree2array(tree, branches='jet1pt')
    jet1eta_     = tree2array(tree, branches='jet1eta')
    jet1phi_     = tree2array(tree, branches='jet1phi')
    jet1M_       = tree2array(tree, branches='jet1M')
    jet2pt_      = tree2array(tree, branches='jet2pt')
    jet2eta_     = tree2array(tree, branches='jet2eta')
    jet2phi_     = tree2array(tree, branches='jet2phi')
    jet2M_       = tree2array(tree, branches='jet2M')
    MET_         = tree2array(tree, branches='MET')
    lep1PID_     = tree2array(tree, branches='lep1PID')
    lep2PID_     = tree2array(tree, branches='lep2PID')
    Mjj_         = tree2array(tree, branches='Mjj')
    dr_ll_jj_    = tree2array(tree, branches='dr_ll_jj')
    dphijj_      = tree2array(tree, branches='dphijj')
    zeppen_lep1_ = tree2array(tree, branches='zeppen_lep1')
    zeppen_lep2_ = tree2array(tree, branches='zeppen_lep2')
    METphi_      = tree2array(tree, branches='METphi')
    detajj_      = tree2array(tree, branches='detajj')
    Mll_         = tree2array(tree, branches='Mll')
    RpT_         = tree2array(tree, branches='RpT')
    LL_Helicity_ = tree2array(tree, branches='LL_Helicity')
    TL_Helicity_ = tree2array(tree, branches='TL_Helicity')
    TT_Helicity_ = tree2array(tree, branches='TT_Helicity')

    ENTRY = tree.GetEntries()
    print("Entry number :",ENTRY)
    lep1pt_set = set(lep1pt_); print(ENTRY-len(lep1pt_set))
    lep2pt_set = set(lep2pt_); print(ENTRY-len(lep2pt_set))
    jet1pt_set = set(jet1pt_); print(ENTRY-len(jet1pt_set))
    jet2pt_set = set(jet2pt_); print(ENTRY-len(jet2pt_set))
    Mjj_set = set(Mjj_); print(ENTRY-len(Mjj_set))
    lep1eta_set = set(lep1eta_); print(ENTRY-len(lep1eta_set))


    InFile.Close()

def main():
    infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_input/SS_4p0M.root" #FIXME
    Check_Overlap(infile)


if __name__=="__main__":
    main()

