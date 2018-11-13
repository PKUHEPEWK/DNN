#include "iostream"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit ;

void n1_RooFit()
{
/*
    TFile *fileSignal = new TFile("../n1_2p5m_result_30bins/PseudoDATA_3ab_hist.root","READ"); // mini stats
    TFile *fileMC0 = new TFile("../n1_2p5m_result_30bins/SS_2p5M_cut_LL_hist.root","READ");
    TFile *fileMC1 = new TFile("../n1_2p5m_result_30bins/SS_2p5M_cut_TTTL_hist.root","READ"); //TODO : add files if there are
    TString HistoName = "dphijj";  //FIXME 
//    TString HistoName = "lep1pt";  //FIXME 
    TH1D *data;
    TH1D *mc0;
    TH1D *mc1;
    data = (TH1D*)fileSignal->Get(HistoName);
    mc0  = (TH1D*)fileMC0->Get(HistoName);
    mc1  = (TH1D*)fileMC1->Get(HistoName);
*/
    //TFile *all = new TFile("lep1pt.root","READ");
    TFile *all = new TFile("Asimov_Dataset_20bins.root","READ"); //FIXME
    Int_t bins = 20;  //FIXME TODO 
//    TString HistoName = "dphijj";  //FIXME 
    TString HistoName = "lep1pt";  //FIXME 
//    TString HistoName = "detajj";  //FIXME 
//    TString HistoName = "jet1pt";  //FIXME 
    TH1D *data;
    TH1D *mc0;
    TH1D *mc1;
    TString histData = HistoName+"_data";
    TString histLL = HistoName+"_LL";    
    TString histTTTL = HistoName+"_TTTL";

    data = (TH1D*)all->Get(histData);
    mc0 = (TH1D*)all->Get(histLL);
    mc1 = (TH1D*)all->Get(histTTTL);


//    RooRealVar x("x",HistoName,-0.5,3.5);  // FIXME The range: for dphijj
    RooRealVar x("x",HistoName,0,800);  // FIXME The range: for lep1pt
//    RooRealVar x("x",HistoName,0,600);  // FIXME The range: for jet1pt
    RooDataHist datahist_data("datahist_data","datahist_data",x, data);
    RooDataHist datahist_mc0("mc0_data","mc0_data",x, mc0);
    RooDataHist datahist_mc1("mc1_data","mc1_data",x, mc1);
    //RooHistPdf pdf_data("pdf_data","pdf_data",x,datahist_data,2);
    RooHistPdf pdf_mc0("pdf_mc0","pdf_mc0",x,datahist_mc0,2);
    //RooHistPdf *pdf_mc0 = new RooHistPdf("pdf_mc0","pdf_mc0",x,datahist_mc0,2);
    RooHistPdf pdf_mc1("pdf_mc1","pdf_mc1",x,datahist_mc1,2);

    //RooRealVar fmc0("fmc0","mc0 fraction",0.05,0.,1.);
    RooRealVar fmc0("fmc0","mc0 fraction",0.,1.);
    //RooRealVar fmc1("fmc1","mc1 fraction",0.,1.);
    RooAddPdf model("model","model",RooArgList(pdf_mc0,pdf_mc1),RooArgList(fmc0));

    RooPlot* frame = x.frame(Title(HistoName),Bins(bins));  //FIXME Title 
    model.plotOn(frame);
    RooArgSet mc0_component(pdf_mc0);
    RooArgSet mc1_component(pdf_mc1);
    //RooFitResult* r = model.fitTo(datahist_data,PrintLevel(-1));
    RooFitResult* r = model.fitTo(datahist_data,Save());
    r->Print() ;
    //r->plotOn(frame,pdf_mc0,fmc0,"ME12ABHV");
    //cout<<"!@#!@#!@#!@#SDFSDFS:"<<r[0]<<endl; 

    Double_t LL_fraction = fmc0.getVal();
    Double_t LL_fraction_error = fmc0.getAsymErrorHi();
    //Double_t TTTL_fraction = fmc1.getVal();
    //Double_t TTTL_fraction_error = fmc1.getAsymErrorHi();

    RooArgSet mc_total(pdf_mc0,pdf_mc1);
    datahist_data.plotOn(frame); 
    model.plotOn(frame,Components(mc0_component),LineStyle(2),LineColor(2));
    model.plotOn(frame,Components(mc1_component),LineStyle(2),LineColor(kBlue));
    model.plotOn(frame,Components(mc_total),LineStyle(2),LineColor(kGreen));
    TCanvas* c = new TCanvas("test_histpdf","test_histpdf",800,400) ; 
    //c->SetLogy(); //FIXME
    frame->Draw();
    frame->Print();

    Double_t Chi2_ndf = frame->chiSquare("model_Norm[x]_Comp[pdf_mc1]","h_datahist_data");  // For Bkg only
//    Double_t Chi2_ndf = frame->chiSquare("model_Norm[x]_Comp[pdf_mc0,pdf_mc1]","h_datahist_data"); //For Bkg+Signal 
    cout<<"Chi2/ndf = "<<Chi2_ndf<<endl;
    cout<<"Chi2 = "<<Chi2_ndf*(bins-2)<<endl;
    Double_t p_value=TMath::Prob(Chi2_ndf*(bins-2), bins-2); //https://root.cern.ch/root/html/src/TMath.cxx.html
    cout<<"P_value = "<<p_value<<endl;
    Double_t significance=RooStats::PValueToSignificance(p_value/2.0);  //FIXME
    cout<<"Significance = "<<significance<<endl;

    TLegend *leg = new TLegend(0.7,0.7,0.9,0.9); TPaveText *pt = new TPaveText(0.7,0.5,0.9,0.7,"NDC"); // right  //FIXME 
//    TLegend *leg = new TLegend(0.1,0.7,0.4,0.9); TPaveText *pt = new TPaveText(0.1,0.5,0.4,0.7,"NDC"); // left
    TLegendEntry* lmc0 = leg->AddEntry(&pdf_mc0,"LL","2 l");
    lmc0->SetLineColor(kRed); lmc0->SetTextColor(kRed); lmc0->SetLineStyle(2);
    TLegendEntry* lmc1 = leg->AddEntry(&pdf_mc1,"TTTL","2l");
    lmc1->SetLineColor(kBlue); lmc1->SetTextColor(kBlue); lmc1->SetLineStyle(2);
    TLegendEntry* ltotal = leg->AddEntry(&mc_total,"Fit","l");
    ltotal->SetLineColor(kGreen); ltotal->SetTextColor(kGreen); ltotal->SetLineStyle(2); 
    leg->AddEntry(&pdf_mc1,"DATA","lp");
    leg->Draw();

    string w_frac0 = "LL : " +to_string(LL_fraction*100) + "% +-" + to_string(LL_fraction_error*100)+"%";
//    string w_frac1 = "TTTL : " +to_string(TTTL_fraction*100) + "% +-" + to_string(TTTL_fraction_error*100)+"%";
    pt->AddText(w_frac0.data());
//    pt->AddText(w_frac1.data());
    pt->Draw();

    TString pdfName = "SSWW_"+HistoName+"_Fit.pdf";
    c->SaveAs(pdfName);


}
