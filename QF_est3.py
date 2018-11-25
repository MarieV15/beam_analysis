# author: Marie Vidal
# date: November 14th 2018

#***********************************************************************************************
# fit neutron and Fe55 events after cuts in energy, rise time, onset and tof.
# uses the mean of the neutron peak to estimate Eee deposited in the detector.
# all functions that I used in this code are in functions_QF
#**********************************************************************************************

import ROOT
import numpy as np
from functions_QF import Recoil_energy_nr, uncertainty_qf

f_in = ROOT.TFile("neutron_spectrum_2018-11-13_bin50.root")
n_h = 4
h_nf5 = f_in.Get("neutron_spectrum_tof_in4.69keVnr")
h_nf8 = f_in.Get("neutron_spectrum_tof_in8.33keVnr")
h_nf15 = f_in.Get("neutron_spectrum_tof_in14.75keVnr")
h_nf27 = f_in.Get("neutron_spectrum_tof_in27.59keVnr")
h_nf5.Sumw2()
h_nf8.Sumw2()
h_nf15.Sumw2()
h_nf27.Sumw2()
f_gaus = ROOT.TF1("f_gaus", "[0]/(sqrt(2*pi)*[1])*exp(-(x-[2])**2/(2*[1]**2))+[3]/(sqrt(2*pi)*[4])*exp(-(x-[5])**2/(2*[4]**2))", 0, 25)
# parameter for 5 keVnr, with 1.3keVee of energy deposited:
f_gaus.SetParameter(0, 27)
f_gaus.SetParameter(1, 0.6)
f_gaus.SetParameter(2, 1.3)
f_gaus.SetParameter(3, 28)
f_gaus.SetParameter(4, 0.8)
f_gaus.SetParameter(5, 5)
h_nf5.Fit("f_gaus", "e")
mean_5 = f_gaus.GetParameter(2)
error_5 = f_gaus.GetParError(2)

# parameter for 8keVnr, with 2.5keVee of energy deposited:
f_gaus.SetParameter(0, 19)
f_gaus.SetParameter(1, 0.7)
f_gaus.SetParameter(2, 2.5)
f_gaus.SetParameter(3, 24)
h_nf8.Fit("f_gaus", "e")
# Get parameters from fit: mean of the gaussian that correspond to energy deposited
mean_8 = f_gaus.GetParameter(2)
error_8 = f_gaus.GetParError(2)

# parameter for 15keVnr, with 6keVee of energy deposited:
f_gaus.SetParameter(0, 27)
f_gaus.SetParameter(1, 0.9)
f_gaus.SetParameter(2, 6)
f_gaus.SetParameter(3, 135)
h_nf15.Fit("f_gaus", "e")
# Get the paramters from fit: mean of gaussian that correspond to energy deposited
mean_15 = f_gaus.GetParameter(2)
error_15 = f_gaus.GetParError(2)

# parameter for 27keVnr, with 10keVee of energy deposited:
f_gaus.SetParameter(0, 150)
f_gaus.SetParameter(1, 4)
f_gaus.SetParameter(2, 10)
f_gaus.SetParameter(3, 65)
h_nf27.Fit("f_gaus", "e")

# Get the parameters from fit: mean of gaussian that correspond to energy deposited
mean_27 = f_gaus.GetParameter(2)
error_27 = f_gaus.GetParError(2)

# calculation of quenching factor:
angles = [9.2, 12.4, 16.2, 22.4]

# uncertainties on the angles, first list is the low uncertainties and second list the high uncertainty:
error_l = [0.8, 1.0, 1.3, 1.7]
error_h = [0.8, 1.1, 1.4, 1.8]
En = 3.85        # neutron energy MeV
error_En = 0.385 # energy resolution of neutron beam
Enr_5 = Recoil_energy_nr(En, angles[0])
Enr_5 *= 1.e3    # conversion in keV

input()
