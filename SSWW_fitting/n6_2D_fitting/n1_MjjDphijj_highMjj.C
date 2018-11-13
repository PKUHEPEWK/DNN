#include "iostream"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit ;

void n1_MjjDphijj_highMjj()
{
    TFile *all = new TFile("TwoD_Histos_MjjDphijj.root","READ");
    Int_t bins = 30;  //FIXME TODO 

    // **********************************************************************//
    // Begin of "MjjDphijj_highMjj"
    TH1D *data_MjjDphijj_highMjj;
    TH1D *mc0_MjjDphijj_highMjj;
    TH1D *mc1_MjjDphijj_highMjj;
    data_MjjDphijj_highMjj = (TH1D*)all->Get("MjjDphijj_highMjj_Asimov");
    mc0_MjjDphijj_highMjj = (TH1D*)all->Get("MjjDphijj_LL_highMjj");
    mc1_MjjDphijj_highMjj = (TH1D*)all->Get("MjjDphijj_TTTL_highMjj");

    RooRealVar x_MjjDphijj_highMjj("x_MjjDphijj_highMjj","dphijj",-0.5,3.5);  // FIXME The range: for dphijj
    RooDataHist datahist_data_MjjDphijj_highMjj("datahist_data_MjjDphijj_highMjj","datahist_data_MjjDphijj_highMjj",x_MjjDphijj_highMjj, data_MjjDphijj_highMjj);
    RooDataHist datahist_mc0_MjjDphijj_highMjj("mc0_data_MjjDphijj_highMjj","mc0_data_MjjDphijj_highMjj",x_MjjDphijj_highMjj, mc0_MjjDphijj_highMjj);
    RooDataHist datahist_mc1_MjjDphijj_highMjj("mc1_data_MjjDphijj_highMjj","mc1_data_MjjDphijj_highMjj",x_MjjDphijj_highMjj, mc1_MjjDphijj_highMjj);
    RooHistPdf pdf_mc0_MjjDphijj_highMjj("pdf_mc0_MjjDphijj_highMjj","pdf_mc0_MjjDphijj_highMjj",x_MjjDphijj_highMjj,datahist_mc0_MjjDphijj_highMjj,2);
    RooHistPdf pdf_mc1_MjjDphijj_highMjj("pdf_mc1_MjjDphijj_highMjj","pdf_mc1_MjjDphijj_highMjj",x_MjjDphijj_highMjj,datahist_mc1_MjjDphijj_highMjj,2);
    RooRealVar fmc0_MjjDphijj_highMjj("fmc0_MjjDphijj_highMjj","mc0 fraction",0.,1.);
    RooAddPdf model_MjjDphijj_highMjj("model_MjjDphijj_highMjj","model_MjjDphijj_highMjj",RooArgList(pdf_mc0_MjjDphijj_highMjj,pdf_mc1_MjjDphijj_highMjj),RooArgList(fmc0_MjjDphijj_highMjj));
    RooPlot* frame_MjjDphijj_highMjj = x_MjjDphijj_highMjj.frame(Title("MjjDphijj_highMjj"),Bins(bins));  //FIXME Title 
    model_MjjDphijj_highMjj.plotOn(frame_MjjDphijj_highMjj);
    RooArgSet mc0_component_MjjDphijj_highMjj(pdf_mc0_MjjDphijj_highMjj);
    RooArgSet mc1_component_MjjDphijj_highMjj(pdf_mc1_MjjDphijj_highMjj);
    RooFitResult* r_MjjDphijj_highMjj = model_MjjDphijj_highMjj.fitTo(datahist_data_MjjDphijj_highMjj,Save());
    r_MjjDphijj_highMjj->Print();

    Double_t LL_fraction_MjjDphijj_highMjj = fmc0_MjjDphijj_highMjj.getVal();
    Double_t LL_fraction_error_MjjDphijj_highMjj = fmc0_MjjDphijj_highMjj.getAsymErrorHi();
    RooArgSet mc_total_MjjDphijj_highMjj(pdf_mc0_MjjDphijj_highMjj,pdf_mc1_MjjDphijj_highMjj);
    datahist_data_MjjDphijj_highMjj.plotOn(frame_MjjDphijj_highMjj);
    model_MjjDphijj_highMjj.plotOn(frame_MjjDphijj_highMjj,Components(mc0_component_MjjDphijj_highMjj),LineStyle(2),LineColor(2));
    model_MjjDphijj_highMjj.plotOn(frame_MjjDphijj_highMjj,Components(mc1_component_MjjDphijj_highMjj),LineStyle(2),LineColor(kBlue));
    model_MjjDphijj_highMjj.plotOn(frame_MjjDphijj_highMjj,Components(mc_total_MjjDphijj_highMjj),LineStyle(2),LineColor(kGreen));
    TCanvas* c_MjjDphijj_highMjj = new TCanvas("MjjDphijj_highMjj","MjjDphijj_highMjj",800,400) ;
    frame_MjjDphijj_highMjj->Draw();
    frame_MjjDphijj_highMjj->Print();

    Double_t Chi2_ndf_MjjDphijj_highMjj = frame_MjjDphijj_highMjj->chiSquare("model_MjjDphijj_highMjj_Norm[x_MjjDphijj_highMjj]_Comp[pdf_mc1_MjjDphijj_highMjj]","h_datahist_data_MjjDphijj_highMjj");  // For Bkg only
    //Double_t Chi2_ndf = frame->chiSquare("model_Norm[x]_Comp[pdf_mc0,pdf_mc1]","h_datahist_data"); //For Bkg+Signal
    cout<<"Chi2/ndf = "<<Chi2_ndf_MjjDphijj_highMjj<<endl;
    cout<<"Chi2 = "<<Chi2_ndf_MjjDphijj_highMjj*bins<<endl;
    Double_t p_value_MjjDphijj_highMjj=TMath::Prob(Chi2_ndf_MjjDphijj_highMjj*bins, bins); //https://root.cern.ch/root/html/src/TMath.cxx.html
    cout<<"P_value = "<<p_value_MjjDphijj_highMjj<<endl;
    Double_t significance_MjjDphijj_highMjj=RooStats::PValueToSignificance(p_value_MjjDphijj_highMjj/2.0);  //FIXME
    cout<<"Significance = "<<significance_MjjDphijj_highMjj<<endl;

    //TLegend *leg = new TLegend(0.7,0.7,0.9,0.9); TPaveText *pt = new TPaveText(0.7,0.5,0.9,0.7,"NDC"); // right  //FIXME 
    TLegend *leg_MjjDphijj_highMjj = new TLegend(0.1,0.7,0.4,0.9);  TPaveText *pt_MjjDphijj_highMjj = new TPaveText(0.1,0.5,0.4,0.7,"NDC"); // left
    TLegendEntry* lmc0_MjjDphijj_highMjj = leg_MjjDphijj_highMjj->AddEntry(&pdf_mc0_MjjDphijj_highMjj,"LL","2 l");
    lmc0_MjjDphijj_highMjj->SetLineColor(kRed); lmc0_MjjDphijj_highMjj->SetTextColor(kRed); lmc0_MjjDphijj_highMjj->SetLineStyle(2);
    TLegendEntry* lmc1_MjjDphijj_highMjj = leg_MjjDphijj_highMjj->AddEntry(&pdf_mc1_MjjDphijj_highMjj,"TTTL","2l");
    lmc1_MjjDphijj_highMjj->SetLineColor(kBlue); lmc1_MjjDphijj_highMjj->SetTextColor(kBlue); lmc1_MjjDphijj_highMjj->SetLineStyle(2);
    TLegendEntry* ltotal_MjjDphijj_highMjj = leg_MjjDphijj_highMjj->AddEntry(&mc_total_MjjDphijj_highMjj,"Fit","l");
    ltotal_MjjDphijj_highMjj->SetLineColor(kGreen); ltotal_MjjDphijj_highMjj->SetTextColor(kGreen); ltotal_MjjDphijj_highMjj->SetLineStyle(2);
    leg_MjjDphijj_highMjj->AddEntry(&pdf_mc1_MjjDphijj_highMjj,"DATA","lp");
    leg_MjjDphijj_highMjj->Draw();
    string w_frac0_MjjDphijj_highMjj = "LL : " +to_string(LL_fraction_MjjDphijj_highMjj*100) + "% +-" + to_string(LL_fraction_error_MjjDphijj_highMjj*100)+"%";
    pt_MjjDphijj_highMjj->AddText(w_frac0_MjjDphijj_highMjj.data());
    pt_MjjDphijj_highMjj->Draw();
    TString pdfName_MjjDphijj_highMjj = "SSWW_MjjDphijj_highMjj_Fit.pdf";
    c_MjjDphijj_highMjj->SaveAs(pdfName_MjjDphijj_highMjj);
    // END of "MjjDphijj_highMjj"
    // **********************************************************************//

    all->Close();
}

