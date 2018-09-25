# Use input file from SSWW_split_input/result/for_DNN/***_comparable.root  TODO
import numpy as np
import os
from DNN_tensorflow_class_py2 import EarlyStopping, DNN
from ROOT import TFile, TTree, TCut, TH1F
from root_numpy import fill_hist
from root_numpy import root2array, tree2array, array2root, array2tree
from root_numpy import testdata
from sklearn.model_selection import train_test_split

model = DNN(n_in=26, n_hiddens=[20], n_out=2) #TODO FIXME
#epochs = 1000
epochs = 3
earlyStop =  1#20       #TODO FIXME
batch_size = 200        #TODO FIXME
Date=20180913          #TODO FIXME
Layer_NUM= 1              #TODO FIXME
Node_on_Each_layer=20   #TODO FIXME
N_train = 340000         #TODO FIXME
#N_train = 2000000
Model_name = str(Date)+"_"+"TrainENum"+str(N_train)+"/"+"LayerNum_"+str(Layer_NUM)+"+"+"Node_"+str(Node_on_Each_layer)+"+"+"BatchSize_"+str(batch_size)
Make_dir = "mkdir -p "+ "tens_model_class/"+Model_name
os.system(Make_dir)
model_name = Model_name +"/"+ "SSWW_tensor_TTTL-LL_comp"

data = TFile.Open('/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_DNN/TTTL_LL_250M_comparable.root')
#data = TFile.Open('/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_split_input/result/for_DNN/TTTL_LL_230M.root')
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

#X_train = ARRAY[0:N_train]
#Y_train = TARGET[0:N_train]
#X_validation = ARRAY[(N_train):]
#Y_validation = TARGET[(N_train):]
#N_validation = ARRAY.shape[0]-(N_train)
X_train = ARRAY[:]
Y_train = TARGET[:]
N_validation = ARRAY.shape[0]-(N_train)

X_train, X_test, Y_train, Y_test = train_test_split(X_train, Y_train, train_size=N_train) 
X_train, X_validation, Y_train, Y_validation = train_test_split(X_train, Y_train, test_size=N_validation)
print(X_train.shape,"x_train");print(X_validation.shape,"x_validation");print(Y_train.shape);print(Y_validation.shape)


make_ROOT_DIR = "mkdir -p tens_model_class/"+Model_name+"/TEST_TRAIN_ROOT/"
os.system(make_ROOT_DIR)
## <SAVE TEST_ROOT>
Test_List = []
Test_List_LL = []; Test_List_TTTL = []
for i in range(len(X_test)):
#    if i>1: break
    TEST = np.append(X_test[i],Y_test[i])
    TEST = tuple(TEST)
    Test_List.append(TEST)
    if(Y_test[i][0] == 1.0):
        Test_List_LL.append(TEST)
    elif(Y_test[i][0] == 0.0):
        Test_List_TTTL.append(TEST)
#print(Test_List)
TEST_nplist = np.array(Test_List,dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep1phi',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),('lep2phi',np.float32),
('jet1pt',np.float32),('jet1eta',np.float32),('jet1phi',np.float32),('jet1M',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),('jet2phi',np.float32),('jet2M',np.float32),
('MET',np.float32),('lep1PID',np.float32),('lep2PID',np.float32),('Mjj',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),('zeppen_lep1',np.float32),('zeppen_lep2',np.float32),
('METphi',np.float32),('detajj',np.float32),('Mll',np.float32),('RpT',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)] )
#print(TEST_nplist)
TEST_nplist_LL = np.array(Test_List_LL,dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep1phi',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),('lep2phi',np.float32),
('jet1pt',np.float32),('jet1eta',np.float32),('jet1phi',np.float32),('jet1M',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),('jet2phi',np.float32),('jet2M',np.float32),
('MET',np.float32),('lep1PID',np.float32),('lep2PID',np.float32),('Mjj',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),('zeppen_lep1',np.float32),('zeppen_lep2',np.float32),
('METphi',np.float32),('detajj',np.float32),('Mll',np.float32),('RpT',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)])

TEST_nplist_TTTL = np.array(Test_List_TTTL,dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep1phi',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),('lep2phi',np.float32),
('jet1pt',np.float32),('jet1eta',np.float32),('jet1phi',np.float32),('jet1M',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),('jet2phi',np.float32),('jet2M',np.float32),
('MET',np.float32),('lep1PID',np.float32),('lep2PID',np.float32),('Mjj',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),('zeppen_lep1',np.float32),('zeppen_lep2',np.float32),
('METphi',np.float32),('detajj',np.float32),('Mll',np.float32),('RpT',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)])

ROOT_filename = "tens_model_class/"+Model_name+"/TEST_TRAIN_ROOT/"+"TEST_ROOT.root"
ROOT_filename_LL = "tens_model_class/"+Model_name+"/TEST_TRAIN_ROOT/"+"TEST_ROOT_LL.root"
ROOT_filename_TTTL = "tens_model_class/"+Model_name+"/TEST_TRAIN_ROOT/"+"TEST_ROOT_TTTL.root"
Test_ROOT = TFile(ROOT_filename,"RECREATE")
tree_test = array2tree(TEST_nplist)
tree_test.Write()
Test_ROOT.Close()

