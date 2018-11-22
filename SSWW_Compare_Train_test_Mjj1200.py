## After Having all txt files, start this process
import sys, os
from HAND_SSWW_Raw_text_to_Tree_root_high import Raw_text_to_Tree_root
sys.path.append("SSWW_fitting/")
from n1_Template_fit_hist_production_n_compare import HistProduction, HistoCompare


#FileDir = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181026_TrainENum1500000/LayerNum_7+Node_300+BatchSize_10"
#FileDir = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum700000/LayerNum_1+Node_150+BatchSize_10"
#FileDir = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum700000/LayerNum_5+Node_150+BatchSize_10"
FileDir = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/Raw_20181115_TrainENum2600000/LayerNum_10+Node_150+BatchSize_10"
FileDir = FileDir + "/TEST_TRAIN_ROOT_Mjj1200"
os.system("mkdir -p "+FileDir)

LL_Mjj = "SS_4p0M_cut_LL_Mjj1200.txt"
TTTL_Mjj = "SS_4p0M_cut_TTTL_Mjj1200.txt"

Raw_text_to_Tree_root(LL_Mjj)
Raw_text_to_Tree_root(TTTL_Mjj)

Infile_list = ("SS_4p0M_cut_TTTL_Mjj1200_tree.root","SS_4p0M_cut_LL_Mjj1200_tree.root")
#Infile_list = ("TRAIN_ROOT_LL_tree.root","TEST_ROOT_LL_tree.root","TRAIN_ROOT_TTTL_tree.root","TEST_ROOT_TTTL_tree.root")
#Infile_list = ("TRAIN_ROOT_TTTL_tree.root","TEST_ROOT_TTTL_tree.root","TRAIN_ROOT_LL_tree.root","TEST_ROOT_LL_tree.root","PseudoDATA_3ab_MERGED_tree.root") #FIXME
histoName = ["LL","TTTL"]
HistP = HistProduction(Infile_list)
Hist_files = HistP.MakeHistoROOT(binNum=200,histoName=histoName)  # FIXME Turn this on if histo production required.
print(Hist_files)

HistoCom = HistoCompare(Hist_files)
HistoCom.CompareHistoROOT_general()
mv_command = "mv *.pdf " + FileDir
os.system(mv_command)
mv_command = "mv *tree_hist.root " + FileDir
os.system(mv_command)

mv_command = "mv *.txt " + FileDir
os.system(mv_command)
mv_command = "mv *_tree.root " + FileDir
os.system(mv_command)

mv_command = "mv TEST_ROOT_LL_tree.root " + FileDir
os.system(mv_command)
mv_command = "mv " + LL_Test_TXT + " " + FileDir
os.system(mv_command)

mv_command = "mv TRAIN_ROOT_LL_tree.root " + FileDir
os.system(mv_command)
mv_command = "mv " + LL_Train_TXT + " " + FileDir
os.system(mv_command)

mv_command = "mv TEST_ROOT_TTTL_tree.root " + FileDir
os.system(mv_command)
mv_command = "mv " + TTTL_Test_TXT + " " + FileDir
os.system(mv_command)

mv_command = "mv TRAIN_ROOT_TTTL_tree.root " + FileDir
os.system(mv_command)
mv_command = "mv " + TTTL_Train_TXT + " " + FileDir
os.system(mv_command)

