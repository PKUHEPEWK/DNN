#include "iostream"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit ;

void n1_MjjDphijj_lowMjj()
{
    TFile *all = new TFile("TwoD_Histos_MjjDphijj.root","READ");
    Int_t bins = 30;  //FIXME TODO 

    // **********************************************************************//
    // Begin of "MjjDphijj_lowMjj"
    TH1D *data_MjjDphijj_lowMjj;
    TH1D *mc0_MjjDphijj_lowMjj;
    TH1D *mc1_MjjDphijj_lowMjj;
    data_MjjDphijj_lowMjj = (TH1D*)all->Get("MjjDphijj_lowMjj_Asimov");
    mc0_MjjDphijj_lowMjj = (TH1D*)all->Get("MjjDphijj_LL_lowMjj");
    mc1_MjjDphijj_lowMjj = (TH1D*)all->Get("MjjDphijj_TTTL_lowMjj");

    RooRealVar x_MjjDphijj_lowMjj("x_MjjDphijj_lowMjj","dphijj",-0.5,3.5);  // FIXME The range: for dphijj
    RooDataHist datahist_data_MjjDphijj_lowMjj("datahist_data_MjjDphijj_lowMjj","datahist_data_MjjDphijj_lowMjj",x_MjjDphijj_lowMjj, data_MjjDphijj_lowMjj);
    RooDataHist datahist_mc0_MjjDphijj_lowMjj("mc0_data_MjjDphijj_lowMjj","mc0_data_MjjDphijj_lowMjj",x_MjjDphijj_lowMjj, mc0_MjjDphijj_lowMjj);
    RooDataHist datahist_mc1_MjjDphijj_lowMjj("mc1_data_MjjDphijj_lowMjj","mc1_data_MjjDphijj_lowMjj",x_MjjDphijj_lowMjj, mc1_MjjDphijj_lowMjj);
    RooHistPdf pdf_mc0_MjjDphijj_lowMjj("pdf_mc0_MjjDphijj_lowMjj","pdf_mc0_MjjDphijj_lowMjj",x_MjjDphijj_lowMjj,datahist_mc0_MjjDphijj_lowMjj,2);
    RooHistPdf pdf_mc1_MjjDphijj_lowMjj("pdf_mc1_MjjDphijj_lowMjj","pdf_mc1_MjjDphijj_lowMjj",x_MjjDphijj_lowMjj,datahist_mc1_MjjDphijj_lowMjj,2);
    RooRealVar fmc0_MjjDphijj_lowMjj("fmc0_MjjDphijj_lowMjj","mc0 fraction",0.,1.);
    RooAddPdf model_MjjDphijj_lowMjj("model_MjjDphijj_lowMjj","model_MjjDphijj_lowMjj",RooArgList(pdf_mc0_MjjDphijj_lowMjj,pdf_mc1_MjjDphijj_lowMjj),RooArgList(fmc0_MjjDphijj_lowMjj));
    RooPlot* frame_MjjDphijj_lowMjj = x_MjjDphijj_lowMjj.frame(Title("MjjDphijj_lowMjj"),Bins(bins));  //FIXME Title 
    model_MjjDphijj_lowMjj.plotOn(frame_MjjDphijj_lowMjj);
    RooArgSet mc0_component_MjjDphijj_lowMjj(pdf_mc0_MjjDphijj_lowMjj);
    RooArgSet mc1_component_MjjDphijj_lowMjj(pdf_mc1_MjjDphijj_lowMjj);
    RooFitResult* r_MjjDphijj_lowMjj = model_MjjDphijj_lowMjj.fitTo(datahist_data_MjjDphijj_lowMjj,Save());
    r_MjjDphijj_lowMjj->Print();

    Double_t LL_fraction_MjjDphijj_lowMjj = fmc0_MjjDphijj_lowMjj.getVal();
    Double_t LL_fraction_error_MjjDphijj_lowMjj = fmc0_MjjDphijj_lowMjj.getAsymErrorHi();
    RooArgSet mc_total_MjjDphijj_lowMjj(pdf_mc0_MjjDphijj_lowMjj,pdf_mc1_MjjDphijj_lowMjj);
    datahist_data_MjjDphijj_lowMjj.plotOn(frame_MjjDphijj_lowMjj);
    model_MjjDphijj_lowMjj.plotOn(frame_MjjDphijj_lowMjj,Components(mc0_component_MjjDphijj_lowMjj),LineStyle(2),LineColor(2));
    model_MjjDphijj_lowMjj.plotOn(frame_MjjDphijj_lowMjj,Components(mc1_component_MjjDphijj_lowMjj),LineStyle(2),LineColor(kBlue));
    model_MjjDphijj_lowMjj.plotOn(frame_MjjDphijj_lowMjj,Components(mc_total_MjjDphijj_lowMjj),LineStyle(2),LineColor(kGreen));
    TCanvas* c_MjjDphijj_lowMjj = new TCanvas("MjjDphijj_lowMjj","MjjDphijj_lowMjj",800,400) ;
    frame_MjjDphijj_lowMjj->Draw();
    frame_MjjDphijj_lowMjj->Print();

    Double_t Chi2_ndf_MjjDphijj_lowMjj = frame_MjjDphijj_lowMjj->chiSquare("model_MjjDphijj_lowMjj_Norm[x_MjjDphijj_lowMjj]_Comp[pdf_mc1_MjjDphijj_lowMjj]","h_datahist_data_MjjDphijj_lowMjj");  // For Bkg only
    //Double_t Chi2_ndf = frame->chiSquare("model_Norm[x]_Comp[pdf_mc0,pdf_mc1]","h_datahist_data"); //For Bkg+Signal
    cout<<"Chi2/ndf = "<<Chi2_ndf_MjjDphijj_lowMjj<<endl;
    cout<<"Chi2 = "<<Chi2_ndf_MjjDphijj_lowMjj*bins<<endl;
    Double_t p_value_MjjDphijj_lowMjj=TMath::Prob(Chi2_ndf_MjjDphijj_lowMjj*bins, bins); //https://root.cern.ch/root/html/src/TMath.cxx.html
    cout<<"P_value = "<<p_value_MjjDphijj_lowMjj<<endl;
    Double_t significance_MjjDphijj_lowMjj=RooStats::PValueToSignificance(p_value_MjjDphijj_lowMjj/2.0);  //FIXME
    cout<<"Significance = "<<significance_MjjDphijj_lowMjj<<endl;

    //TLegend *leg = new TLegend(0.7,0.7,0.9,0.9); TPaveText *pt = new TPaveText(0.7,0.5,0.9,0.7,"NDC"); // right  //FIXME 
    TLegend *leg_MjjDphijj_lowMjj = new TLegend(0.1,0.7,0.4,0.9);  TPaveText *pt_MjjDphijj_lowMjj = new TPaveText(0.1,0.5,0.4,0.7,"NDC"); // left
    TLegendEntry* lmc0_MjjDphijj_lowMjj = leg_MjjDphijj_lowMjj->AddEntry(&pdf_mc0_MjjDphijj_lowMjj,"LL","2 l");
    lmc0_MjjDphijj_lowMjj->SetLineColor(kRed); lmc0_MjjDphijj_lowMjj->SetTextColor(kRed); lmc0_MjjDphijj_lowMjj->SetLineStyle(2);
    TLegendEntry* lmc1_MjjDphijj_lowMjj = leg_MjjDphijj_lowMjj->AddEntry(&pdf_mc1_MjjDphijj_lowMjj,"TTTL","2l");
    lmc1_MjjDphijj_lowMjj->SetLineColor(kBlue); lmc1_MjjDphijj_lowMjj->SetTextColor(kBlue); lmc1_MjjDphijj_lowMjj->SetLineStyle(2);
    TLegendEntry* ltotal_MjjDphijj_lowMjj = leg_MjjDphijj_lowMjj->AddEntry(&mc_total_MjjDphijj_lowMjj,"Fit","l");
    ltotal_MjjDphijj_lowMjj->SetLineColor(kGreen); ltotal_MjjDphijj_lowMjj->SetTextColor(kGreen); ltotal_MjjDphijj_lowMjj->SetLineStyle(2);
    leg_MjjDphijj_lowMjj->AddEntry(&pdf_mc1_MjjDphijj_lowMjj,"DATA","lp");
    leg_MjjDphijj_lowMjj->Draw();    
    string w_frac0_MjjDphijj_lowMjj = "LL : " +to_string(LL_fraction_MjjDphijj_lowMjj*100) + "% +-" + to_string(LL_fraction_error_MjjDphijj_lowMjj*100)+"%";
    pt_MjjDphijj_lowMjj->AddText(w_frac0_MjjDphijj_lowMjj.data());
    pt_MjjDphijj_lowMjj->Draw();
    TString pdfName_MjjDphijj_lowMjj = "SSWW_MjjDphijj_lowMjj_Fit.pdf";
    c_MjjDphijj_lowMjj->SaveAs(pdfName_MjjDphijj_lowMjj);
    // END of "MjjDphijj_lowMjj"
    // **********************************************************************//

     all->Close();
}

