#author: Marie Vidal
#date: September 4th 2018
#********************************************************************************************************************************
#first attempt to display the beam data: rise time vs energy, energy spectrum, cut in risetime --> spectrum
#WITH CORRECTION FOR ENERGY
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

def cut(n, chain_tree, a, time_a):
    spectrum_in = ROOT.TH1F("h_in"+str(n), "Energy spectrum of the detector inside onset window; Energy[ADC]; counts", 150, 0., 20.)
    spectrum_out = ROOT.TH1F("h_out"+str(n), "Energy spectrum of the detector outside onset window; Energy[ADC]; counts", 150, 0., 20.)
    rt_in = ROOT.TH2F("rt_in"+str(n), "Rise time vs energy: inside onset window; Energy [ADC]; Rise time [ns]", 200, 0, 20, 200, 0., 3)
    rt_out = ROOT.TH2F("rt_out"+str(n), "Rise time vs energy: outside onset window; Energy [ADC]; Rise time [ns]", 200, 0, 20, 200, 0, 3)
    for event in chain_tree:
        cut = [0, 0]
        S15_ch = i_channel(0, event)
        time = event.UnixStartTime[S15_ch]
        index = (np.abs(time_a-time)).argmin()
        onset10 = event.DD_Rise10pct[S15_ch]
       
        S15_w2=event.DD_AmplADU[S15_ch]
        S15_w2*= a[index]
        RT = event.DD_Rise[S15_ch]
        if cut[0]==0:
            if S15_w2>1000.*a[index] and RT<1.51 and RT>1.1 and onset10>=39. and onset10<=47.:
                spectrum_in.Fill(S15_w2)
                rt_in.Fill(S15_w2, RT)
                cut[0]=1
        if cut[1]==0:
            if S15_w2>1000.*a[index] and RT<1.51 and RT>1.1 and ((onset10<36. and onset10>15.) or (onset10>50. and onset10<=110.)):
                #print(S15_w2)
                spectrum_out.Fill(S15_w2)
                rt_out.Fill(S15_w2, RT)
                cut[1]=1
                
    return spectrum_in, spectrum_out, rt_in, rt_out


def main():
    
    #recover correction of a:
    f = ROOT.TFile("/home/mvidal/tunl/analysis/Fe55_beamchi2_2018-09-11.root")
    graph = f.Get("a_vs_time_calibration")
    time_a = graph.GetX()
    a = graph.GetY()
    nentries = graph.GetN()
    list_timea = []
    for i in range(0, nentries):
        list_timea.append(time_a[i])
    array_time = np.array(list_timea, dtype=float)
    
    f_off = ROOT.TFile("/home/mvidal/tunl/data/T2/beam_off/SIS3316Raw_20180524181418.root")
    tree_off = f_off.Get("T2")
    
    directory = '../data/T2/beam_data/neutron/'
    list_run = [directory+'run3', directory+'run4', directory+'run5', directory+'run6']
    #list_run = [directory+'run3']
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
        spectrum_in, spectrum_out, rt_in, rt_out = cut(n, chain, a, array_time)
        spectrum_inside.append(spectrum_in)
        spectrum_outside.append(spectrum_out)
        risetime_in.append(rt_in)
        risetime_out.append(rt_out)
        
    list_titles = ["Neutron spectrum (39-47micros): 8 keVnr", "Neutron spectrum (39-47micros): 5 keVnr", "Neutron spectrum (39-47micros): 15 keVnr", "Neutron spectrum (39-47micros): 28 keVnr"]  
    for i in range(0, len(list_run)):
        c = ROOT.TCanvas("c"+str(i), "c"+str(i))
        spectrum_inside[i].Draw()
        c1 = ROOT.TCanvas("c1"+str(i), "c1"+str(i))
        spectrum_outside[i].Draw() 
        c2 = ROOT.TCanvas("c2"+str(i), "c2"+str(i))
        h_sub = ROOT.TH1D("h_subs"+str(i), "Neutron spectrum: substraction spectrum; Energy [keV]; counts", 150, 0., 20.)
        spectrum_outside[i].Scale(0.125)
        h_sub.Add(spectrum_inside[i], 1)
        h_sub.Add(spectrum_outside[i], -1)
        h_sub.SetTitle(list_titles[i])
        h_sub.Draw()
        
        input()
    
if __name__=='__main__':
    main()