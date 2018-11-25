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

def list_tree(directory):
    """return a list of tree
    """
    trees = []
    f_list = [] 
    for filename in sorted(glob(directory+'/*.root')):
        f = ROOT.TFile(filename)
        f_list.append(f)
        trees.append(f.Get('T2'))
    print(trees)
    return trees

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

list_tree5 = []
list_tree5 = list_tree(list_run[0])
#list_tree8 = list_tree(list_run[1])
#list_tree15 = list_tree(list_run[2])
#list_tree28 = list_tree(list_run[3])

print(list_tree5)
#list_QF = []
#list_Enr = []
# for energy 5 keV:
#h_sub5 = ROOT.TH1D("h_sub", 'neutron spectrum 5 keVnr; Energy [keV]; counts', 50, 0, 25)
#h_sub5.Sumw2()
#for i, tree in enumerate(list_tree5):
#    h_in = ROOT.TH1D('h_inside'+str(i), 'neutron spectrum with all cuts; inside onset window; Energy [keV]; counts', 50 , 0, 25)
#    h_out = ROOT.TH1D('h_outside'+str(i), 'neutron spectrum with all cuts; outside onset window; Energy [keV]; counts', 50, 0, 25)
#    index = 8+i
#    a = scale[index]
#    h_in, h_out = selection_correction_method1(tree, a, h_in, h_out)
#    h_out.Scale(0.098)
#    h_sub5.Add(h_in, 1)
#    h_sub5.Add(h_out, -1)
#Enr_5 = Recoil_energy_nr(En, angles[0])
#Eee5, Eee_error5 = Eee2(h_sub5)
#QF5 = Eee5/Enr5
#list_QF.append(QF5)
#list_Enr.append(Enr_5)
#h_sub5.Draw()
#c2 = ROOT.TCanvas()
#QF = np.array(list_QF, dtype=np.double)
#E = np.array(list_Enr, dtype=np.double)
#graph = ROOT.TGraph(len(list_QF), E, QF)
#graph.GetXaxis().SetTitle('Energy [keV]')
#graph.GetYaxis().SetTitle('quenching factor')
#graph.SetTitle('Quenching factor as a function of recoil energy')
#graph.Draw()



input()
f_out.Close()
