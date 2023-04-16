# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 19:05 2022

@author: weixin87167
@info: Definition von Variablen, Hardcoded
"""
import numpy as np
import matplotlib.pyplot as plt
import snap7
from snap7.types import*
from snap7.util import*

##### definition Globale Variablen as dictionary"
pumpA = {"Bezeichnung": "Pumpe A", 
         "max_rev" : 3000,  # maximale Drezahl 
         "min_rev" : 0, # minimale Drezahl
         "max_acc_psec" : 100, # maximale Beschleunigung
         "min_acc_psec" : 1  # minimale Beschleunigung
         }

pumpB = {"Bezeichnung": "Pumpe B", 
         "max_rev" : 3000, # maximale Drezahl
         "min_rev" : 0, # minimale Drezahl
         "max_acc_psec" : 100, # maximale Beschleunigung
         "min_acc_psec" : 1 # minimale Beschleunigung
         }

vent_reg = {"Bezeichnung": "Regelventil",
            "max_pos": 100, # oberer Totpunkt
            "min_pos": 0, # unterer Totpunkt
            "max_acc": 1, # maximale Geschwindigkeit
            "min_acc": 0.1 # minimale Geschwindigkeit
            }


test_config ={"duration_min": 240,
              "min_time_between_steps_sec" : 50,
              "max_time_between_steps_sec" : 300
              }

"""Datenquellen für den SPS Austausch"""
"""Bezeichnung(wie in der SPS), aus Datenbaustein (true/false), Nummer Datenbaustein, Offset oder Adresse, Datentyp"""

pumpA_signals_r = np.array([("Drucksensor_A1",1,27,0,S7WLReal),
                            ("Drucksensor_A2",1,27,20,S7WLReal),
                            ("Motor_A_Elektrische_Leistung",1,27,260,S7WLReal),
                            ("Motor_A_Wirkleistung",1,27,268,S7WLReal),
                            ("Motor_A_Leistungsfaktor",1,27,276,S7WLReal),
                            ("Motor_A_Drehmoment",1,27,284,S7WLReal)
                            ])

"""Messungen Pump_B"""

pumpB_signals_r = np.array([("Drucksensor_B1",1,27,40,S7WLReal),
                            ("Drucksensor_B2",1,27,60,S7WLReal),
                            ("Motor_B_Elektrische_Leistung",1,27,296,S7WLReal),
                            ("Motor_B_Wirkleistung",1,27,304,S7WLReal),
                            ("Motor_B_Leistungsfaktor",1,27,312,S7WLReal),
                            ("Motor_B_Drehmoment",1,27,320,S7WLReal)
                            ])
"""Messungen System"""

system_signals_r = np.array([("Drucksensor_Q1",1,27,80,S7WLReal),
                            ("Drucksensor_Q2",1,27,100,S7WLReal),
                            ("Differenzdruck_unterer_Tank",1,27,160,S7WLReal),
                            ("Differenzdruck_oberer_Tank",1,27,180,S7WLReal),
                            ("Temperatur",1,27,200,S7WLReal)
                            ])

"""Messungen Regelventil"""

vent_reg_signals_r = np.array([("Drucksensor_R1",1,27,120,S7WLReal),
                            ("Drucksensor_R2",1,27,140,S7WLReal),
                            ("Temperatur",1,27,200,S7WLReal),
                            ("Regelventil_Stellung",1,27,220,S7WLReal)
                            ])


def show_config():
    """
    Ausgabe aller Configurationsparameter 

    Returns
    -------
    None.

    """
    print (pumpA)
    print (pumpB)
    print (vent_reg)
    print (test_config)
    print (plc)
    print (seeds)
    print (pumpA_signals_r)
    return

show_config()




