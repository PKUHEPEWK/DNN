#include "iostream"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
#include "RooChi2Var.h"
using namespace RooFit ;

void n1_RooFit_forDNN()
{
//    TFile *all = new TFile("Asimov_Dataset_forDNN_New.root","READ"); //FIXME
    TFile *all = new TFile("Asimov_Dataset_forDNN_Raw4p0M.root","READ");
    Int_t bins = 20;  //bins=bins;
    Int_t int_order = 1;//FIXME
    TString HistoName = "DNN";  //FIXME 
    TH1D *data;
    TH1D *mc0;
    TH1D *mc1;
    TString histData = "Asimov_data";
    TString histLL = "LL_LL";    
    TString histTTTL = "TTTL_LL";

    data = (TH1D*)all->Get(histData);
    mc0 = (TH1D*)all->Get(histLL);
    mc1 = (TH1D*)all->Get(histTTTL);

    
    Double_t LL_scale = 384.768/mc0->Integral();
    Double_t TTTL_scale = 8159.94/mc1->Integral();
    mc0->Scale(LL_scale);
    mc1->Scale(TTTL_scale);
    cout<<"!@#!@#!@#"<<mc0->Integral()<<endl;
    

    RooRealVar x("x",HistoName,0,1);  
    RooDataHist datahist_data("datahist_data","datahist_data",x, data);
    RooDataHist datahist_mc0("datahist_mc0","datahist_mc0",x, mc0);
    RooDataHist datahist_mc1("datahist_mc1","datahist_mc1",x, mc1);
    //RooHistPdf pdf_data("pdf_data","pdf_data",x,datahist_data,2);
    RooHistPdf pdf_mc0("pdf_mc0","pdf_mc0",x,datahist_mc0,2);
    //RooHistPdf *pdf_mc0 = new RooHistPdf("pdf_mc0","pdf_mc0",x,datahist_mc0,2);
    RooHistPdf pdf_mc1("pdf_mc1","pdf_mc1",x,datahist_mc1,int_order);

    //RooRealVar fmc0("fmc0","mc0 fraction",0.,1.);
    RooRealVar fmc1("fmc1","mc1 fraction",0.,1.);
    //RooAddPdf model("model","model",RooArgList(pdf_mc0,pdf_mc1),RooArgList(fmc0));
    RooAddPdf model("model","model",RooArgList(pdf_mc1,pdf_mc0),RooArgList(fmc1));

    RooPlot* frame = x.frame(Title(HistoName),Bins(bins));  //FIXME Title 
    model.plotOn(frame);
    RooArgSet mc0_component(pdf_mc0);
    RooArgSet mc1_component(pdf_mc1);
    //RooFitResult* r = model.fitTo(datahist_data,PrintLevel(-1));
    RooFitResult* r = model.fitTo(datahist_data,Save());
    r->Print();
//    cout<<"!@#!@#!@#"<<r->Print()<<endl;
//    cout<<r->GetNDF()<<endl;

   
     //r->plotOn(frame,pdf_mc0,fmc0,"ME12ABHV");
    //cout<<"!@#!@#!@#!@#SDFSDFS:"<<r[0]<<endl; 

    //Double_t LL_fraction = fmc0.getVal();
    //Double_t LL_fraction_error = fmc0.getAsymErrorHi();
    Double_t TTTL_fraction = fmc1.getVal();
    Double_t TTTL_fraction_error = fmc1.getAsymErrorHi();

    RooArgSet mc_total(pdf_mc0,pdf_mc1);
    datahist_data.plotOn(frame); 
    model.plotOn(frame,Components(mc0_component),LineStyle(2),LineColor(2));
    model.plotOn(frame,Components(mc1_component),LineStyle(2),LineColor(kBlue));
    model.plotOn(frame,Components(mc_total),LineStyle(2),LineColor(kGreen));
    TCanvas* c = new TCanvas("test_histpdf","test_histpdf",800,400) ; 
    //c->SetLogy(); //FIXME
    frame->Draw();
    frame->Print(); 

    Double_t Chi2_ndf = frame->chiSquare("model_Norm[x]_Comp[pdf_mc1]","h_datahist_data",1);  // For Bkg only
    //Double_t Chi2_ndf = frame->chiSquare("model_Norm[x]_Comp[pdf_mc0,pdf_mc1]","h_datahist_data"); //For Bkg+Signal 
    cout<<"Chi2/ndf = "<<Chi2_ndf<<endl;
    cout<<"Chi2 = "<<Chi2_ndf*(bins-1-int_order)<<endl; //https://www.physi.uni-heidelberg.de/~nberger/teaching/ws12/statistics/Lecture10.pdf
    //Double_t p_value=TMath::Prob(Chi2_ndf*(bins-1), bins-1); //https://root.cern.ch/root/html/src/TMath.cxx.html // https://root-forum.cern.ch/t/degrees-of-freedom-via-chi2-for-th1/21355
    Double_t p_value=TMath::Prob(Chi2_ndf*(bins-1-int_order), (bins-1-int_order));
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

//    string w_frac0 = "LL : " +to_string(LL_fraction*100) + "% +-" + to_string(LL_fraction_error*100)+"%";
    string w_frac1 = "TTTL : " +to_string(TTTL_fraction*100) + "% +-" + to_string(TTTL_fraction_error*100)+"%";
//    pt->AddText(w_frac0.data());
    pt->AddText(w_frac1.data());
    pt->Draw();

//    TString pdfName = "SSWW_"+HistoName+"_Fit_FormerHigh.pdf"; //FIXME
    TString pdfName = "SSWW_"+HistoName+"_Fit_Raw_Mjj.pdf"; //FIXME
    c->SaveAs(pdfName);

    /*
    //??????
    TCanvas* cc = new TCanvas("c_test_histpdf","c_test_histpdf",800,400) ;
    RooPlot* plot = x.frame();
    datahist_data.plotOn(plot);
    pdf_mc1.plotOn(plot);
    //pdf_mc1.fitTo(datahist_data);
    RooChi2Var chi2("chi2","chi2",pdf_mc1,datahist_data);
    Double_t chi2_val = chi2.getVal();
    cout<<"!@#!@#!@#"<<chi2_val<<endl;
    cout<<"P_value = "<<TMath::Prob(chi2_val*1, 1)<<endl;
    cout<<"Significance = "<<RooStats::PValueToSignificance(TMath::Prob(chi2_val*1, 1)/2.0)<<endl;
    plot->Draw();
    cc->SaveAs("TEST.pdf");
    //?????
    */

/*
    TCanvas* can = new TCanvas("histpdf","histpdf",800,400) ;
    RooHist *rh = frame->getHist("h_datahist_data");
    can->SaveAs("rm.pdf");
*/
}
