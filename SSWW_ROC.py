from ROOT import *
import sys, os, math
import numpy as np
from array import array

def ROC_List_Maker(dirname='./', verbose=0):
    LL_filename = dirname+"/TEST_ROOT_LL_tree_hist.root"
    TTTL_filename = dirname +"/TEST_ROOT_TTTL_tree_hist.root" 

    LL_TFile = TFile(LL_filename,"READ") 
    TTTL_TFile = TFile(TTTL_filename,"READ")   

    LL_LL_Hist = LL_TFile.Get("LL")
    TTTL_LL_Hist = TTTL_TFile.Get("LL")

    if verbose==1:
        #LL_var_filename = dirname+"/TEST_ROOT_LL_hist.root"
        #TTTL_var_filename = dirname+"/TEST_ROOT_TTTL_hist.root"
        LL_var_filename = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/ROC_PureMC_input/SS_2p5M_cut_LL_hist.root"
        TTTL_var_filename = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/ROC_PureMC_input/SS_2p5M_cut_TTTL_hist.root"
        LL_var_TFile = TFile(LL_var_filename,"READ")
        TTTL_var_TFile = TFile(TTTL_var_filename,"READ")
        LL_lep1pt_Hist = LL_var_TFile.Get("lep1pt")
        TTTL_lep1pt_Hist = TTTL_var_TFile.Get("lep1pt")
        LL_dphijj_Hist = LL_var_TFile.Get("dphijj")
        TTTL_dphijj_Hist = TTTL_var_TFile.Get("dphijj")
        LL_detajj_Hist = LL_var_TFile.Get("detajj")
        TTTL_detajj_Hist = TTTL_var_TFile.Get("detajj")
        LL_Mjj_Hist = LL_var_TFile.Get("Mjj")
        TTTL_Mjj_Hist = TTTL_var_TFile.Get("Mjj")
        LL_jet1pt_Hist = LL_var_TFile.Get("jet1pt")
        TTTL_jet1pt_Hist = TTTL_var_TFile.Get("jet1pt")

    DNN_list = list()
    ROC_list = list()
    TotalBinNum = LL_LL_Hist.GetSize()-2
    if(TotalBinNum!= TTTL_LL_Hist.GetSize()-2):
        print("LL and TTTL histo bin number is not identical, ERROR!")
        return

    LL_ETotal=0; TTTL_ETotal=0;
    for i in range(TotalBinNum):
        LL_ETotal += LL_LL_Hist.GetBinContent(i+1)
        TTTL_ETotal += TTTL_LL_Hist.GetBinContent(i+1)
    print("Total Entry for True LL :",LL_ETotal)
    print("Total Entry for True TTTL :",TTTL_ETotal)
   
    LL_temp=0; TTTL_temp=0 
    for i in range(TotalBinNum):    
        temp_list = []
        LL_temp += LL_LL_Hist.GetBinContent(i+1)
        TTTL_temp += TTTL_LL_Hist.GetBinContent(i+1)
        TPR = (LL_ETotal-LL_temp)/LL_ETotal
        FPR = (TTTL_ETotal-TTTL_temp)/TTTL_ETotal
        temp_list.append(TPR);
        temp_list.append(FPR);
        DNN_list.append(temp_list)
        del temp_list
    ROC_list.append(DNN_list)
    del DNN_list


    if verbose==1:
        lep1pt_list = []; dphijj_list = []; detajj_list = []; Mjj_list = []; jet1pt_list = [];
        TotalBinNum_var = TTTL_dphijj_Hist.GetSize()-2
        LL_var_ETotal=0; TTTL_var_ETotal=0;
        for i in range(TotalBinNum_var):
            LL_var_ETotal += LL_dphijj_Hist.GetBinContent(i+1)
            TTTL_var_ETotal += TTTL_dphijj_Hist.GetBinContent(i+1)

        LL_lep1pt_temp=0; TTTL_lep1pt_temp=0
        LL_dphijj_temp=0; TTTL_dphijj_temp=0
        LL_detajj_temp=0; TTTL_detajj_temp=0
        LL_Mjj_temp=0; TTTL_Mjj_temp=0
        LL_jet1pt_temp=0; TTTL_jet1pt_temp=0
        for i in range(TotalBinNum_var):
            temp_lep1pt_list = []; temp_dphijj_list = []; temp_detajj_list = []; temp_Mjj_list = []; temp_jet1pt_list=[];
            LL_lep1pt_temp += LL_lep1pt_Hist.GetBinContent(i+1)
            TTTL_lep1pt_temp += TTTL_lep1pt_Hist.GetBinContent(i+1)
            LL_dphijj_temp += LL_dphijj_Hist.GetBinContent(i+1)
            TTTL_dphijj_temp += TTTL_dphijj_Hist.GetBinContent(i+1)
            LL_detajj_temp += LL_detajj_Hist.GetBinContent(i+1)
            TTTL_detajj_temp += TTTL_detajj_Hist.GetBinContent(i+1)
            LL_Mjj_temp += LL_Mjj_Hist.GetBinContent(i+1)
            TTTL_Mjj_temp += TTTL_Mjj_Hist.GetBinContent(i+1)
            LL_jet1pt_temp += LL_jet1pt_Hist.GetBinContent(i+1)
            TTTL_jet1pt_temp += TTTL_jet1pt_Hist.GetBinContent(i+1)
            TPR_lep1pt = (LL_var_ETotal-LL_lep1pt_temp)/LL_var_ETotal 
            FPR_lep1pt = (TTTL_var_ETotal-TTTL_lep1pt_temp)/TTTL_var_ETotal
            TPR_dphijj = (LL_var_ETotal-LL_dphijj_temp)/LL_var_ETotal
            FPR_dphijj = (TTTL_var_ETotal-TTTL_dphijj_temp)/TTTL_var_ETotal
            TPR_detajj = (LL_var_ETotal-LL_detajj_temp)/LL_var_ETotal
            FPR_detajj = (TTTL_var_ETotal-TTTL_detajj_temp)/TTTL_var_ETotal
            TPR_Mjj = (LL_var_ETotal-LL_Mjj_temp)/LL_var_ETotal
            FPR_Mjj = (TTTL_var_ETotal-TTTL_Mjj_temp)/TTTL_var_ETotal
            TPR_jet1pt = (LL_var_ETotal-LL_jet1pt_temp)/LL_var_ETotal
            FPR_jet1pt = (TTTL_var_ETotal-TTTL_jet1pt_temp)/TTTL_var_ETotal
            temp_lep1pt_list.append(TPR_lep1pt); temp_lep1pt_list.append(FPR_lep1pt);
            temp_dphijj_list.append(TPR_dphijj); temp_dphijj_list.append(FPR_dphijj);
            temp_detajj_list.append(TPR_detajj); temp_detajj_list.append(FPR_detajj);
            temp_Mjj_list.append(TPR_Mjj); temp_Mjj_list.append(FPR_Mjj);
            temp_jet1pt_list.append(TPR_jet1pt); temp_jet1pt_list.append(FPR_jet1pt);
            lep1pt_list.append(temp_lep1pt_list)
            dphijj_list.append(temp_dphijj_list)
            detajj_list.append(temp_detajj_list)
            Mjj_list.append(temp_Mjj_list)
            jet1pt_list.append(temp_jet1pt_list)
            del temp_lep1pt_list; del temp_dphijj_list; del temp_detajj_list; del temp_Mjj_list; del temp_jet1pt_list;
        ROC_list.append(lep1pt_list);
        ROC_list.append(dphijj_list);
        ROC_list.append(detajj_list);
        ROC_list.append(Mjj_list);
        ROC_list.append(jet1pt_list); 
    #print(ROC_list)
    return ROC_list


