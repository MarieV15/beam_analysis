# author: Marie Vidal
# date: 21 of November 2018

#***************************************************************************************
# test on energy scale uncertainty on quenching factor estimation
#***************************************************************************************

import ROOT
import numpy as np
from functions_QF import Recoil_energy_nr, extract_h, def_hist, Eee, selection_correction_method1, Eee2
from glob import glob

En = 3.85
angles = [9.2, 12.4, 16.2, 22.4]
gauss = ROOT.gRandom.Gaus

Enr = Recoil_energy_nr(En, angles[0])
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
directory = '/home/mvidal/tunl/data/T2/beam_data/neutron/'
run4 = directory+'run4'
files_run4 = []
for filename in sorted(glob(run4+'/*.root')):
    files_run4.append(filename)

list_tree = []
f_list = []
for i,f in enumerate(files_run4):
    f_list.append(ROOT.TFile(f))
    filen = f_list[-1]
    #filen = ROOT.TFile(f)
    print(f)
    print(filen.Get('T2'))
    list_tree.append(filen.Get('T2'))
       
print(list_tree)
QF_a = ROOT.TH1D("QF_a", "QF histogram with energy scale uncertainty; quenching factor; counts", 130, 0, 1)

for i in range(0, 100):
    h_sub = ROOT.TH1D("h_sub"+str(i), 'neutron spectrum 5 keVnr; Energy [keV]; counts', 50, 0, 25)
    h_sub.Sumw2()
    print("a number:", i)
    for n, t in enumerate(list_tree):
        h_in = ROOT.TH1D('h_inside'+str(i)+str(n), 'neutron spectrum with all cuts; inside onset window; Energy [keV]; counts', 50 , 0, 25)
        h_out = ROOT.TH1D('h_outside'+str(i)+str(n), 'neutron spectrum with all cuts; outside onset window; Energy [keV]; counts', 50, 0, 25)
        index = 8+n
        a = scale[index]
        #print("original a:", a)
        error = scale_error[index] 
        #print("error:", error)
        A = gauss(a, error)
        #print("a chosen:", A)
        h_in, h_out = selection_correction_method1(t, A, h_in, h_out)
        h_out.Scale(0.098)
        h_sub.Add(h_in, 1)
        h_sub.Add(h_out, -1)
    Eee5, Eee_error5 = Eee2(h_sub)
    QF = Eee5/Enr
    QF_a.Fill(QF)
c = ROOT.TCanvas()
#QF_a.Draw()
f_out = ROOT.TFile("scale_uncertainty_qf2.root", "recreate")
QF_a.Write("scale")
f_out.Close()
input()

