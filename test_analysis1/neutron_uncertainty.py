# author: Marie Vidal
# date: 16th of November 2018

#***********************************************************************************
# calculation of the contribution of the neutron energy uncertainty on the quenching
# factor estimation.
# use of a Monte Carlo 
#***********************************************************************************

import ROOT

gauss = ROOT.gRandom.Gaus
h = ROOT.TH1D("h_gaus", "neutron energy distribution; Energy [MeV]; counts", 100, 0, 10)
for i in range(0, 1000):
    h.Fill(gauss(3.85, 0.385))
h.Draw()
h.Fit("gaus", "q")
input()