def ROC_plotter(Roc_list,dirname,verbose=0):
    xarray_TPR = array( 'd' ); yarray_FPR=array( 'd' ); 
    for i,content in enumerate(Roc_list[0]):
        xarray_TPR.append(1-content[1])
        yarray_FPR.append(content[0])
    #print(xarray_TPR); print(yarray_FPR)

    c1 = TCanvas('c1', 'A Simple Graph Example', 200, 10, 700, 500);
    gr = TGraph( len(Roc_list[0]), xarray_TPR, yarray_FPR )
    gr.SetLineColor(kRed)
    gr.SetLineWidth( 4 )
    gr.SetMarkerColor(kRed)
    gr.SetMarkerStyle( 21 )
    gr.SetTitle('ROC')
    gr.GetXaxis().SetTitle( '1-FPR' )
    gr.GetYaxis().SetTitle( 'TPR' )
    gr.Draw( 'ACP' )
    #gr.Draw( 'ALP' )

    if verbose==1:
        xarray_lep1pt_TPR = array( 'd' ); yarray_lep1pt_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[1]):
            xarray_lep1pt_TPR.append(1-content[0])
            yarray_lep1pt_FPR.append(content[1])
        xarray_dphijj_TPR = array( 'd' ); yarray_dphijj_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[2]):
            xarray_dphijj_TPR.append(1-content[1])
            yarray_dphijj_FPR.append(content[0])
        xarray_detajj_TPR = array( 'd' ); yarray_detajj_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[3]):
            xarray_detajj_TPR.append(1-content[1])
            yarray_detajj_FPR.append(content[0])
        xarray_Mjj_TPR = array( 'd' ); yarray_Mjj_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[4]):
            xarray_Mjj_TPR.append(1-content[1])
            yarray_Mjj_FPR.append(content[0])
        xarray_jet1pt_TPR = array( 'd' ); yarray_jet1pt_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[5]):
            xarray_jet1pt_TPR.append(1-content[0])
            yarray_jet1pt_FPR.append(content[1])

        gr_lep1pt = TGraph( len(Roc_list[1]), xarray_lep1pt_TPR, yarray_lep1pt_FPR)
        gr_lep1pt.SetLineColor(kBlue); gr_lep1pt.SetLineWidth(4); gr_lep1pt.SetMarkerColor(kBlue); gr_lep1pt.SetMarkerStyle(21); gr_lep1pt.Draw("CP SAME")
        gr_dphijj = TGraph( len(Roc_list[2]), xarray_dphijj_TPR, yarray_dphijj_FPR)
        gr_dphijj.SetLineColor(kGreen); gr_dphijj.SetLineWidth(4); gr_dphijj.SetMarkerColor(kGreen); gr_dphijj.SetMarkerStyle(21); gr_dphijj.Draw("LP SAME")
        gr_detajj = TGraph( len(Roc_list[3]), xarray_detajj_TPR, yarray_detajj_FPR)
        gr_detajj.SetLineColor(kMagenta); gr_detajj.SetLineWidth(4); gr_detajj.SetMarkerColor(kMagenta); gr_detajj.SetMarkerStyle(21); gr_detajj.Draw("CP SAME")
        gr_Mjj = TGraph( len(Roc_list[4]), xarray_Mjj_TPR, yarray_Mjj_FPR)
        gr_Mjj.SetLineColor(41); gr_Mjj.SetLineWidth(4); gr_Mjj.SetMarkerColor(41); gr_Mjj.SetMarkerStyle(21); gr_Mjj.Draw("CP SAME")
        gr_jet1pt = TGraph( len(Roc_list[5]), xarray_jet1pt_TPR, yarray_jet1pt_FPR)
        gr_jet1pt.SetLineColor(kBlack); gr_jet1pt.SetLineWidth(4); gr_jet1pt.SetMarkerColor(kBlack); gr_jet1pt.SetMarkerStyle(21); gr_jet1pt.Draw("CP SAME")

    gr_cross = TGraph(2, array('d',[0,1]),array('d',[1,0]))   
    #gr_hori = TGraph(2, array('d',[0,1]),array('d',[1,1]))
    #gr_verti = TGraph(2, array('d',[1,0]),array('d',[1,1]))
    gr_cross.Draw("same"); #gr_hori.Draw("same"); gr_verti.Draw("same")



    legend = TLegend(0.8,0.8,1.0,1.0)
    legend.AddEntry(gr,"DNN","l")
    if verbose==1:
        legend.AddEntry(gr_lep1pt,"lep1pt","l")
        legend.AddEntry(gr_dphijj,"dphijj","l")
        legend.AddEntry(gr_detajj,"detajj","l")
        legend.AddEntry(gr_Mjj,"Mjj","l")
        legend.AddEntry(gr_jet1pt,"jet1pt","l")
    legend.Draw()

    c1.SaveAs("ROC_test.pdf")
    mv_cmd = "mv ROC_test.pdf " + dirname
    os.system(mv_cmd)


def main():
    dirname = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum1000000/LayerNum_7+Node_150+BatchSize_10/TEST_TRAIN_ROOT" #FIXME
    verbose = 1  #FIXME


    Roc_list = ROC_List_Maker(dirname=dirname,verbose=verbose)
    ROC_plotter(Roc_list=Roc_list,dirname=dirname,verbose=verbose)



if __name__=="__main__":
    main()
