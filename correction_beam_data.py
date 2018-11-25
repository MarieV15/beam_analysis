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
    # 2 first histograms for psd cut:
    h_rt = ROOT.TH2F("h_rt"+str(n), "Rise time vs energy of sphere with psd>1.3 cut; Energy [ADC]; Rise time [micros]", 250, 0., 20., 250, 0., 10.)
    h_energy = ROOT.TH1F("h_energy"+str(n), "Energy spectrum of the detector; Energy[ADC]; counts", 150, 0., 20.)
    # energy spectrum and onset with rise time cut:
    spectr_rt_cut = ROOT.TH1F("spectr_rt_cut"+str(n), "Energy spectrum of the detector; Energy[ADC]; counts", 150, 0., 20.)
    h_onset10 = ROOT.TH1F("h_onset10"+str(), "Onset 10; [micros]; counts", 120, 0., 130.)
    #h_onset25 = ROOT.TH1F("h_onset25"+str(), "Onset 25", 150, 0., 130.)
    #h_onset75 = ROOT.TH1F("h_onset75"+str(), "Onset 75", 150, 0., 130.)
    #h_onset90 = ROOT.TH1F("h_onset90"+str(), "Onset 90", 150, 0., 130.)
    #energy spctrum with rise time and onset cuts:
    spectrum_rt_onset_cut = ROOT.TH1F("spectrum_rt_onset"+str(n), "Energy spectrum of the detector with rise time and onset cuts; Energy [ADC]; counts", 150, 0., 20.)
    for event in chain_tree:
        cut = [0, 0, 0, 0]
        S15_ch = i_channel(0, event)
        time = event.UnixStartTime[S15_ch]
        index = (np.abs(time_a-time)).argmin()
        onset10 = event.DD_Rise10pct[S15_ch]
        #onset25 = event.DD_Rise25pct[S15_ch]
        #onset75 = event.DD_Rise75pct[S15_ch]
        #onset90 = event.DD_Rise90pct[S15_ch]
        for channel in range(5, 16):
            pmt_i =  i_channel(channel, event)
            S15_w2=event.DD_AmplADU[S15_ch]
            S15_w2*= a[index]
            RT = event.DD_Rise[S15_ch]
            if cut[0]==0:
                if S15_w2>1000.*a[index]:
                    h_rt.Fill(S15_w2, RT)
                    h_energy.Fill(S15_w2)
                    cut[0]=1
            if cut[1]==0:
                if S15_w2>1000.*a[index] and RT<1.51 and RT>1.1:
                    spectr_rt_cut.Fill(S15_w2)
                    h_onset10.Fill(onset10)
                    cut[1]=1
            if cut[2]==0:
                if S15_w2>1000.*a[index] and RT<1.51 and RT>1.1 and onset10>=39. and onset10<=45.:
                    spectrum_rt_onset_cut.Fill(S15_w2)
                    cut[2]=1
                
    return h_rt, h_energy, spectr_rt_cut, h_onset10, spectrum_rt_onset_cut
            
            
def main():
    #recover correction of a:
    f = ROOT.TFile("/home/mvidal/tunl/analysis/Fe55_cal.root")
    graph_calibration = f.Get("a_vs_time_calibration")
    time_a = graph_calibration.GetX()
    a = graph_calibration.GetY()
    nentries = graph_calibration.GetN()
    list_timea = []
    for i in range(0, nentries):
        list_timea.append(time_a[i])
    array_time = np.array(list_timea, dtype=float)
    
    f_off = ROOT.TFile("/home/mvidal/tunl/data/T2/beam_off/SIS3316Raw_20180524181418.root")
    tree_off = f_off.Get("T2")
    
    directory = '../data/T2/beam_data/neutron/'
    #list_run = [directory+'run3', directory+'run4', directory+'run5', directory+'run6']
    list_run = [directory+'run5']
    list_chaintree = []
    rt_h = []
    spectrum = []
    cut_spectrum_rt = []
    onset10 = []
    rt_onset_cuts = []
    
    h_rt_off = ROOT.TH2F("h_rt_off", "Rise time vs energy for beam off data; Energy [ADC]; Rise time [micros]", 250, 0., 20., 250, 0., 10.)
    h_spectrum_off = ROOT.TH1F("h_spectrum_off", "Spectrum of beam off; Energy [ADC]; rise time [micros]", 150, 0., 20.)
    h_spectrum_off_cut = ROOT.TH1F("h_spectrum_off_cut", " Spectrum of beam off: Energy [ADC]; Rise time [micros]", 150, 0., 20.)
    i=0
    for event in tree_off:
        S15_ch = i_channel(0, event)
        S15_w2=event.DD_AmplADU[S15_ch]
        RT = event.DD_Rise[S15_ch]
        if i==0:
            time = event.UnixStartTime[S15_ch]
            index = (np.abs(array_time-time)).argmin()
        if S15_w2>1000.:
            h_rt_off.Fill(S15_w2*a[index], RT)
            h_spectrum_off.Fill(S15_w2*a[index])
            if RT<1.48 and RT>1.1:
                h_spectrum_off_cut.Fill(S15_w2*a[index])
    
    for run in list_run:
        print("run:", run)
        chain_tree = ROOT.TChain("T2")
        for filename in glob(run+'/*.root'):
            chain_tree.Add(filename)
        list_chaintree.append(chain_tree)
    
    
    for n, chain in enumerate(list_chaintree):
        h_rt, h_spectrum, h_spectrum_rt_cut, h_10, h_rt_onset_cut = cut(n, chain, a, array_time)
        rt_h.append(h_rt)
        spectrum.append(h_spectrum)
        cut_spectrum_rt.append(h_spectrum_rt_cut)
        onset10.append(h_10)
        rt_onset_cuts.append(h_rt_onset_cut)
       
    
    for i in range(0, len(list_run)):
        c = ROOT.TCanvas("c"+str(i), "c"+str(i))
        c.Divide(2,1)
        c.cd(1)
        rt_h[i].Draw("colz")
        c.cd(2)
        spectrum[i].Draw()
        c5 = ROOT.TCanvas("c1"+str(i), "c1"+str(i))
        c5.Divide(2,1)
        c5.cd(1)
        cut_spectrum_rt[i].Draw() 
        c5.cd(2)
        rt_onset_cuts[i].Draw()
        c2 = ROOT.TCanvas("c2"+str(i), "onset"+str(i))
        onset10[i].Draw()
        input()
    
    c1 = ROOT.TCanvas()
    c1.Divide(2,1)
    c1.cd(1)
    h_rt_off.Draw("col")
    c1.cd(2)
    h_spectrum_off.Draw()
    c3 = ROOT.TCanvas()
    h_spectrum_off_cut.Draw()
    input()
    #c1 = ROOT.TCanvas("c1", "run3: 12degree-8keVnr")
    #rt_h[0].Draw("colz")
    #c5 = ROOT.TCanvas()
    #c5.Divide(2,1)
    #c5.cd(1)
    #cut_rt[0].Draw("colz")
    #c5.cd(2)
    #cut_spectrum[0].Draw()
    
    
if __name__=='__main__':
    main()