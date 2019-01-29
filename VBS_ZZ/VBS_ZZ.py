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
    branchScalarHT = treeReader.UseBranch("ScalarHT")

    Selected_Event = []

    selected_Events = 0
    flag_lepton_num = 0
    rm_selected_events = 0
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
        elif "TL" in ForW_Heli:
            TL_Helicity = 1
        elif "LT" in ForW_Heli:
            TL_Helicity = 1    #TODO ADD into Ntuple
        else:
            #print("ERROR, No W Helicity Info")
            pass
            #continue
        #print "The W boson Helicity :", LL_Helicity, TL_Helicity, TT_Helicity

        #### lepton saving starts here
        Lep_dict = dict()
        LepPT_orderList = []
        if(branchMuon.GetEntries() + branchElectron.GetEntries() >= 4):
            num_mu = 0; num_ele = 0
            lepton_plus=0; lepton_minus=0
            for mu_in in range(branchMuon.GetEntries()):
                lepton_first_pick.append(branchMuon.At(mu_in))
                num_mu = num_mu + 1
                Lep_dict[num_mu]=branchMuon.At(mu_in)
                if(branchMuon.At(mu_in).Charge > 0):
                    lepton_plus += 1
                else:
                    lepton_minus += 1
            for ele_in in range(branchElectron.GetEntries()):
                lepton_first_pick.append(branchElectron.At(ele_in))
                num_ele = num_ele + 1
                Lep_dict[num_ele+num_mu]=branchElectron.At(ele_in)
                if(branchElectron.At(ele_in).Charge > 0):
                    lepton_plus += 1
                else:
                    lepton_minus += 1
            num_lep = num_mu + num_ele
        else:
            #print(branchMuon.GetEntries() + branchElectron.GetEntries(),"Leptons... Skip this event..")
            continue
        if((lepton_plus<2)|(lepton_minus<2)):
            continue
        #print("Lepton Dictionary :",Lep_dict)

        LepMother_List = []
        temp_rota = 1; temp_Mllrange_dict = dict(); dictnum=1
        for i in range(len(Lep_dict)-1):
            store_index1 = 0; store_index2 = 0
            index1 = i+1
            temp_Mll_range = 30
            temp_lep1 = TLorentzVector();
            temp_lep1.SetPtEtaPhiM(Lep_dict[index1].PT,Lep_dict[index1].Eta,Lep_dict[index1].Phi,0)
            for j in range(len(Lep_dict) - temp_rota):
                index2 = j+temp_rota+1
                if( (Lep_dict[index1].GetName()==Lep_dict[index2].GetName()) & (Lep_dict[index1].Charge == -Lep_dict[index2].Charge) ):
                    temp_lep2 = TLorentzVector();
                    temp_lep2.SetPtEtaPhiM(Lep_dict[index2].PT,Lep_dict[index2].Eta,Lep_dict[index2].Phi,0)
                    if(abs((temp_lep1 + temp_lep2).M()-90)<temp_Mll_range):   # 60 < Mll < 120
                        temp_Mll_range = abs((temp_lep1 + temp_lep2).M()-90)
                        store_index1 = index1
                        store_index2 = index2
                else:
                    continue
            temp_rota += 1
            if((store_index1!=0) & (store_index2!=0)):
                LepMother_List.append([store_index1,store_index2])
                temp_Mllrange_dict[dictnum]=temp_Mll_range; dictnum += 1 
        if(len(LepMother_List)<2):
            continue        
        elif(len(LepMother_List)>2):
            temp_list1 = []; temp_Mll_order_list = []
            for i in sorted(temp_Mllrange_dict.values(),reverse=False):
                temp_list1.append(i)
            for i,mll_1 in enumerate(temp_list1):
                for num,mll_2 in temp_Mllrange_dict.items():
                    if mll_2 == mll_1:
                        temp_Mll_order_list.append(num)
            t_rota = 1
            mll_index1=0; mll_index2=0
            for i in range(len(temp_Mll_order_list)):  
                br_command = 0
                id1 = i
                for j in range(len(temp_Mll_order_list)-t_rota):
                    id2 = j+t_rota
                    if(LepMother_List[temp_Mll_order_list[i]-1][0] == LepMother_List[temp_Mll_order_list[id2]-1][0]):
                        continue
                    elif(LepMother_List[temp_Mll_order_list[i]-1][0] == LepMother_List[temp_Mll_order_list[id2]-1][1]):
                        continue
                    elif(LepMother_List[temp_Mll_order_list[i]-1][1] == LepMother_List[temp_Mll_order_list[id2]-1][0]):
                        continue
                    elif(LepMother_List[temp_Mll_order_list[i]-1][1] == LepMother_List[temp_Mll_order_list[id2]-1][1]):
                        continue
                    else:
                        br_command = 1
                        mll_index1 = temp_Mll_order_list[i]-1; mll_index2 = temp_Mll_order_list[id2]-1
                        break
                if(br_command==1):
                    break
                t_rota += 1
            #print(LepMother_List)
            LepMother_List1 = list()
            LepMother_List1.append(LepMother_List[mll_index1])
            LepMother_List1.append(LepMother_List[mll_index2])                
            LepMother_List = LepMother_List1
            #print(temp_Mll_order_list)
        elif(len(LepMother_List)==2):
            if(LepMother_List[0][0] == LepMother_List[1][0]):
                continue
            if(LepMother_List[0][0] == LepMother_List[1][1]):
                continue
            if(LepMother_List[0][1] == LepMother_List[1][0]):
                continue
            if(LepMother_List[0][1] == LepMother_List[1][1]):
                continue
        else:
            pass
        LepMother_List1 = []; flat_LepMother_List = []
        for i in range(len(LepMother_List)):
            if(Lep_dict[LepMother_List[i][0]].Charge <0):
                temp = [LepMother_List[i][1],LepMother_List[i][0]]; LepMother_List1.append(temp)
                flat_LepMother_List.append(LepMother_List[i][1])
                flat_LepMother_List.append(LepMother_List[i][0])
            else:
                temp = [LepMother_List[i][0],LepMother_List[i][1]]; LepMother_List1.append(temp)
                flat_LepMother_List.append(LepMother_List[i][0])
                flat_LepMother_List.append(LepMother_List[i][1])
        LepMother_List = LepMother_List1; del LepMother_List1

        temp_LepPT_List = []
        for i in flat_LepMother_List:
            temp_LepPT_List.append(Lep_dict[i].PT)
        temp_LepPT_List = sorted(temp_LepPT_List, reverse=True)
        #print(temp_LepPT_List)
        for i,lepPT in enumerate(temp_LepPT_List):
            for num, lep in Lep_dict.items():
                if lep.PT == lepPT:
                    LepPT_orderList.append(num)
                    break
        #print(LepPT_orderList)        
        del temp_LepPT_List
        if(len(LepPT_orderList)!=4):
            print("ERROR with Lep PT")
            continue
        '''
        for i in range(len(Lep_dict)-1):
            print(Lep_dict[LepPT_orderList[i]].PT)
            if(Lep_dict[LepPT_orderList[i]].PT<Lep_dict[LepPT_orderList[i+1]].PT):
                print("LepPT_order Error!!!!"); 
                continue
        '''
        #### 'Lep_dict' : keep all selected leptons including Electrons and Muons.
        #### 'LepPT_orderList' : The desending order of lepPT, in terms of Lep_dict.key().
        #### 'LepMother_List' : Mother of di-leptons, two most probable Z boson, ordered by narrowest window of Z. [[+,-],[+,-]]
        #### 'flat_LepMother_List' : Mother of di-leptons, two most probable Z boson, based on narrowest window of Z. [+,-,+,-]
        #### lepton saving is done here

        #### jet saving starts here
        Jet_dict = dict()
        JetPT_orderList = []
        if(branchJet.GetEntries()>=2):
            for jetNum in range(branchJet.GetEntries()): 
                Jet_dict[jetNum+1]=branchJet.At(jetNum)
        else:
            #print(branchJet.GetEntries(),"Jets... Skip this event..")
            continue
        #print(Jet_dict)
        temp_JetPT_List = []
        for i in Jet_dict.values():
            temp_JetPT_List.append(i.PT)
        for i,JetPT in enumerate(temp_JetPT_List):
            for num, jet in Jet_dict.items():
                if jet.PT == JetPT:
                    JetPT_orderList.append(num)
                    break
        del temp_JetPT_List
        #print(JetPT_orderList)
        #### 'Jet_dict' : keep all selected jets, 
        #### 'JetPT_orderList' : The desending order of JetPT, in terms of Jet_dict.key()
        #### jet saving is done here

        #### Lepton only related Cut starts here
        if(Lep_dict[LepPT_orderList[-1]].PT < 7):
            continue
        if(Lep_dict[LepPT_orderList[0]].PT < 20):
            continue
        if(Lep_dict[LepPT_orderList[1]].PT < 12):
            continue
        #### Lepton only related Cut is done here

        #### Jet only related Cut starts here
        if(Jet_dict[JetPT_orderList[1]].PT<30):
            continue
        if(Jet_dict[JetPT_orderList[0]].Eta>4.7):
            continue
        if(Jet_dict[JetPT_orderList[1]].Eta>4.7):
            continue
        jet1 = TLorentzVector(); jet2 = TLorentzVector();
        jet1.SetPtEtaPhiM(Jet_dict[JetPT_orderList[0]].PT, Jet_dict[JetPT_orderList[0]].Eta, Jet_dict[JetPT_orderList[0]].Phi, Jet_dict[JetPT_orderList[0]].Mass)
        jet2.SetPtEtaPhiM(Jet_dict[JetPT_orderList[1]].PT, Jet_dict[JetPT_orderList[1]].Eta, Jet_dict[JetPT_orderList[1]].Phi, Jet_dict[JetPT_orderList[1]].Mass)
        Mjj = (jet1 + jet2).M()
        detajj = abs(Jet_dict[JetPT_orderList[0]].Eta - Jet_dict[JetPT_orderList[1]].Eta)
        if(detajj<2.4): #VBS cut, not applied for non-VBS region study
            continue
        if(Mjj<300):    # Applied relately lower Mjj, since Mjj>200 applied on GEN level
            continue
        #### Jet only related Cut is done here

        #### Lepton and Jets related Cut starts here
        drlj_flag = 0; drlj_continue_flag = 0
        for i in range(len(LepPT_orderList)):
            if(drlj_flag>0):
                drlj_continue_flag = 1
                break
            for j in range(len(JetPT_orderList)):
                drlj = math.sqrt((Lep_dict[LepPT_orderList[i]].Phi-Jet_dict[JetPT_orderList[j]].Phi)**2 + (Lep_dict[LepPT_orderList[i]].Eta-Jet_dict[JetPT_orderList[j]].Eta)**2)
                if(drlj<0.3):
                    drlj_flag = 1
                    break
        if(drlj_continue_flag!=0):
            continue

        drll_flag = 0; drll_continue_flag = 0
        for i in range(len(LepPT_orderList)-1):
            if(drll_flag>0):
                drll_continue_flag = 1
                break
            for j in range(len(LepPT_orderList)-1-i):
                index1 = i
                index2 = j+i+1
                drll = math.sqrt((Lep_dict[LepPT_orderList[index1]].Phi-Lep_dict[LepPT_orderList[index2]].Phi)**2 + (Lep_dict[LepPT_orderList[index1]].Eta-Lep_dict[LepPT_orderList[index2]].Eta)**2) 
                if(drll<0.3):
                    drll_flag = 1
                    break
        if(drll_continue_flag!=0):
            #print(drll)
            continue
        #### Lepton and Jets related Cut is done here

        #### Other Cut starts here
        btagging = 0
        for jet_num in range(branchJet.GetEntries()):
            if((branchJet.At(jet_num).PT > 30) & branchJet.At(jet_num).BTag):
                #print(branchJet.At(jet_num).BTag)
                btagging = btagging + 1
        if(btagging>0):
            pass
            continue
        #### Other Cut is done here

        flag_lepton_num = flag_lepton_num + 1  # FIXME

        #### Discriminant Saving starts here
        # Lep1,2,3,4(Pt,Eta,Phi,E), Jet1,2(Pt,Eta,Phi,M) #done
        # Z1_lep1,Z1_lep2,Z2_lep1,Z2_lep2(Pt,Eta,Phi,E) #done
        # MET, METphi  #done
        # Mll_Z1, Mll_Z2, Z1_Mt, Z2_Mt, detall_Z1, detall_Z2, dphill_Z1, dphill_Z2, Ptll_Z1, Ptll_Z2, Ell_Z1, Ell_Z2, Mllll #done
        # Mjj, Mtjj, detajj, dphijj, Ejj, Ptjj, Etajj, Phijj #done
        # Z1,2(Pt,Eta,Phi,M) #done
        # E_ZZ, Pt_ZZ, M_ZZ, EtaZZ, dphi_ZZ, deta_ZZ  #done 
        # Z1Z2jj_pt, Z1Z2jj_eta, Z1Z2jj_phi, Z1Z2jj_M, Z1Z2jj_E, Zeppen_Z1, Zeppen_Z2, RpT_jets, Rpt_hard
        # Weight of Event, scalar sum of transverse momenta(ScalarHT) #done

        # Lep1,2,3,4(Pt,Eta,Phi,E)
        lep1pt = Lep_dict[LepPT_orderList[0]].PT
        lep1eta = Lep_dict[LepPT_orderList[0]].Eta
        lep1phi = Lep_dict[LepPT_orderList[0]].Phi
        Lead_LEP = TLorentzVector();
        Lead_LEP.SetPtEtaPhiM(lep1pt,lep1eta, lep1phi,0)
        lep1e = Lead_LEP.Energy()
        lep2pt = Lep_dict[LepPT_orderList[1]].PT
        lep2eta = Lep_dict[LepPT_orderList[1]].Eta
        lep2phi = Lep_dict[LepPT_orderList[1]].Phi
        SubLead_LEP = TLorentzVector();
        SubLead_LEP.SetPtEtaPhiM(lep2pt,lep2eta, lep2phi,0)
        lep2e = SubLead_LEP.Energy()
        lep3pt = Lep_dict[LepPT_orderList[2]].PT
        lep3eta = Lep_dict[LepPT_orderList[2]].Eta
        lep3phi = Lep_dict[LepPT_orderList[2]].Phi
        ThirdLead_LEP = TLorentzVector();
        ThirdLead_LEP.SetPtEtaPhiM(lep3pt, lep3eta, lep3phi,0)
        lep3e = ThirdLead_LEP.Energy()
        lep4pt = Lep_dict[LepPT_orderList[3]].PT
        lep4eta = Lep_dict[LepPT_orderList[3]].Eta
        lep4phi = Lep_dict[LepPT_orderList[3]].Phi
        ForthLead_LEP = TLorentzVector();
        ForthLead_LEP.SetPtEtaPhiM(lep4pt, lep4eta, lep4phi,0)
        lep4e = ForthLead_LEP.Energy()


        #Jet1,2(Pt,Eta,Phi,M)
        jet1pt = Jet_dict[JetPT_orderList[0]].PT
        jet1eta = Jet_dict[JetPT_orderList[0]].Eta
        jet1phi = Jet_dict[JetPT_orderList[0]].Phi
        jet1m = Jet_dict[JetPT_orderList[0]].Mass
        jet2pt = Jet_dict[JetPT_orderList[1]].PT
        jet2eta = Jet_dict[JetPT_orderList[1]].Eta
        jet2phi = Jet_dict[JetPT_orderList[1]].Phi
        jet2m = Jet_dict[JetPT_orderList[1]].Mass


        #Z1_lep1,Z1_lep2,Z2_lep1,Z2_lep2(Pt,Eta,Phi,E)
        Z1_lep_p_pt = Lep_dict[LepMother_List[0][0]].PT
        Z1_lep_p_eta = Lep_dict[LepMother_List[0][0]].Eta
        Z1_lep_p_phi = Lep_dict[LepMother_List[0][0]].Phi
        Z1_LEP_P = TLorentzVector(); Z1_LEP_P.SetPtEtaPhiM(Z1_lep_p_pt,Z1_lep_p_eta,Z1_lep_p_phi,0)
        Z1_lep_p_e = Z1_LEP_P.Energy()
        Z1_lep_m_pt = Lep_dict[LepMother_List[0][1]].PT
        Z1_lep_m_eta = Lep_dict[LepMother_List[0][1]].Eta
        Z1_lep_m_phi = Lep_dict[LepMother_List[0][1]].Phi
        Z1_LEP_M = TLorentzVector(); Z1_LEP_M.SetPtEtaPhiM(Z1_lep_m_pt,Z1_lep_m_eta,Z1_lep_m_phi,0)
        Z1_lep_m_e = Z1_LEP_M.Energy()
        
        Z2_lep_p_pt = Lep_dict[LepMother_List[1][0]].PT
        Z2_lep_p_eta = Lep_dict[LepMother_List[1][0]].Eta
        Z2_lep_p_phi = Lep_dict[LepMother_List[1][0]].Phi
        Z2_LEP_P = TLorentzVector(); Z2_LEP_P.SetPtEtaPhiM(Z2_lep_p_pt,Z2_lep_p_eta,Z2_lep_p_phi,0)
        Z2_lep_p_e = Z2_LEP_P.Energy()
        Z2_lep_m_pt = Lep_dict[LepMother_List[1][1]].PT
        Z2_lep_m_eta = Lep_dict[LepMother_List[1][1]].Eta
        Z2_lep_m_phi = Lep_dict[LepMother_List[1][1]].Phi
        Z2_LEP_M = TLorentzVector(); Z2_LEP_M.SetPtEtaPhiM(Z2_lep_m_pt,Z2_lep_m_eta,Z2_lep_m_phi,0)
        Z2_lep_m_e = Z2_LEP_M.Energy()


        # MET, METphi
        MET = branchMissingET.At(0).MET
        METphi = branchMissingET.At(0).Phi


        # Mll_Z1, Mll_Z2, Z1_Mt, Z2_Mt, detall_Z1, detall_Z2, dphill_Z1, dphill_Z2, Ptll_Z1, Ptll_Z2, Ell_Z1, Ell_Z2, Mllll 
        LL_Z1 = Z1_LEP_P + Z1_LEP_M
        LL_Z2 = Z2_LEP_P + Z2_LEP_M 
        Mll_Z1 = LL_Z1.M()
        Mll_Z2 = LL_Z2.M()
        Z1_Mt = LL_Z1.Mt()
        Z2_Mt = LL_Z2.Mt()
        detall_Z1 = abs(Z1_LEP_P.Eta() - Z1_LEP_M.Eta())
        detall_Z2 = abs(Z2_LEP_P.Eta() - Z2_LEP_M.Eta())
        if(abs(Z1_LEP_P.Phi() - Z1_LEP_M.Phi())<= 3.14159265359):
            dphill_Z1 = abs(Z1_LEP_P.Phi() - Z1_LEP_M.Phi())
        else:
            dphill_Z1 = 3.14159265359*2 - abs(Z1_LEP_P.Phi() - Z1_LEP_M.Phi())
        if(abs(Z2_LEP_P.Phi() - Z2_LEP_M.Phi())<= 3.14159265359):
            dphill_Z2 = abs(Z2_LEP_P.Phi() - Z2_LEP_M.Phi())
        else:
            dphill_Z2 = 3.14159265359*2 - abs(Z2_LEP_P.Phi() - Z2_LEP_M.Phi())
        Ptll_Z1 = LL_Z1.Pt()
        Ptll_Z2 = LL_Z2.Pt()
        Ell_Z1 = LL_Z1.Energy()
        Ell_Z2 = LL_Z2.Energy()
        Mllll = (Z1_LEP_P+Z1_LEP_M+Z2_LEP_P+Z2_LEP_M).M()


        # Mjj, Mtjj, detajj, dphijj, Ejj, Ptjj, Etajj, Phijj
        JET1 = TLorentzVector(); JET1.SetPtEtaPhiM(jet1pt,jet1eta,jet1phi,jet1m)
        JET2 = TLorentzVector(); JET2.SetPtEtaPhiM(jet2pt,jet2eta,jet2phi,jet2m)
        Mjj = (JET1 + JET2).M()
        Mtjj = (JET1 + JET2).Mt()
        Ejj = (JET1 + JET2).Energy()
        Ptjj = (JET1 + JET2).Pt()
        Etajj = (JET1 + JET2).Eta()
        Phijj = (JET1 + JET2).Phi()
        detajj = abs(JET1.Eta() - JET2.Eta())
        if(abs(JET1.Phi() - JET2.Phi())<= 3.14159265359):
            dphijj = abs(JET1.Phi() - JET2.Phi())
        else:
            dphijj = 3.14159265359*2 - abs(JET1.Phi() - JET2.Phi())

 
        # Z1,2(Pt,Eta,Phi,Energy,Mass)
        Tight_Z1 = Z1_LEP_P + Z1_LEP_M
        Tight_Z2 = Z2_LEP_P + Z2_LEP_M
        Tight_Z1_pt = Tight_Z1.Pt()
        Tight_Z1_eta = Tight_Z1.Eta()
        Tight_Z1_phi = Tight_Z1.Phi()
        Tight_Z1_e = Tight_Z1.Energy()
        Tight_Z1_mass = Tight_Z1.M()
        Tight_Z2_pt = Tight_Z2.Pt()
        Tight_Z2_eta = Tight_Z2.Eta()
        Tight_Z2_phi = Tight_Z2.Phi()
        Tight_Z2_e = Tight_Z2.Energy()
        Tight_Z2_mass = Tight_Z2.M()


        # E_ZZ, Pt_ZZ, M_ZZ, EtaZZ, PhiZZ, dphi_ZZ, deta_ZZ
        Z1Z2 = Tight_Z1 + Tight_Z2
        E_ZZ = Z1Z2.Energy();
        Pt_ZZ = Z1Z2.Pt();
        M_ZZ = Z1Z2.M();
        EtaZZ = Z1Z2.Eta(); 
        PhiZZ = Z1Z2.Phi(); 
        if(abs(Tight_Z1.Phi() - Tight_Z2.Phi())<= 3.14159265359):
            dphi_ZZ = abs(Tight_Z1.Phi() - Tight_Z2.Phi())
        elif (abs(Tight_Z1.Phi() - Tight_Z2.Phi())> 3.14159265359):
            dphi_ZZ = 3.14159265359*2 - abs(Tight_Z1.Phi() - Tight_Z2.Phi())
        deta_ZZ = abs(Tight_Z1.Eta() - Tight_Z2.Eta())

        
        # Z1Z2jj_pt, Z1Z2jj_eta, Z1Z2jj_phi, Z1Z2jj_M, Z1Z2jj_E, Zeppen_Z1, Zeppen_Z2, RpT_jets, Rpt_hard
        Z1Z2jj_pt = (Z1Z2 + JET1 + JET2).Pt()
        Z1Z2jj_eta = (Z1Z2 + JET1 + JET2).Eta()
        Z1Z2jj_phi = (Z1Z2 + JET1 + JET2).Phi()
        Z1Z2jj_M = (Z1Z2 + JET1 + JET2).M()
        Z1Z2jj_E = (Z1Z2 + JET1 + JET2).Energy()
        Zeppen_Z1 = Tight_Z1_eta - (jet1eta + jet2eta)/2
        Zeppen_Z2 = Tight_Z2_eta - (jet1eta + jet2eta)/2
        RpT_jets = Ptjj / (jet1pt + jet2pt)
        Rpt_hard = Z1Z2jj_pt / (Tight_Z1_pt+Tight_Z2_pt+jet1pt+jet2pt)

        # Weight of Event, scalar sum of transverse momenta(ScalarHT)
        Weight = (branchEvent.At(0)).Weight
        ScalarHT = (branchScalarHT.At(0)).HT

        temp_list = [lep1pt,lep1eta,lep1phi,lep1e, lep2pt,lep2eta,lep2phi,lep2e, lep3pt,lep3eta,lep3phi,lep3e, lep4pt,lep4eta,
                     lep4phi,lep4e, jet1pt,jet1eta,jet1phi,jet1m, jet2pt,jet2eta,jet2phi,jet2m, 
                     Z1_lep_p_pt,Z1_lep_p_eta,Z1_lep_p_phi,Z1_lep_p_e, Z1_lep_m_pt,Z1_lep_m_eta,Z1_lep_m_phi,Z1_lep_m_e,
                     Z2_lep_p_pt,Z2_lep_p_eta,Z2_lep_p_phi,Z2_lep_p_e, Z2_lep_m_pt,Z2_lep_m_eta,Z2_lep_m_phi,Z2_lep_m_e,
                     MET, METphi,
                     Mll_Z1, Mll_Z2, Z1_Mt, Z2_Mt, detall_Z1, detall_Z2, dphill_Z1, dphill_Z2, Ptll_Z1, Ptll_Z2, Ell_Z1, Ell_Z2, Mllll,
                     Mjj, Mtjj, detajj, dphijj, Ejj, Ptjj, Etajj, Phijj,
                     Tight_Z1_pt,Tight_Z1_eta,Tight_Z1_phi,Tight_Z1_e,Tight_Z1_mass,
                     Tight_Z2_pt,Tight_Z2_eta,Tight_Z2_phi,Tight_Z2_e,Tight_Z2_mass, 
                     E_ZZ,Pt_ZZ,M_ZZ,EtaZZ,PhiZZ,dphi_ZZ,deta_ZZ,
                     Z1Z2jj_pt, Z1Z2jj_eta, Z1Z2jj_phi, Z1Z2jj_M, Z1Z2jj_E, Zeppen_Z1, Zeppen_Z2, RpT_jets, Rpt_hard,
                     Weight, ScalarHT, LL_Helicity, TL_Helicity, TT_Helicity  ] 
        Selected_Event.append(temp_list)

        #### Discriminant Saving is done here

