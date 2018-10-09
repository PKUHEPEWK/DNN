import os, sys
import numpy as np
import tensorflow as tf
from DNN_tensorflow_class_py2 import EarlyStopping, DNN
from ROOT import TFile, TTree, TCut, TH1F
from root_numpy import fill_hist
from root_numpy import root2array, tree2array, array2root, array2tree
from root_numpy import testdata
from sklearn.model_selection import train_test_split
from c0_READ_PATH_FILE_ROOT import read_file_name_root

def InputROOT_OutputTXT(infileROOT,ModelName):
    inputFile = read_file_name_root(infileROOT)
    ROOT_input = inputFile[2]
    Text_output = inputFile[0] + "reg.txt"
    data = TFile.Open(ROOT_input)
    tree = data.Get('tree')

    ####################################### Input DATA Sets !!!!! 
    reco_bj1_Energy_    = tree2array(tree, branches='reco_bj1_Energy')
    reco_bj1_Theta_     = tree2array(tree, branches='reco_bj1_Theta')
    reco_bj1_Phi_       = tree2array(tree, branches='reco_bj1_Phi')
    reco_bj2_Energy_    = tree2array(tree, branches='reco_bj2_Energy')
    reco_bj2_Theta_     = tree2array(tree, branches='reco_bj2_Theta')
    reco_bj2_Phi_       = tree2array(tree, branches='reco_bj2_Phi')
    reco_MW1_Energy_    = tree2array(tree, branches='reco_MW1_Energy')
    reco_MW1_Theta_     = tree2array(tree, branches='reco_MW1_Theta')
    reco_MW1_Phi_       = tree2array(tree, branches='reco_MW1_Phi')
    reco_MW2_Energy_    = tree2array(tree, branches='reco_MW2_Energy')
    reco_MW2_Theta_     = tree2array(tree, branches='reco_MW2_Theta')
    reco_MW2_Phi_       = tree2array(tree, branches='reco_MW2_Phi')
    reco_l1_Energy_     = tree2array(tree, branches='reco_l1_Energy')
    reco_l1_Theta_      = tree2array(tree, branches='reco_l1_Theta')
    reco_l1_Phi_        = tree2array(tree, branches='reco_l1_Phi')
    reco_l2_Energy_     = tree2array(tree, branches='reco_l2_Energy')
    reco_l2_Theta_      = tree2array(tree, branches='reco_l2_Theta')
    reco_l2_Phi_        = tree2array(tree, branches='reco_l2_Phi')
    reco_l3_Energy_     = tree2array(tree, branches='reco_l3_Energy')
    reco_l3_Theta_      = tree2array(tree, branches='reco_l3_Theta')
    reco_l3_Phi_        = tree2array(tree, branches='reco_l3_Phi')
    reco_mET_Pt_        = tree2array(tree, branches='reco_mET_Pt')
    reco_mET_Phi_       = tree2array(tree, branches='reco_mET_Phi')
    mHT_            = tree2array(tree, branches='mHT')

    Gen_BjetTopHad_E_       = tree2array(tree, branches='Gen_BjetTopHad_E')
    Gen_WTopHad_mW_     = tree2array(tree, branches='Gen_WTopHad_mW')
    Gen_BjetTopLep_E_       = tree2array(tree, branches='Gen_BjetTopLep_E')
    Gen_NeutTopLep_Phi_     = tree2array(tree, branches='Gen_NeutTopLep_Phi')
    Gen_WTopLep_mW_     = tree2array(tree, branches='Gen_WTopLep_mW')
    #Kin_BjetTopHad_E_       = tree2array(tree, branches='Kin_BjetTopHad_E')
    #Kin_WTopHad_mW_     = tree2array(tree, branches='Kin_WTopHad_mW')
    #Kin_BjetTopLep_E_       = tree2array(tree, branches='Kin_BjetTopLep_E')
    #Kin_NeutTopLep_Phi_     = tree2array(tree, branches='Kin_NeutTopLep_Phi')
    #Kin_WTopLep_mW_     = tree2array(tree, branches='Kin_WTopLep_mW')
    ###############################################################################################################

    ##################################### Target DATA !!!!!
    mc_mem_ttz_weight_evalgenmax_log = tree2array(tree, branches='mc_mem_ttz_weight_evalgenmax_log')
    #mc_kin_ttz_weight_logmax = tree2array(tree, branches='mc_kin_ttz_weight_logmax')
    ###############################################################################################################

    ENTRY = mc_mem_ttz_weight_evalgenmax_log.size
    num_Valid = np.zeros(ENTRY)
    print "ENTRY :", ENTRY

    for i2 in range(ENTRY):
        num_Valid[i2] = i2

    I2 = ENTRY
    reco_bj1_Energy = np.zeros(I2)
    reco_bj1_Theta  = np.zeros(I2)
    reco_bj1_Phi    = np.zeros(I2)
    reco_bj2_Energy = np.zeros(I2)
    reco_bj2_Theta  = np.zeros(I2)
    reco_bj2_Phi    = np.zeros(I2)
    reco_MW1_Energy = np.zeros(I2)
    reco_MW1_Theta  = np.zeros(I2)
    reco_MW1_Phi    = np.zeros(I2)
    reco_MW2_Energy = np.zeros(I2)
    reco_MW2_Theta  = np.zeros(I2)
    reco_MW2_Phi    = np.zeros(I2)
    reco_l1_Energy  = np.zeros(I2)
    reco_l1_Theta   = np.zeros(I2)
    reco_l1_Phi = np.zeros(I2)
    reco_l2_Energy  = np.zeros(I2)
    reco_l2_Theta   = np.zeros(I2)
    reco_l2_Phi = np.zeros(I2)
    reco_l3_Energy  = np.zeros(I2)
    reco_l3_Theta   = np.zeros(I2)
    reco_l3_Phi = np.zeros(I2)
    reco_mET_Pt = np.zeros(I2)
    reco_mET_Phi    = np.zeros(I2)
    mHT     = np.zeros(I2)
    Gen_BjetTopHad_E    = np.zeros(I2)
    Gen_WTopHad_mW      = np.zeros(I2)
    Gen_BjetTopLep_E    = np.zeros(I2)
    Gen_NeutTopLep_Phi  = np.zeros(I2)
    Gen_WTopLep_mW  = np.zeros(I2)
    #Kin_BjetTopHad_E    = np.zeros(I2)
    #Kin_WTopHad_mW      = np.zeros(I2)
    #Kin_BjetTopLep_E    = np.zeros(I2)
    #Kin_NeutTopLep_Phi  = np.zeros(I2)
    #Kin_WTopLep_mW  = np.zeros(I2)
    TARGET  = np.zeros(I2)

    for j1 in range(reco_bj1_Energy.size):
        jj1 = int(num_Valid[j1])
        reco_bj1_Energy[j1] = reco_bj1_Energy_[jj1]
        reco_bj1_Theta[j1]  = reco_bj1_Theta_[jj1]
        reco_bj1_Phi[j1]    = reco_bj1_Phi_[jj1]
        reco_bj2_Energy[j1] = reco_bj2_Energy_[jj1]
        reco_bj2_Theta[j1]  = reco_bj2_Theta_[jj1]
        reco_bj2_Phi[j1]    = reco_bj2_Phi_[jj1]
        reco_MW1_Energy[j1] = reco_MW1_Energy_[jj1]
        reco_MW1_Theta[j1]  = reco_MW1_Theta_[jj1]
        reco_MW1_Phi[j1]    = reco_MW1_Phi_[jj1]
        reco_MW2_Energy[j1] = reco_MW2_Energy_[jj1]
        reco_MW2_Theta[j1]  = reco_MW2_Theta_[jj1]
        reco_MW2_Phi[j1]    = reco_MW2_Phi_[jj1]
        reco_l1_Energy[j1]  = reco_l1_Energy_[jj1]
        reco_l1_Theta[j1]   = reco_l1_Theta_[jj1]
        reco_l1_Phi[j1]     = reco_l1_Phi_[jj1]
        reco_l2_Energy[j1]  = reco_l2_Energy_[jj1]
        reco_l2_Theta[j1]   = reco_l2_Theta_[jj1]
        reco_l2_Phi[j1]     = reco_l2_Phi_[jj1]
        reco_l3_Energy[j1]  = reco_l3_Energy_[jj1]
        reco_l3_Theta[j1]   = reco_l3_Theta_[jj1]
        reco_l3_Phi[j1]     = reco_l3_Phi_[jj1]
        reco_mET_Pt[j1]     = reco_mET_Pt_[jj1]
        reco_mET_Phi[j1]    = reco_mET_Phi_[jj1]
        mHT[j1]         = mHT_[jj1]
        Gen_BjetTopHad_E[j1]        = Gen_BjetTopHad_E_[jj1]
        Gen_WTopHad_mW[j1]          = Gen_WTopHad_mW_[jj1]
        Gen_BjetTopLep_E[j1]        = Gen_BjetTopLep_E_[jj1]
        Gen_NeutTopLep_Phi[j1]      = Gen_NeutTopLep_Phi_[jj1]
        Gen_WTopLep_mW[j1]          = Gen_WTopLep_mW_[jj1]
        #Kin_BjetTopHad_E[j1]        = Kin_BjetTopHad_E_[jj1]
        #Kin_WTopHad_mW[j1]          = Kin_WTopHad_mW_[jj1]
        #Kin_BjetTopLep_E[j1]        = Kin_BjetTopLep_E_[jj1]
        #Kin_NeutTopLep_Phi[j1]      = Kin_NeutTopLep_Phi_[jj1]
        #Kin_WTopLep_mW[j1]          = Kin_WTopLep_mW_[jj1]
        TARGET[j1]      = mc_mem_ttz_weight_evalgenmax_log[jj1]

    ARRAY = np.stack((reco_bj1_Energy, reco_bj1_Theta, reco_bj1_Phi, reco_bj2_Energy, reco_bj2_Theta, reco_bj2_Phi, reco_MW1_Energy, reco_MW1_Theta, reco_MW1_Phi, reco_MW2_Energy, reco_MW2_Theta, reco_MW2_Phi, reco_l1_Energy, reco_l1_Theta, reco_l1_Phi, reco_l2_Energy, reco_l2_Theta, reco_l2_Phi, reco_l3_Energy, reco_l3_Theta, reco_l3_Phi, reco_mET_Pt, reco_mET_Phi, mHT, Gen_BjetTopHad_E, Gen_WTopHad_mW, Gen_BjetTopLep_E, Gen_NeutTopLep_Phi, Gen_WTopLep_mW))
    TARGET = np.stack([TARGET])
    
    ARRAY = ARRAY.T
    TARGET = TARGET.T
    X_part = ARRAY[:]
    Y_part = TARGET[:]
    print(X_part.shape,"x_train"); print(Y_part.shape)
        
    model = DNN(n_in=29, n_hiddens=[150,150,150,150,150,150,150,150,150,150], n_out=1)  ##FIXME TODO
    model.regression_model_read(ModelName=ModelName)
    accuracy = model.regression_evaluate(X_part, Y_part)
    print('Error value :', accuracy)
    #np.set_printoptions(threshold='nan')
    print("REAL Y :",Y_part)
    Regressed_values = model.Indicated_regressed_ttZ(X_part, Y_part)
   
    OF = open(Text_output,"w+")
    print("Length of DATA :", len(Regressed_values))
    for i in range(len(Regressed_values)):
        if i==0: OF.write("%s\n" %"Real Regressed")
        OF.write("%s " %(str(Y_part[i][0])))
        OF.write("%s\n" %(str(Regressed_values[i][0])))


def main():
    infileROOT = "/Users/leejunho/Desktop/test_regression/TEST_TRAIN_ROOT/TEST_ROOT.root"
    #infileROOT = "/Users/leejunho/Desktop/test_regression/TEST_TRAIN_ROOT/TRAIN_ROOT.root"
    ModelName = "/Users/leejunho/Desktop/test_regression/ttZ_Reg_EP815.ckpt"

    InputROOT_OutputTXT(infileROOT=infileROOT, ModelName=ModelName)



if __name__=="__main__":
    main()

