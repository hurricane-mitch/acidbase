# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 14:40:05 2016

@author: Mitchell Huot
"""

import numpy as np

class Titration:
    def __init__(self, 
                 acid_pKa, 
                 acid_conc, 
                 acid_vol, 
                 titrant_conc, 
                 Kw, 
                 base_vol, 
                 interval=0.1):
        self.acid_pKa = acid_pKa
        self.acid_Ka = 10**-acid_pKa
        self.acid_conc = acid_conc
        self.acid_vol = acid_vol
        self.titrant_conc = titrant_conc
        self.Kw = Kw
        self.base_vol = base_vol
        self.interval = interval
        self.calc_titrant_axis()
        self.calc_Cha()
        self.calc_Ca()
        self.calc_a1()
        self.calc_a2()
        self.calc_a3()
        self.calc_Q()
        self.calc_R()
        self.calc_theta()
        self.calc_H()
        self.calc_pH()
        self.x = self.titrant_axis
        self.y = self.pH
        
    def calc_titrant_axis(self):
        if self.base_vol != 0:
            self.titrant_axis = np.arange(0, self.base_vol, self.interval)
        else:
            self.titrant_axis = np.array([0])
        
    def calc_Cha(self): 
        self.Cha = ((self.acid_conc * self.acid_vol - 
                    self.titrant_axis * self.titrant_conc)/
                    (self.acid_vol + self.titrant_axis))
    
    def calc_Ca(self):
        self.Ca = []
        for data_point in self.titrant_axis:
            if data_point * self.titrant_conc < self.acid_conc * self.acid_vol:
                self.Ca.append((self.titrant_conc * data_point)/
                               (self.acid_vol + data_point))
            else:
                self.Ca.append((self.acid_conc * self.acid_vol)/
                               (self.acid_vol + data_point))
        self.Ca = np.array(self.Ca)
    
    def calc_a1(self):        
        self.a1 = self.acid_Ka + self.Ca
    
    def calc_a2(self):        
        self.a2 = -(self.Kw + self.acid_Ka * self.Cha)
    
    def calc_a3(self):        
        self.a3 = -self.acid_Ka * self.Kw
     
    def calc_Q(self):       
        self.Q = (self.a1**2-3*self.a2)/9
    
    def calc_R(self):        
        self.R = (2 * self.a1**3-9*self.a1*self.a2+27*self.a3)/54
    
    def calc_theta(self):    
        self.theta = []
        for i, row in enumerate(self.R):
            self.theta.append(np.arccos(row/np.sqrt(self.Q[i]**3)))
        self.theta = np.array(self.theta)

    def calc_H(self):    
        self.H = []
        for i, row in enumerate(self.titrant_axis):
            self.H.append(-2 * 
                          np.sqrt(self.Q[i]) * 
                          np.cos((self.theta[i] + 2 * np.pi) / 3) - 
                          self.a1[i] / 3)
        self.H = np.array(self.H)

    def calc_pH(self):        
        self.pH = []
        for i, row in enumerate(self.H):   
            self.pH.append(-(np.log10(row)))
        self.pH = np.array(self.pH)
        

    def add_base(self, vol):
        new_base_vol = []
        for volume in self.titrant_axis:
            new_base_vol.append(volume)
        try:
            new_base_vol.append(new_base_vol[-1] + vol)
        except IndexError:
            new_base_vol.append(vol)
        self.titrant_axis = np.array(new_base_vol)
        self.calc_Cha()
        self.calc_Ca()
        self.calc_a1()
        self.calc_a2()
        self.calc_a3()
        self.calc_Q()
        self.calc_R()
        self.calc_theta()
        self.calc_H()
        self.calc_pH()
        self.x = self.titrant_axis
        self.y = self.pH