# author: Marie Vidal
# date: October 9th 2018

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
    
    #list of time and energy scale a: [[time0, a0], [time1, a1], ...]
    list_time_a = []
    for i in range(0, nentries):
        list_time_a.append([xb[i], yb[i], graph_beam.GetErrorX(i), graph_beam.GetErrorY(i)])
    
    for i in range(0, nentries_c):
        list_time_a.append([x[i], y[i], graph_calibration.GetErrorX(i), graph_calibration.GetErrorX(i)])
    array_time_a = np.array(list_time_a, dtype=float)
    
    merged_graph = ROOT.TGraphErrors(len(list_time_a), np.array([row[0] for row in array_time_a], dtype=float), np.array([row[1] for row in array_time_a], dtype=float), np.array([row[2] for row in array_time_a], dtype=float), np.array([row[3] for row in array_time_a], dtype=float))
    merged_graph.SetMarkerStyle(21)
    merged_graph.SetMarkerSize(0.5)
    merged_graph.SetMarkerColor(9)
    merged_graph.SetTitle("Merged calibration and beam Fe55 data")
    merged_graph.GetXaxis().SetTitle("Time [h]")
    merged_graph.GetYaxis().SetTitle("Energy scale [keV/ADC]")
    merged_graph.Draw("ap")
    fit = ROOT.TF1("fit_funct", "pol2(0)", 0, 61)
    merged_graph.Fit("fit_funct")
    p0 = fit.GetParameter(0)
    p1 = fit.GetParameter(1)
    p2 = fit.GetParameter(2)
    
    
    directory = '../data/T2/beam_data/Fe55/'
    #directory = '../data/T2/beam_test'
    chain_tree = ROOT.TChain("T2")
    for filename in sorted(glob(directory+'/*.root')):
        chain_tree.Add(filename)
        
    ini_time_file = ROOT.TFile("/home/mvidal/tunl/data/T2/beam_data/Fe55/SIS3316Raw_20180524041524_new.root")
    tree_ini_time = ini_time_file.Get("T2")
    for event in tree_ini_time:
        S15_ch = i_channel(0, event)
        initime = event.UnixStartTime[S15_ch]
        break
    print(initime)    
    h_Fe55_m1 = ROOT.TH1F("h_Fe55_m1", "Fe55 Energy spectrum correction, comparison methods; Energy[ADC]; counts", 150, 0., 20.)
    h_Fe55_m2 = ROOT.TH1F("h_Fe55_m2", "Fe55 Energy spectrum, method 2; Energy[ADC]; counts", 150, 0., 20.)
    
    for i, event in enumerate(chain_tree):
        cut = [0, 0]
        S15_ch = i_channel(0, event)
        time_run = event.UnixStartTime[S15_ch]
        S15_w2=event.DD_AmplADU[S15_ch]
        RT = event.DD_Rise[S15_ch]
        if cut[0]==0:
            if S15_w2>1000. and RT<1.51 and RT>1.1:
                timestamp_event = event.TimeStamp[S15_ch]*4e-9 
                time_event_h = (time_run + timestamp_event - initime)/3600
                #print(time_event_h)
                # 1st method using existing energy scale:
                for j in range(0, len(list_time_a)):
                    index = (np.abs(array_time_a[j][0]-time_event_h)).argmin()
                energy1 = S15_w2*array_time_a[index][1]
                h_Fe55_m1.Fill(energy1)
                cut[0]=1
                # 2nd method using fit function:
                energy_scale = p0 + p1*time_event_h + p2 * time_event_h**2
                energy2 = S15_w2*energy_scale
                h_Fe55_m2.Fill(energy2)
                
   
    c1 = ROOT.TCanvas()                
    h_Fe55_m1.Draw()
    #c2 = ROOT.TCanvas()
    h_Fe55_m2.SetLineColor(6)
    h_Fe55_m2.Draw("same")
    legend = ROOT.TLegend(0.6, 0.7, 0.8, 0.9)
    legend.AddEntry(h_Fe55_m1, "method 1", "l")
    legend.AddEntry(h_Fe55_m2, "method 2", "l")
    legend.Draw('same')
    input()
    
if __name__ == '__main__':
    main()