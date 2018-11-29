# Author: Marie Vidal
# date: 22nd of November 2018

#***************************************************************************************                             
# test on energy scale uncertainty on quenching factor estimation                                                      #***************************************************************************************                               

import ROOT
import numpy as np
from functions_QF import Recoil_energy_nr, extract_h, def_hist, Eee, selection_correction_method1, Eee2
from glob import glob

def list_histograms(a1, error1, tree1, n):
    # list of histograms h_in and h_out:                                                                             
    list_hin = []
    list_hout = []
    # loop over trials of a                                                                                           
    for a in range(0, 5):
        print(a)
        sc_e = gauss(a1, error1)
        #h_a.Fill(sc_e)
        h_in = ROOT.TH1D("h_in"+str(a)+str(n), "histogram inside onset window", 50, 0, 25)
        h_out = ROOT.TH1D("h_out"+str(a)+str(n), "histogram outside onset window", 50, 0, 25)
        h_in, h_out = selection_correction_method1(tree1, sc_e, h_in, h_out)
        list_hin.append(h_in)
        list_hout.append(h_out.Scale(0.098))
    return list_hin, list_hout


#En = 3.85
#angle = 9.2
#Enr = Recoil_energy_nr(En, angle)
#gauss = ROOT.gRandom.Gaus
#
#f_scale = ROOT.TFile('/home/mvidal/tunl/analysis/Fe55_beamchi2_2018-10-05gaus.root')
#g_scale = f_scale.Get('a_vs_time_gaussian')
#scale = g_scale.GetY()
#nb = g_scale.GetN()
#list_a = []
#list_a_error = []
#for i in range(0, nb):
#    list_a.append(scale[i])
#    list_a_error.append(g_scale.GetErrorY(i))
#f_scale.Close()
#scale_e = np.array(list_a, dtype=np.double)
#scale_error = np.array(list_a_error, dtype=np.double)
#
#f1 = ROOT.TFile('/home/mvidal/tunl/data/T2/beam_data/neutron/run4/SIS3316Raw_20180524195005_new.root')
#tree1 = f1.Get("T2")
##a1 = scale_e[8]
##error1 = scale_error[8]
#test_tree = []
#test_tree.append(tree1)
#f2 = ROOT.TFile('/home/mvidal/tunl/data/T2/beam_data/neutron/run4/SIS3316Raw_20180524212808_new.root')
#tree2 = f2.Get("T2")
#test_tree.append(tree2)
#f3 = ROOT.TFile('/home/mvidal/tunl/data/T2/beam_data/neutron/run4/SIS3316Raw_20180524223643_new.root')
#tree3 = f3.Get("T2")
#test_tree.append(tree3)
#print(test_tree)



directory = '/home/mvidal/tunl/data/T2/beam_data/neutron/run4/'
list_tree = []
k = 0
flist = []
for filename in sorted(glob(directory+'*.root')):
    f = ROOT.TFile(filename)
    flist.append(f)
    #f = flist[-1]
    list_tree.append(f.Get("T2"))
    print(f)
    print(f.Get('T2'))
    #f.Close()
    if k==2:
        break
    k+=1
print(list_tree)
exit()
# list of lists of histograms:
list_in = []
list_out = []
for i,t in enumerate(list_tree):
    h_in, h_out = list_histograms(scale_e[8+i], scale_error[8+i], t, i)
    list_in.append(h_in)
    list_out.append(h_out)

h_QF = ROOT.TH1D("h_QF", "Distribution of the quenching factor considering energy scale", 50, 0, 1)

for j in range(0, len(list_in[0])):
    hsub = ROOT.TH1D("hsub"+str(j), "neutron spectrum; energy [keV]; counts", 50, 0, 25)
    for i in range(0, len(list_in)):
        hsub.Add(list_in[i][j], 1)
        hsub.Add(list_out[i][j], -1)
    mean, spread = Eee2(hsub)
    QF = mean/Enr
    h_QF.Fill(QF)
plot = ROOT.TCanvas()
h_QF.Draw()
    
# list of histograms h_in and h_out:
#list_hin1 = []
#list_hout1 = []

#h_a = ROOT.TH1D('h_a', "distribution of a", 50, 0.00025, 0.00029)
# loop over trials of a
#for a in range(0, 10):
#    print(a)
#    sc_e = gauss(a1, error1)
#    h_a.Fill(sc_e)
#    h_in = ROOT.TH1D("h_in"+str(a), "histogram inside onset window", 50, 0, 25)
#    h_out = ROOT.TH1D("h_out"+str(a), "histogram outside onset window", 50, 0, 25)
#    h_in, h_out = selection_correction_method1(tree1, sc_e, h_in, h_out)
#    list_hin1.append(h_in)
#    list_hout1.append(h_out)


    

input()
    
