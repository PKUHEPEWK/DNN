#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
#include <fstream>
using namespace RooFit;

void n3_FlucToy_Roofit()
{
    TRandom *r0 = new TRandom();
//    int x = r0->Poisson(100); cout<<x<<endl;    

    TString HistoName = "dphijj";
    TFile *all = new TFile(HistoName+".root","READ"); //TODO 
    Int_t Trials = 50000;  //TODO

    TH1D *data;
    TH1D *mc0;
    TH1D *mc1;
    data = (TH1D*)all->Get("PseudoData");
    mc0 = (TH1D*)all->Get("LL");
    mc1 = (TH1D*)all->Get("TTTL");

    Int_t binNum = data->GetSize()-2; cout<<binNum<<endl;
    Double_t LowBin = data->GetXaxis()->GetXmin(); cout<<LowBin<<endl;
    Double_t HighBin = data->GetXaxis()->GetXmax(); cout<<HighBin<<endl;

    RooRealVar x("x",HistoName,LowBin,HighBin);
    RooDataHist datahist_mc0("mc0_data","mc0_data",x, mc0);
    RooDataHist datahist_mc1("mc1_data","mc1_data",x, mc1);
    RooHistPdf pdf_mc0("pdf_mc0","pdf_mc0",x,datahist_mc0,2);
    RooHistPdf pdf_mc1("pdf_mc1","pdf_mc1",x,datahist_mc1,2);
    RooRealVar fmc0("fmc0","mc0 fraction",0.,1.);
    //RooRealVar fmc1("fmc1","mc1 fraction",0.,1.);
    RooAddPdf model("model","model",RooArgList(pdf_mc0,pdf_mc1),RooArgList(fmc0));


    Double_t LL_fraction=0;
    Double_t LL_fraction_error=0;

    //ofstream outfile;
    //outfile.open("data.txt",ios::in);
    TCanvas *cv = new TCanvas("cv","cv",1200,900);
    TH1D *ProbHist = new TH1D(HistoName+"_Roofit",HistoName+"_Roofit",50,0,0.2);

    cout<<"Now starts the PseudoDATA Fluctuation."<<endl<<endl;
    for(Int_t i=0; i<Trials; i++)
    {
        if(i%100==0) {cout<<"Now looping "<<i<<"th Trials"<<endl;}
        TH1D *TempHist = new TH1D("TempPseudoData","TempPseudoData",binNum,LowBin,HighBin); 
        for(Int_t j=1; j<=binNum; j++)
        {
            Int_t thisContent = data->GetBinContent(j);
            Int_t FillContent = r0->Poisson(thisContent);
            //cout<<thisContent<<"!@#!@#!"<<FillContent<<endl;
            TempHist->SetBinContent(j,FillContent);
        }
        RooDataHist datahist_data("mc0_data","mc0_data",x, TempHist);
        RooPlot* frame = x.frame(Title("temp"),Bins(10));  //FIXME Title 
        model.plotOn(frame);
        RooArgSet mc0_component(pdf_mc0);
        RooArgSet mc1_component(pdf_mc1);
        model.fitTo(datahist_data);
        //RooFitResult* r = model.fitTo(datahist_data,Save());
        //r->Print() ;

        //outfile<<fmc0.getVal()<<'\n';
        ProbHist->Fill(fmc0.getVal());
        //LL_fraction += fmc0.getVal();
        //LL_fraction_error += fmc0.getAsymErrorHi();
        
        TempHist->Delete();
    }
    //LL_fraction = LL_fraction/Trials;
    //LL_fraction_error = LL_fraction_error/Trials;
    //cout<<LL_fraction*100<<"% +- "<<LL_fraction_error*100<<"%"<<endl;

    ProbHist->Draw();
    cv->SaveAs(HistoName+"_FracRoofit.pdf");  
 
    //outfile.close();

}
