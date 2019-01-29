#!/usr/bin/env python
#from root_numpy import fill_hist
#from root_numpy import root2array, tree2array, array2root
#from root_numpy import testdata
import sys, os, math
import numpy as np
#sys.path.append("/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/func")
#sys.path.append("/Users/leejunho/Desktop/MG5_aMC_v2_6_1/Delphes/")
from ROOT import *
from c0_READ_PATH_FILE import read_file_name
from c0_READ_PATH_FILE_ROOT import read_file_name_root
import ROOT
#gInterpreter.Declare('#include "TLorentzVector.h"')
gInterpreter.Declare('#include "/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/classes/DelphesClasses.h"')
gInterpreter.Declare('#include "/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/external/ExRootAnalysis/ExRootTreeReader.h"')

def READ_ExRoot(filename):
    Filename_list = read_file_name(filename)
    Filename = Filename_list[2]
    chain = TChain("Delphes")   ## in C++ :: "TChain chain("LHEF");"
    chain.Add(Filename)
    ROOT.gSystem.Load("libDelphes")
    treeReader = ExRootTreeReader(chain)
    Entries = treeReader.GetEntries()
    print "Total Entry number :", Entries    
    return [Entries,treeReader]



def Do_selection(filename):
    temp_list = READ_ExRoot(filename)
    Entry = temp_list[0]
    treeReader = temp_list[1]
    branchEvent = treeReader.UseBranch("Event")
    branchJet = treeReader.UseBranch("Jet")
    branchElectron = treeReader.UseBranch("Electron")
    branchMuon = treeReader.UseBranch("Muon")
#    branchTau = treeReader.UseBranch("Tau")
    branchMissingET = treeReader.UseBranch("MissingET")
    #branchGenParticle = treeReader.UseBranch("GenParticle")
    branchLHEParticle = treeReader.UseBranch("Particle")
    branchGenMissingET = treeReader.UseBranch("GenMissingET")

    Selected_Event = []

    selected_Events = 0
    flag_lepton_num = 0
    for entry in range(Entry):
