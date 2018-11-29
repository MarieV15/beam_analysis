# author: Marie Vidal
# date: 28th November 2018

import ROOT
import math
from functions_QF import QF_uncertainty_En, QF_uncertainty_angle, mean_sigma

f = ROOT.TFile("neutron_spectrum_2018-11-26.root")
spectrum_5 = f.Get("spectrum_5")
spectrum_8 = f.Get("spectrum_8")
spectrum_15 = f.Get("spectrum_15")
spectrum_28 = f.Get("spectrum_28")

n_5 = spectrum_5.Integral()
n_8 = spectrum_8.Integral()
n_15 = spectrum_15.Integral()
n_28 = spectrum_28.Integral()

# uncertainty on En mean
unc_5 = 0.385/math.sqrt(n_5)
unc_8 = 0.385/math.sqrt(n_8)
unc_15 = 0.385/math.sqrt(n_15)
unc_28 = 0.385/math.sqrt(n_28)

# uncertainty on angle mean
unc_angle_5 = 0.8/math.sqrt(n_5)
unc_angle_8 = 1.1/math.sqrt(n_8)
unc_angle_15 = 1.4/math.sqrt(n_15)
unc_angle_28 = 1.8/math.sqrt(n_28)

print(unc_5, unc_8, unc_15, unc_28)
print(unc_angle_5, unc_angle_8, unc_angle_15, unc_angle_28)

QF_En_5 = ROOT.TH1D("QF_En_5", "En contribution to QF distribution", 90, 0, 1)
QF_En_8 = ROOT.TH1D("QF_En_8", "En contribution to QF distribution", 90, 0 ,1)
QF_En_15 = ROOT.TH1D("QF_En_15", "En contribution to QF distribution", 90, 0 ,1)
QF_En_28 = ROOT.TH1D("QF_En_28", "En contribution to QD distribution", 90, 0 ,1)

QF_angle_5 = ROOT.TH1D("QF_angle_5", "angle contribution to QF distribution", 90 , 0 ,1)
QF_angle_8 = ROOT.TH1D("QF_angle_8", " angle contribution to QF distribution", 90, 0 ,1)
QF_angle_15 = ROOT.TH1D("QF_angle_15", "angle contribution to QF distribution", 90, 0, 1)
QF_angle_28 = ROOT.TH1D("QF_angle_28", "angle contribution to QF distribution", 90, 0, 1)


En = 3.85
trials = 5000
angles = [9.2, 12.4, 16.2, 22.4]
f_spectrum = ROOT.TFile("neutron_spectrum_2018-11-26.root")
h_5 = f_spectrum.Get("spectrum_5")
h_8 = f_spectrum.Get("spectrum_8")
h_15 = f_spectrum.Get("spectrum_15")
h_28 = f_spectrum.Get("spectrum_28")

mean_5, sigma_5 = mean_sigma(h_5)
mean_8, sigma_8 = mean_sigma(h_8)
mean_15, sigma_15 = mean_sigma(h_15)
mean_28, sigma_28 = mean_sigma(h_28)

QF_uncertainty_En(trials, En, unc_5,angles[0], mean_5, QF_En_5)
QF_uncertainty_En(trials, En, unc_8, angles[1],mean_8, QF_En_8)
QF_uncertainty_En(trials, En, unc_15, angles[2], mean_8, QF_En_15)
QF_uncertainty_En(trials, En, unc_28, angles[3], mean_28, QF_En_28)

QF_uncertainty_angle(trials, En, angles[0], unc_angle_5, mean_5, QF_angle_5)
QF_uncertainty_angle(trials, En, angles[1], unc_angle_8, mean_8, QF_angle_8)
QF_uncertainty_angle(trials, En, angles[2], unc_angle_15, mean_15, QF_angle_15)
QF_uncertainty_angle(trials, En, angles[3], unc_angle_28, mean_28, QF_angle_28)

f_out = ROOT.TFile("En_angle_uncertainty.root", "recreate")
QF_En_5.Write("QF_En_5")
QF_En_8.Write("QF_En_8")
QF_En_15.Write("QF_En_15")
QF_En_28.Write("QF_En_28")
QF_angle_5.Write("QF_angle_5")
QF_angle_8.Write("QF_angle_8")
QF_angle_15.Write("QF_angle_15")
QF_angle_28.Write("QF_angle_28")

print("End program")
