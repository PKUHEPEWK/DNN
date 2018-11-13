#include "iostream"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit ;

void n1_lep1ptDphijj_lowlep1pt()
{
    TFile *all = new TFile("TwoD_Histos_lep1ptDphijj.root","READ");
    Int_t bins = 30;  //FIXME TODO 

    // **********************************************************************//
    // Begin of "lep1ptDphijj_lowlep1pt"
    TH1D *data_lep1ptDphijj_lowlep1pt;
    TH1D *mc0_lep1ptDphijj_lowlep1pt;
    TH1D *mc1_lep1ptDphijj_lowlep1pt;
    data_lep1ptDphijj_lowlep1pt = (TH1D*)all->Get("lep1ptDphijj_lowlep1pt_Asimov");
    mc0_lep1ptDphijj_lowlep1pt = (TH1D*)all->Get("lep1ptDphijj_LL_lowlep1pt");
    mc1_lep1ptDphijj_lowlep1pt = (TH1D*)all->Get("lep1ptDphijj_TTTL_lowlep1pt");

    RooRealVar x_lep1ptDphijj_lowlep1pt("x_lep1ptDphijj_lowlep1pt","dphijj",-0.5,3.5);  // FIXME The range: for dphijj
    RooDataHist datahist_data_lep1ptDphijj_lowlep1pt("datahist_data_lep1ptDphijj_lowlep1pt","datahist_data_lep1ptDphijj_lowlep1pt",x_lep1ptDphijj_lowlep1pt, data_lep1ptDphijj_lowlep1pt);
    RooDataHist datahist_mc0_lep1ptDphijj_lowlep1pt("mc0_data_lep1ptDphijj_lowlep1pt","mc0_data_lep1ptDphijj_lowlep1pt",x_lep1ptDphijj_lowlep1pt, mc0_lep1ptDphijj_lowlep1pt);
    RooDataHist datahist_mc1_lep1ptDphijj_lowlep1pt("mc1_data_lep1ptDphijj_lowlep1pt","mc1_data_lep1ptDphijj_lowlep1pt",x_lep1ptDphijj_lowlep1pt, mc1_lep1ptDphijj_lowlep1pt);
    RooHistPdf pdf_mc0_lep1ptDphijj_lowlep1pt("pdf_mc0_lep1ptDphijj_lowlep1pt","pdf_mc0_lep1ptDphijj_lowlep1pt",x_lep1ptDphijj_lowlep1pt,datahist_mc0_lep1ptDphijj_lowlep1pt,2);
    RooHistPdf pdf_mc1_lep1ptDphijj_lowlep1pt("pdf_mc1_lep1ptDphijj_lowlep1pt","pdf_mc1_lep1ptDphijj_lowlep1pt",x_lep1ptDphijj_lowlep1pt,datahist_mc1_lep1ptDphijj_lowlep1pt,2);
    RooRealVar fmc0_lep1ptDphijj_lowlep1pt("fmc0_lep1ptDphijj_lowlep1pt","mc0 fraction",0.,1.);
    RooAddPdf model_lep1ptDphijj_lowlep1pt("model_lep1ptDphijj_lowlep1pt","model_lep1ptDphijj_lowlep1pt",RooArgList(pdf_mc0_lep1ptDphijj_lowlep1pt,pdf_mc1_lep1ptDphijj_lowlep1pt),RooArgList(fmc0_lep1ptDphijj_lowlep1pt));
    RooPlot* frame_lep1ptDphijj_lowlep1pt = x_lep1ptDphijj_lowlep1pt.frame(Title("lep1ptDphijj_lowlep1pt"),Bins(bins));  //FIXME Title 
    model_lep1ptDphijj_lowlep1pt.plotOn(frame_lep1ptDphijj_lowlep1pt);
    RooArgSet mc0_component_lep1ptDphijj_lowlep1pt(pdf_mc0_lep1ptDphijj_lowlep1pt);
    RooArgSet mc1_component_lep1ptDphijj_lowlep1pt(pdf_mc1_lep1ptDphijj_lowlep1pt);
    RooFitResult* r_lep1ptDphijj_lowlep1pt = model_lep1ptDphijj_lowlep1pt.fitTo(datahist_data_lep1ptDphijj_lowlep1pt,Save());
    r_lep1ptDphijj_lowlep1pt->Print();

    Double_t LL_fraction_lep1ptDphijj_lowlep1pt = fmc0_lep1ptDphijj_lowlep1pt.getVal();
    Double_t LL_fraction_error_lep1ptDphijj_lowlep1pt = fmc0_lep1ptDphijj_lowlep1pt.getAsymErrorHi();
    RooArgSet mc_total_lep1ptDphijj_lowlep1pt(pdf_mc0_lep1ptDphijj_lowlep1pt,pdf_mc1_lep1ptDphijj_lowlep1pt);
    datahist_data_lep1ptDphijj_lowlep1pt.plotOn(frame_lep1ptDphijj_lowlep1pt);
    model_lep1ptDphijj_lowlep1pt.plotOn(frame_lep1ptDphijj_lowlep1pt,Components(mc0_component_lep1ptDphijj_lowlep1pt),LineStyle(2),LineColor(2));
    model_lep1ptDphijj_lowlep1pt.plotOn(frame_lep1ptDphijj_lowlep1pt,Components(mc1_component_lep1ptDphijj_lowlep1pt),LineStyle(2),LineColor(kBlue));
    model_lep1ptDphijj_lowlep1pt.plotOn(frame_lep1ptDphijj_lowlep1pt,Components(mc_total_lep1ptDphijj_lowlep1pt),LineStyle(2),LineColor(kGreen));
    TCanvas* c_lep1ptDphijj_lowlep1pt = new TCanvas("lep1ptDphijj_lowlep1pt","lep1ptDphijj_lowlep1pt",800,400) ;
    frame_lep1ptDphijj_lowlep1pt->Draw();
    frame_lep1ptDphijj_lowlep1pt->Print();

    Double_t Chi2_ndf_lep1ptDphijj_lowlep1pt = frame_lep1ptDphijj_lowlep1pt->chiSquare("model_lep1ptDphijj_lowlep1pt_Norm[x_lep1ptDphijj_lowlep1pt]_Comp[pdf_mc1_lep1ptDphijj_lowlep1pt]","h_datahist_data_lep1ptDphijj_lowlep1pt");  // For Bkg only
    //Double_t Chi2_ndf = frame->chiSquare("model_Norm[x]_Comp[pdf_mc0,pdf_mc1]","h_datahist_data"); //For Bkg+Signal
    cout<<"Chi2/ndf = "<<Chi2_ndf_lep1ptDphijj_lowlep1pt<<endl;
    cout<<"Chi2 = "<<Chi2_ndf_lep1ptDphijj_lowlep1pt*bins<<endl;
    Double_t p_value_lep1ptDphijj_lowlep1pt=TMath::Prob(Chi2_ndf_lep1ptDphijj_lowlep1pt*bins, bins); //https://root.cern.ch/root/html/src/TMath.cxx.html
    cout<<"P_value = "<<p_value_lep1ptDphijj_lowlep1pt<<endl;
    Double_t significance_lep1ptDphijj_lowlep1pt=RooStats::PValueToSignificance(p_value_lep1ptDphijj_lowlep1pt/2.0);  //FIXME
    cout<<"Significance = "<<significance_lep1ptDphijj_lowlep1pt<<endl;

    //TLegend *leg = new TLegend(0.7,0.7,0.9,0.9); TPaveText *pt = new TPaveText(0.7,0.5,0.9,0.7,"NDC"); // right  //FIXME 
    TLegend *leg_lep1ptDphijj_lowlep1pt = new TLegend(0.1,0.7,0.4,0.9);  TPaveText *pt_lep1ptDphijj_lowlep1pt = new TPaveText(0.1,0.5,0.4,0.7,"NDC"); // left
    TLegendEntry* lmc0_lep1ptDphijj_lowlep1pt = leg_lep1ptDphijj_lowlep1pt->AddEntry(&pdf_mc0_lep1ptDphijj_lowlep1pt,"LL","2 l");
    lmc0_lep1ptDphijj_lowlep1pt->SetLineColor(kRed); lmc0_lep1ptDphijj_lowlep1pt->SetTextColor(kRed); lmc0_lep1ptDphijj_lowlep1pt->SetLineStyle(2);
    TLegendEntry* lmc1_lep1ptDphijj_lowlep1pt = leg_lep1ptDphijj_lowlep1pt->AddEntry(&pdf_mc1_lep1ptDphijj_lowlep1pt,"TTTL","2l");
    lmc1_lep1ptDphijj_lowlep1pt->SetLineColor(kBlue); lmc1_lep1ptDphijj_lowlep1pt->SetTextColor(kBlue); lmc1_lep1ptDphijj_lowlep1pt->SetLineStyle(2);
    TLegendEntry* ltotal_lep1ptDphijj_lowlep1pt = leg_lep1ptDphijj_lowlep1pt->AddEntry(&mc_total_lep1ptDphijj_lowlep1pt,"Fit","l");
    ltotal_lep1ptDphijj_lowlep1pt->SetLineColor(kGreen); ltotal_lep1ptDphijj_lowlep1pt->SetTextColor(kGreen); ltotal_lep1ptDphijj_lowlep1pt->SetLineStyle(2);
    leg_lep1ptDphijj_lowlep1pt->AddEntry(&pdf_mc1_lep1ptDphijj_lowlep1pt,"DATA","lp");
    leg_lep1ptDphijj_lowlep1pt->Draw();    
    string w_frac0_lep1ptDphijj_lowlep1pt = "LL : " +to_string(LL_fraction_lep1ptDphijj_lowlep1pt*100) + "% +-" + to_string(LL_fraction_error_lep1ptDphijj_lowlep1pt*100)+"%";
    pt_lep1ptDphijj_lowlep1pt->AddText(w_frac0_lep1ptDphijj_lowlep1pt.data());
    pt_lep1ptDphijj_lowlep1pt->Draw();
    TString pdfName_lep1ptDphijj_lowlep1pt = "SSWW_lep1ptDphijj_lowlep1pt_Fit.pdf";
    c_lep1ptDphijj_lowlep1pt->SaveAs(pdfName_lep1ptDphijj_lowlep1pt);
    // END of "lep1ptDphijj_lowlep1pt"
    // **********************************************************************//

     all->Close();
}

