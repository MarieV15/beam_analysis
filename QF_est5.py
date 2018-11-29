# Author: Marie Vidal
# date: 21st of November 2018

#**********************************************************************************
# Quenching factor calculation using, interpolation of background spectrum as a function, 
# then fit inside onset window with this function + gaussian
#**********************************************************************************

import ROOT
import numpy as np
from functions_QF import extract_h, Eee, def_hist


f_spectrum = ROOT.TFile("neutron_spectrum_2018-11-26.root")
list_in = []
list_out = []
list_in.append(f_spectrum.Get("signal_5"))
list_in.append(f_spectrum.Get("signal_8"))
list_in.append(f_spectrum.Get("signal_15"))
list_in.append(f_spectrum.Get("signal_28"))
list_out.append(f_spectrum.Get("BG_5"))
list_out.append(f_spectrum.Get("BG_8"))
list_out.append(f_spectrum.Get("BG_15"))
list_out.append(f_spectrum.Get("BG_28"))

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

# eval graph:
x = np.linspace(0, 25, 1000)
y = []
for i in range(0, len(x)):
    y.append(graph.Eval(x[i]))
spectrum = np.array(y, dtype=np.double)
graph2 = ROOT.TGraph(len(x), x, spectrum)
c3 = ROOT.TCanvas()
graph2.Draw()
input()
