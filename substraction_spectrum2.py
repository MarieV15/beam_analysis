#author: Marie Vidal
#date: September 2th 2018
#********************************************************************************************************************************
# Neutron spectrum: merging of the energy scale calibration and beam data calibration
#********************************************************************************************************************************
import ROOT
from glob import glob
import os
import numpy as np

def i_channel(pmt_channel, event):
    for i in range(len(event.Channel)):
        if event.Channel[i]==pmt_channel:
            return i
    return -1

def cut(n, chain_tree, time_a, p0, p1, p2, initime):
    """n: number of runs considered
       chain_tree: chain of tree for 1 run
       time_a: double list of time and energy scale
       return: spectrum with cuts (energy, rise time, onset) and rise time vs energy.
    """
    spectrum_in = ROOT.TH1F("h_in"+str(n), "Energy spectrum of the detector inside onset window; Energy[ADC]; counts", 100, 0., 20.)
    spectrum_out = ROOT.TH1F("h_out"+str(n), "Energy spectrum of the detector outside onset window; Energy[ADC]; counts", 100, 0., 20.)
    rt_in = ROOT.TH2F("rt_in"+str(n), "Rise time vs energy: inside onset window; Energy [ADC]; Rise time [ns]", 200, 0, 20, 200, 0., 3)
    rt_out = ROOT.TH2F("rt_out"+str(n), "Rise time vs energy: outside onset window; Energy [ADC]; Rise time [ns]", 200, 0, 20, 200, 0, 3)
    for i, event in enumerate(chain_tree):
        cut = [0, 0]
        S15_ch = i_channel(0, event)
        time_run = event.UnixStartTime[S15_ch]
        S15_w2=event.DD_AmplADU[S15_ch]
        RT = event.DD_Rise[S15_ch]
        onset10 = event.DD_Rise10pct[S15_ch]
        if cut[0]==0:
            if S15_w2>1000. and RT<1.51 and RT>1.1 and onset10>39. and onset10<47.:
                timestamp_event = event.TimeStamp[S15_ch]*4e-9 
                time_event_h = (time_run + timestamp_event - initime)/3600
                energy_scale = p0 + p1*time_event_h + p2 * time_event_h**2
                energy2 = S15_w2*energy_scale
                spectrum_in.Fill(energy2)
                rt_in.Fill(energy2, RT)
                cut[0]=1
        if cut[1]==0:
            if S15_w2>1000. and RT<1.51 and RT>1.1 and ((onset10<36. and onset10>15.) or (onset10>50. and onset10<=110.)):
                timestamp_event = event.TimeStamp[S15_ch]*4e-9 
                time_event_h = (time_run + timestamp_event - initime)/3600
                energy_scale = p0 + p1*time_event_h + p2 * time_event_h**2
                energy2 = S15_w2*energy_scale
                spectrum_out.Fill(energy2)
                rt_out.Fill(energy2, RT)
                cut[1]=1
    return spectrum_in, spectrum_out, rt_in, rt_out


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
    
    ini_time_file = ROOT.TFile("/home/mvidal/tunl/data/T2/beam_data/Fe55/SIS3316Raw_20180524041524_new.root")
    tree_ini_time = ini_time_file.Get("T2")
    for event in tree_ini_time:
        S15_ch = i_channel(0, event)
        initime = event.UnixStartTime[S15_ch]
        break
    
    f_out = ROOT.TFile("neutron_spectrum_2018-10-17_run6.root", "recreate")
    
    directory = '../data/T2/beam_data/neutron/'
    list_run = [directory+'run3', directory+'run4', directory+'run5', directory+'run6']
    #list_run = [directory+'run6']
    list_chaintree = []
    
    spectrum_inside = []
    spectrum_outside = []
    risetime_in = []
    risetime_out = []
    
    for run in list_run:
        print("run:", run)
        chain_tree = ROOT.TChain("T2")
        for filename in sorted(glob(run+'/*.root')):
            chain_tree.Add(filename)
        list_chaintree.append(chain_tree)
    
    for n, chain in enumerate(list_chaintree):
        spectrum_in, spectrum_out, rt_in, rt_out = cut(n, chain, array_time_a, p0, p1, p2, initime)
        spectrum_inside.append(spectrum_in)
        spectrum_outside.append(spectrum_out)
        #risetime_in.append(rt_in)
        #risetime_out.append(rt_out)
        
    #list_titles = ["Neutron spectrum (39-47micros): 8 keVnr", "Neutron spectrum (39-47micros): 5 keVnr", "Neutron spectrum (39-47micros): 15 keVnr", "Neutron spectrum (39-47micros): 28 keVnr"] 
    titles = ["8.33keVnr", '4.69keVnr', '14.75keVnr', '27.59keVnr']
    for i in range(0, len(list_run)):
        c = ROOT.TCanvas("c"+str(i), "c"+str(i))
        spectrum_inside[i].Draw()
        spectrum_inside[i].Write('spectrum_inside_'+titles[i])
        #risetime_in[i].GetXaxis().SetTitle("Energy [keV]")
        #risetime_in[i].GetYaxis().SetTitle("Rise time [ns]")
        #risetime_in[i].SetTitle("Rise time vs energy: inside onset window"+ str(titles[i]))
        #risetime_in[i].Draw("colz")
        c1 = ROOT.TCanvas("c1"+str(i), "c1"+str(i))
        spectrum_outside[i].Draw() 
        spectrum_outside[i].Write("spectrum_outside"+titles[i])
        #risetime_out[i].GetXaxis().SetTitle("Energy [keV]")
        #risetime_out[i].GetYaxis().SetTitle("Rise time [ns]")
        #risetime_out[i].SetTitle("Rise time vs energy: outside onset window"+ str(titles[i]))
        #risetime_out[i].Draw("colz")
        c2 = ROOT.TCanvas("c2"+str(i), "c2"+str(i))
        h_sub = ROOT.TH1D("h_subs"+str(i), "Neutron spectrum: substraction spectrum; Energy [keV]; counts", 100, 0., 20.)
        spectrum_outside[i].Scale(0.098)
        h_sub.Add(spectrum_inside[i], 1)
        h_sub.Add(spectrum_outside[i], -1)
        h_sub.SetTitle(list_titles[i])
        h_sub.Draw()
        h_sub.Write("neutron_spectrum"+titles[i])
        
        input()
    f_out.Close()
    
if __name__=='__main__':
    main()