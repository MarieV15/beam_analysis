# author: Marie Vidal
# date: 7th September 2018

import ROOT
from glob import glob
import numpy as np

def i_channel(pmt_channel, event):
    for i in range(len(event.Channel)):
        if event.Channel[i]==pmt_channel:
            return i
    return -1
    
def rise_time(tree, hist):
    for event in tree:
        S15_ch = i_channel(0, event)
        S15_w2 = event.DD_AmplADU[S15_ch]
        rise_time = event.DD_Rise[S15_ch]
        if S15_w2>1000.:
            hist.Fill(S15_w2, rise_time)
    return hist
    
def main():
    # file from trap filter + DD processing:
    #f = ROOT.TFile("/home/mvidal/tunl/data/T2/beam_data/Fe55/SIS3316Raw_20180525154302_new.root")
    f = ROOT.TFile("/home/mvidal/tunl/data/T2/beam_data/Fe55/SIS3316Raw_20180526094504_new.root")
    tree = f.Get("T2")
    # file from DD processing:
    #f_DD = ROOT.TFile("/home/mvidal/tunl/data/test_DD/SIS3316Raw_20180525154302.root")
    f_DD = ROOT.TFile("/home/mvidal/tunl/data/test_DD/SIS3316Raw_20180526094504.root")
    tree_DD = f_DD.Get("T2")
    # calibration file:
    f_calibration = ROOT.TFile("/home/mvidal/tunl/data/T2/calibration/SIS3316Raw_20180526093950.root")
    tree_cal = f_calibration.Get("T2")
    list_tree = [tree, tree_DD, tree_cal]
    list_time = []
    list_a = []
    h_rt_DD = ROOT.TH2F("h_rt_DD", "Rise time vs time: DD processing; Energy [ADC]; Rise time [micros]", 250, 0., 50000., 250, 0., 10.)
    h_rt_DDtrap = ROOT.TH2F("h_rt_DDtrap", "Rise time vs time: DD processing; Energy [ADC]; Rise time [micros]", 250, 0., 50000., 250, 0., 10.)
    h_rt_calibration = ROOT.TH2F("h_rt_DD", "Rise time vs time: DD processing; Energy [ADC]; Rise time [micros]", 250, 0., 50000., 250, 0., 10.)
    h_DD = rise_time(tree_DD, h_rt_DD)
    h_DDtrap = rise_time(tree, h_rt_DD)
    h_cal = rise_time(tree_cal, h_rt_calibration)
    c = ROOT.TCanvas()
    c.Divide(2,1)
    c.cd(1)
    h_DDtrap.Draw("colz")
    c.cd(2)
    h_DD.Draw("colz")
    c2 = ROOT.TCanvas()
    h_cal.Draw("colz")
    
    input()
    


if __name__ == '__main__':
    main()