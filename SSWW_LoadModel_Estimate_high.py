# This input ROOT file with DNN model Loaded together, outputs probability of softmax txt
import numpy as np
import os, sys
from DNN_tensorflow_class_py2 import DNN
from ROOT import TFile, TTree, TCut, TH1F
from root_numpy import fill_hist
from root_numpy import root2array, tree2array, array2root, array2tree
from root_numpy import testdata
from sklearn.model_selection import train_test_split
from c0_READ_PATH_FILE_ROOT import read_file_name_root
sys.path.append("/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting")
from n1_Template_fit_hist_production_n_compare import HistProduction, HistoCompare


def InputROOT_OutputTXT(infileROOT,ModelName):
    inputFile = read_file_name_root(infileROOT)
    ROOT_input = inputFile[2]
    ROOT_Estimated_LL = inputFile[3] + "Estimated_LL.root"
    ROOT_Estimated_TTTL = inputFile[3] + "Estimated_TTTL.root"
#    ROOT_Estimated_TTTL = inputFile[3] + inputFile[0] + "_Esti_TTTL.root"
    print(ROOT_Estimated_LL, ROOT_Estimated_TTTL)   

    data = TFile.Open(ROOT_input)
    tree = data.Get('tree')
    ####################################### Input DATA Sets !!!!! 
    lep1pt_      = tree2array(tree, branches='lep1pt')
    lep1eta_     = tree2array(tree, branches='lep1eta')
    #lep1phi_     = tree2array(tree, branches='lep1phi')
    lep2pt_      = tree2array(tree, branches='lep2pt')
    lep2eta_     = tree2array(tree, branches='lep2eta')
    #lep2phi_     = tree2array(tree, branches='lep2phi')
    jet1pt_      = tree2array(tree, branches='jet1pt')
    jet1eta_     = tree2array(tree, branches='jet1eta')
    #jet1phi_     = tree2array(tree, branches='jet1phi')
    #jet1M_       = tree2array(tree, branches='jet1M')
    jet2pt_      = tree2array(tree, branches='jet2pt')
    jet2eta_     = tree2array(tree, branches='jet2eta')
    #jet2phi_     = tree2array(tree, branches='jet2phi')
    #jet2M_       = tree2array(tree, branches='jet2M')
    MET_         = tree2array(tree, branches='MET')
    #lep1PID_     = tree2array(tree, branches='lep1PID')
    #lep2PID_     = tree2array(tree, branches='lep2PID')
    #Mjj_         = tree2array(tree, branches='Mjj')
    dr_ll_jj_    = tree2array(tree, branches='dr_ll_jj')
    dphijj_      = tree2array(tree, branches='dphijj')
    #zeppen_lep1_ = tree2array(tree, branches='zeppen_lep1')
    #zeppen_lep2_ = tree2array(tree, branches='zeppen_lep2')
    #METphi_      = tree2array(tree, branches='METphi')
    detajj_      = tree2array(tree, branches='detajj')
    Mll_         = tree2array(tree, branches='Mll')
    #RpT_         = tree2array(tree, branches='RpT')
    ###############################################################################################################

    ##################################### Target DATA !!!!!
    LL_Helicity_ = tree2array(tree, branches='LL_Helicity')
    TTTL_Helicity_ = tree2array(tree, branches='TTTL_Helicity')
    #TL_Helicity_ = tree2array(tree, branches='TL_Helicity')
    #TT_Helicity_ = tree2array(tree, branches='TT_Helicity')
    ###############################################################################################################

    ENTRY = LL_Helicity_.size
    print "ENTRY :", ENTRY

    lep1pt = np.zeros(ENTRY)
    lep1eta = np.zeros(ENTRY)
    #lep1phi = np.zeros(ENTRY)
    lep2pt = np.zeros(ENTRY)
    lep2eta = np.zeros(ENTRY)
    #lep2phi = np.zeros(ENTRY)
    jet1pt = np.zeros(ENTRY)
    jet1eta = np.zeros(ENTRY)
    #jet1phi = np.zeros(ENTRY)
    #jet1M = np.zeros(ENTRY)
    jet2pt = np.zeros(ENTRY)
    jet2eta = np.zeros(ENTRY)
    #jet2phi = np.zeros(ENTRY)
    #jet2M = np.zeros(ENTRY)
    MET = np.zeros(ENTRY)
    #lep1PID = np.zeros(ENTRY)
    #lep2PID = np.zeros(ENTRY)
    #Mjj = np.zeros(ENTRY)
    dr_ll_jj = np.zeros(ENTRY)
    dphijj = np.zeros(ENTRY)
    #zeppen_lep1 = np.zeros(ENTRY)
    #zeppen_lep2 = np.zeros(ENTRY)
    #METphi = np.zeros(ENTRY)
    detajj = np.zeros(ENTRY)
    Mll = np.zeros(ENTRY)
    #RpT = np.zeros(ENTRY)

    LL_Helicity = np.zeros(ENTRY)
    TTTL_Helicity = np.zeros(ENTRY)
    #TL_Helicity = np.zeros(ENTRY)
    #TT_Helicity = np.zeros(ENTRY)
    ###############################################################################################################
    for j1 in range(ENTRY):
        lep1pt[j1] = lep1pt_[j1]
        lep1eta[j1] = lep1eta_[j1]
        #lep1phi[j1] = lep1phi_[j1]
        lep2pt[j1] = lep2pt_[j1]
        lep2eta[j1] = lep2eta_[j1]
        #lep2phi[j1] = lep2phi_[j1]
        jet1pt[j1] = jet1pt_[j1]
        jet1eta[j1] = jet1eta_[j1]
        #jet1phi[j1] = jet1phi_[j1]
        #jet1M[j1] = jet1M_[j1]
        jet2pt[j1] = jet2pt_[j1]
        jet2eta[j1] = jet2eta_[j1]
        #jet2phi[j1] = jet2phi_[j1]
        #jet2M[j1] = jet2M_[j1]
        MET[j1] = MET_[j1]
        #lep1PID[j1] = lep1PID_[j1]
        #lep2PID[j1] = lep2PID_[j1]
        #Mjj[j1] = Mjj_[j1]
        dr_ll_jj[j1] = dr_ll_jj_[j1]
        dphijj[j1] = dphijj_[j1]
        #zeppen_lep1[j1] = zeppen_lep1_[j1]
        #zeppen_lep2[j1] = zeppen_lep2_[j1]
        #METphi[j1] = METphi_[j1]
        detajj[j1] = detajj_[j1]
        Mll[j1] = Mll_[j1]
        #RpT[j1] = RpT_[j1]
        LL_Helicity[j1] = LL_Helicity_[j1]
        TTTL_Helicity[j1] = TTTL_Helicity_[j1]
        #TL_Helicity[j1] = TL_Helicity_[j1]
        #TT_Helicity[j1] = TT_Helicity_[j1]

    #ARRAY = np.stack((lep1pt, lep1eta, lep1phi, lep2pt, lep2eta, lep2phi, jet1pt, jet1eta, jet1phi, jet1M, jet2pt, jet2eta, jet2phi, jet2M, MET, lep1PID, lep2PID, Mjj, dr_ll_jj, dphijj, zeppen_lep1, zeppen_lep2, METphi, detajj, Mll, RpT))
    ARRAY = np.stack((lep1pt, lep1eta, lep2pt, lep2eta, jet1pt, jet1eta, jet2pt, jet2eta, MET, dr_ll_jj, dphijj, detajj, Mll))
    TARGET = np.stack((LL_Helicity, TTTL_Helicity))
    #TARGET = np.stack((LL_Helicity, TL_Helicity, TT_Helicity))

    ARRAY = ARRAY.T
    TARGET = TARGET.T

    ##'''
    X_part = ARRAY[:]
    Y_part = TARGET[:]
    #N_validation = ARRAY.shape[0]-(N_train)
    print(X_part.shape,"x_train"); print(Y_part.shape)
    #model = DNN(n_in=26, n_hiddens=[150], n_out=2)  ##FIXME TODO
    model = DNN(n_in=13, n_hiddens=[200,200,200,200,200], n_out=2)  ##FIXME TODO
    model.fit_classify_model_read(ModelName=ModelName)
    accuracy = model.evaluate(X_part, Y_part)
    print('accuracy:', accuracy)
    np.set_printoptions(threshold='nan')
    LL_TTTL_prob_tuple = model.Indicate_classified_LL_TTTL(X_part, Y_part)

    print(len(LL_TTTL_prob_tuple[2]))

    #List = []; 
    List_LL = []; List_TTTL = []
    for i in range(len(LL_TTTL_prob_tuple[2])):
        LL_n_TTTL = str(LL_TTTL_prob_tuple[2][i]).replace("[","")
        LL_n_TTTL = LL_n_TTTL.replace("]","")
       
        XY_part = np.append(X_part[i],Y_part[i])
        XY_part = tuple(XY_part) 
        #List.append(XY_part)
        LL_p, TTTL_p = LL_n_TTTL.split(); LL_p = float(LL_p); TTTL_p = float(TTTL_p)
        #print(LL_n_TTTL, LL_p, TTTL_p)
        if(LL_p>0.5):
            List_LL.append(XY_part)
        elif(TTTL_p>0.5):
            List_TTTL.append(XY_part)
        else:
            print("ERROR on LL, TTTL proportion!")
            break
    
    nplist_LL = np.array(List_LL, dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),
    ('jet1pt',np.float32),('jet1eta',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),
    ('MET',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),
    ('detajj',np.float32),('Mll',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)] )

    nplist_TTTL = np.array(List_TTTL, dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),
    ('jet1pt',np.float32),('jet1eta',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),
    ('MET',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),
    ('detajj',np.float32),('Mll',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)] )

    LL_ROOT = TFile(ROOT_Estimated_LL,"RECREATE")
    tree_LL = array2tree(nplist_LL)
    tree_LL.Write()
    LL_ROOT.Close()

    TTTL_ROOT = TFile(ROOT_Estimated_TTTL,"RECREATE")
    tree_TTTL = array2tree(nplist_TTTL)
    tree_TTTL.Write()
    TTTL_ROOT.Close()

    return [ROOT_Estimated_LL,ROOT_Estimated_TTTL]

