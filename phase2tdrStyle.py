#! /usr/bin/env python

#=====================================#
#                                     #
#  Original Authors:                  #
#      Alberto Zucchetta              #
#      Jacopo Pazzini                 #
#                                     #
#  2017-07-25                         #
#                                     #
#=====================================#

import os, copy, math
from array import array
from ROOT import ROOT, gROOT, gStyle, gPad, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1, TH1F, TH2F, THStack, TGraph, TGraphAsymmErrors
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TLine, TBox

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

def setCanvas(split=False, r=1.15):

    # create canvas
    can = TCanvas("can", "can", 800, 800 if split else 600)    
    if split:
        can.Divide(1, 2)        
        can.GetPad(1).SetPad('Top', '', 0., 0.25, 1.0, 1.0, 0, -1, 0)
        can.GetPad(1).SetTopMargin(0.06*r)
        can.GetPad(1).SetBottomMargin(0.016*r)
        can.GetPad(1).SetRightMargin(0.04*r)
        can.GetPad(1).SetLeftMargin(0.12*r)
        can.GetPad(1).SetTicks(1, 1)        
        can.GetPad(2).SetPad("Bottom", '', 0., 0., 1.0, 0.25, 0, -1, 0)
        can.GetPad(2).SetTopMargin(0.008*r)
        can.GetPad(2).SetBottomMargin(0.32*r)
        can.GetPad(2).SetRightMargin(0.04*r)
        can.GetPad(2).SetLeftMargin(0.12*r)
        can.GetPad(2).SetTicks(1, 1)     
    else:   
        can.GetPad(0).SetTopMargin(0.06*r)
        can.GetPad(0).SetRightMargin(0.04*r)
        can.GetPad(0).SetLeftMargin(0.12*r)
        can.GetPad(0).SetBottomMargin(0.1*r)
        can.GetPad(0).SetTicks(1, 1)

    can.cd(1)

    return can

def draw(hist, drawhist=False, ratio=False, log=False):
        
    # create canvas
    can = setCanvas(ratio)
    if log:
        can.GetPad(ratio).SetLogy()
        
    # draw histograms
    drawOption = 'HIST' if drawhist else 'E'
    for ih, h in enumerate(hist):
        h.Draw(drawOption if ih == 0 else drawOption+', SAME')
        formatHisto(h)          

    # create ratio wrt hist[0]
    unc = hist[0].Clone('unc')
    unc.SetFillColor(1)
    unc.SetFillStyle(3005)
    unc.SetMarkerSize(0)
    hratio = {}
    if ratio :
        hist[0].GetXaxis().SetLabelOffset(hist[0].GetXaxis().GetLabelOffset()*2)
        can.cd(2)
        unc.SetTitle('')
        unc.GetYaxis().SetTitle('Ratio')
        unc.GetYaxis().CenterTitle()
        for i in range(1, unc.GetNbinsX()+1):
            unc.SetBinContent(i, 1)
            if hist[0].GetBinContent(i) > 0:
                unc.SetBinError(i, hist[0].GetBinError(i)/hist[0].GetBinContent(i))
        formatRatio(unc)
        unc.Draw('E2')        
        for ih, h in enumerate(hist[1:]):
            hratio[ih] = h.Clone('hratio_%d'%ih)
            hratio[ih].Divide(hist[0])
            hratio[ih].Draw('PE0, SAME')

    can.Update()
    can.GetPad(ratio).RedrawAxis()    
    can.cd(ratio)
    
    # return objects created by the draw() function:
    # can    -> TCanvas
    # unc    -> TH1 with uncertainty on hist[0]     (meaningful only if ratio = True)
    # hratio -> dictionary of TH1 ratio wrt hist[0] (meaningful only if ratio = True)
    return can, unc, hratio

def formatHisto(hist, r=1.15):
    hist.GetXaxis().SetTitleSize(hist.GetXaxis().GetTitleSize()*r*r)
    hist.GetXaxis().SetLabelSize(hist.GetXaxis().GetLabelSize()*r*r)
    hist.GetXaxis().SetLabelOffset(hist.GetXaxis().GetLabelOffset()*r*r*r*r*r)
    hist.GetXaxis().SetTitleOffset(hist.GetXaxis().GetTitleOffset())

    hist.GetYaxis().SetTitleSize(hist.GetYaxis().GetTitleSize()*r*r)
    hist.GetYaxis().SetLabelSize(hist.GetYaxis().GetLabelSize()*r*r)
    hist.GetYaxis().SetTitleOffset(hist.GetYaxis().GetTitleOffset()*r*r)

    hist.GetZaxis().SetTitleSize(hist.GetZaxis().GetTitleSize()*r*r)
    hist.GetZaxis().SetLabelSize(hist.GetZaxis().GetLabelSize()*r*r)
    hist.GetZaxis().SetTitleOffset(hist.GetZaxis().GetTitleOffset()*r)

def formatRatio(h, r=4):
    h.GetXaxis().SetLabelSize(h.GetXaxis().GetLabelSize()*(r-1));
    h.GetXaxis().SetLabelOffset(h.GetXaxis().GetLabelOffset()*(r-1)/2);
    h.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize()*(r-1));
    h.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize()*(r-1));
    h.GetYaxis().SetNdivisions(505);
    h.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize()*(r-1));
    h.GetYaxis().SetTitleOffset(h.GetYaxis().GetTitleOffset()/(r-1));
    h.GetYaxis().SetRangeUser(0.4, 1.6)

def drawCMS(onTop=False, r=1.15):
    text='Phase-2 Simulation'
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(62)
    latex.SetTextSize(0.045*r)
    latex.DrawLatex(0.18, 0.85 if not onTop else 0.94, "CMS")
    latex.SetTextSize(0.036*r)
    latex.SetTextFont(52)
    latex.DrawLatex(0.18+0.075*r, 0.85 if not onTop else 0.94, text)
    
def drawEnPu(pileup=None, lumi=None, r=1.15):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.040*r)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    tex = '14 TeV'
    if pileup: tex += ', {0} PU'.format(pileup)
    if lumi: tex = '{0}, '.format(lumi) + tex
    latex.DrawLatex(0.95, 0.94, tex)