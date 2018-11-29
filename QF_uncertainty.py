# author: Marie Vidal
# date: 27th of November 2018

#**************************************************************************************************
# calculation of quenching factor with uncertainties 
# extraction of uncertainties from En, angle, Eee and energy scale from files:
# uncertainties_QF_En_Eee_angle.root: provide distribution of the QF regarding those 3 quantities 
# for the 4 energies investigated.
# scale_uncertainty_qf2_5keVnr.root: distribution of the QF regarding energy scale: 5keVnr
# scale_uncertainty_qf2_8keVnr.root: "  "  ": 8 keVnr
# scale_uncertainty_qf2_15keVnr.root: "  "  ": 15 keVnr
# scale_uncertainty_qf2_28keVnr.root: "  "  ": 28 keVnr
# when extracting distibutions assume they are gaussian
#*************************************************************************************************

import ROOT
import numpy as np
from functions_QF import Eee2, mean_sigma, Enr_uncertainty, Recoil_energy_nr
import math

#*************************************************************************************************            # VARIABLES                                                                                                   
En = 3.85                                # neutron energy --> MeV                                             
angles = [9.2, 12.4, 16.2, 22.4]         # list of the scattering angles --> degrees                          
gauss = ROOT.gRandom.Gaus                # gaussian number generator                  
#*************************************************************************************************


# extraction of distributions for En, angle and Eee contribution
f = ROOT.TFile("uncertainties_QF_En_Eee_angle.root")
Eee_uncertainty_5 = f.Get("Eee_5")
Eee_uncertainty_8 = f.Get("Eee_uncertainty_8")
Eee_uncertainty_15 = f.Get("Eee_uncertainty_15")
Eee_uncertainty_28 = f.Get("Eee_uncertainty_28")
f_unc = ROOT.TFile("En_angle_uncertainty.root")
QF_En_5 = f_unc.Get("QF_En_5")
QF_En_8 = f_unc.Get("QF_En_8")
QF_En_15 = f_unc.Get("QF_En_15")
QF_En_28 = f_unc.Get("QF_En_28")
QF_angle_5 = f_unc.Get("QF_angle_5")
QF_angle_8 = f_unc.Get("QF_angle_8")
QF_angle_15 = f_unc.Get("QF_angle_15")
QF_angle_28 = f_unc.Get("QF_angle_28")

# extraction of distribution for energy scale for all the angles:
f_scale = ROOT.TFile("scale_uncertainty_qf2_5keVnr.root")
f_scale_8 = ROOT.TFile("scale_uncertainty_qf2_8keVnr.root")
f_scale_15 = ROOT.TFile("scale_uncertainty_qf2_15keVnr.root")
f_scale_28 = ROOT.TFile("scale_uncertainty_qf2_28keVnr.root")
scale_5 = f_scale.Get("scale")
scale_8 = f_scale_8.Get("scale")
scale_15 = f_scale_15.Get("scale")
scale_28 = f_scale_28.Get("scale")

# energy 5keVnr:
mean_5_En, sigma_5_En = mean_sigma(QF_En_5)
mean_5_angle, sigma_5_angle = mean_sigma(QF_angle_5)
mean_5_Eee, sigma_5_Eee = mean_sigma(Eee_uncertainty_5)
mean_5_a, sigma_5_a = mean_sigma(scale_5)

print("Calculations for 5keVnr:")
print("mean of QF distribution for En:", mean_5_En, "and sigma:", sigma_5_En)
print("mean of QF distribution for angle:", mean_5_angle, "and sigma:", sigma_5_angle)
print("mean of QF distribution for Eee:", mean_5_Eee, "and sigma:", sigma_5_Eee)
print("mean of QF distribution for energy scale:", mean_5_a, "and sigma:", sigma_5_a)
QF_sigma_5 = math.sqrt(sigma_5_En**2+sigma_5_angle**2+sigma_5_Eee**2+sigma_5_a**2)
print("quenching factor uncertainty for energy 5keVnr:", QF_sigma_5)
QF_mean_5 = (mean_5_En+mean_5_angle+mean_5_Eee+mean_5_a)/4
print("quenching factor mean for energy 5keVnr:", QF_mean_5)


# energy 8keVnr:                                                                                                          
mean_8_En, sigma_8_En = mean_sigma(QF_En_8)
mean_8_angle, sigma_8_angle = mean_sigma(QF_angle_8)
mean_8_Eee, sigma_8_Eee = mean_sigma(Eee_uncertainty_8)
mean_8_a, sigma_8_a = mean_sigma(scale_8)

print("Calculations for 8keVnr:")
print("mean of QF distribution for En:", mean_8_En, "and sigma:", sigma_8_En)
print("mean of QF distribution for angle:", mean_8_angle, "and sigma:", sigma_8_angle)
print("mean of QF distribution for Eee:", mean_8_Eee, "and sigma:", sigma_8_Eee)
print("mean of QF distribution for energy scale:", mean_8_a, "and sigma:", sigma_8_a)
QF_sigma_8 = math.sqrt(sigma_8_En**2+sigma_8_angle**2+sigma_8_Eee**2+sigma_8_a**2)
print("quenching factor uncertainty for energy 5keVnr:", QF_sigma_8)
QF_mean_8 = (mean_8_En+mean_8_angle+mean_8_Eee+mean_8_a)/4
print("quenching factor mean for energy 8keVnr:", QF_mean_8)


