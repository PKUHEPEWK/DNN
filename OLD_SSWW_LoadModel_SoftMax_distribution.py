import numpy as np
import os
from DNN_tensorflow_class_py2 import DNN
from ROOT import TFile, TTree, TCut, TH1F
from root_numpy import fill_hist
from root_numpy import root2array, tree2array, array2root, array2tree
from root_numpy import testdata
from sklearn.model_selection import train_test_split

#ModelName = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/20180903_TrainENum230000/LayerNum_3+Node_150+BatchSize_200/SSWW_tensor_TTTL-LL_comp_EP51.ckpt"
ModelName = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/20180904_TrainENum310000/LayerNum_3+Node_150+BatchSize_200/SSWW_tensor_TTTL-LL_comp_EP67.ckpt"

N_train = 310000

data = TFile.Open('/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_DNN/TTTL_LL_230M_comparable.root')
#data = TFile.Open('/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_split_TTTL_LL/SS_230M_MergedTTTL.root')
#data = TFile.Open('/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_split_TTTL_LL/SS_230M_MergedLL.root')
tree = data.Get('tree')
####################################### Input DATA Sets !!!!! 
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
lep1phi = np.zeros(ENTRY)
lep2pt = np.zeros(ENTRY)
lep2eta = np.zeros(ENTRY)
lep2phi = np.zeros(ENTRY)
jet1pt = np.zeros(ENTRY)
jet1eta = np.zeros(ENTRY)
jet1phi = np.zeros(ENTRY)
jet1M = np.zeros(ENTRY)
jet2pt = np.zeros(ENTRY)
jet2eta = np.zeros(ENTRY)
jet2phi = np.zeros(ENTRY)
jet2M = np.zeros(ENTRY)
MET = np.zeros(ENTRY)
lep1PID = np.zeros(ENTRY)
lep2PID = np.zeros(ENTRY)
Mjj = np.zeros(ENTRY)
dr_ll_jj = np.zeros(ENTRY)
dphijj = np.zeros(ENTRY)
zeppen_lep1 = np.zeros(ENTRY)
zeppen_lep2 = np.zeros(ENTRY)
METphi = np.zeros(ENTRY)
detajj = np.zeros(ENTRY)
Mll = np.zeros(ENTRY)
RpT = np.zeros(ENTRY)

LL_Helicity = np.zeros(ENTRY)
TTTL_Helicity = np.zeros(ENTRY)
#TL_Helicity = np.zeros(ENTRY)
#TT_Helicity = np.zeros(ENTRY)
###############################################################################################################
for j1 in range(ENTRY):
    lep1pt[j1] = lep1pt_[j1]
    lep1eta[j1] = lep1eta_[j1]
    lep1phi[j1] = lep1phi_[j1]
    lep2pt[j1] = lep2pt_[j1]
    lep2eta[j1] = lep2eta_[j1]
    lep2phi[j1] = lep2phi_[j1]
    jet1pt[j1] = jet1pt_[j1]
    jet1eta[j1] = jet1eta_[j1]
    jet1phi[j1] = jet1phi_[j1]
    jet1M[j1] = jet1M_[j1]
    jet2pt[j1] = jet2pt_[j1]
    jet2eta[j1] = jet2eta_[j1]
    jet2phi[j1] = jet2phi_[j1]
    jet2M[j1] = jet2M_[j1]
    MET[j1] = MET_[j1]
    lep1PID[j1] = lep1PID_[j1]
    lep2PID[j1] = lep2PID_[j1]
    Mjj[j1] = Mjj_[j1]
    dr_ll_jj[j1] = dr_ll_jj_[j1]
    dphijj[j1] = dphijj_[j1]
    zeppen_lep1[j1] = zeppen_lep1_[j1]
    zeppen_lep2[j1] = zeppen_lep2_[j1]
    METphi[j1] = METphi_[j1]
    detajj[j1] = detajj_[j1]
    Mll[j1] = Mll_[j1]
    RpT[j1] = RpT_[j1]
    LL_Helicity[j1] = LL_Helicity_[j1]
    TTTL_Helicity[j1] = TTTL_Helicity_[j1]
    #TL_Helicity[j1] = TL_Helicity_[j1]
    #TT_Helicity[j1] = TT_Helicity_[j1]

ARRAY = np.stack((lep1pt, lep1eta, lep1phi, lep2pt, lep2eta, lep2phi, jet1pt, jet1eta, jet1phi, jet1M, jet2pt, jet2eta, jet2phi, jet2M, MET, lep1PID, lep2PID, Mjj, dr_ll_jj, dphijj, zeppen_lep1, zeppen_lep2, METphi, detajj, Mll, RpT))
TARGET = np.stack((LL_Helicity, TTTL_Helicity))
#TARGET = np.stack((LL_Helicity, TL_Helicity, TT_Helicity))

ARRAY = ARRAY.T
TARGET = TARGET.T

##'''
X_part = ARRAY[:]
Y_part = TARGET[:]
#N_validation = ARRAY.shape[0]-(N_train)
print(X_part.shape,"x_train"); print(Y_part.shape)
model = DNN(n_in=26, n_hiddens=[150,150,150], n_out=2)
model.fit_classify_model_read(ModelName=ModelName)
accuracy = model.evaluate(X_part, Y_part)
print('accuracy:', accuracy)
np.set_printoptions(threshold='nan')
LL_TTTL_prob_tuple = model.Indicate_classified_LL_TTTL(X_part, Y_part)
##'''


'''
X_train = ARRAY[:]
Y_train = TARGET[:]
N_validation = ARRAY.shape[0]-(N_train)
X_train, X_test, Y_train, Y_test = train_test_split(X_train, Y_train, train_size=N_train)
X_train, X_validation, Y_train, Y_validation = train_test_split(X_train, Y_train, test_size=N_validation)
print(X_train.shape,"x_train");print(X_validation.shape,"x_validation");print(Y_train.shape);print(Y_validation.shape)
model = DNN(n_in=26, n_hiddens=[150,150,150], n_out=2)
model.fit_classify_model_read(ModelName=ModelName)
accuracy = model.evaluate(X_test, Y_test)
print('accuracy:', accuracy)
np.set_printoptions(threshold='nan')
LL_TTTL_prob_tuple = model.Indicate_classified_LL_TTTL(X_test,Y_test)
'''

OF = open("softmax_test_all.txt","a+")
for i in range(len(LL_TTTL_prob_tuple)):
    OF.write("%s" %LL_TTTL_prob_tuple[i])
    OF.write("\n")
OF.close()


'''
OF_LL = open("softmax_test_LL.txt","a+")
OF_TTTL = open("softmax_test_TTTL.txt","a+")
for i in range(len(Y_test)):
#    if i>5: break
#    print(Y_test[i][0])
#    print(Y_test[i][1])
#    print("")
    if(Y_test[i][0]==1.0):
        OF_LL.write("%s" %LL_TTTL_prob_tuple[i])
    elif(Y_test[i][1]==1.0):
        OF_TTTL.write("%s" %LL_TTTL_prob_tuple[i])
OF_LL.close()
OF_TTTL.close()
'''


