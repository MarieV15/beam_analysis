#author: Marie Vidal
#date: August 31st 2018
#*********************************************************************************************************************************
#first attempt to display the beam data: rise time vs energy, energy spectrum, cut in risetime --> spectrum
#no correction applied
#*********************************************************************************************************************************
import ROOT
from glob import glob
import os

def i_channel(pmt_channel, event):
    for i in range(len(event.Channel)):
        if event.Channel[i]==pmt_channel:
            return i
    return -1

def display(n, chain_tree, h_rt, h_spectrum):
    h_cut = ROOT.TH1F("h_cut"+str(n), "Beam spectrum with cut in rise time: S15 triggered, run; Energy [ADC]; counts", 200, 0., 130000.)
    for event in chain_tree:
        S15_ch = i_channel(0, event)
        S15_w2 = event.DD_AmplADU[S15_ch]
        RT = event.DD_Rise[S15_ch]
        if S15_w2>1000.:
            h_rt.Fill(S15_w2, RT)
            h_spectrum.Fill(S15_w2)
            if RT>1.1 and RT<1.55:
                h_cut.Fill(S15_w2)
    return h_rt, h_spectrum, h_cut

def main():
    directory = '../data/T2/beam_data/neutron/'
    list_run = [directory+'run3', directory+'run4', directory+'run5', directory+'run6']
    list_chaintree = []
    for run in list_run:
        print("run:", run)
        chain_tree = ROOT.TChain("T2")
        for filename in glob(run+'/*.root'):
            chain_tree.Add(filename)
            #print("number of entries chain tree:",chain_tree.GetEntries())
        list_chaintree.append(chain_tree)
    #print("list chain tree:", list_chaintree)
    rt_h = []
    spectrum = []
    cut = []
    for n, chain in enumerate(list_chaintree):
        h_rt = ROOT.TH2F("h_rt"+str(n), "Rise time vs energy: beam data, run; Energy [ADC]; Rise time [micros]", 250, 0., 130000., 150, 0., 10.)
        h_spectrum = ROOT.TH1F("h_spectrum"+str(n), "Beam spectrum: S15 triggered, run; Energy [ADC]; counts", 200, 0., 130000.)
        h_rt, h_spectrum, h_cut = display(n, chain, h_rt, h_spectrum)
        rt_h.append(h_rt)
        spectrum.append(h_spectrum)
        cut.append(h_cut)
     
    c1 = ROOT.TCanvas("c1", "run3: 12degree-8keVnr")
    c1.Divide(2,1)
    c1.cd(1)
    rt_h[0].Draw("colz")
    c1.cd(2)
    spectrum[0].Draw()
    
    c2 = ROOT.TCanvas("c2", "run4: 9degree-5keVnr")
    c2.Divide(2,1)
    c2.cd(1)
    rt_h[1].Draw("colz") 
    c2.cd(2)
    spectrum[1].Draw()
    
    c3 = ROOT.TCanvas("c3", "run5: 16degree-15keVnr")
    c3.Divide(2,1)
    c3.cd(1)
    rt_h[2].Draw("colz")
    c3.cd(2)
    spectrum[2].Draw()
    
    c4 = ROOT.TCanvas("c4", "run6: 22degree-28keVnr")
    c4.Divide(2,1)
    c4.cd(1)
    rt_h[3].Draw("colz")
    c4.cd(2)
    spectrum[3].Draw()
    
    c5 = ROOT.TCanvas("c5", "run3: 12degree-8keVnr")
    cut[0].Draw()
    c6 = ROOT.TCanvas("c6", "run4: 9degree-5keVnr")
    cut[1].Draw()
    c7 = ROOT.TCanvas("c7", "run5: 16degree-15keVnr")
    cut[2].Draw()
    c8 = ROOT.TCanvas("c8", "run6: 22degree-28keVnr")
    cut[3].Draw()
    input()
    
if __name__=='__main__':
    main()