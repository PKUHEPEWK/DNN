#include "iostream"
void n3_Template_fit_perform()
{
    
    TFile *fileSignal = new TFile("n1_2p5m_result_8bins/PseudoDATA_3ab_hist.root","READ"); // mini stats
    TFile *fileMC0 = new TFile("n1_2p5m_result_8bins/SS_2p5M_cut_LL_hist.root","READ");
    TFile *fileMC1 = new TFile("n1_2p5m_result_8bins/SS_2p5M_cut_TTTL_hist.root","READ"); //TODO : add files if there are
    

    /*
    TFile *fileSignal = new TFile("/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180924_TrainENum240000/LayerNum_1+Node_20+BatchSize_100/TEST_TRAIN_ROOT/Ntuple_PseudoData_DECAY_1M_MERGED_tree_hist10.root","READ");
    TFile *fileMC0 = new TFile("/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180924_TrainENum240000/LayerNum_1+Node_20+BatchSize_100/TEST_TRAIN_ROOT/TRAIN_ROOT_LL_tree_hist10.root","READ");
    TFile *fileMC1 = new TFile("/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/High_20180924_TrainENum240000/LayerNum_1+Node_20+BatchSize_100/TEST_TRAIN_ROOT/TRAIN_ROOT_TTTL_tree_hist10.root","READ");
    */

    /*
    TFile *fileSignal = new TFile("/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum1000000/LayerNum_7+Node_150+BatchSize_10/TEST_TRAIN_ROOT/PseudoDATA_3ab_hist.root","READ");
    TFile *fileMC0 = new TFile("/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum1000000/LayerNum_7+Node_150+BatchSize_10/TEST_TRAIN_ROOT/Estimated_LL_hist.root","READ");
    TFile *fileMC1 = new TFile("/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum1000000/LayerNum_7+Node_150+BatchSize_10/TEST_TRAIN_ROOT/Estimated_TTTL_hist.root","READ");
    */

    //TString HistoName = "LL"; // TODO
    //TString HistoName = "lep1pt"; // TODO
    TString HistoName = "dphijj"; // TODO
    //TString HistoName = "jet1pt"; // TODO
    //TString HistoName = "MET"; // TODO
    //TString HistoName = "Mjj"; // TODO
    //TString HistoName = "detajj"; // TODO
    //TString HistoName = "dr_ll_jj"; // TODO
    //TString HistoName = "jet1eta"; // TODO

    const int MCFracs = 2;   //////TODO : the MC fraction numbers
    //const int Rotations = 2;
    double br[MCFracs],brer[MCFracs];

    gStyle->SetOptStat(0);
 
    TH1D *data;
    TH1D *mc0;
    TH1D *mc1;

    TObjArray *mc = new TObjArray(2); 
    //TFile *fileSignal = new TFile("PseudoDATA_for_n2/PseudoDATA_DECAY1M.root","READ");
    ////TFile *fileSignal = new TFile("PseudoDATA_for_n2/PseudoDATA_DECAY.root","READ"); // mini stats
    //TFile *fileMC0 = new TFile("Template_for_n2/LL_120M.root","READ");
    //TFile *fileMC1 = new TFile("Template_for_n2/TTTL_120M.root","READ"); //TODO : add files if there are

    data = (TH1D*)fileSignal->Get(HistoName); data->SetLineWidth(2); data->SetLineColor(kBlack); //TODO : histo name
    mc0  = (TH1D*)fileMC0->Get(HistoName); mc0->SetLineColor(kRed); mc0->SetFillStyle(3000); mc0->SetFillColor(kRed); //TODO : histo name
    mc1  = (TH1D*)fileMC1->Get(HistoName); mc1->SetLineColor(kBlue); mc1->SetFillStyle(3000); mc1->SetFillColor(kBlue); //TODO : histo name, add files if there are

    mc->Add(mc0);
    mc->Add(mc1); //TODO : add files if there are

    float scale_to = data->GetEntries(); //cout<<scale_to<<endl;
    float Scale_mc0 = 1.0/mc0->GetEntries()*scale_to;
    float Scale_mc1 = 1.0/mc1->GetEntries()*scale_to; //TODO : add files if there are
    cout<<scale_to<<endl<<Scale_mc0<<endl<<Scale_mc1<<endl;

    mc0->Scale(Scale_mc0);
    mc1->Scale(Scale_mc1);

    /*
    // Set bin error to zero
    for(int i=0; i<20; i++)
    {
        int j = i+1;
        mc0->SetBinError(j,0);
        mc1->SetBinError(j,0);
    }
    //mc1->Draw("hist e");
    */
    

    TFractionFitter* fit = new TFractionFitter(data, mc);
    fit->Constrain(0,0.0,1.0);
    //fit->Constrain(0,0.0,0.2); // FIXME
    fit->Constrain(1,0.0,1.0);  // TODO : constrains on MC fractions
    //fit->SetRangeX(3,6);  // TODO : Perform fitting on given bin range
    //fit->SetRangeX(5,15);

    Int_t status = fit->Fit();
    std::cout << "fit status: " << status << std::endl;
    if (status == 0) 
    {                       // check on fit status
        TCanvas *cv = new TCanvas("cv","cv",1200,900);
        for (int iz=0; iz<MCFracs; iz++){
            fit -> GetResult(iz,br[iz],brer[iz]);
        }
        TPad *p1 = new TPad();
        p1->SetFillStyle(4050);
        p1->Draw();

        TH1F* result = (TH1F*) fit->GetPlot(); result->SetLineColor(kGreen); result->SetLineWidth(3);
        result->GetXaxis()->SetTitle(HistoName);
        result->Draw("e hist");
        data->Draw("ep same");
        mc0->Scale(br[0]); /*mc0->SetFillStyle(3050);*/ mc0->Draw("e hist same");
        mc1->Scale(br[1]); /*mc1->SetFillStyle(4050);*/ mc1->Draw("e hist same"); // TODO add files if there are
        TLegend *leg = new TLegend(0.8,0.8,1.0,1.0);
        leg->AddEntry(data,"PseudoDATA");
        leg->AddEntry(result,"Fitted");
        leg->AddEntry(mc0,"LL");
        leg->AddEntry(mc1,"TT&TL");
        leg->Draw();
        TPaveText *pt = new TPaveText(.8,.6,1.0,0.8,"NDC");
        double fmc0 = (int)(br[0]*1000000) / 10000.0; double fmc0_e = (int)(brer[0]*10000000) / 100000.0; 
        double fmc1 = (int)(br[1]*1000000) / 10000.0; double fmc1_e = (int)(brer[1]*10000000) / 100000.0; //TODO. add files if there are
        string Fmc0 = to_string(fmc0); string E_Fmc0 = to_string(fmc0_e);
        string Fmc1 = to_string(fmc1); string E_Fmc1 = to_string(fmc1_e); //TODO. add files if there are
        string w_frac0 = "LL : " +Fmc0 + "% +-" + E_Fmc0; 
        string w_frac1 = "TT&TL : " +Fmc1 + "% +-" + E_Fmc1;
        pt->AddText(w_frac0.data());
        pt->AddText(w_frac1.data());
        pt->Draw();
        TString Name1 = "Fitting_" + HistoName + ".pdf";
        cv->SaveAs(Name1);

        TCanvas *cv_log = new TCanvas("cv","cv",1200,900);
        TPad *p2 = new TPad();
        p2->SetFillStyle(4050);
        p2->Draw();
        cv_log->SetLogy(); 
        result->Draw("e hist");
        data->Draw("ep same");
        mc0->Scale(br[0]); /*mc0->SetFillStyle(3050);*/ mc0->Draw("e hist same");
        mc1->Scale(br[1]); /*mc1->SetFillStyle(4050);*/ mc1->Draw("e hist same"); // TODO add files if there are
        leg->Draw();
        pt->Draw();
        TString Name2 = "Fitting_" + HistoName + "_log.pdf";
        cv_log->SaveAs(Name2);
        //cv_log->Delete();

    }
    cout<<endl;
    for (int i=0; i<MCFracs; i++)
    {
        cout<<"The fraction of "<<i<<"th : "<<br[i]<<", error : "<<brer[i]<<endl;
    }
    cout<<"Chi-square Value : "<<fit->GetChisquare()<<endl;
    cout<<"Degree of Freedom : "<<fit->GetNDF()<<endl;
    cout<<"Fit probability : "<<fit->GetProb()<<endl;

    fileSignal->Close();  
    fileMC0->Close();
    fileMC1->Close(); 

    /*
    TH1D* mcp0 = (TH1D*)fit->GetMCPrediction(0); mcp0->Scale(Scale_mc0); mcp0->Scale(7.06528e-02);
    TH1D* mcp1 = (TH1D*)fit->GetMCPrediction(1); mcp1->Scale(Scale_mc1); mcp1->Scale(9.29408e-01);
    TH1D *ADD_ALL_MC = new TH1D(); ADD_ALL_MC->Add(mcp0); //ADD_ALL_MC->Add(mcp1);//ADD_ALL_MC->Add(mcp2);
    TH1D *ADD_TL_TT = new TH1D(); ADD_TL_TT->Add(mcp1); //ADD_TL_TT->Add(mcp2);
    ADD_ALL_MC->SetFillColor(kRed); ADD_ALL_MC->Draw("hsame P0");
    //ADD_TL_TT->SetFillColor(kBlue) ; ADD_TL_TT->Draw("hsame");  
    
    TLegend *leg = new TLegend(0.6,0.6,0.9,0.9);
    leg->AddEntry(data,"Pseudo DATA");
    leg->AddEntry(ADD_ALL_MC,"LL");// 9.99966e-01");
    leg->AddEntry(ADD_TL_TT,"TT&TL");// 4.08737e-07");
    leg->Draw();
    data->Draw("same Ep");
    */
 

//    mcp0->Draw("hsame");
//    mcp1->Draw("hsame");
//    mcp2->Draw("hsame");

/*
    TH1D *ADD_ALL_MC = new TH1D(); ADD_ALL_MC->SetLineColor(kBlack);
    ADD_ALL_MC->Add(mc0);
    ADD_ALL_MC->Add(mc1);
    ADD_ALL_MC->Add(mc2);
    float all_inte = 1.0/ADD_ALL_MC->Integral();
    cout<<all_inte<<endl;
    ADD_ALL_MC->Scale(all_inte);
    //ADD_ALL_MC->Draw("hist");

    //mc0->Scale(Scale_mc0);
    mc0->Scale(8.98453e-01);
    //mc1->Scale(Scale_mc1);
    mc1->Scale(1.72052e-09);
    //mc2->Scale(Scale_mc2);
    mc2->Scale(1.01540e-01);
    mc0->Draw("hsame");
    mc1->Draw("hsame");
    mc2->Draw("hsame");
//    ADD_ALL_MC->Draw("hsame");

    TLegend *leg = new TLegend(0.6,0.6,0.9,0.9);
    leg->AddEntry(mc0,"LL");
    leg->AddEntry(mc1,"TT");
    leg->AddEntry(mc2,"TL");
    leg->Draw();
//    leg->AddEntry(ADD_ALL_MC);
*/

//    fileSignal->Close();  Error when fitting
//    fileMC0->Close();
//    fileMC1->Close();
//    fileMC2->Close();

}
