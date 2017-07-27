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

import phase2tdrStyle
from ROOT import TH1F, TH2F, TLegend, gStyle



### declare and fill histos
histo_a = TH1F('histo_a','200 PU;some var (unit);Events;',100,0,100)
histo_a.FillRandom('landau',10000)
histo_a.SetLineColor(1)
histo_a.SetMarkerColor(1)
histo_a.SetMarkerStyle(20)

histo_b = TH1F('histo_b','0 PU;some var (unit);Events;',100,0,100)
histo_b.FillRandom('pol0',10000)
histo_b.SetLineColor(633)
histo_b.SetMarkerColor(633)
histo_b.SetMarkerStyle(21)

histo_c = TH1F('histo_c','histo_c;some var (unit);Events;',100,0,3)
histo_c.FillRandom('gaus',100000)
histo_c.SetLineColor(601)
histo_c.SetLineWidth(2)
histo_c.SetMarkerColor(601)
histo_c.SetMarkerStyle(22)

histo_d = TH1F('histo_d','histo_d;some var (unit);Events;',100,0,100)
histo_d.FillRandom('pol2',100000)
histo_d.SetLineColor(418)
histo_d.SetFillColor(417)

histo_e = TH2F('histo_e','histo_e;some var (unit);some other var (unit);Events',100,0,100,50,0,50)
for ix in range(1,histo_e.GetNbinsX()+1):
    for iy in range(1,histo_e.GetNbinsY()+1):
        histo_e.SetBinContent(ix,iy,ix**2-iy**2)

#---- Draw histogram with ratio ----#

### create a list of histogram (a,b)
histos = [histo_a, histo_b]

### define a legend for histograms (a,b)
leg = TLegend(0.7, 0.85-0.10*len(histos), 0.95, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetFillColor(0)
for h in histos:
    leg.AddEntry(h,h.GetTitle(),'lp')

### draw histograms
### 
### mandatory argument:
###   list of TH1 
### 
### options:
###   drawhist (default=False)  -> draw TH1 with 'HIST' option
###   ratio    (default=False)  -> draw ratio of all histograms wrt hist[0]
###   log      (default=False)  -> draw in log scale
### 
### returns a list of objects:
###   thecanvas -> TCanvas
###   theunc    -> TH1 stat. uncertainty on ratio         (meaningful only if ratio is drawn)
###   theratios -> disctionary of TH1 ratio wrt histos[0] (meaningful only if ratio is drawn)
###
###                            phase2tdrStyle.draw([h0,h1,...], drawhist, ratio, log   ) 
Acanvas, Aunc, Aratios = phase2tdrStyle.draw(histos,            False,    True,  True )

### draw "CMS Phase-2 Preliminary" 
### 
### options:
###   onTop  (default = False)  -> place it outside the pad
phase2tdrStyle.drawCMS()

### draw "14 TeV, xxx PU"
### 
### options:
###   PU   value (default = None) -> if no PU value is specified, only "14 TeV" is drawn
###                                  both string or int format can be used
###   LUMI value (default = None) -> if no LUMI value is specified, only "14 TeV" is drawn
###                                  add lumi as LaTex formatted string, e.g.: '3 ab^{-1}'
phase2tdrStyle.drawEnPu()

### draw the legend and save the canvas
leg.Draw()
Acanvas.Print('Aplot.png')
Acanvas.Print('Aplot.pdf')




#---- Draw histogram w/o ratio ----#

### draw histograms
Bcanvas, Bunc, Bratios = phase2tdrStyle.draw([histo_c],      True,    False,  False )

### draw "CMS Phase-2 Preliminary" 
phase2tdrStyle.drawCMS(True)

### draw "14 TeV, xxx PU"
phase2tdrStyle.drawEnPu(pileup=140, lumi='3 ab^{-1}')

### save the canvas
Bcanvas.Print('Bplot.png')
Bcanvas.Print('Bplot.pdf')



#---- Draw Canvas and fill with own histogram ----#

### draw canvas
Ccanvas = phase2tdrStyle.setCanvas()

### draw histogram (formatHisto can be used to adjust labels and titles size)
phase2tdrStyle.formatHisto(histo_d)
histo_d.Draw('HIST')

### draw "CMS Phase-2 Preliminary" 
phase2tdrStyle.drawCMS()

### draw "14 TeV"
phase2tdrStyle.drawEnPu(pileup='200')

### save the canvas
Ccanvas.Print('Cplot.png')
Ccanvas.Print('Cplot.pdf')



#---- Draw Canvas and fill with own 2D histogram ----#

### draw canvas
Dcanvas = phase2tdrStyle.setCanvas()

### draw histogram
phase2tdrStyle.formatHisto(histo_e)
gStyle.SetPalette(53)
histo_e.SetContour(999)
histo_e.Draw('COL')

### draw "CMS Phase-2 Preliminary" 
phase2tdrStyle.drawCMS(True)

### draw "14 TeV"
phase2tdrStyle.drawEnPu(lumi='3000 fb^{-1}')

### save the canvas
Dcanvas.Print('Dplot.png')
Dcanvas.Print('Dplot.pdf')