#        rm_selected_events += 1
#        print(rm_selected_events) 
#        continue   
    print "selected Event Num :", flag_lepton_num
    return Selected_Event
        #break
        #Till Here
        ############################################################################################
        ############################################################################################







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

    lep1pt=np.zeros(1,dtype=float); lep1eta=np.zeros(1,dtype=float); lep1phi=np.zeros(1,dtype=float); lep1e=np.zeros(1,dtype=float);
    lep2pt=np.zeros(1,dtype=float); lep2eta=np.zeros(1,dtype=float); lep2phi=np.zeros(1,dtype=float); lep2e=np.zeros(1,dtype=float);
    lep3pt=np.zeros(1,dtype=float); lep3eta=np.zeros(1,dtype=float); lep3phi=np.zeros(1,dtype=float); lep3e=np.zeros(1,dtype=float);
    lep4pt=np.zeros(1,dtype=float); lep4eta=np.zeros(1,dtype=float); lep4phi=np.zeros(1,dtype=float); lep4e=np.zeros(1,dtype=float);
    jet1pt=np.zeros(1,dtype=float); jet1eta=np.zeros(1,dtype=float); jet1phi=np.zeros(1,dtype=float); jet1m=np.zeros(1,dtype=float);
    jet2pt=np.zeros(1,dtype=float); jet2eta=np.zeros(1,dtype=float); jet2phi=np.zeros(1,dtype=float); jet2m=np.zeros(1,dtype=float);
    Z1_lep_p_pt=np.zeros(1,dtype=float); Z1_lep_p_eta=np.zeros(1,dtype=float); Z1_lep_p_phi=np.zeros(1,dtype=float); Z1_lep_p_e=np.zeros(1,dtype=float);
    Z1_lep_m_pt=np.zeros(1,dtype=float); Z1_lep_m_eta=np.zeros(1,dtype=float); Z1_lep_m_phi=np.zeros(1,dtype=float); Z1_lep_m_e=np.zeros(1,dtype=float);
    Z2_lep_p_pt=np.zeros(1,dtype=float); Z2_lep_p_eta=np.zeros(1,dtype=float); Z2_lep_p_phi=np.zeros(1,dtype=float); Z2_lep_p_e=np.zeros(1,dtype=float);
    Z2_lep_m_pt=np.zeros(1,dtype=float); Z2_lep_m_eta=np.zeros(1,dtype=float); Z2_lep_m_phi=np.zeros(1,dtype=float); Z2_lep_m_e=np.zeros(1,dtype=float);
    MET=np.zeros(1,dtype=float); METphi=np.zeros(1,dtype=float);
    Mll_Z1=np.zeros(1,dtype=float); Mll_Z2=np.zeros(1,dtype=float); Z1_Mt=np.zeros(1,dtype=float); Z2_Mt=np.zeros(1,dtype=float);
    detall_Z1=np.zeros(1,dtype=float); detall_Z2=np.zeros(1,dtype=float); dphill_Z1=np.zeros(1,dtype=float); dphill_Z2=np.zeros(1,dtype=float);
    Ptll_Z1=np.zeros(1,dtype=float); Ptll_Z2=np.zeros(1,dtype=float); Ell_Z1=np.zeros(1,dtype=float); Ell_Z2=np.zeros(1,dtype=float); Mllll=np.zeros(1,dtype=float); 
    Mjj=np.zeros(1,dtype=float); Mtjj=np.zeros(1,dtype=float); detajj=np.zeros(1,dtype=float); dphijj=np.zeros(1,dtype=float); Ejj=np.zeros(1,dtype=float); Ptjj=np.zeros(1,dtype=float); Etajj=np.zeros(1,dtype=float); Phijj=np.zeros(1,dtype=float);
    Tight_Z1_pt=np.zeros(1,dtype=float); Tight_Z1_eta=np.zeros(1,dtype=float); Tight_Z1_phi=np.zeros(1,dtype=float); Tight_Z1_e=np.zeros(1,dtype=float); Tight_Z1_mass=np.zeros(1,dtype=float);
    Tight_Z2_pt=np.zeros(1,dtype=float); Tight_Z2_eta=np.zeros(1,dtype=float); Tight_Z2_phi=np.zeros(1,dtype=float); Tight_Z2_e=np.zeros(1,dtype=float); Tight_Z2_mass=np.zeros(1,dtype=float); 
    E_ZZ=np.zeros(1,dtype=float); Pt_ZZ=np.zeros(1,dtype=float); M_ZZ=np.zeros(1,dtype=float); EtaZZ=np.zeros(1,dtype=float); PhiZZ=np.zeros(1,dtype=float); dphi_ZZ=np.zeros(1,dtype=float); deta_ZZ=np.zeros(1,dtype=float);
    Z1Z2jj_pt=np.zeros(1,dtype=float); Z1Z2jj_eta=np.zeros(1,dtype=float); Z1Z2jj_phi=np.zeros(1,dtype=float); Z1Z2jj_M=np.zeros(1,dtype=float); Z1Z2jj_E=np.zeros(1,dtype=float); Zeppen_Z1=np.zeros(1,dtype=float); Zeppen_Z2=np.zeros(1,dtype=float); RpT_jets=np.zeros(1,dtype=float); Rpt_hard=np.zeros(1,dtype=float);
    Weight=np.zeros(1,dtype=float); ScalarHT=np.zeros(1,dtype=float); LL_Helicity=np.zeros(1,dtype=float); TL_Helicity=np.zeros(1,dtype=float); TT_Helicity=np.zeros(1,dtype=float); 


    tree.Branch('lep1pt',lep1pt,'lep1pt/D'); tree.Branch('lep1eta',lep1eta,'lep1eta/D');tree.Branch('lep1phi',lep1phi,'lep1phi/D');tree.Branch('lep1e',lep1e,'lep1e/D');
    tree.Branch('lep2pt',lep2pt,'lep2pt/D'); tree.Branch('lep2eta',lep2eta,'lep2eta/D');tree.Branch('lep2phi',lep2phi,'lep2phi/D');tree.Branch('lep2e',lep2e,'lep2e/D');
    tree.Branch('lep3pt',lep3pt,'lep3pt/D'); tree.Branch('lep3eta',lep3eta,'lep3eta/D');tree.Branch('lep3phi',lep3phi,'lep3phi/D');tree.Branch('lep3e',lep3e,'lep3e/D');
    tree.Branch('lep4pt',lep4pt,'lep4pt/D'); tree.Branch('lep4eta',lep4eta,'lep4eta/D');tree.Branch('lep4phi',lep4phi,'lep4phi/D');tree.Branch('lep4e',lep4e,'lep4e/D');
    tree.Branch('jet1pt',jet1pt,'jet1pt/D'); tree.Branch('jet1eta',jet1eta,'jet1eta/D');tree.Branch('jet1phi',jet1phi,'jet1phi/D');tree.Branch('jet1m',jet1m,'jet1m/D');
    tree.Branch('jet2pt',jet2pt,'jet2pt/D'); tree.Branch('jet2eta',jet2eta,'jet2eta/D');tree.Branch('jet2phi',jet2phi,'jet2phi/D');tree.Branch('jet2m',jet2m,'jet2m/D');
    tree.Branch('Z1_lep_p_pt',Z1_lep_p_pt,'Z1_lep_p_pt/D'); tree.Branch('Z1_lep_p_eta',Z1_lep_p_eta,'Z1_lep_p_eta/D');tree.Branch('Z1_lep_p_phi',Z1_lep_p_phi,'Z1_lep_p_phi/D');tree.Branch('Z1_lep_p_e',Z1_lep_p_e,'Z1_lep_p_e/D');
    tree.Branch('Z1_lep_m_pt',Z1_lep_m_pt,'Z1_lep_m_pt/D'); tree.Branch('Z1_lep_m_eta',Z1_lep_m_eta,'Z1_lep_m_eta/D');tree.Branch('Z1_lep_m_phi',Z1_lep_m_phi,'Z1_lep_m_phi/D');tree.Branch('Z1_lep_m_e',Z1_lep_m_e,'Z1_lep_m_e/D');
    tree.Branch('Z2_lep_p_pt',Z2_lep_p_pt,'Z2_lep_p_pt/D'); tree.Branch('Z2_lep_p_eta',Z2_lep_p_eta,'Z2_lep_p_eta/D');tree.Branch('Z2_lep_p_phi',Z2_lep_p_phi,'Z2_lep_p_phi/D');tree.Branch('Z2_lep_p_e',Z2_lep_p_e,'Z2_lep_p_e/D');
    tree.Branch('Z2_lep_m_pt',Z2_lep_m_pt,'Z2_lep_m_pt/D'); tree.Branch('Z2_lep_m_eta',Z2_lep_m_eta,'Z2_lep_m_eta/D');tree.Branch('Z2_lep_m_phi',Z2_lep_m_phi,'Z2_lep_m_phi/D');tree.Branch('Z2_lep_m_e',Z2_lep_m_e,'Z2_lep_m_e/D');
    tree.Branch('MET',MET,'MET/D'); tree.Branch('METphi',METphi,'METphi/D');
    tree.Branch('Mll_Z1',Mll_Z1,'Mll_Z1/D'); tree.Branch('Mll_Z2',Mll_Z2,'Mll_Z2/D');tree.Branch('Z1_Mt',Z1_Mt,'Z1_Mt/D');tree.Branch('Z2_Mt',Z2_Mt,'Z2_Mt/D');
    tree.Branch('detall_Z1',detall_Z1,'detall_Z1/D'); tree.Branch('detall_Z2',detall_Z2,'detall_Z2/D');tree.Branch('dphill_Z1',dphill_Z1,'dphill_Z1/D');tree.Branch('dphill_Z2',dphill_Z2,'dphill_Z2/D');
    tree.Branch('Ptll_Z1',Ptll_Z1,'Ptll_Z1/D'); tree.Branch('Ptll_Z2',Ptll_Z2,'Ptll_Z2/D');tree.Branch('Ell_Z1',Ell_Z1,'Ell_Z1/D');tree.Branch('Ell_Z2',Ell_Z2,'Ell_Z2/D'); tree.Branch('Mllll',Mllll,'Mllll/D');
    tree.Branch('Mjj',Mjj,'Mjj/D'); tree.Branch('Mtjj',Mtjj,'Mtjj/D');tree.Branch('detajj',detajj,'detajj/D');tree.Branch('dphijj',dphijj,'dphijj/D');
    tree.Branch('Ejj',Ejj,'Ejj/D'); tree.Branch('Ptjj',Ptjj,'Ptjj/D');tree.Branch('Etajj',Etajj,'Etajj/D');tree.Branch('Phijj',Phijj,'Phijj/D');
    tree.Branch('Tight_Z1_pt',Tight_Z1_pt,'Tight_Z1_pt/D'); tree.Branch('Tight_Z1_eta',Tight_Z1_eta,'Tight_Z1_eta/D');tree.Branch('Tight_Z1_phi',Tight_Z1_phi,'Tight_Z1_phi/D');tree.Branch('Tight_Z1_e',Tight_Z1_e,'Tight_Z1_e/D'); tree.Branch('Tight_Z1_mass',Tight_Z1_mass,'Tight_Z1_mass/D');
    tree.Branch('Tight_Z2_pt',Tight_Z2_pt,'Tight_Z2_pt/D'); tree.Branch('Tight_Z2_eta',Tight_Z2_eta,'Tight_Z2_eta/D');tree.Branch('Tight_Z2_phi',Tight_Z2_phi,'Tight_Z2_phi/D');tree.Branch('Tight_Z2_e',Tight_Z2_e,'Tight_Z2_e/D'); tree.Branch('Tight_Z2_mass',Tight_Z2_mass,'Tight_Z2_mass/D');
    tree.Branch('E_ZZ',E_ZZ,'E_ZZ/D'); tree.Branch('Pt_ZZ',Pt_ZZ,'Pt_ZZ/D');tree.Branch('M_ZZ',M_ZZ,'M_ZZ/D');tree.Branch('EtaZZ',EtaZZ,'EtaZZ/D');
    tree.Branch('PhiZZ',PhiZZ,'PhiZZ/D'); tree.Branch('dphi_ZZ',dphi_ZZ,'dphi_ZZ/D');tree.Branch('deta_ZZ',deta_ZZ,'deta_ZZ/D');
    tree.Branch('Z1Z2jj_pt',Z1Z2jj_pt,'Z1Z2jj_pt/D'); tree.Branch('Z1Z2jj_eta',Z1Z2jj_eta,'Z1Z2jj_eta/D');tree.Branch('Z1Z2jj_phi',Z1Z2jj_phi,'Z1Z2jj_phi/D');tree.Branch('Z1Z2jj_M',Z1Z2jj_M,'Z1Z2jj_M/D'); tree.Branch('Z1Z2jj_E',Z1Z2jj_E,'Z1Z2jj_E/D');
    tree.Branch('Zeppen_Z1',Zeppen_Z1,'Zeppen_Z1/D'); tree.Branch('Zeppen_Z2',Zeppen_Z2,'Zeppen_Z2/D');tree.Branch('RpT_jets',RpT_jets,'RpT_jets/D');tree.Branch('Rpt_hard',Rpt_hard,'Rpt_hard/D');
    tree.Branch('Weight',Weight,'Weight/D'); tree.Branch('ScalarHT',ScalarHT,'ScalarHT/D');
    tree.Branch('LL_Helicity',LL_Helicity,'LL_Helicity/D'); tree.Branch('TL_Helicity',TL_Helicity,'TL_Helicity/D')
    tree.Branch('TT_Helicity',TT_Helicity,'TT_Helicity/D')


    for i in range(len(Selected_Event_list)):
        lep1pt[0]=Selected_Event_list[i][0]; lep1eta[0]=Selected_Event_list[i][1]; lep1phi[0]=Selected_Event_list[i][2]; lep1e[0]=Selected_Event_list[i][3];
        lep2pt[0]=Selected_Event_list[i][4]; lep2eta[0]=Selected_Event_list[i][5]; lep2phi[0]=Selected_Event_list[i][6]; lep2e[0]=Selected_Event_list[i][7];
        lep3pt[0]=Selected_Event_list[i][8]; lep3eta[0]=Selected_Event_list[i][9]; lep3phi[0]=Selected_Event_list[i][10]; lep3e[0]=Selected_Event_list[i][11];
        lep4pt[0]=Selected_Event_list[i][12]; lep4eta[0]=Selected_Event_list[i][13]; lep4phi[0]=Selected_Event_list[i][14]; lep4e[0]=Selected_Event_list[i][15];
        jet1pt[0]=Selected_Event_list[i][16]; jet1eta[0]=Selected_Event_list[i][17]; jet1phi[0]=Selected_Event_list[i][18]; jet1m[0]=Selected_Event_list[i][19];
        jet2pt[0]=Selected_Event_list[i][20]; jet2eta[0]=Selected_Event_list[i][21]; jet2phi[0]=Selected_Event_list[i][22]; jet2m[0]=Selected_Event_list[i][23];
        Z1_lep_p_pt[0]=Selected_Event_list[i][24]; Z1_lep_p_eta[0]=Selected_Event_list[i][25]; Z1_lep_p_phi[0]=Selected_Event_list[i][26]; Z1_lep_p_e[0]=Selected_Event_list[i][27]; 
        Z1_lep_m_pt[0]=Selected_Event_list[i][28]; Z1_lep_m_eta[0]=Selected_Event_list[i][29]; Z1_lep_m_phi[0]=Selected_Event_list[i][30]; Z1_lep_m_e[0]=Selected_Event_list[i][31];
        Z2_lep_p_pt[0]=Selected_Event_list[i][32]; Z2_lep_p_eta[0]=Selected_Event_list[i][33]; Z2_lep_p_phi[0]=Selected_Event_list[i][34]; Z2_lep_p_e[0]=Selected_Event_list[i][35];
        Z2_lep_m_pt[0]=Selected_Event_list[i][36]; Z2_lep_m_eta[0]=Selected_Event_list[i][37]; Z2_lep_m_phi[0]=Selected_Event_list[i][38]; Z2_lep_m_e[0]=Selected_Event_list[i][39];
        MET[0]=Selected_Event_list[i][40]; METphi[0]=Selected_Event_list[i][41];
        Mll_Z1[0]=Selected_Event_list[i][42]; Mll_Z2[0]=Selected_Event_list[i][43]; Z1_Mt[0]=Selected_Event_list[i][44]; Z2_Mt[0]=Selected_Event_list[i][45];
        detall_Z1[0]=Selected_Event_list[i][46]; detall_Z2[0]=Selected_Event_list[i][47]; dphill_Z1[0]=Selected_Event_list[i][48]; dphill_Z2[0]=Selected_Event_list[i][49];
        Ptll_Z1[0]=Selected_Event_list[i][50]; Ptll_Z2[0]=Selected_Event_list[i][51]; Ell_Z1[0]=Selected_Event_list[i][52]; Ell_Z2[0]=Selected_Event_list[i][53]; Mllll[0]=Selected_Event_list[i][54];
        Mjj[0]=Selected_Event_list[i][55]; Mtjj[0]=Selected_Event_list[i][56]; detajj[0]=Selected_Event_list[i][57]; dphijj[0]=Selected_Event_list[i][58];
        Ejj[0]=Selected_Event_list[i][59]; Ptjj[0]=Selected_Event_list[i][60]; Etajj[0]=Selected_Event_list[i][61]; Phijj[0]=Selected_Event_list[i][62];
        Tight_Z1_pt[0]=Selected_Event_list[i][63]; Tight_Z1_eta[0]=Selected_Event_list[i][64]; Tight_Z1_phi[0]=Selected_Event_list[i][65]; Tight_Z1_e[0]=Selected_Event_list[i][66]; Tight_Z1_mass[0]=Selected_Event_list[i][67];
        Tight_Z2_pt[0]=Selected_Event_list[i][68]; Tight_Z2_eta[0]=Selected_Event_list[i][69]; Tight_Z2_phi[0]=Selected_Event_list[i][70]; Tight_Z2_e[0]=Selected_Event_list[i][71]; Tight_Z2_mass[0]=Selected_Event_list[i][72];
        E_ZZ[0]=Selected_Event_list[i][73]; Pt_ZZ[0]=Selected_Event_list[i][74]; M_ZZ[0]=Selected_Event_list[i][75]; EtaZZ[0]=Selected_Event_list[i][76]; PhiZZ[0]=Selected_Event_list[i][77]; dphi_ZZ[0]=Selected_Event_list[i][78]; deta_ZZ[0]=Selected_Event_list[i][79];
        Z1Z2jj_pt[0]=Selected_Event_list[i][80]; Z1Z2jj_eta[0]=Selected_Event_list[i][81]; Z1Z2jj_phi[0]=Selected_Event_list[i][82]; Z1Z2jj_M[0]=Selected_Event_list[i][83]; Z1Z2jj_E[0]=Selected_Event_list[i][84];
        Zeppen_Z1[0]=Selected_Event_list[i][85]; Zeppen_Z2[0]=Selected_Event_list[i][86]; RpT_jets[0]=Selected_Event_list[i][87]; Rpt_hard[0]=Selected_Event_list[i][88];
        Weight[0]=Selected_Event_list[i][89]; ScalarHT[0]=Selected_Event_list[i][90]; LL_Helicity[0]=Selected_Event_list[i][91]; TL_Helicity[0]=Selected_Event_list[i][92]; TT_Helicity[0]=Selected_Event_list[i][93];
        tree.Fill()

    outROOT_file.Write()
    outROOT_file.Close()
    print("Create Output Ntuple.root :", Outfile)

def main():
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/PseudoData/delphes_VBSsignal.root"    
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/PseudoData/delphes_decay_VBSsignal_NoWDecay.root"
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/delphes_decay_VBS_SS_WW_TT_template.root"
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/delphes_decay_VBS_SS_WW_TL_template.root"
#    infile_test = "/Users/leejunho/Desktop/git/My_git/My_temp/n51_VBS_SSWW_PyROOT/Template/delphes_decay_VBS_SS_WW_LL_template.root"

    Store_ROOT(infile_test)

if __name__=="__main__":
    main()


