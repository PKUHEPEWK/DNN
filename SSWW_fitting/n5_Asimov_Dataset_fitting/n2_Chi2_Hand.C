void n2_Chi2_Hand()
{
    //TFile *infile = new TFile("Asimov_Dataset_forDNN_New.root","READ");
    TFile *infile = new TFile("Asimov_Dataset_forDNN_Raw4p0M.root","READ");
    TH1D *Asimov_data = (TH1D*)infile->Get("Asimov_data");
    TH1D *LL_LL = (TH1D*)infile->Get("LL_LL");
    TH1D *TTTL_LL = (TH1D*)infile->Get("TTTL_LL");

    cout<<"Data Inte = "<<Asimov_data->Integral()<<endl;
    Double_t TTTL_scale = 8159.94;
    TTTL_LL->Scale(TTTL_scale/TTTL_LL->Integral());
    cout<<"TTTL Inte = "<<TTTL_LL->Integral()<<endl;

    Int_t BinNum = TTTL_LL->GetSize()-2;
    Double_t Chi2_b = 0;
    Double_t Chi2_f = 0;
    for(Int_t i=0; i<BinNum; i++)
    {
        if(Asimov_data->GetBinContent(i+1)==0)
            continue;
        //Chi2_b = Chi2_b + (Asimov_data->GetBinContent(i+1)-TTTL_LL->GetBinContent(i+1))*(Asimov_data->GetBinContent(i+1)-TTTL_LL->GetBinContent(i+1))/TTTL_LL->GetBinContent(i+1);
        Chi2_b = Chi2_b + (Asimov_data->GetBinContent(i+1)-TTTL_LL->GetBinContent(i+1))*(Asimov_data->GetBinContent(i+1)-TTTL_LL->GetBinContent(i+1))/Asimov_data->GetBinContent(i+1);
        //cout<<Asimov_data->GetBinContent(i+1)<<endl;
        cout<<i+1<<",  "<<Chi2_b<<endl;
    }
    cout<<"Chi2 before divide into d.o.f : "<<Chi2_b<<endl;
    Chi2_f = Chi2_b /(BinNum-1);
    cout<<"Chi2 after divide into d.o.f : "<<Chi2_f<<endl;
    //Double_t p_value=TMath::Prob(Chi2_b, BinNum-1);
    Double_t p_value=TMath::Prob(Chi2_b, 1);
    cout<<"P_value = "<<p_value<<endl;
    Double_t significance=RooStats::PValueToSignificance(p_value/2.0);  //FIXME
    //Double_t significance=RooStats::PValueToSignificance(p_value);
    cout<<"Significance = "<<significance<<endl;

    infile->Close();
}
