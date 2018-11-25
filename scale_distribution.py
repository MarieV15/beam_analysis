# author: Marie Vidal
# date: 21st of November

# check energy scale on Fe55 peak mean distribution

import ROOT
import numpy as np
from functions_QF import i_channel
gauss = ROOT.gRandom.Gaus

f = ROOT.TFile("/home/mvidal/tunl/data/T2/beam_data/neutron/run4/SIS3316Raw_20180524195005_new.root")
tree = f.Get("T2")

f_scale = ROOT.TFile('/home/mvidal/tunl/analysis/Fe55_beamchi2_2018-10-05gaus.root')
g_scale = f_scale.Get('a_vs_time_gaussian')
scale = g_scale.GetY()
nb = g_scale.GetN()
list_a = []
list_a_error = []
for i in range(0, nb):
    list_a.append(scale[i])
    list_a_error.append(g_scale.GetErrorY(i))
scale_e = np.array(list_a, dtype=np.double)
scale_error = np.array(list_a_error, dtype=np.double)
a = scale_e[8]
error = scale_error[8]
print("original a:", a)
print("error on a:", error)
h_mean = ROOT.TH1D("h_mean", "distribution of the mean of the Fe55; Energy [keV]; counts", 100, 0, 10)
for i in range(0, 20):
    h = ROOT.TH1D("h"+str(i), "Fe55 spectrum; Energy [keV]; counts", 100, 0, 10)
    A = gauss(a, error)
    print("scale chosen:", A)
    for event in tree:
        S15_ch = i_channel(0, event)
        RT = event.DD_Rise[S15_ch]
        S15_w2 = event.DD_AmplADU[S15_ch]
        if S15_w2>1000 and RT>1.1 and RT<1.51:
            energy = S15_w2*A
            h.Fill(energy)
    h.Fit("gaus", "q")
    results = h.GetFunction("gaus")
    mean_result = results.GetParameter(1)
    h_mean.Fill(mean_result)

c2 = ROOT.TCanvas()
h_mean.Draw()
input()
        
