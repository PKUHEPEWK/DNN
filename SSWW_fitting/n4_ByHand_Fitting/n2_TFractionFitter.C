#include "iostream"
void n2_TFractionFitter()
{
    TString HistoName = "lep1pt"; // TODO 
    TFile *all = new TFile("lep1pt.root","READ"); //TODO
    const int MCFracs = 2;   //////TODO : the MC fraction numbers
    double br[MCFracs],brer[MCFracs];
    gStyle->SetOptStat(0);

    TH1D *data;
    TH1D *mc0;
    TH1D *mc1;
    TObjArray *mc = new TObjArray(2);
    data = (TH1D*)all->Get("PseudoData"); data->SetLineWidth(2); data->SetLineColor(kBlack); //TODO : histo name
    mc0 = (TH1D*)all->Get("LL"); mc0->SetLineColor(kRed); mc0->SetFillStyle(3000); mc0->SetFillColor(kRed); //TODO : histo name
    mc1 = (TH1D*)all->Get("TTTL"); mc1->SetLineColor(kBlue); mc1->SetFillStyle(3000); mc1->SetFillColor(kBlue); //TODO : histo name, add files if there are


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
        TString Name1 = "TFac_" + HistoName + ".pdf";
        cv->SaveAs(Name1);

        //TCanvas *cv_log = new TCanvas("cv","cv",1200,900);
        //TPad *p2 = new TPad();
        //p2->SetFillStyle(4050);
        //p2->Draw();
        //cv_log->SetLogy(); 
        //result->Draw("e hist");
        //data->Draw("ep same");
        //mc0->Scale(br[0]); /*mc0->SetFillStyle(3050);*/ mc0->Draw("e hist same");
        //mc1->Scale(br[1]); /*mc1->SetFillStyle(4050);*/ mc1->Draw("e hist same"); // TODO add files if there are
        //leg->Draw();
        //pt->Draw();
        //TString Name2 = "TFac_" + HistoName + "_log.pdf";
        //cv_log->SaveAs(Name2);

    }
    cout<<endl;
    for (int i=0; i<MCFracs; i++)
    {
        cout<<"The fraction of "<<i<<"th : "<<br[i]<<", error : "<<brer[i]<<endl;
    }
    cout<<"Chi-square Value : "<<fit->GetChisquare()<<endl;
    cout<<"Degree of Freedom : "<<fit->GetNDF()<<endl;
    cout<<"Fit probability : "<<fit->GetProb()<<endl;

}