# energy 15keVnr:
mean_15_En, sigma_15_En = mean_sigma(QF_En_15)
mean_15_angle, sigma_15_angle = mean_sigma(QF_angle_15)
mean_15_Eee, sigma_15_Eee = mean_sigma(Eee_uncertainty_15)
mean_15_a, sigma_15_a = mean_sigma(scale_15)

print("Calculations for 15keVnr:")
print("mean of QF distribution for En:", mean_15_En, "and sigma:", sigma_15_En)
print("mean of QF distribution for angle:", mean_15_angle, "and sigma:", sigma_15_angle)
print("mean of QF distribution for Eee:", mean_15_Eee, "and sigma:", sigma_15_Eee)
print("mean of QF distribution for energy scale:", mean_15_a, "and sigma:", sigma_15_a)
QF_sigma_15 = math.sqrt(sigma_15_En**2+sigma_15_angle**2+sigma_15_Eee**2+sigma_15_a**2)
print("quenching factor uncertainty for energy 15keVnr:", QF_sigma_15)
QF_mean_15 = (mean_15_En+mean_15_angle+mean_15_Eee+mean_15_a)/4
print("quenching factor mean for energy 15keVnr:", QF_mean_15)


# energy 5keVnr:                                                                                                           
mean_28_En, sigma_28_En = mean_sigma(QF_En_28)
mean_28_angle, sigma_28_angle = mean_sigma(QF_angle_28)
mean_28_Eee, sigma_28_Eee = mean_sigma(Eee_uncertainty_28)
mean_28_a, sigma_28_a = mean_sigma(scale_28)

print("Calcultation for 28keVnr:")
print("mean of QF distribution for En:", mean_28_En, "and sigma:", sigma_28_En)
print("mean of QF distribution for angle:", mean_28_angle, "and sigma:", sigma_28_angle)
print("mean of QF distribution for Eee:", mean_28_Eee, "and sigma:", sigma_28_Eee)
print("mean of QF distribution for energy scale:", mean_28_a, "and sigma:", sigma_28_a)
QF_sigma_28 = math.sqrt(sigma_28_En**2+sigma_28_angle**2+sigma_28_Eee**2+sigma_28_a**2)
print("quenching factor uncertainty for energy 28keVnr:", QF_sigma_28)
QF_mean_28 = (mean_28_En+mean_28_angle+mean_28_Eee+mean_28_a)/4
print("quenching factor mean for energy 28keVnr:", QF_mean_28)

# uncertainty on the recoil energy:                                   
Enr_5 = Recoil_energy_nr(En, angles[0])
Enr_8 = Recoil_energy_nr(En, angles[1])
Enr_15 = Recoil_energy_nr(En, angles[2])
Enr_28 = Recoil_energy_nr(En, angles[3])                                                    

#n = 10000
#Enr_5, spread_5 = Enr_uncertainty(n, En, En_sigma, angles[0], angles_spread_h[0])
#Enr_8, spread_8 = Enr_uncertainty(n, En, En_sigma, angles[1], angles_spread_h[1])
#Enr_15, spread_15 = Enr_uncertainty(n ,En, En_sigma, angles[2], angles_spread_h[2])
#Enr_28, spread_28 = Enr_uncertainty(n, En, En_sigma, angles[3], angles_spread_h[3])
#print("\n")
#print("first energy mean:", Enr_5, "and standard deviation:", spread_5)
#print("second energy mean:", Enr_8, "and standard deviation:", spread_8)
#print("third energy mean:", Enr_15, "and standard deviation:", spread_15)
#print("fourth energy mean:", Enr_28, "and standard deviation:", spread_28)
er = np.array([0,0,0,0])
QF = np.array([QF_mean_5, QF_mean_8, QF_mean_15, QF_mean_28])
QF_sigma = np.array([QF_sigma_5, QF_sigma_8, QF_sigma_15, QF_sigma_28])
Enr = np.array([Enr_5, Enr_8, Enr_15, Enr_28])
#Enr_sigma = np.array([spread_5, spread_8, spread_15, spread_28])
QF_graph = ROOT.TGraphErrors(len(QF), Enr, QF, er, QF_sigma)
QF_graph.SetMarkerSize(0.5)
QF_graph.SetMarkerStyle(21)
c1 = ROOT.TCanvas()
QF_graph.SetTitle("quenching factor of Neon at 500mbar as a function of recoil energy")
QF_graph.GetXaxis().SetTitle("Recoil energy [keVnr]")
QF_graph.GetYaxis().SetTitle("Quenching factor")
QF_graph.Draw("ap")
f_qf = ROOT.TFile("QF_vs_Enr.root", "recreate")
QF_graph.Write("QF")
f_qf.Close()
input()
