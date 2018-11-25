# author: Marie Vidal
# date: 23rd of November 2018

#**********************************************************************
# energy vs onset 
#**********************************************************************

import ROOT
import numpy as np
from functions_QF import i_channel
from glob import glob

directory = '/home/mvidal/tunl/data/T2/beam_data/neutron/run4/'
files = []
for filename in sorted(glob(directory+'*.root')):
    files.append(filename)

list_tree = []
list_file = []
for f in files:
    F = ROOT.TFile(f)
    list_file.append(F)
    list_tree.append(F.Get("T2"))

print(list_tree)
#f = ROOT.TFile('/home/mvidal/tunl/data/T2/beam_data/neutron/run4/SIS3316Raw_20180524195005_new.root')
#tree = f.Get("T2")

h_e_onset = ROOT.TH2D("h_e_onset", "energy vs onset for beam data; onset [micros]; energy [keV]", 200, 0, 120, 200, 0, 20)

f_scale = ROOT.TFile('/home/mvidal/tunl/analysis/Fe55_beamchi2_2018-10-05gaus.root')
g_scale = f_scale.Get('a_vs_time_gaussian')
scale = g_scale.GetY()
print(scale[8])

for i,tree in enumerate(list_tree):
    for event in tree:
        cut = 0
        S15_ch = i_channel(0, event)
        energy = event.DD_AmplADU[S15_ch]
        onset = event.DD_Rise10pct[S15_ch]
        RT = event.DD_Rise[S15_ch]
        if energy>1000 and RT>1.1 and RT<1.51:
            for i in range(5, 16):
                pmt_i = i_channel(i, event)
                bpm_ch = i_channel(4, event)
                cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
                cfd_bpm = event.cfdPulse_CFDNS[bpm_ch]
                if cut == 0:
                    if cfd_pmt>0 and cfd_pmt<1600 and cfd_bpm>0 and cfd_bpm<1600:
                        h_e_onset.Fill(onset, energy*scale[8+i])

h_e_onset.Draw()
input()
