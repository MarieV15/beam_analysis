# author: Marie Vidal
# date: November 14th 2018

#**********************************************************************
# functions used to calculate quenching factor:
# --> i_channel(pmt_channel, event)
# --> uncertainty_qf(delta_Eee, Eee, delta_Enr, Enr, qf)
# --> Recoil_energy_nr(En, theta)
# --> uncertainty_cos(theta, delta_theta)
# --> uncertainty_sin2(theta, delta_theta)
# --> extract_h(file)
# values for masses: PDG 2012
#*********************************************************************

import ROOT
import math
import numpy as np
gauss = ROOT.gRandom.Gaus

def i_channel(pmt_channel, event):
    """argument: channel we want to find
       argument: event of the tree
       return: channel of the backing detector, sphere or bpm 
    """
    for i in range(len(event.Channel)):
        if event.Channel[i]==pmt_channel:
            return i
    return -1

def Recoil_energy_nr(En, theta):
    """calculate the recoil energy of the nucleus
       argument: En in MeV (energy of the incident neutron)
       argument: theta (scattering angle of neutron)
       return: nuclear recoil energy of the neutron in keV
    """
    mp = 938.272046         # mass proton MeV
    mn = 939.565379         # mass neutron MeV
    Z = 10                  # number of proton in Neon
    N = 10                  # number of neutron in Neon
    mt = Z*mp+N*mn          # mass target: nucleus in MeV
    angle = math.radians(theta)  # angle in radian: need to convert from degree to rad for math.sin and math.cos
    Enr = 2*En*(mn**2/(mn+mt)**2)*((mt/mn)+math.sin(angle)**2-math.cos(angle)*math.sqrt((mt/mn)**2-math.sin(angle)**2))
    return Enr*1e3

def uncertainty_qf(delta_Eee, Eee, delta_Enr, Enr, qf):
    """calculation of quenching factor uncertainties linked with nuclear recoil energy uncertainty and uncertainty on Eee
       argument: uncertainty on energy deposited in detector (error from mean: fit) --> keV
       argument: mean of energy deposited (mean: fit) --> keV
       argument: error in nuclear recoil energy (error comes from angle uncertainty and neutron energy uncertainty) --> keV
       argument: nuclear recoil energy --> keV
       return: quenching factor uncertainty
    """
    list_dqf = []
    for i in range(0, len(Eee)):
        delta_qf = qf[i]*math.sqrt((delta_Eee[i]/Eee[i])**2+(delta_Enr[i]/Enr[i])**2)
        list_dqf.append(delta_qf)
    delta_qf = np.array(list_dqf, dtype=np.double)
    return delta_qf

def uncertainty_cos(theta, delta_theta):
    """calculate the uncertainty of cos theta 
       argument: scattering angle --> degree
       argument: uncertainty of the scattering angle --> degree
       return: uncertainty of cos theta --> radian
    """
    # angle conversion from degree to radian:
    angle = math.radians(theta)
    delta = math.radians(delta_theta)
    return math.abs(-math.sin(angle))*delta

def uncertainty_sin2(theta, delta_theta):
    """calculate the uncertainty of sin^2 theta
       argument: scattering angle --> degree
       argument: uncertainty of the scattering angle --> degree
       return: uncertainty if sin^2 theta --> radian
    """
    # angle conversion from degree to radian
    angle = math.radians(theta)
    delta = math.radians(delta_theta)
    return 2*math.sin(angle)*math.cos(angle)*delta


def extract_h(f1):
    """extract histograms from file
       argument: file
       return: 2 list of histograms, one for histogram that corresponds to inside onset window and the other outside onset 
    """
    h_5_in = f1.Get("neutron_spectrum_tof_in4.69keVnr")
    h_5_out = f1.Get("neutron_spectrum_tof_out4.69keVnr")
    h_8_in = f1.Get("neutron_spectrum_tof_in8.33keVnr")
    h_8_out = f1.Get("neutron_spectrum_tof_out8.33keVnr")
    h_15_in = f1.Get("neutron_spectrum_tof_in14.75keVnr")
    h_15_out= f1.Get("neutron_spectrum_tof_out14.75keVnr")
    h_28_in = f1.Get("neutron_spectrum_tof_in27.59keVnr")
    h_28_out = f1.Get("neutron_spectrum_tof_out27.59keVnr")
    list_in = [h_5_in, h_8_in, h_15_in, h_28_in]
    list_out = [h_5_out, h_8_out, h_15_out, h_28_out]
    return list_in, list_out