Test_ROOT_LL = TFile(ROOT_filename_LL,"RECREATE")
tree_test_LL = array2tree(TEST_nplist_LL)
tree_test_LL.Write()
Test_ROOT_LL.Close()

Test_ROOT_TTTL = TFile(ROOT_filename_TTTL,"RECREATE")
tree_test_TTTL = array2tree(TEST_nplist_TTTL)
tree_test_TTTL.Write()
Test_ROOT_TTTL.Close()
del Test_List
del TEST_nplist
## </SAVE TEST_ROOT>

## <SAVE TRAIN ROOT>
Train_List = []
Train_List_LL = []; Train_List_TTTL = []
for i in range(len(X_train)):
    TRAIN = np.append(X_train[i],Y_train[i])
    TRAIN = tuple(TRAIN)
    Train_List.append(TRAIN)
    if(Y_train[i][0] == 1.0):
        Train_List_LL.append(TRAIN)
    elif(Y_train[i][0] == 0.0):
        Train_List_TTTL.append(TRAIN)
TRAIN_nplist = np.array(Train_List,dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep1phi',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),('lep2phi',np.float32),
('jet1pt',np.float32),('jet1eta',np.float32),('jet1phi',np.float32),('jet1M',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),('jet2phi',np.float32),('jet2M',np.float32),
('MET',np.float32),('lep1PID',np.float32),('lep2PID',np.float32),('Mjj',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),('zeppen_lep1',np.float32),('zeppen_lep2',np.float32),
('METphi',np.float32),('detajj',np.float32),('Mll',np.float32),('RpT',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)])

TRAIN_nplist_LL = np.array(Train_List_LL,dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep1phi',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),('lep2phi',np.float32),
('jet1pt',np.float32),('jet1eta',np.float32),('jet1phi',np.float32),('jet1M',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),('jet2phi',np.float32),('jet2M',np.float32),
('MET',np.float32),('lep1PID',np.float32),('lep2PID',np.float32),('Mjj',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),('zeppen_lep1',np.float32),('zeppen_lep2',np.float32),
('METphi',np.float32),('detajj',np.float32),('Mll',np.float32),('RpT',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)])

TRAIN_nplist_TTTL = np.array(Train_List_TTTL,dtype=[('lep1pt',np.float32),('lep1eta',np.float32),('lep1phi',np.float32),('lep2pt',np.float32),('lep2eta',np.float32),('lep2phi',np.float32),
('jet1pt',np.float32),('jet1eta',np.float32),('jet1phi',np.float32),('jet1M',np.float32),('jet2pt',np.float32),('jet2eta',np.float32),('jet2phi',np.float32),('jet2M',np.float32),
('MET',np.float32),('lep1PID',np.float32),('lep2PID',np.float32),('Mjj',np.float32),('dr_ll_jj',np.float32),('dphijj',np.float32),('zeppen_lep1',np.float32),('zeppen_lep2',np.float32),
('METphi',np.float32),('detajj',np.float32),('Mll',np.float32),('RpT',np.float32), ('LL_Helicity',np.float32), ('TTTL_Helicity',np.float32)])

ROOT_filename = "tens_model_class/"+Model_name+"/TEST_TRAIN_ROOT/"+"TRAIN_ROOT.root"
ROOT_filename_LL = "tens_model_class/"+Model_name+"/TEST_TRAIN_ROOT/"+"TRAIN_ROOT_LL.root"
ROOT_filename_TTTL = "tens_model_class/"+Model_name+"/TEST_TRAIN_ROOT/"+"TRAIN_ROOT_TTTL.root"
Train_ROOT = TFile(ROOT_filename,"RECREATE")
tree_train = array2tree(TRAIN_nplist)
tree_train.Write()
Train_ROOT.Close()

Train_ROOT_LL = TFile(ROOT_filename_LL,"RECREATE")
tree_train_LL = array2tree(TRAIN_nplist_LL)
tree_train_LL.Write()
Train_ROOT_LL.Close()

Train_ROOT_TTTL = TFile(ROOT_filename_TTTL,"RECREATE")
tree_train_TTTL = array2tree(TRAIN_nplist_TTTL)
tree_train_TTTL.Write()
Train_ROOT_TTTL.Close()

del Train_List
del TRAIN_nplist
## </SAVE TRAIN ROOT>



model.fit_classify(X_train, Y_train, X_validation, Y_validation, epochs=epochs, batch_size=batch_size, p_keep=0.5, earlyStop=earlyStop, model_name = model_name)
accuracy = model.evaluate(X_test, Y_test)
print('accuracy:', accuracy)
plot_name = "tens_model_class/"+Model_name+"/"+"SSWW_classification_TTTL-LL_comp.pdf"
model.Plot_acc_loss(plot_name = plot_name)




