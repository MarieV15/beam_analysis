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
from functions_QF import selection_correction_method1, Eee2, Recoil_energy_nr

def neutron_spectrum(directory, scale, index, sub):
    """select and correct event for neutron spectrum
       argument: directory of file
       argument: energy scale array
       argument: index where to start in the energy scale array
       argument: neutron spectrum histrogram empty
       return: filled neutron histogram
    """
    trees = []
    for i, filename in enumerate(sorted(glob(directory+'/*.root'))):
        f = ROOT.TFile(filename)
        t = f.Get("T2")
        print(filename)
        h_in = ROOT.TH1D("h_in"+str(i), " inside onset window events; Energy [keV]; counts", 50, 0, 25)
        h_out = ROOT.TH1D("h_out"+str(i), "outside onset window events; Energy [keV]; counts", 50, 0, 25)
        a = scale[index+i]
        selection_correction_method1(t, a, h_in, h_out)
        h_out.Scale(0.098)
        sub.Add(h_in, 1)
        sub.Add(h_out, -1)
    
    
En = 3.85
angles = [9.2, 12.4, 16.2, 22.4]

# open file, and use graph with energy scale for Fe55 calibration for beam data only                      
f2 = ROOT.TFile("../analysis/Fe55_beamchi2_2018-10-05gaus.root")
graph_beam = f2.Get("a_vs_time_gaussian")
yb = graph_beam.GetY()
nentries = graph_beam.GetN()

list_a = []
for i in range(0, nentries):
    list_a.append(yb[i])
scale = np.array(list_a, dtype=float)

f_out = ROOT.TFile("neutron_spectrum_2018-11-13_bin50.root", "recreate")
directory = '/home/mvidal/tunl/data/T2/beam_data/neutron/'
list_run = [directory+'run3', directory+'run4', directory+'run5', directory+'run6']

list_QF = []
list_Enr = []
# for energy 5 keV:
h_sub5 = ROOT.TH1D("h_sub", 'neutron spectrum 5 keVnr; Energy [keV]; counts', 50, 0, 25)
h_sub5.Sumw2()
neutron_spectrum(list_run[1], scale, 8, h_sub5)
Enr_5 = Recoil_energy_nr(En, angles[0])
Eee5, Eee_error5 = Eee2(h_sub5)
QF5 = Eee5/Enr_5
print("Eee5:", Eee5)
print("Enr5:", Enr_5)
list_QF.append(QF5)
list_Enr.append(Enr_5)
#h_sub5.Draw()
c2 = ROOT.TCanvas()
QF = np.array(list_QF, dtype=np.double)
print(QF5)
E = np.array(list_Enr, dtype=np.double)
graph = ROOT.TGraph(len(list_QF), E, QF)
graph.GetXaxis().SetTitle('Energy [keV]')
graph.GetYaxis().SetTitle('quenching factor')
graph.SetTitle('Quenching factor as a function of recoil energy')
graph.Draw()



input()
f_out.Close()
