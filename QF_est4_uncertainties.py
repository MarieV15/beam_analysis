# author: Marie Vidal
# date: 19th of November 2018

#**********************************************************************************
# estimation of QF and its uncertainties
# calculation of each uncertainties contribution on quenching factor independently
# uncertainties on neutron energy, angle, Eee, and energy scale
#**********************************************************************************

import ROOT
import numpy as np
from functions_QF import Recoil_energy_nr, extract_h, def_hist, Eee, selection_correction_method1, Eee2
from glob import glob

f_spectrum = ROOT.TFile("neutron_spectrum_2018-11-13_bin50.root")
# extraction of histograms from file: list = [5, 8, 15, 28] keVnr 
list_in, list_out = extract_h(f_spectrum)

# list of histograms for neutron spectra 
list_sub = def_hist()

# calculation of Eee
Eee_5, Eee_5_error = Eee(list_in[0], list_out[0], list_sub[0])
Eee_8, Eee_8_error = Eee(list_in[1], list_out[1], list_sub[1])
Eee_15, Eee_15_error = Eee(list_in[2], list_out[2], list_sub[2])
Eee_28, Eee_28_error = Eee(list_in[3], list_out[3], list_sub[3])

#*********************************************************************************
# VARIABLES
En = 3.85                                # neutron energy --> MeV
En_sigma = 0.385                         # spread of neutron energy --> MeV
angles = [9.2, 12.4, 16.2, 22.4]         # list of the scattering angles --> degrees
angles_spread_l = [0.8, 1, 1.3, 1.7]     # list of low uncertainties on the angles --> degrees
angles_spread_h = [0.8, 1.1, 1.4, 1.8]   # list of high uncertainties on the angles --> degrees
gauss = ROOT.gRandom.Gaus                # gaussian number generator
#*********************************************************************************
f_out = ROOT.TFile("uncertainties_QF2.root", "recreate")

# calculation of uncertainty due to neutron energy
# Eee, angle, a: fixed
# Energy 5keV, angle 9.2:
QF_En = ROOT.TH1D("QF_En", "QF histogram with neutron energy uncertainty; quenching factor; counts", 90, 0, 1)
for i in range(0, 10000):
    n = gauss(En, En_sigma)
    Enr = Recoil_energy_nr(n, angles[0])
    QF = Eee_5/Enr
    QF_En.Fill(QF)
c1 = ROOT.TCanvas()
QF_En.Draw()
QF_En.Write("En_uncertainty")

# calculation of uncertainty due to spread angle
# Eee, En, a: fixed
# Energy 5keV, angle 9.2:
QF_angle = ROOT.TH1D("QF_angle", "QF histogram with angle uncertainty; quenching factor; counts", 90, 0, 1)
for i in range(0, 10000):
    theta = gauss(angles[0], angles_spread_l[0])
    Enr = Recoil_energy_nr(En, theta)
    QF = Eee_5/Enr
    QF_angle.Fill(QF)
c2 = ROOT.TCanvas()
QF_angle.Draw()
QF_angle.Write("angle_uncertainty")

# calculation of uncertainty due to Eee spread
# En, angle, a: fixed
# Energy 5keV, angle 9.2:
QF_Eee = ROOT.TH1D("QF_Eee", "QF histogram with Eee uncertainty; quenching factor; counts", 90, 0, 1)
Enr = Recoil_energy_nr(En, angles[0])
for i in range(0, 10000):
    mean = gauss(Eee_5, Eee_5_error)
    QF = mean/Enr
    QF_Eee.Fill(QF)
c3 = ROOT.TCanvas()
QF_Eee.Draw()    
QF_Eee.Write("Eee")

# calculation of the uncertainty due to the energy scale
# En, angle, Eee: fixed
# Energy 5keV, angle 9.2:
#QF_a = ROOT.TH1D("QF_a", "QF histogram with energy scale uncertainty; quenching factor; counts", 90, 0, 1)
# recover graph with energy scale vs time:
#f_scale = ROOT.TFile("/home/mvidal/tunl/analysis/Fe55_beamchi2_2018-10-05gaus.root")
#g_scale = f_scale.Get("a_vs_time_gaussian")
#g_scale.Draw("ap")
#scale = g_scale.GetY()
#nb = g_scale.GetN()
# conversion ROOT object Buffer to array
#list_a = []
#list_error_a = []
#for i in range(0, nb):
#    list_a.append(scale[i])
#    list_error_a.append(g_scale.GetErrorY(i))
#print(list_a)
#scale_e = np.array(list_a, dtype=np.double)
#scale_error = np.array(list_error_a, dtype=np.double)
#directory = '/home/mvidal/tunl/data/T2/beam_data/neutron/'
# run associated with energy 5keV:
#run4 = directory+'run4'
#files_run4 = []
#for filename in sorted(glob(run4+'/*.root')):
#    files_run4.append(filename)

#list_tree = []
#for f in files_run4:
#    filen = ROOT.TFile(f)
#    tree = filen.Get("T2")
#    list_tree.append(tree)#

#for i in range(0, 8):
#    h_sub = ROOT.TH1D("h_sub"+str(i), "neutron spectrum 5 keVnr; Energy [keV]; counts", 50, 0, 25)
#    print(h_sub)
#    h_sub.Sumw2()
    #print(h_sub)
#    print("a number:", i)
#    for n, t in enumerate(list_tree):
#        print('file number:', n)
#        h_in = ROOT.TH1D("h_inside"+str(i)+str(n), "neutron spectrum with all cuts: inside onset window; Energy [keV]; counts", 50, 0, 25)
#        h_out = ROOT.TH1D("h_outside"+str(i)+str(n), "neutron spectrum with all cuts: outside onset wondow; Energy [keV]; counts", 50, 0, 25)
#        a = scale[7+n]
#        error = scale_error[7+n]
#        print(a)
#        print(error)
#        A = gauss(a, error)
#        
#        h_in, h_out = selection_correction_method1(t, A, h_in, h_out)
        #t.Delete()
        #print(h_sub)
#        h_out.Scale(0.098)
#        h_sub.Add(h_in, 1)
#        h_sub.Add(h_out, -1)
#    Eee5, Eee_error5 = Eee2(h_sub)
#    QF = Eee5/Enr
#    QF_a.Fill(QF)
#c4 = ROOT.TCanvas()
#QF_a.Draw()        
#QF_a.Write("scale")

input()
