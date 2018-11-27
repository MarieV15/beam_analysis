# author: Marie Vidal
# date: 19th of November 2018

#**********************************************************************************
# estimation of QF and its uncertainties
# calculation of each uncertainties contribution on quenching factor independently
# uncertainties on neutron energy, angle, Eee
# uncertainty from energy scale is calculated in another code: QF_a_uncertainty.py 
#**********************************************************************************

import ROOT
import numpy as np
from functions_QF import Recoil_energy_nr, extract_h, def_hist, Eee, selection_correction_method1, Eee2, QF_uncertainty_En, QF_uncertainty_angle, QF_uncertainty_Eee
from glob import glob

f_spectrum = ROOT.TFile("neutron_spectrum_2018-11-26.root")
# extraction of histograms from file: list = [5, 8, 15, 28] keVnr 
h_sub5 = f_spectrum.Get('spectrum_5')
h_sub8 = f_spectrum.Get('spectrum_8')
h_sub15 = f_spectrum.Get('spectrum_15')
h_sub28 = f_spectrum.Get('spectrum_28')

# list of histograms for neutron spectra 
list_sub = def_hist()

# calculation of Eee
Eee_5, Eee_5_error = Eee2(h_sub5)
Eee_8, Eee_8_error = Eee2(h_sub8)
Eee_15, Eee_15_error = Eee2(h_sub15)
Eee_28, Eee_28_error = Eee2(h_sub28)

#*********************************************************************************
# VARIABLES
En = 3.85                                # neutron energy --> MeV
En_sigma = 0.385                         # spread of neutron energy --> MeV
angles = [9.2, 12.4, 16.2, 22.4]         # list of the scattering angles --> degrees
angles_spread_l = [0.8, 1, 1.3, 1.7]     # list of low uncertainties on the angles --> degrees
angles_spread_h = [0.8, 1.1, 1.4, 1.8]   # list of high uncertainties on the angles --> degrees
gauss = ROOT.gRandom.Gaus                # gaussian number generator
#*********************************************************************************
f_out = ROOT.TFile("uncertainties_QF2_5keVnr.root", "recreate")

# calculation of uncertainty due to neutron energy
# Eee, angle, a: fixed
# Energy 5keV, angle 9.2:
c1 = ROOT.TCanvas()
QF_En_5 = ROOT.TH1D("QF_En_5", "QF histogram with neutron energy uncertainty 5keVnr; quenching factor; counts", 90, 0, 1)
QF_uncertainty_En(10000, En, En_sigma, angles[0], Eee_5, QF_En_5)
QF_En_5.Draw()
QF_En_5.Write("En_uncertainty_5")

# calculation of uncertainty due to spread angle
# Eee, En, a: fixed
# Energy 5keV, angle 9.2:
QF_angle_5 = ROOT.TH1D("QF_angle_5", "QF histogram with angle uncertainty 5keVnr; quenching factor; counts", 90, 0, 1)
QF_uncertainty_angle(10000, En, angles[0], angles_spread_l[0], Eee_5, QF_angle_5)
c2 = ROOT.TCanvas()
QF_angle_5.Draw()
QF_angle_5.Write("angle_uncertainty_5")

# calculation of uncertainty due to Eee spread
# En, angle, a: fixed
# Energy 5keV, angle 9.2:
QF_Eee_5 = ROOT.TH1D("QF_Eee_5", "QF histogram with Eee uncertainty 5keVnr; quenching factor; counts", 90, 0, 1)
QF_uncertainty_Eee(10000, En, angles[0], Eee_5, Eee_5_error, QF_Eee_5)
c3 = ROOT.TCanvas()
QF_Eee_5.Draw()    
QF_Eee_5.Write("Eee_5")

# calculation of QF uncertainty due to neutron energy
# Energy 8keVnr, angle 12.4:
c4 = ROOT.TCanvas()
QF_En_8 = ROOT.TH1D("QF_En_8", "QF histogram with neutron energy uncertainty 8keVnr; Energy [keV]; counts", 90, 0, 1)
QF_uncertainty_En(10000, En, En_sigma, angles[1], Eee_8, QF_En_8)
QF_En_8.Draw()
QF_En_8.Write("En_uncertainty_8")