#    for entry in range(1000):
        lepton_first_pick = []
        lepton_order_list = []
        treeReader.ReadEntry(entry)
        if(entry%5000 ==0):
            print "now looping",entry,"th event..."
        LL_Helicity = 0
        TL_Helicity = 0
        TT_Helicity = 0
        ForW_Heli = read_file_name_root(filename)[0]
        if "LL" in ForW_Heli:
            LL_Helicity = 1
        elif "TT" in ForW_Heli:
            TT_Helicity = 1
        else:
            LL_Helicity = 1
            TT_Helicity = 1
            TL_Helicity = 1
            pass
        #elif "TL" in ForW_Heli:
        #    TL_Helicity = 1
        #elif "LT" in ForW_Heli:
        #    TL_Helicity = 1    #TODO ADD into Ntuple
        #print "The W boson Helicity :", LL_Helicity, TL_Helicity, TT_Helicity

        '''
        lhe_flag = 0
        Num_LHEParticles = branchLHEParticle.GetEntries()
        for lhe_parti in range(Num_LHEParticles):
            parti_lhe = branchLHEParticle.At(lhe_parti)
            if((abs(parti_lhe.PID==11)| abs(parti_lhe.PID==13))&(parti_lhe.Status==1)): 
            #if((parti_lhe.Status==23) & (abs(parti_lhe.PID==24))): 
                lhe_flag += 1
            #if(parti_lhe.Status==23):   #### Mother, GrandMother, untill reach very top
                #print(parti_lhe.PID)
                #lhe_flag += 1
                
 
        print(lhe_flag)
        print ""
        '''

        if(branchMuon.GetEntries() + branchElectron.GetEntries() >= 2):
            num_mu = 0; num_ele = 0
            for mu_in in range(branchMuon.GetEntries()):
                lepton_first_pick.append(branchMuon.At(mu_in))
                num_mu = num_mu + 1
            for ele_in in range(branchElectron.GetEntries()):
                lepton_first_pick.append(branchElectron.At(ele_in))
                num_ele = num_ele + 1
            num_lep = num_mu + num_ele
        else:
            continue
        leading = 0
        sec_leading = 0
        for lep_order in range(len(lepton_first_pick)):
            if(lep_order==0):
                Leading_lepPT = lepton_first_pick[0].PT;    
                #print("Leading_lepPT:",Leading_lepPT)
                leading = lep_order
                continue
            if lepton_first_pick[lep_order].PT > Leading_lepPT:
                Leading_lepPT = lepton_first_pick[lep_order].PT
                leading = lep_order
            if lep_order == len(lepton_first_pick)-1:
                lepton_order_list.append(lepton_first_pick[leading])
                sec_flag = 0
                for sec_lep_order in range(len(lepton_first_pick)):
                    if(sec_lep_order == leading):
                        continue
                    elif((sec_flag==0)):
                        sec_Leading_lepPT = lepton_first_pick[sec_lep_order].PT
                        sec_leading = sec_lep_order
                        sec_flag = sec_flag + 1
                    if(lepton_first_pick[sec_lep_order].PT > sec_Leading_lepPT ):
                        sec_Leading_lepPT = lepton_first_pick[sec_lep_order].PT
                        sec_leading = sec_lep_order
                lepton_order_list.append(lepton_first_pick[sec_leading])
        if(leading <= num_mu-1):
            lep1PID = 13
        else:
            lep1PID = 11
        if(sec_leading <= num_mu-1):
            lep2PID = 13
        else:
            lep2PID = 11

        #print lepton_order_list[0].PT, lepton_order_list[1].PT
        if lepton_order_list[1].PT < 20:
            continue
        if (lepton_order_list[0].Eta >2.4) | (lepton_order_list[1].Eta >2.4):
            continue
        #print(lepton_order_list[0].Charge, lepton_order_list[1].Charge) #FIXME
        if (lepton_order_list[0].Charge) != (lepton_order_list[1].Charge): #FIXME uncomment
            continue #FIXME uncomment
        #if (lepton_order_list[0].Charge) <0:  #FIXME
        #    continue
        lep1 = TLorentzVector(); lep2 = TLorentzVector();
        lep1.SetPtEtaPhiM(lepton_order_list[0].PT, lepton_order_list[0].Eta, lepton_order_list[0].Phi, 0.0)
        lep2.SetPtEtaPhiM(lepton_order_list[1].PT, lepton_order_list[1].Eta, lepton_order_list[1].Phi, 0.0)
        Mll = (lep1 + lep2).M()
        if ((lep1 + lep2).M() < 40) | (((lep1 + lep2).M() >= 70) & ((lep1 + lep2).M() <= 110)) :
            continue
        if abs(lepton_order_list[0].Eta - lepton_order_list[1].Eta) > 2.0:   #FIXME
            continue
        if(branchMissingET.GetEntries() != 1):
            continue
        if(branchMissingET.At(0).MET < 40):
            continue
        if(branchJet.GetEntries()<2):
            continue      
        j_leading = 0
        sec_j_leading = 0
        jet_order_list = []
        for jet_order in range(branchJet.GetEntries()):
            if(jet_order==0):
                Leading_jetPT = branchJet.At(jet_order).PT;    #print(Leading_lepPT) 
                j_leading = jet_order
                continue
            if branchJet.At(jet_order).PT > Leading_jetPT:
                Leading_jetPT = branchJet.At(jet_order).PT
                j_leading = jet_order
            if jet_order == branchJet.GetEntries()-1:
                jet_order_list.append(branchJet.At(j_leading))
                sec_flag = 0
                for sec_jet_order in range(branchJet.GetEntries()):
                    if(sec_jet_order == j_leading):
                        continue
                    elif((sec_flag==0)):
                        sec_Leading_jetPT = branchJet.At(sec_jet_order).PT
                        sec_j_leading = sec_jet_order
                        sec_flag = sec_flag + 1
                    if(branchJet.At(sec_jet_order).PT > sec_Leading_jetPT ):
                        sec_Leading_jetPT = branchJet.At(sec_jet_order).PT
                        sec_j_leading = sec_jet_order
                jet_order_list.append(branchJet.At(sec_jet_order)) 
        #print jet_order_list[0].PT, jet_order_list[1].PT
        if jet_order_list[1].PT < 30:
            continue
        if (jet_order_list[0].Eta > 4.7) | (jet_order_list[1].Eta > 4.7):
            continue
        jet1 = TLorentzVector(); jet2 = TLorentzVector();
        jet1.SetPtEtaPhiM(jet_order_list[0].PT, jet_order_list[0].Eta, jet_order_list[0].Phi, jet_order_list[0].Mass)
        jet2.SetPtEtaPhiM(jet_order_list[1].PT, jet_order_list[1].Eta, jet_order_list[1].Phi, jet_order_list[1].Mass)
        #print (jet1 + jet2).M(), jet_order_list[0].Mass
        if((jet1 + jet2).M() < 850):   # FIXME uncomment 
            continue  # FIXME uncomment
        if(abs(jet_order_list[0].Eta - jet_order_list[1].Eta) < 2.5):   #FIXME
            continue
        btagging = 0
        for jet_num in range(branchJet.GetEntries()):
            if((branchJet.At(jet_num).PT > 30) & branchJet.At(jet_num).BTag):
                #print(branchJet.At(jet_num).BTag)
                btagging = btagging + 1
        if(btagging>0):
            continue
        dr_ll_jj = math.sqrt(((lep1+lep2).Phi() - (jet1+jet2).Phi())**2 + ((lep1+lep2).Eta() - (jet1+jet2).Eta())**2)
        if(dr_ll_jj > 6):
            continue
        drlj_flag = 0
        for i in range(len(lepton_order_list)):
            for j in range(len(jet_order_list)):
                drlj = math.sqrt((lepton_order_list[i].Phi-jet_order_list[j].Phi)**2 + (lepton_order_list[i].Eta-jet_order_list[j].Eta)**2)
                if(drlj<0.3):
                    drlj_flag = drlj_flag + 1
        if(drlj_flag > 0):
            continue
        #print drlj

        if(abs(jet_order_list[0].Phi - jet_order_list[1].Phi)<= 3.14159265359):
            dphijj = abs(jet1.Phi() - jet2.Phi())
        elif (abs(jet_order_list[0].Phi - jet_order_list[1].Phi)> 3.14159265359):
            dphijj = 3.14159265359*2 - abs(jet1.Phi() - jet2.Phi())
        else:
            continue
        #print(dphijj)

        #print(abs(lepton_order_list[0].Eta), abs(jet_order_list[0].Eta))
        #print(abs(lepton_order_list[1].Eta), abs(jet_order_list[0].Eta))
        #print(abs(lepton_order_list[0].Eta), abs(jet_order_list[1].Eta))
        #print(abs(lepton_order_list[1].Eta), abs(jet_order_list[1].Eta))

        if((abs(lepton_order_list[0].Eta)>abs(jet_order_list[0].Eta)) | (abs(lepton_order_list[1].Eta)>abs(jet_order_list[0].Eta))):
            continue
        if((abs(lepton_order_list[0].Eta)>abs(jet_order_list[1].Eta)) | (abs(lepton_order_list[1].Eta)>abs(jet_order_list[1].Eta))):
            continue

        detajj = abs(jet_order_list[0].Eta - jet_order_list[1].Eta)
        if(detajj<2.5):
            continue

        flag_lepton_num = flag_lepton_num + 1  # FIXME

        ### TODO  #### variables
        lep1pt = lepton_order_list[0].PT; lep1eta = lepton_order_list[0].Eta; lep1phi = lepton_order_list[0].Phi; #lep1E = lepton_order_list[0].E; 
        lep2pt = lepton_order_list[1].PT; lep2eta = lepton_order_list[1].Eta; lep2phi = lepton_order_list[1].Phi; #lep2E = lepton_order_list[1].E;
        jet1pt = jet_order_list[0].PT; jet1eta = jet_order_list[0].Eta; jet1phi = jet_order_list[0].Phi; jet1M = jet_order_list[0].Mass;
        jet2pt = jet_order_list[1].PT; jet2eta = jet_order_list[1].Eta; jet2phi = jet_order_list[1].Phi; jet2M = jet_order_list[1].Mass;
        
        MET = branchMissingET.At(0).MET; #lep1charge = lepton_order_list[0].Charge; lep2charge = lepton_order_list[1].Charge;
        lep1PID = lep1PID; lep2PID = lep2PID; Mjj = (jet1 + jet2).M(); dr_ll_jj = dr_ll_jj; dphijj = dphijj
        zeppen_lep1 = (lepton_order_list[0].Eta-(jet_order_list[0].Eta+jet_order_list[1].Eta)/2.0)/(abs(jet_order_list[0].Eta-jet_order_list[1].Eta)); zeppen_lep2 = (lepton_order_list[1].Eta-(jet_order_list[0].Eta+jet_order_list[1].Eta)/2.0)/(abs(jet_order_list[0].Eta-jet_order_list[1].Eta));
        METphi = branchMissingET.At(0).Phi; detajj=detajj; Mll=Mll;
        RpT = (lep1pt*lep2pt)/(jet1pt*jet2pt)
        LL_Helicity=LL_Helicity; TL_Helicity=TL_Helicity; TT_Helicity=TT_Helicity


        ### TODO  #### list
        #temp_list = [lep1pt,lep1eta,lep1phi,lep2pt,lep2eta,lep2phi,jet1pt,jet1eta,jet1phi,jet2pt,jet2eta,jet2phi,MET,lep1charge,lep2charge,lep1PID,lep2PID, Mjj, dr_ll_jj, zeppen_lep1, zeppen_lep2]
        temp_list = [lep1pt,lep1eta,lep1phi,lep2pt,lep2eta,lep2phi,jet1pt,jet1eta,jet1phi,jet1M,jet2pt,jet2eta,jet2phi,jet2M,MET,lep1PID,lep2PID, Mjj, dr_ll_jj, dphijj, zeppen_lep1, zeppen_lep2, METphi, detajj, Mll, RpT, LL_Helicity, TL_Helicity, TT_Helicity]
        Selected_Event.append(temp_list)

    print "selected Event Num :", flag_lepton_num
    return Selected_Event

