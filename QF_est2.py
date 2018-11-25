#author: Marie Vidal
#date: october 16th 2018
#********************************************************************************************************************************
# Neutron spectrum: merging of the energy scale calibration and beam data calibration
# TOF cut
#********************************************************************************************************************************
import ROOT
from glob import glob
import os
import numpy as np
import math
from functions_QF import Recoil_energy_nr

def uncertainty(delta_Eee, Eee, delta_Enr, Enr, qf):
    list_dqf = []
    for i in range(0, len(Eee)):
        delta_qf = qf[i]*math.sqrt((delta_Eee[i]/Eee[i])**2+(delta_Enr[i]/Enr[i])**2)
        list_dqf.append(delta_qf)
    delta_qf = np.array(list_dqf, dtype=np.double)
    return delta_qf

def main():
    
    f1 = ROOT.TFile("neutron_spectrum_2018-11-13_bin50.root")
    h_5_in = f1.Get("neutron_spectrum_tof_in4.69keVnr")
    h_5_out = f1.Get("neutron_spectrum_tof_out4.69keVnr")
    h_8_in = f1.Get("neutron_spectrum_tof_in8.33keVnr")
    h_8_out = f1.Get("neutron_spectrum_tof_out8.33keVnr")
    h_15_in = f1.Get("neutron_spectrum_tof_in14.75keVnr")
    h_15_out= f1.Get("neutron_spectrum_tof_out14.75keVnr")
    h_28_in = f1.Get("neutron_spectrum_tof_in27.59keVnr")
    h_28_out = f1.Get("neutron_spectrum_tof_out27.59keVnr")
    list_in = [h_5_in, h_8_in, h_15_in, h_28_in]
    list_out = [h_5_out, h_8_out, h_15_out, h_28_out]
    
    
    h_sub_5 = ROOT.TH1D("h_sub_5", "Neutron spectrum 4.69 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_8 = ROOT.TH1D("h_sub_8", "Neutron spectrum 8.33 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_15 = ROOT.TH1D("h_sub_15", "Neutron spectrum 14.75 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_28 = ROOT.TH1D("h_sub_28", "Neutron spectrum 27.59 keVnr; Energy [keV]", 50, 0., 25)
    list_sub = [h_sub_5, h_sub_8, h_sub_15, h_sub_28]
    h_sub_5.Sumw2()
    h_sub_8.Sumw2()
    h_sub_15.Sumw2()
    h_sub_28.Sumw2()
    
    list_recoil = []
    list_error_recoil = []
    for i in range(0, 4):
        c1 = ROOT.TCanvas("c1"+str(i), "c1"+str(i))
        list_out[i].Scale(0.098)
        list_sub[i].Add(list_in[i], 1)
        list_sub[i].Add(list_out[i], -1)
        list_sub[i].Draw("E")
        list_sub[i].Fit("gaus")
        fit = list_sub[i].GetFunction("gaus")
        list_recoil.append(fit.GetParameter(1))
        list_error_recoil.append(fit.GetParError(1))
        c2 = ROOT.TCanvas("c2"+str(i), "c"+str(i))
        list_in[i].Draw()
        list_out[i].SetLineColor(2)
        list_out[i].Draw("same")
        legend = ROOT.TLegend(0.1, 0.7, 0.48, 0.9)
        legend.AddEntry(list_out[i], "histogram of events outside onset window", "l")
        legend.AddEntry(list_in[i], "histogram of events inside onset window", "l")
        legend.Draw("same")
        #input()
    
    
    #energy neutron beam:
    energy_n = 3850 # keV
    energy_n_err = energy_n*10/100
    list_angles = [9, 12, 16, 22]
    list_nr = [4.953, 8.977, 15.2678, 28.963]
    list_qf = []
    #list_error_qf = []
    for i in range(0, 4):
        print("Angle:", list_angles[i])
        print("Recoil energy ee:", list_recoil[i])
        print("Recoil energy nr", list_nr[i])
        QF = list_recoil[i]/list_nr[i]
        print("QF=Eee/Enr:", QF)
        list_qf.append(QF)
        #err_qf = QF*math.sqrt((list_error_recoil[i]/list_recoil[i])**2+(energy_n_err/energy_n)**2)
        #list_error_qf.append(err_qf)
    
    f_out = ROOT.TFile("estimation_qf.root", "recreate")
    c = ROOT.TCanvas()
    E_nr = np.array(list_nr, dtype=float)
    print("len of E_nr:", len(E_nr))
    qf = np.array(list_qf, dtype=float)
    error_Enrl = np.array([0.66, 1.15, 1.96, 3.63])
    error_Enrh = np.array([0.66, 1.19, 2.02, 3.71])
    error_qfl = uncertainty(list_error_recoil, list_recoil, error_Enrl, E_nr, qf)
    error_qfh = uncertainty(list_error_recoil, list_recoil, error_Enrh, E_nr, qf)
    print("error on mean:", list_error_recoil)
    print("qf for:", qf)
    print("error l on qf:", error_qfl)
    #graph = ROOT.TGraphErrors(len(list_angles), E_recoil, qf, err_x, qf_err)
    graph = ROOT.TGraphAsymmErrors(len(E_nr), E_nr, qf, error_Enrl, error_Enrh, error_qfl, error_qfh)
    graph.GetXaxis().SetTitle("Recoil energy [keV]")
    graph.GetYaxis().SetTitle("Quenching factor")
    graph.SetTitle("QF measurement: 1st estimation")
    graph.GetYaxis().SetRangeUser(0, 1)
    graph.GetXaxis().SetLimits(0, 30)
    c.Update()
    graph.SetMarkerStyle(20)
    graph.Draw("ap")
    graph.Write("qf_vs_energy")
    h_sub_5.Write("5_nr")
    h_sub_8.Write("8_nr")
    h_sub_15.Write("15_nr")
    h_sub_28.Write("28_nr")
    #lindhard = ROOT.TF1("lindhard", "[0]*", 0, 30)
    input()
    
    
if __name__=='__main__':
    main()
