# author: Marie Vidal
# date: October 11th 2018

import ROOT
from substraction_spectrum2 import i_channel
from glob import glob
import numpy as np


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
print(list_time_a)    
for i in range(0, nentries_c):
    list_time_a.append([x[i], y[i], graph_calibration.GetErrorX(i), graph_calibration.GetErrorX(i)])
array_time_a = np.array(list_time_a, dtype=float)
    
merged_graph = ROOT.TGraphErrors(len(list_time_a), np.array([row[0] for row in array_time_a], dtype=float), np.array([row[1] for row in array_time_a], dtype=float), np.array([row[2] for row in array_time_a], dtype=float), np.array([row[3] for row in array_time_a], dtype=float))
#merged_graph.SetMarkerStyle(21)
#merged_graph.SetMarkerSize(0.5)
#merged_graph.SetMarkerColor(9)
#merged_graph.SetTitle("Merged calibration and beam Fe55 data")
#merged_graph.GetXaxis().SetTitle("Time [h]")
#merged_graph.GetYaxis().SetTitle("Energy scale [keV/ADC]")
#merged_graph.Draw("ap")
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


f_out = ROOT.TFile("neutron_spectrum_tof_cut_2018-10-16_run6_14-54_bin50.root", "recreate")

directory = '../data/T2/beam_data/neutron/'
list_run = [directory+'run3', directory+'run4', directory+'run5', directory+'run6']
#list_run = [directory+'run6']


list_chaintree = []
for run in list_run:
    print("run:", run)
    chain_tree = ROOT.TChain("T2")
    for filename in sorted(glob(run+'/*.root')):
        chain_tree.Add(filename)
    list_chaintree.append(chain_tree)
            
print("coucou")
titles = ["8.33keVnr", '4.69keVnr', '14.75keVnr', '27.59keVnr']

for n, chain in enumerate(list_chaintree):
    #loop over the list of chain tree: all files of run3 together, run4 together etc.
    #h_TOF = ROOT.TH1D("h_tof", "TOF neutron", 250, 0, 500)
    h_inside = ROOT.TH1D("h_inside"+str(n), "neutron spectrum with TOF cut: in onset window; Energy [keV]; counts", 50, 0, 25)
    h_outside = ROOT.TH1D("h_outside"+str(n), "neutron spectrum with TOF cut: out onset window; Energy [keV]; counts", 50, 0, 25)
    for event in chain:
        #loop over the elements of one chain tree: 1 run (run3, 4 etc.)
        cut = [0, 0]
        S15_ch = i_channel(0, event)
        bpm_ch = i_channel(4, event)
        RT = event.DD_Rise[S15_ch]
        time_run = event.UnixStartTime[S15_ch]
        S15_w2 = event.DD_AmplADU[S15_ch]
        onset10 = event.DD_Rise10pct[S15_ch]
        if cut[0]==0:
            #first cut: for inside window onset
            #h_TOF.Fill(tof)
            #inside onset window (same cut as in substraction_spectrum2.py):
            if S15_w2>1000. and RT<1.51 and RT>1.1 and onset10>39. and onset10<47.:
                # if event passes the first cuts (applied on sphere energy, rise time etc)
                # loop over the pmt channel numbers to calculate the time of flight: time pmt - time bpm
                for n_channel in range(5, 16): 
                    pmt_i = i_channel(n_channel, event)
                    cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
                    cfd_bpm = event.cfdPulse_CFDNS[bpm_ch]
                    # calculation of the tof for events that pass first cut
                    tof = (cfd_pmt-cfd_bpm)%400.
                    # cut on tof: time of flight of neutrons
                    # if tof passes cut then selection, energy scale calculation, energy correction of the event
                    if tof<335 and tof>295:
                        timestamp_event = event.TimeStamp[S15_ch]*4e-9 
                        time_event_h = (time_run + timestamp_event - initime)/3600
                        energy_scale = p0 + p1*time_event_h + p2 * time_event_h**2
                        energy2 = S15_w2*energy_scale
                        # fill histogram with energy corrected for events that pass cuts
                        h_inside.Fill(energy2)
                        # set cut[0]=1 to allow event to pass the next range of cuts (outside onset window spectrum)
                        cut[0]=1
                        #exit the loop over the PMTs if event passes all cuts
                        break
        # same cuts as previously (opposite for onset cut)
        if cut[1]==0:
            if S15_w2>1000. and RT<1.51 and RT>1.1 and ((onset10<36. and onset10>15.) or (onset10>50. and onset10<=110.)):
                for n_channel in range(5, 16): #loop over the pmt channel numbers
                    #print("n_channel:", n_channel)
                    pmt_i = i_channel(n_channel, event)
                    w2 = event.rawInput_w2[pmt_i]
                    cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
                    cfd_bpm = event.cfdPulse_CFDNS[bpm_ch]
                    tof = (cfd_pmt-cfd_bpm)%400.
                    if tof<335 and tof>295:
                        timestamp_event = event.TimeStamp[S15_ch]*4e-9 
                        time_event_h = (time_run + timestamp_event - initime)/3600
                        energy_scale = p0 + p1*time_event_h + p2 * time_event_h**2
                        energy2 = S15_w2*energy_scale
                        h_outside.Fill(energy2)
                        cut[1]=1
                        break

    c1 = ROOT.TCanvas()
    h_outside.Draw()
    h_outside.Write("neutron_spectrum_tof_out"+titles[n])
    #h_TOF.Draw()
    c2 = ROOT.TCanvas("c"+str(n), "c"+str(n))
    h_inside.Draw()
    h_inside.Write("neutron_spectrum_tof_in"+titles[n])
input()
f_out.Close()
        
