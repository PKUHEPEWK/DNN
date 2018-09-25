# Author : JUNHO LEE
from ROOT import TFile, TTree
import numpy
import os 

def Raw_text_to_Tree_root(filename, outputpath = "."):
    
    f = open(filename,"r")

    if(filename[0]=="/"):
        filename = filename
    else:
        filename = os.getcwd() + "/" + filename   # get the path included filename
    loca=len(filename)
    for i in range (1,len(filename)+1):       # find the "/" location
        if(filename[-i] == "/"):
            loca = i-1
            break

    FILENAME = filename.replace(filename[:-loca],"")   # this is the shorten filename, excluded path 
    Filename = FILENAME.replace(".txt","")
    filename_NoTxt = filename.replace(filename[len(filename)-loca:len(filename)],"")
#    print(FILENAME); print(Filename); print(filename);print(filename_NoTxt)

    outName = Filename + "_tree.root"

    if(outputpath == ''):
        outfileName = filename_NoTxt + "/" + Filename
        outfileName = outfileName.replace("//","/")
#        print("!@#!@!@#!@ ",outfileName)
    elif(outputpath[0] == "/"):
        outfileName = outputpath + "/" + Filename
        outfileName = outfileName.replace("//","/")
#        print("!@#!@!@#!@ ",outfileName)
    elif(outputpath[0] == "~"):
        outfileName = outputpath.replace("~",os.environ['HOME']) + "/" + Filename
        outfileName = outfileName.replace("//","/")
#        print("!@#!@!@#!@ ",outfileName)
    else:
        outfileName = os.getcwd() + "/" + outputpath+ "/" + Filename
        outfileName = outfileName.replace("//","/")
#        print("!@#!@!@#!@ ",outfileName)

#    isExists=os.path.exists(outfileName)
#    if not isExists:
#        os.makedirs(outfileName)
#    else:
#        print("*****************************************************")
#        print("There is already a file with same name, please check!")
#        print("*****************************************************")

#    SAVE_DIR = outfileName

    outfileName = outfileName + "_tree.root"
#    print(outfileName)
    outFile = TFile(outfileName,"RECREATE")
    #tree = TTree(Filename,Filename)
    tree =  TTree("tree","tree")

    Firstline = f.readline()

    LL = []
    if(Firstline[-1] == "\n"):
        Firstline = Firstline.replace("\n","")
        LL = Firstline.split()

    List_branch = []
    for branch in LL:
        branch = numpy.zeros(1, dtype=float)
        List_branch.append(branch)

    for i in range(len(List_branch)):
        tree.Branch(LL[i],List_branch[i],LL[i]+"/D")

    for line in f:
        LL1 = []
        LL1 = line.split()
        for j in range(len(LL1)):
            List_branch[j][0] = float(LL1[j])
        tree.Fill()

    tree.Write()
    outFile.Close()
    f.close()
#    print("!@#!@@!#$@$@#",outfileName)
    return outfileName


def main():
#    Infile = "/Users/leejunho/Desktop/git/python3Env/group_study/fruit_team/ROOT/Project/tranfer_test/data/concrete.txt"
#    Infile = "/Users/leejunho/Desktop/git/python3Env/group_study/project_pre/data_txt/BINANCE_DATA.txt"

    Infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180913_TrainENum240000/LayerNum_1+Node_20+BatchSize_200/TEST_TRAIN_ROOT/TRAIN_ROOT_LL.txt"
#    Infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180913_TrainENum240000/LayerNum_1+Node_20+BatchSize_200/TEST_TRAIN_ROOT/TRAIN_ROOT_TTTL.txt"
#    Infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180913_TrainENum240000/LayerNum_1+Node_20+BatchSize_200/TEST_TRAIN_ROOT/TEST_ROOT_LL.txt"
#    Infile = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180913_TrainENum240000/LayerNum_1+Node_20+BatchSize_200/TEST_TRAIN_ROOT/TEST_ROOT_TTTL.txt"

    Raw_text_to_Tree_root(Infile,".")


if __name__ == "__main__":
    main()


 
