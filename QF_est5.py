# Author: Marie Vidal
# date: 21st of November 2018

#**********************************************************************************
# Quenching factor calculation using, interpolation of background spectrum as a function, 
# then fit inside onset window with this function + gaussian
#**********************************************************************************

import ROOT
import numpy as np
from functions_QF import extract_h, Eee, def_hist


f_spectrum = ROOT.TFile("neutron_spectrum_2018-11-13_bin50.root")
list_in, list_out = extract_h(f_spectrum)

h_in = list_in[0]
h_out = list_out[0]

# get a function from h_out: 
# 1st step h_out --> TGraph
# 2nd step TGraph --> Interpolate --> function

c1 = ROOT.TCanvas()
h_out.Draw()

print('Hello')
size_h = h_out.GetSize()-2
#print(size_h)
energies = []
counts = []
for i in range(0, size_h):
    counts.append(h_out.GetBinContent(i))
    energies.append(h_out.GetXaxis().GetBinCenter(i))
x = np.array(energies, dtype=np.double)
y = np.array(counts, dtype=np.double)

c2 = ROOT.TCanvas()
graph = ROOT.TGraph(len(energies), x, y)
graph.SetMarkerStyle(21)
graph.SetMarkerSize(0.5)
graph.Draw("ap")
input()
