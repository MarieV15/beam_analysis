# author: Marie Vidal
# date: September 2018

import ROOT
import numpy as np
import math
from glob import glob
from substraction_spectrum import i_channel

def main():
    f1 = ROOT.TFile("../analysis/Fe55_calibrationchi2_2018-10-05gaus.root")
    graph_calibration = f1.Get("a_vs_time_gaussian")
    f2 = ROOT.TFile("../analysis/Fe55_beamchi2_2018-10-05gaus.root")
    graph_beam = f2.Get("a_vs_time_gaussian")
    x = graph_calibration.GetX()
    y = graph_calibration.GetY()
    xb = graph_beam.GetX()
    yb = graph_beam.GetY()
    nentries = graph_beam.GetN()
    nentries_c = graph_calibration.GetN()
    cal_time = []
    beam_time = []
    #for i in range(0, nentries):
    #    cal_time.append(x[i])
    
    
    list_time = []
    for i in range(0, nentries):
        list_time.append(xb[i])
    array_time = np.array(list_time, dtype=float)
   
    c = ROOT.TCanvas()
    graph_beam.GetXaxis().SetTitle("Time [h]")
    graph_beam.GetYaxis().SetTitle("Energy scale [keV/ADC]")
    graph_beam.SetTitle(r"Energy of the 55Fe source in function of time")
    graph_beam.SetMarkerColor(6)
    graph_beam.Draw('ap')
    #graph_calibration.SetMarkerColor(4)

    fit = ROOT.TF1("fit_funct", "pol2(0)", 0, 61)
    graph_beam.Fit("fit_funct")
    p0 = fit.GetParameter(0)
    p1 = fit.GetParameter(1)
    p2 = fit.GetParameter(2)
    
    directory = '../data/T2/beam_data/neutron/run3'
    #directory = '../data/T2/cal_test'
    chain_tree = ROOT.TChain("T2")
    for filename in sorted(glob(directory+'/*.root')):
        chain_tree.Add(filename)
    # on run3 if the correction is better using function or energy scale:
    h_Fe55_m1 = ROOT.TH1F("h_Fe55_m1", "Fe55 Energy spectrum, method 1; Energy[ADC]; counts", 150, 0., 20.)
    h_Fe55_m2 = ROOT.TH1F("h_Fe55_m2", "Fe55 Energy spectrum, method 2; Energy[ADC]; counts", 150, 0., 20.)
    i = 0
    k=0
    l=0
    for event in chain_tree:
        cut = [0, 0]
        S15_ch = i_channel(0, event)
        time = event.UnixStartTime[S15_ch]/3600.
        index = (np.abs(array_time-time)).argmin()
        onset10 = event.DD_Rise10pct[S15_ch]
        S15_w2=event.DD_AmplADU[S15_ch]
        RT = event.DD_Rise[S15_ch]
        if i==0:
            initial_time = time
        # 1st method using existing energy scale:
        if cut[0]==0:
            if S15_w2>1000. and RT<1.51 and RT>1.1:
                    S15_w2_c = S15_w2*yb[index]
                    h_Fe55_m1.Fill(S15_w2_c)
                    cut[0]=1
                    k+=1
            # 2nd method using fit function:
            if cut[1]==0:
                if S15_w2>1000. and RT<1.51 and RT>1.1:
                    time -= initial_time
                    energy_scale = p0 + p1*time + p2 * time**2
                    e = S15_w2*energy_scale
                    h_Fe55_m2.Fill(e)
                    cut[1]=1
                    l+=1
        i+=1
    print("number of times it passes the cut for classic correction:", k)
    print("number of times it passes the cut for new correction:", l)
    c1 = ROOT.TCanvas()                
    h_Fe55_m1.Draw()
    c2 = ROOT.TCanvas()
    h_Fe55_m2.SetLineColor(6)
    h_Fe55_m2.Draw()
    input()
    
if __name__ == '__main__':
    main()