def main():
    infileROOT = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20181003_TrainENum1250000/LayerNum_5+Node_200+BatchSize_100/TEST_TRAIN_ROOT/TEST_ROOT.root" #FIXME
#    infileROOT = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180925_TrainENum4000000/LayerNum_2+Node_200+BatchSize_100/TEST_TRAIN_ROOT/PseudoDATA_3ab_MERGED.root" #FIXME
    PseudoDATA = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_fitting/PseudoDATA/PseudoDATA_3ab.root" #FIXME PseudoDATA

    inputFile = read_file_name_root(infileROOT)
    ModelName = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20181003_TrainENum1250000/LayerNum_5+Node_200+BatchSize_100/SSWW_tensor_TTTL-LL_comp_EP10.ckpt" #FIXME
    ROOT_LL_TTTL = InputROOT_OutputTXT(infileROOT=infileROOT, ModelName=ModelName)
    #print(ROOT_LL_TTTL)
    Appending = [inputFile[3]+"TEST_ROOT_LL.root",inputFile[3]+"TEST_ROOT_TTTL.root"]
    ROOT_LL_TTTL.append(Appending[0]); ROOT_LL_TTTL.append(Appending[1])
    ROOT_LL_TTTL.append(PseudoDATA)

    histoName = ["lep1pt", "lep1eta", "lep2pt", "lep2eta", "jet1pt", "jet1eta", "jet2pt", "jet2eta", "MET", "dr_ll_jj", "dphijj", "detajj", "Mll"]
    HistP = HistProduction(ROOT_LL_TTTL)
    Hist_files = HistP.MakeHistoROOT(binNum=20,histoName=histoName)  # FIXME Turn this on if histo production required.
    print(Hist_files)
    HistoCom = HistoCompare(Hist_files)
    HistoCom.CompareHistoROOT_general()
   
    move_command = "mv *.pdf " + inputFile[3]
    os.system(move_command)
    print(move_command)

    move_command = "mv Estimated_*_hist.root " + inputFile[3]
    os.system(move_command)
    print(move_command)

    move_command = "mv *.root " + inputFile[3]
    os.system(move_command)
    print(move_command)

if __name__=="__main__":
    main()



