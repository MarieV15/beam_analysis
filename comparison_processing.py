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
    for index, Tree in enumerate(list_tree):
        h_spectrum = ROOT.TH1F("h_Fe"+str(index), "Fe55 spectrum; Energy [ADC]; counts", 150, 0., 50000.)
        i=0
        for event in Tree:
            S15_ch = i_channel(0, event)
            S15_w2 = event.DD_AmplADU[S15_ch]
            rise_time = event.DD_Rise[S15_ch]
            if i==0:
                time = event.UnixStartTime[S15_ch]
                list_time.append(time)
                i=1
            if S15_w2>1000. and rise_time>1.1 and rise_time<1.51:
                h_spectrum.Fill(S15_w2)
        h_spectrum.Draw()
        fit_data = ROOT.TF1("fit_data", '[0]*(1-[1])/(sqrt(2*pi)*[2])*exp(-([3]*x-5.9)**2/(2*[2]**2))+[0]*[1]/(2*[4])*exp([2]**2/(2*[4]**2)+([3]*x-5.9)/[4])*erfc([2]/(sqrt(2)*[4])+([3]*x-5.9)/(sqrt(2)*[2]))+[5]+[6]*x', 1000., 50000.)
        if index != 2:
            fit_data.SetParLimits(0, 20., 400.)
            fit_data.SetParLimits(1, 0.08, 0.9)
            fit_data.SetParLimits(2, 0.3, 0.8)
            fit_data.SetParLimits(3, 0.0001, 0.0004)
            fit_data.SetParLimits(4, 0.5, 7.)
            fit_data.SetParLimits(5, 0.8, 5.)
            fit_data.SetParameter(6, 0.)
        else:
            fit_data.SetParLimits(0, 300., 800.)
            fit_data.SetParLimits(1, 0.1, 0.7)
            fit_data.SetParLimits(2, 0.4, 0.6)
            fit_data.SetParLimits(3, 0.0001, 0.0004)
            fit_data.SetParLimits(4, 1., 5.)
            fit_data.SetParLimits(5, 1., 5.)
            fit_data.SetParameter(6, 0.)
        h_spectrum.Fit("fit_data", "em")
        print("Energy scale factor a:", fit_data.GetParameter(3))
        list_a.append(fit_data.GetParameter(3))
        input()
    #time_array = np.array(list_time, dtype=float)
    #print(time_array)
    #energy_scale = np.array(list_a, dtype=float)
    #print(energy_scale)
    c2 = ROOT.TCanvas()
    
    time_a = np.array(list_time[0])
    energy_scale = np.array(list_a[0])
    time_a1 = np.array(list_time[1])
    energy_scale1 = np.array(list_a[1])
    time_a2 = np.array(list_time[2])
    energy_scale2 = np.array(list_a[2])
    print("trap+DD time", time_a)
    print("trap+DD a:", energy_scale)
    print("DD time:", time_a1)
    print("DD a:", energy_scale1)
    print("calibration time:", time_a2)
    print("calibration a:", energy_scale2)
    # trap + DD processing
    g = ROOT.TGraph(1, time_a, energy_scale)
    g.GetXaxis().SetTitle("Time [h]")
    g.GetYaxis().SetTitle("Energy scale [keV/ADC]")
    g.SetTitle("Energy scale vs time comparison")
    g.SetMarkerColor(6)
    g.SetMarkerStyle(21)
    g.SetMarkerSize(0.5)
    g.Draw("ap")
    # DD processing
    g2 = ROOT.TGraph(1, time_a1, energy_scale1)
    g2.SetMarkerColor(1)
    g2.SetMarkerStyle(21)
    g2.SetMarkerSize(0.5)
    g2.Draw("same p")
    # calibration data: DD processing
    g3 = ROOT.TGraph(1, time_a2, energy_scale2)
    g3.SetMarkerColor(4)
    g3.SetMarkerStyle(21)
    g3.SetMarkerSize(0.5)
    g3.Draw("same p")
    legend =  ROOT.TLegend(0.6, 0.7, 0.8, 0.9)
    legend.AddEntry(g, "trap + DD: beam data", "p")
    legend.AddEntry(g2, "DD: beam data", "p")
    legend.AddEntry(g3, "DD: calibration", "p")
    input()
    


if __name__ == '__main__':
    main()