def def_hist():
    """neutron histogram definition
       return: list of histograms
    """
    h_sub_5 = ROOT.TH1D("h_sub_5", "Neutron spectrum 4.69 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_8 = ROOT.TH1D("h_sub_8", "Neutron spectrum 8.33 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_15 = ROOT.TH1D("h_sub_15", "Neutron spectrum 14.75 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_28 = ROOT.TH1D("h_sub_28", "Neutron spectrum 27.59 keVnr; Energy [keV]", 50, 0., 25)
    h_sub_5.Sumw2()
    h_sub_8.Sumw2()
    h_sub_15.Sumw2()
    h_sub_28.Sumw2()
    list_sub = [h_sub_5, h_sub_8, h_sub_15, h_sub_28]
    return list_sub

def Eee2(neutron_spectrum):
    """calculation of the energy deposited by nuclear recoil in detector --> quenched energy in electron equivalent
       argument: neutron spectrum
       return: mean and error of the energy deposited in the detector by nuclear recoil
    """
    neutron_spectrum.Fit('gaus')
    results_fit = neutron_spectrum.GetFunction('gaus')
    mean_energy = results_fit.GetParameter(1)
    spread_energy = results_fit.GetParError(1)
    return mean_energy, spread_energy

def Eee(h_in, h_out, neutron_spectrum):
    """calculation of the energy deposited by nuclear recoil in detector --> quenched energy in electron equivalent
       argument: inside onset window: neutron + BG events: energy spectrum --> keV
       argument: outside onset window: BG events: energy spectrum --> keV
       argument: empty histogram for neutron events spectrum: recoils spectrum --> keV
       return: mean and error of the energy deposited in the detector by nuclear recoil
    """
    h_out.Scale(0.098)
    neutron_spectrum.Add(h_in, 1)
    neutron_spectrum.Add(h_out, -1)
    neutron_spectrum.Fit('gaus')
    #neutron_spectrum.Draw()
    #input()
    results_fit = neutron_spectrum.GetFunction('gaus')
    mean_energy = results_fit.GetParameter(1)
    spread_energy = results_fit.GetParError(1)
    return mean_energy, spread_energy

def selection_correction_method1(tree, scale, h_in, h_out):
    """selection and correction in energy of the events
       argument: tree
       argument: energy scale we want to use to correct in energy our data
       argument: histogram for events inside the onset window
       argument: histogram for events outside the onser window
       return: histogram of events passing the cuts: energy in sphere, rise time, onset and tof
    """
    #h_in = ROOT.TH1D("h_in", "neutron spectrum with all cuts: inside onset window; Energy [keV]; counts", 50, 0, 25)
    #h_out = ROOT.TH1D("h_out", "neutron spectrum with all cuts: outside onset window; Energy [keV]; counts", 50, 0, 25)
    for event in tree:
        cut = [0, 0]
        S15_ch = i_channel(0, event)
        bpm_ch = i_channel(4, event)
        RT = event.DD_Rise[S15_ch]
        S15_w2 = event.DD_AmplADU[S15_ch]
        onset = event.DD_Rise10pct[S15_ch]
        if cut[0]==0:
            # first cut: for inside onset window
            # if event passes the first cuts
            if S15_w2>1000 and RT>1.1 and RT<1.51 and onset>39 and onset<47:
                # loop over the pmt channel numbers to calculate the time of flight: time bd - time bpm
                for n_channel in range(5, 16):
                    pmt_i = i_channel(n_channel, event)
                    cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
                    cfd_bpm = event.cfdPulse_CFDNS[bpm_ch]
                    # calculation of the time of flight
                    tof = (cfd_pmt-cfd_bpm)%400
                    #cut on tof: time of flight of the neutron
                    if tof<335 and tof>295:
                        energy2 = S15_w2*scale
                        # fill histogram inside onset window
                        h_in.Fill(energy2)
                        cut[0]=1
                        break
        if cut[1]==0:
            if S15_w2>1000 and RT<1.51 and RT>1.1 and ((onset<36 and onset>15) or (onset>50 and onset<=110)):
                for n_channel in range(5, 16):
                    pmt_i = i_channel(n_channel, event)
                    cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
                    cfd_bpm = event.cfdPulse_CFDNS[bpm_ch]
                    tof = (cfd_pmt-cfd_bpm)%400
                    if tof<335 and tof>295:
                        energy2 = S15_w2*scale
                        h_out.Fill(energy2)
                        cut[1]=1
                        break
    return h_in, h_out
                        
                        
def selection_correction_method1_v2(tree, scale, h_in, h_out):
    """selection and correction in energy of the events
       argument: tree
       argument: energy scale we want to use to correct in energy our data
       argument: histogram for events inside the onset window
       argument: histogram for events outside the onser window
       return: histogram of events passing the cuts: energy in sphere, rise time, onset and tof
    """
    #h_in = ROOT.TH1D("h_in", "neutron spectrum with all cuts: inside onset window; Energy [keV]; counts", 50, 0, 25)
    #h_out = ROOT.TH1D("h_out", "neutron spectrum with all cuts: outside onset window; Energy [keV]; counts", 50, 0, 25)
    for event in tree:
        cut = [0, 0]
        S15_ch = i_channel(0, event)
        bpm_ch = i_channel(4, event)
        RT = event.DD_Rise[S15_ch]
        S15_w2 = event.DD_AmplADU[S15_ch]
        onset = event.DD_Rise10pct[S15_ch]
        if cut[0]==0:
            # first cut: for inside onset window
            # if event passes the first cuts
            if S15_w2>1000 and RT>1.1 and RT<1.51 and onset>39 and onset<47:
                # loop over the pmt channel numbers to calculate the time of flight: time bd - time bpm
                for n_channel in range(5, 16):
                    pmt_i = i_channel(n_channel, event)
                    cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
                    cfd_bpm = event.cfdPulse_CFDNS[bpm_ch]
                    # calculation of the time of flight
                    tof = (cfd_pmt-cfd_bpm)%400
                    #cut on tof: time of flight of the neutron
                    if tof<335 and tof>295:
                        energy2 = S15_w2*scale
                        # fill histogram inside onset window
                        h_in.Fill(energy2)
                        cut[0]=1
                        break
        if cut[1]==0:
            if S15_w2>1000 and RT<1.51 and RT>1.1 and ((onset<36 and onset>15) or (onset>50 and onset<=110)):
                for n_channel in range(5, 16):
                    pmt_i = i_channel(n_channel, event)
                    cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
                    cfd_bpm = event.cfdPulse_CFDNS[bpm_ch]
                    tof = (cfd_pmt-cfd_bpm)%400
                    if tof<335 and tof>295:
                        energy2 = S15_w2*scale
                        h_out.Fill(energy2)
                        cut[1]=1
                        break

def QF_uncertainty_En(trials, En, En_sigma, angle, Eee, QF_En):
    for i in range(0, trials):
        n = gauss(En, En_sigma)
        Enr = Recoil_energy_nr(n, angle)
        QF = Eee/Enr
        QF_En.Fill(QF)
    return QF_En

def QF_uncertainty_angle(trials, En, angle, sigma_angle, Eee, QF_angle):
    for i in range(0, trials):
        theta = gauss(angle, sigma_angle)
        Enr = Recoil_energy_nr(En, theta)
        QF = Eee/Enr
        QF_angle.Fill(QF)
    return QF_angle
    
def QF_uncertainty_Eee(trials, En, angle, Eee, Eee_error, QF_Eee):
    Enr = Recoil_energy_nr(En, angle)
    for i in range(0, 10000):
        mean = gauss(Eee, Eee_error)
        QF = mean/Enr
        QF_Eee.Fill(QF)
    return QF_Eee
