#include "iostream"

void n4_FlucToy_TFrac()
{
    TRandom *r0 = new TRandom();
//    int x = r0->Poisson(100); cout<<x<<endl;    

    TString HistoName = "lep1pt";
    TFile *all = new TFile(HistoName+".root","READ"); //TODO 
    Int_t Trials = 100000;  //TODO

    const int MCFracs = 2; //TODO
    double br[MCFracs],brer[MCFracs];
    TH1D *data;
    TH1D *mc0;
    TH1D *mc1;
    data = (TH1D*)all->Get("PseudoData");
    mc0 = (TH1D*)all->Get("LL");
    mc1 = (TH1D*)all->Get("TTTL");

    float scale_to = data->GetEntries();
    float Scale_mc0 = 1.0/mc0->GetEntries()*scale_to;
    float Scale_mc1 = 1.0/mc1->GetEntries()*scale_to;
    mc0->Scale(Scale_mc0);
    mc1->Scale(Scale_mc1);

    Int_t binNum = data->GetSize()-2; cout<<binNum<<endl;
    Double_t LowBin = data->GetXaxis()->GetXmin(); cout<<LowBin<<endl;
    Double_t HighBin = data->GetXaxis()->GetXmax(); cout<<HighBin<<endl;
    Double_t LL_fraction=0;
    Double_t LL_fraction_error=0;

    TObjArray *mc = new TObjArray(2);
    mc->Add(mc0);
    mc->Add(mc1); 

    cout<<"Now starts the PseudoDATA Fluctuation."<<endl<<endl;
    Double_t fmc0; Double_t fmc0_e;
    Double_t fmc1; Double_t fmc1_e;

    TCanvas *cv = new TCanvas("cv","cv",1200,900);
    TH1D *ProbHist = new TH1D(HistoName+"_TFracFitter",HistoName+"_TFracFitter",50,0,0.2);

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
        float Scale_temp = 1.0/TempHist->GetEntries()*scale_to;
        TempHist->Scale(Scale_temp);

        TFractionFitter* fit = new TFractionFitter(TempHist, mc);
        fit->Constrain(0,0.0,1.0);
        fit->Constrain(1,0.0,1.0);
        //fit->SetRangeX(5,15);
        Int_t status = fit->Fit();

        std::cout << "fit status: " << status << std::endl;
        if (status == 0)
        {
            for (int iz=0; iz<MCFracs; iz++)
            {
                fit -> GetResult(iz,br[iz],brer[iz]);
            }
            fmc0 = (int)(br[0]*1000000) / 10000.0; fmc0_e = (int)(brer[0]*10000000) / 100000.0;
            fmc1 = (int)(br[1]*1000000) / 10000.0; fmc1_e = (int)(brer[1]*10000000) / 100000.0; //TODO. add files if there are
            ProbHist->Fill(fmc0);
            //string Fmc0 = to_string(fmc0); string E_Fmc0 = to_string(fmc0_e);
            //string Fmc1 = to_string(fmc1); string E_Fmc1 = to_string(fmc1_e); //TODO. add files if there are
        }
        else
        {
            continue;
        }

        //LL_fraction += fmc0;
        //LL_fraction_error += fmc0_e;

        TempHist->Delete();
    }


    //LL_fraction = LL_fraction/Trials;
    //LL_fraction_error = LL_fraction_error/Trials;
    //cout<<LL_fraction*100<<"% +- "<<LL_fraction_error*100<<"%"<<endl;

    ProbHist->Draw();
    cv->SaveAs(HistoName+"_FracTFraction.pdf");

}