def Store_ROOT(filename):
    Selected_Event_list = Do_selection(filename)
    FileName_list = read_file_name(filename)
    Infile_name = FileName_list[0]
    InputFile_dir = FileName_list[3]
    outROOT_file_name = "Ntuple_" + Infile_name
    Outfile = InputFile_dir + outROOT_file_name
    #print Outfile
    outROOT_file = TFile(Outfile,"recreate")
    tree = TTree('tree','tree')
    ### TODO  #### branch first
    lep1pt = np.zeros(1,dtype=float); lep1eta=np.zeros(1,dtype=float); lep1phi=np.zeros(1,dtype=float); #lep1E=np.zeros(1,dtype=float);
    lep2pt = np.zeros(1,dtype=float); lep2eta=np.zeros(1,dtype=float); lep2phi=np.zeros(1,dtype=float); #lep2E=np.zeros(1,dtype=float);
    jet1pt = np.zeros(1,dtype=float); jet1eta=np.zeros(1,dtype=float); jet1phi=np.zeros(1,dtype=float); jet1M=np.zeros(1,dtype=float);
    jet2pt = np.zeros(1,dtype=float); jet2eta=np.zeros(1,dtype=float); jet2phi=np.zeros(1,dtype=float); jet2M=np.zeros(1,dtype=float);
    MET = np.zeros(1,dtype=float); #lep1charge=np.zeros(1,dtype=float); lep2charge=np.zeros(1,dtype=float)
    lep1PID = np.zeros(1,dtype=float); lep2PID = np.zeros(1,dtype=float); Mjj=np.zeros(1,dtype=float); dr_ll_jj=np.zeros(1,dtype=float)
    dphijj=np.zeros(1,dtype=float);
    zeppen_lep1 = np.zeros(1,dtype=float); zeppen_lep2 = np.zeros(1,dtype=float)
    METphi = np.zeros(1,dtype=float); detajj = np.zeros(1,dtype=float); Mll = np.zeros(1,dtype=float);
    RpT = np.zeros(1,dtype=float);
    LL_Helicity=np.zeros(1,dtype=float); TL_Helicity=np.zeros(1,dtype=float); TT_Helicity=np.zeros(1,dtype=float);

    ### TODO  #### branch second
    tree.Branch('lep1pt',lep1pt,'lep1pt/D'); tree.Branch('lep1eta',lep1eta,'lep1eta/D');tree.Branch('lep1phi',lep1phi,'lep1phi/D'); #tree.Branch('lep1E',lep1E,'lep1E/D');
    tree.Branch('lep2pt',lep2pt,'lep2pt/D'); tree.Branch('lep2eta',lep2eta,'lep2eta/D');tree.Branch('lep2phi',lep2phi,'lep2phi/D'); #tree.Branch('lep2E',lep2E,'lep2E/D')
    tree.Branch('jet1pt',jet1pt,'jet1pt/D'); tree.Branch('jet1eta',jet1eta,'jet1eta/D');tree.Branch('jet1phi',jet1phi,'jet1phi/D'); tree.Branch('jet1M',jet1M,'jet1M/D')
    tree.Branch('jet2pt',jet2pt,'jet2pt/D'); tree.Branch('jet2eta',jet2eta,'jet2eta/D');tree.Branch('jet2phi',jet2phi,'jet2phi/D'); tree.Branch('jet2M',jet2M,'jet2M/D')
    tree.Branch('MET',MET,'MET/D');#tree.Branch('lep1charge',lep1charge,'lep1charge/D'); tree.Branch('lep2charge',lep2charge,'lep2charge/D');
    tree.Branch('lep1PID',lep1PID,'lep1PID/D'); tree.Branch('lep2PID',lep2PID,'lep2PID/D'); tree.Branch('Mjj',Mjj,'Mjj/D'); tree.Branch('dr_ll_jj',dr_ll_jj,'dr_ll_jj/D'); tree.Branch('dphijj',dphijj,'dphijj/D')
    tree.Branch('zeppen_lep1',zeppen_lep1,'zeppen_lep1/D'); tree.Branch('zeppen_lep2',zeppen_lep2,'zeppen_lep2/D')
    tree.Branch('METphi',METphi,'METphi/D'); tree.Branch('detajj',detajj,'detajj/D');
    tree.Branch('Mll',Mll,'Mll/D'); tree.Branch('RpT',RpT,'RpT/D')
    tree.Branch('LL_Helicity',LL_Helicity,'LL_Helicity/D'); tree.Branch('TL_Helicity',TL_Helicity,'TL_Helicity/D')
    tree.Branch('TT_Helicity',TT_Helicity,'TT_Helicity/D')


    ### TODO #### branch fill
    for i in range(len(Selected_Event_list)):
        lep1pt[0] = Selected_Event_list[i][0]; lep1eta[0] = Selected_Event_list[i][1]; lep1phi[0] = Selected_Event_list[i][2]; #lep1E[0] = Selected_Event_list[i][3];
        lep2pt[0] = Selected_Event_list[i][3]; lep2eta[0] = Selected_Event_list[i][4]; lep2phi[0] = Selected_Event_list[i][5]; #lep2E[0] = Selected_Event_list[i][7];
        jet1pt[0] = Selected_Event_list[i][6]; jet1eta[0] = Selected_Event_list[i][7]; jet1phi[0] = Selected_Event_list[i][8];jet1M[0] = Selected_Event_list[i][9];
        jet2pt[0] = Selected_Event_list[i][10]; jet2eta[0] = Selected_Event_list[i][11]; jet2phi[0] = Selected_Event_list[i][12]; jet2M[0] = Selected_Event_list[i][13];
        MET[0] = Selected_Event_list[i][14]; #lep1charge[0] = Selected_Event_list[i][13]; lep2charge[0] = Selected_Event_list[i][14];
        lep1PID[0] = Selected_Event_list[i][15]; lep2PID[0] = Selected_Event_list[i][16]; Mjj[0] = Selected_Event_list[i][17];
        dr_ll_jj[0] = Selected_Event_list[i][18]; dphijj[0] = Selected_Event_list[i][19];
        zeppen_lep1[0] = Selected_Event_list[i][20]; zeppen_lep2[0] = Selected_Event_list[i][21];
        METphi[0] = Selected_Event_list[i][22]; detajj[0] = Selected_Event_list[i][23]; Mll[0] = Selected_Event_list[i][24];
        RpT[0] = Selected_Event_list[i][25]; LL_Helicity[0] = Selected_Event_list[i][26];
        TL_Helicity[0] = Selected_Event_list[i][27]; TT_Helicity[0] = Selected_Event_list[i][28];
        tree.Fill()
    outROOT_file.Write()
    outROOT_file.Close()

def main():
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/PseudoData/delphes_VBSsignal.root"    
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/PseudoData/delphes_decay_VBSsignal_NoWDecay.root"
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/delphes_decay_VBS_SS_WW_TT_template.root"
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/delphes_decay_VBS_SS_WW_TL_template.root"
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/delphes_decay_VBS_SS_WW_LL_template.root"
#    infile_test = "/eos/cms/store/user/junho/ttbar/batch1/phamom.root"
    infile_test = "/eos/cms/store/user/junho/ttbar/batch1/Test_DP.root"

    Store_ROOT(infile_test)

if __name__=="__main__":
    main()