#calculation of the uncertainty due to spread of the angle
# energy 8 keVnr, angle 12.4:
QF_angle_8 = ROOT.TH1D("QF_angle_8", "QF histogram with angle uncertainty 8 keVnr; Energy [keV]; counts", 90, 0, 1)
QF_uncertainty_angle(10000, En, angles[1], angles_spread_h[1], Eee_8, QF_angle_8)
c5 = ROOT.TCanvas()
QF_angle_8.Draw()
QF_angle_8.Write("angle_uncertainty_8")

# calculation of the uncertainty due to Eee spread
# Energy 8keVnr, 12.4:
QF_Eee_8 = ROOT.TH1D("QF_Eee_8", "QF histogram with Eee uncertainty 8 keVnr; Energy [keV]; counts", 90, 0, 1)
c6 = ROOT.TCanvas()
QF_uncertainty_Eee(10000, En, angles[1], Eee_8, Eee_8_error, QF_Eee_8)
QF_Eee_8.Draw()
QF_Eee_8.Write("Eee_uncertainty_8")

# calculation for 15 keVnr, 16.2 angle:
#calculation of QF uncertainty due to En
QF_En_15 = ROOT.TH1D("QF_En_15", "QF histogram with En uncertainty 15 keVnr; Energy [keV]; counts", 90, 0, 1)
c7 = ROOT.TCanvas()
QF_uncertainty_En(10000, En, En_sigma, angles[2], Eee_15, QF_En_15)
QF_En_15.Draw()
QF_En_15.Write("En_uncertainty_15")

# calculation of QF uncertainty due to angle:
QF_angle_15 = ROOT.TH1D("QF_angle_15", "QF histogran with angle uncertainty 15 keVnr; Energy [keV]; counts", 90, 0, 1)
c8 = ROOT.TCanvas()
QF_uncertainty_angle(10000, En, angles[2], angles_spread_h[2], Eee_15, QF_angle_15)
QF_angle_15.Draw()
QF_angle_15.Write("angle_uncertainty_15")

# calculation of QF uncertainty due to Eee:
QF_Eee_15 = ROOT.TH1D("QF_Eee_15", "QF histogram with Eee uncertainty 15 keVnr; Energy [keV]; counts", 90, 0, 1)
c9 = ROOT.TCanvas()
QF_uncertainty_Eee(10000, En, angles[2], Eee_15, Eee_15_error, QF_Eee_15)
QF_Eee_15.Draw()
QF_Eee_15.Write("Eee_uncertainty_15")

# calculation for 28 keVnr, 22.4 angle:
# calculation QF uncertainty due to En spread
QF_En_28 = ROOT.TH1D("QF_En_28", "QF histogram with En uncertainty 28 keV; Energy [keV]; counts", 90, 0, 1)
c10 = ROOT.TCanvas()
QF_uncertainty_En(10000, En, En_sigma, angles[3], Eee_28, QF_En_28)
QF_En_28.Draw()
QF_En_28.Write("En_uncertainty_28")

# calculation QF uncertainty due to angle spread
QF_angle_28 = ROOT.TH1D("QF_angle_28", "QF histogram angle uncertainty 28 keVnr; Energy [keV]; counts", 90, 0,1)
c11 = ROOT.TCanvas()
QF_uncertainty_angle(10000, En, angles[3], angles_spread_h[3], Eee_28, QF_angle_28)
QF_angle_28.Draw()
QF_angle_28.Write("angle_uncertainty_28")

# calculation QF uncertainty due to Eee spread
QF_Eee_28 = ROOT.TH1D("QF_Eee_28", "QF histogram Eee uncertainty 28 keVnr; Energy [keV]; counts", 90, 0, 1)
c12 = ROOT.TCanvas()
QF_uncertainty_Eee(10000, En, angles[3], Eee_28, Eee_28_error, QF_Eee_28)
QF_Eee_28.Draw()
QF_Eee_28.Write("Eee_uncertainty_28")

input()
