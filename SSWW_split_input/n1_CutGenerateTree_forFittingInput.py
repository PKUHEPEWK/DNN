from ROOT import TFile, TH1D, TH1F, TCanvas, TColor, TGaxis, TPad, gBenchmark, TTree
import os, sys
import numpy
import collections

sys.path.append("..")
from c0_READ_PATH_FILE_ROOT import read_file_name_root

class SplitROOT(object):
    def __init__(self,infile):
        self._infile = infile
    
    
    def get_branch_list_all(self):
        PATH_included_root = read_file_name_root(self._infile)[2]
        SetBranchNameList = list()               # make a set of branchNameList
        f = TFile(PATH_included_root,"READ")
        dirlist = f.GetListOfKeys()
        ITER = dirlist.MakeIterator()
        key = ITER.Next()

        while key:
            tree = key.ReadObj()
            branchlist = tree.GetListOfBranches()
            if(branchlist.IsEmpty()):
                continue

            ITER_b = branchlist.MakeIterator()
            key_b = ITER_b.Next()
            while key_b:
                #SetBranchNameList.add(key_b.GetName())
                SetBranchNameList.append(key_b.GetName())
                key_b = ITER_b.Next()
            key = ITER.Next()
        f.Close()
        return SetBranchNameList

    def get_branch_list_each_tree(self):
        PATH_included_root = read_file_name_root(self._infile)[2]
        DicTreeBranchNameList = {}

        f = TFile(PATH_included_root,"READ")
        dirlist = f.GetListOfKeys()
        ITER = dirlist.MakeIterator()
        key = ITER.Next()

        while key:
            BranchNameList = []
            tree = key.ReadObj()
            branchlist = tree.GetListOfBranches()
            if(branchlist.IsEmpty()):
                continue

            ITER_b = branchlist.MakeIterator()
            key_b = ITER_b.Next()
            while key_b:
                BranchNameList.append(key_b.GetName())
                key_b = ITER_b.Next()
            DicTreeBranchNameList[tree.GetName()] = BranchNameList
            key = ITER.Next()
        f.Close()
        return DicTreeBranchNameList


    def SplitTree(self):
        FileNameList = read_file_name_root(self._infile)
        BranchListAll = self.get_branch_list_all()
        BranchListEachTree = self.get_branch_list_each_tree()

        DicNumpyArray_branch = {}
        for numpyarray in BranchListAll:
            a = numpy.array([0],'d')
            DicNumpyArray_branch[numpyarray] = a
        DicNumpyArray_branch = collections.OrderedDict(sorted(DicNumpyArray_branch.items())) 
        print(DicNumpyArray_branch)

        DicNumpyArray_branch_w = {}
        for numpyarray_w in BranchListAll:
            a_w = numpy.array([0],'d')
            DicNumpyArray_branch_w[numpyarray_w] = a_w
        DicNumpyArray_branch_w = collections.OrderedDict(sorted(DicNumpyArray_branch_w.items()))
        print(DicNumpyArray_branch_w)

        gBenchmark.Start("Regerating tree root")
        f = TFile(FileNameList[2],"READ")
        dirlist = f.GetListOfKeys();
        ITER = dirlist.MakeIterator()
        key = ITER.Next()

        outfileName = os.getcwd() + "/" + FileNameList[0] + "_cut.root"        
        print("CREATING... :",outfileName)        
        outfile = TFile(outfileName,"RECREATE")

        ijk = 0
        break_flag = 0
        while key:
            if(break_flag==1): break
            break_flag += 1
            tree = key.ReadObj()
            tree_f = TTree(tree.GetName()+"_f",tree.GetName()+"_f")
            ENTRY = tree.GetEntries();  #print(ENTRY)
            for i in range(len(DicNumpyArray_branch)):
                if(list(DicNumpyArray_branch.keys())[i] in BranchListEachTree[tree.GetName()]):
                    tree.SetBranchAddress(list(DicNumpyArray_branch.keys())[i],list(DicNumpyArray_branch.values())[i])
                    tree_f.Branch(list(DicNumpyArray_branch_w.keys())[i],list(DicNumpyArray_branch_w.values())[i],list(DicNumpyArray_branch_w.keys())[i]+"/D")
                else:
                    continue

            print("for tree", tree.GetName())
            for j in range(ENTRY):
                tree.GetEntry(j)
                if(j%5000 == 0):
                    print("now looping", j, "th Events, total of ", ENTRY, "events")
                for k in range(len(DicNumpyArray_branch)):
                    if(list(DicNumpyArray_branch.keys())[k] in BranchListEachTree[tree.GetName()]):    ### FIXED MAYBE not correct....
                        pass
                    else:
                        continue          
                    list(DicNumpyArray_branch_w.values())[k][0] = list(DicNumpyArray_branch.values())[k][0]
                if(True 
                   & (list(DicNumpyArray_branch.values())[0][0] == 1)  # LL  #FIXME
                   #& (list(DicNumpyArray_branch.values())[0][0] == 0)  # TT and TL  #FIXME
                  ): 
                    ijk = ijk + 1
                    tree_f.Fill()
                else:
                    continue
            print(" Event left after filtering : ", ijk, "!!!!!!!!!")
            print("\n")
            ijk=0
            if(tree_f.GetEntries() ==0):
                print("!!!!!!! ", tree_f.GetName()," is Empty, would not be written !!!!!")
            else:
                tree_f.Write()

            key = ITER.Next()


        print("")
        print("////////////////////////////////////////////////")
        print("outputfile : ")
        print(outfileName)
        print("////////////////////////////////////////////////")
        print("")

        outfile.Close()
        f.Close()
        print("*********************************************************************************************")
        gBenchmark.Show("Regerating tree root")
        print("*********************************************************************************************")

        return outfileName



def main():
    infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_input/SS_120M.root" 
    test_split = SplitROOT(infile) 
    branchList = test_split.get_branch_list_all()
    print(branchList)
    branchDic = test_split.get_branch_list_each_tree() 
    print(branchDic)
    test_split.SplitTree()

if __name__ == "__main__":
    main()

