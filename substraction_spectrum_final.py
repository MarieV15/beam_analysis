# author: Marie Vidal                                                                                     
# date: October 11th and November 13th 2018                                                              

#*****************************************************************************************                
# Study of neutron events. Uses the cuts of TOF2.py: energy of event in SPC, rise time,        
# and time of flight.                                                                                     
# To correct in energy the data I use the corresponding energy scale of each file.                        
#*****************************************************************************************                
import ROOT
from substraction_spectrum2 import i_channel
from glob import glob
import numpy as np
from functions_QF import selection_correction_method1_v2, Eee2, Recoil_energy_nr

def neutron_spectrum(directory, scale, index, sub):
    """select and correct event for neutron spectrum
       argument: directory of file
       argument: energy scale array
       argument: index where to start in the energy scale array
       argument: neutron spectrum histrogram empty
       return: filled neutron histogram and signal histogram and BG histogram for each angle
    """
    h_signal = ROOT.TH1D("h_signal"+str(index), "Signal histogram: inside onset window; Energy [keV]; counts", 50, 0, 25)
    h_BG = ROOT.TH1D("h_BG"+str(index), "Background historgram: outside onset window; Energy [keV]; counts", 50, 0, 25)
    trees = []
    for i, filename in enumerate(sorted(glob(directory+'/*.root'))):
        f = ROOT.TFile(filename)
        t = f.Get("T2")
        print(filename)
        h_in = ROOT.TH1D("h_in"+str(i), " inside onset window events; Energy [keV]; counts", 50, 0, 25)
        h_out = ROOT.TH1D("h_out"+str(i), "outside onset window events; Energy [keV]; counts", 50, 0, 25)
        a = scale[index+i]
        selection_correction_method1_v2(t, a, h_in, h_out)
        h_out.Scale(0.098)
        sub.Add(h_in, 1)
        sub.Add(h_out, -1)
        h_signal.Add(h_in, 1)
        h_BG.Add(h_out, 1)
    return h_signal, h_BG
    
    
En = 3.85
angles = [9.2, 12.4, 16.2, 22.4]

# open file, and use graph with energy scale for Fe55 calibration for beam data only                      
f2 = ROOT.TFile("../analysis/Fe55_beam_energy_scale_2018-11-26.root")
graph_beam = f2.Get("a_vs_time_gaussian")
yb = graph_beam.GetY()
nentries = graph_beam.GetN()

list_a = []
for i in range(0, nentries):
    list_a.append(yb[i])
scale = np.array(list_a, dtype=float)

directory = '/home/mvidal/tunl/data/T2/beam_data/neutron/'
list_run = [directory+'run3', directory+'run4', directory+'run5', directory+'run6']

list_QF = []
list_Enr = []
# for energy 5 keV:
h_sub5 = ROOT.TH1D("h_sub", 'neutron spectrum 5 keVnr; Energy [keV]; counts', 50, 0, 25)
h_sub5.Sumw2()
h_signal5, h_BG5 = neutron_spectrum(list_run[1], scale, 8, h_sub5)
Enr_5 = Recoil_energy_nr(En, angles[0])
Eee5, Eee_error5 = Eee2(h_sub5)
QF5 = Eee5/Enr_5
print("Eee5:", Eee5)
print("Enr5:", Enr_5)
list_QF.append(QF5)
list_Enr.append(Enr_5)

# for energy 8 keVnr:
h_sub8 = ROOT.TH1D('h_sub8', "neutron spectrum 8 keVnr; Energy [keV]; counts", 50, 0, 25)
h_sub8.Sumw2()
h_signal8, h_BG8 = neutron_spectrum(list_run[0], scale, 0, h_sub8)
Enr_8 = Recoil_energy_nr(En, angles[1])
Eee8, Eee_error8 = Eee2(h_sub8)
QF8 = Eee8/Enr_8
print("Eee8:", Eee8)
print("Enr8:", Enr_8)
list_QF.append(QF8)
list_Enr.append(Enr_8)

# for energy 15 keVnr:
h_sub15 = ROOT.TH1D("h_sub15", "neutron spectrum 15 keVnr; Energy [keV]; counts", 50, 0, 25)
h_sub15.Sumw2()
h_signal15, h_BG15 = neutron_spectrum(list_run[2], scale, 24, h_sub15)
Enr_15 = Recoil_energy_nr(En, angles[2])
Eee15, Eee_error15 = Eee2(h_sub15)
QF15 = Eee15/Enr_15
list_QF.append(QF15)
list_Enr.append(Enr_15)

# for energy 28 keVnr:
h_sub28 = ROOT.TH1D("h_sub28", "neutron spectrum 28 keVnr; Energy [keV]; counts", 50, 0, 25)
h_sub28.Sumw2()
h_signal28, h_BG28 = neutron_spectrum(list_run[3], scale, 35, h_sub28)
Enr_28 = Recoil_energy_nr(En, angles[3])
Eee28, Eee_error28 = Eee2(h_sub28)
QF28 = Eee28/Enr_28
list_QF.append(QF28)
list_Enr.append(Enr_28)

c2 = ROOT.TCanvas()
QF = np.array(list_QF, dtype=np.double)
print(QF5)
E = np.array(list_Enr, dtype=np.double)
graph = ROOT.TGraph(len(list_QF), E, QF)
graph.GetXaxis().SetTitle('Energy [keV]')
graph.GetYaxis().SetTitle('quenching factor')
graph.SetTitle('Quenching factor as a function of recoil energy')
graph.SetMarkerSize(0.5)
graph.Draw("ap")

f_out = ROOT.TFile("neutron_spectrum_2018-11-26.root", "recreate")
h_signal5.Write("signal_5")
h_BG5.Write("BG_5")
h_signal8.Write("signal_8")
h_BG8.Write("BG_8")
h_signal15.Write("signal_15")
h_BG15.Write("BG_15")
h_signal28.Write("signal_28")
h_BG28.Write("BG_28")
h_sub5.Write("spectrum_5")
h_sub8.Write("spectrum_8")
h_sub15.Write("spectrum_15")
h_sub28.Write("spectrum_28")
graph.Write("QF_estimation")


input()
f_out.Close()
