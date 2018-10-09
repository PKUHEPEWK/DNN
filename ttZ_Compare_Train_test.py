## After Having all txt files, start this process
import sys, os
from HAND_ttZ_Raw_text_to_Tree_root import Raw_text_to_Tree_root
sys.path.append("SSWW_fitting/")
from n1_Template_fit_hist_production_n_compare import HistProduction, HistoCompare_ttZ


#FileDir = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20181003_TrainENum1250000/LayerNum_5+Node_200+BatchSize_100" #FIXME 
FileDir = "/Users/leejunho/Desktop/test_regression"
FileDir = FileDir + "/TEST_TRAIN_ROOT"

Test_TXT = "TEST_ROOTreg.txt"
Train_TXT = "TRAIN_ROOTreg.txt"
Raw_text_to_Tree_root(Test_TXT)
Raw_text_to_Tree_root(Train_TXT)

#Infile_list = ("TRAIN_ROOT_LL_tree.root","TEST_ROOT_LL_tree.root","TRAIN_ROOT_TTTL_tree.root","TEST_ROOT_TTTL_tree.root")
Infile_list = ("TEST_ROOTreg_tree.root","TRAIN_ROOTreg_tree.root") #FIXME
#histoName = ["Real","Regressed"]
histoName = ["Regressed","Real"]
HistP = HistProduction(Infile_list)
Hist_files = HistP.MakeHistoROOT_ttZ(binNum=100,histoName=histoName)  # FIXME Turn this on if histo production required.
print(Hist_files)

HistoCom = HistoCompare_ttZ(Hist_files)
HistoCom.CompareHistoROOT_general()
mv_command = "mv *.pdf " + FileDir
os.system(mv_command)
mv_command = "mv *tree_hist.root " + FileDir
os.system(mv_command)

mv_command = "mv TEST_ROOTreg.txt " + FileDir
os.system(mv_command)
mv_command = "mv TRAIN_ROOTreg.txt " + FileDir
os.system(mv_command)

mv_command = "mv TRAIN_ROOTreg_tree.root " + FileDir
os.system(mv_command)

mv_command = "mv TEST_ROOTreg_tree.root " + FileDir
os.system(mv_command)


