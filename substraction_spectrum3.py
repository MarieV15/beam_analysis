#author: Marie Vidal
#date: october 16th 2018
#********************************************************************************************************************************
# Neutron spectrum: substraction spectra for the 4 angles
#********************************************************************************************************************************
import ROOT
from glob import glob
import os
import numpy as np

def main():
    
    f1 = ROOT.TFile("neutron_spectrum_tof_cut_2018-10-16_run6_14-54_bin50.root")
    h_5_in = f1.Get("neutron_spectrum_tof_in4.69keVnr")
    h_5_out = f1.Get("neutron_spectrum_tof_out4.69keVnr")
    h_8_in = f1.Get("neutron_spectrum_tof_in8.33keVnr")
    h_8_out = f1.Get("neutron_spectrum_tof_out8.33keVnr")
    h_15_in = f1.Get("neutron_spectrum_tof_in14.75keVnr")
    h_15_out= f1.Get("neutron_spectrum_tof_out14.75keVnr")
    h_28_in = f1.Get("neutron_spectrum_tof_in27.59keVnr")
    h_28_out = f1.Get("neutron_spectrum_tof_out27.59keVnr")
    
    
    h_sub_5 = ROOT.TH1D("h_sub_5", "Neutron spectrum 4.69 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_8 = ROOT.TH1D("h_sub_8", "Neutron spectrum 8.33 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_15 = ROOT.TH1D("h_sub_15", "Neutron spectrum 14.75 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_28 = ROOT.TH1D("h_sub_28", "Neutron spectrum 27.59 keVnr; Energy [keV]", 50, 0., 25)

    c1 = ROOT.TCanvas()
    h_5_out.Scale(0.098)
    h_sub_5.Add(h_5_in, 1)
    h_sub_5.Add(h_5_out, -1)
    h_sub_5.Draw()
    h_sub_5.Fit("gaus")
    c2 = ROOT.TCanvas()
    h_8_out.Scale(0.098)
    h_sub_8.Add(h_8_in, 1)
    h_sub_8.Add(h_8_out, -1)
    h_sub_8.Draw()
    h_sub_8.Fit("gaus")
    c3 = ROOT.TCanvas()
    h_15_out.Scale(0.098)
    h_sub_15.Add(h_15_in, 1)
    h_sub_15.Add(h_15_out, -1)
    h_sub_15.Draw()
    h_sub_15.Fit("gaus")
    c4 = ROOT.TCanvas()
    h_28_out.Scale(0.098)
    h_sub_28.Add(h_28_in, 1)
    h_sub_28.Add(h_28_out, -1)
    h_sub_28.Draw()
    h_sub_28.Fit("gaus")
    
    input()
    
    
if __name__=='__main__':
    main()