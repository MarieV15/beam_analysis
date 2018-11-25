#author: Marie Vidal
#date: November 8th 2018
#*****************************************************************************
# quit code to obtain onset window
#*****************************************************************************
import ROOT
from beam_data1 import i_channel
from glob import glob

def main():
    directory = '../data/T2/beam_data/neutron/run4/'
    chain_tree = ROOT.TChain("T2")
    for filename in glob(directory+'*.root'):
        chain_tree.Add(filename)
        
    h_onset = ROOT.TH1D('h_onset', 'Time spectrum of the signal window (onset); Time [micros]; counts', 100, 0, 130)

    for event in chain_tree:
        cut = 0
        S15_ch = i_channel(0, event)
        S15_energy = event.DD_AmplADU[S15_ch]
        RT = event.DD_Rise[S15_ch]
        onset = event.DD_Rise10pct[S15_ch]
        #for i in range(5, 16):
        #    pmt_i = i_channel(i, event)
        #    bpm_channel = i_channel(4, event)
        #    cfd_pmt = event.cfdPulse_CFDNS[pmt_i]
        #    cfd_bpm = event.cfdPulse_CFDNS[bpm_channel]
        #    if cut ==0:
        #        if S15_energy>1000. and RT>1.1 and RT<1.51 and cfd_pmt>0 and cfd_pmt<1600 and cfd_bpm>0 and cfd_bpm<1600:
        if RT<1.51 and RT>1.1:
            h_onset.Fill(onset)

    h_onset.Draw()
    input()
    



if __name__ == '__main__':
    main()
