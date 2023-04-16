"""
Created on Wed Apr 27 19:05 2022

@author: weixin87167
@info: PLC-Settings
"""

from multiprocessing.connection import Client
import snap7 
import Component as cp
from eventhandler import EventHandler
from enum import Enum
from time import sleep
import threading

class Device(object):

    def __init__(self, name, ip, rack, slot):

        self.name = name    #Given name of the plc   
        self.ip = ip        #IP-Address of the plc
        self.rack = rack    #Rack of given plc
        self.slot = slot    #Slot of given plc
        self.error = "No error stored"
        self.S7Device = snap7.client.Client()
        self.AutomaticEventHandler = EventHandler('StartAutomatic')
        self.AutomaticEventHandlerStop = EventHandler('StopAutomatic')
        self.AutomaticList = []
        self.__automaticEnabled = False
        self.Automaticthread = threading.Thread(target=self.OnAutomaticThread)
        self.CommunicationBusy = False      #Variable which informs if the system is sending or reading out
          
        #try:
        #    self.Connect()
        #except Exception as ex:
        #    self.error = ex

        # Errorlist = new Errorlist(this.Name);    //Create a new Errorlist
        # Connectionlist = new Connectinformations(this.Name); //Create a new List of Connectinformations
        # ComponentList = new List<Structs.StoredComponentInDevice>();
        # NumberOfError = 0;  //Counter of Errors
        # NumberOfBitsPUTGET = 0;        
    
    def CheckConnection(self):
        # Rückgabe ob eine Verbindung aufgebaut wurde oder nicht
        try:
            return self.S7Device.get_connected()       
        except Exception as ex:           
            return ex

    def GetDeviceInformation(self):
        # Gibt Informationen über verbundene SPS zurück (<bool>,<String>)
        try:
            return self.S7Device.get_cpu_info(), self.S7Device.get_cpu_state()
        except Exception as ex:
            return ex
       
    def Connect(self):
        #Manueller Aufbau einer Verbindung zur SPS
        print("Connecting...")
        #self.S7Device.connect(self.ip, self.rack, self.slot)
        try:
            self.S7Device.connect(self.ip, self.rack, self.slot)
            print("Connection ok")
            return "Connection ok"
        except Exception as ex:
            self.error = ex
            return self.error
    
    def StartAutomatic(self):
        print("Device.StartAllAutomatic.Start")

        self.__automaticEnabled = True

        if(self.Automaticthread != None):
            if not self.Automaticthread.is_alive():
                try:
                    self.Automaticthread.start()
                except Exception as ex:
                    print(str(ex))
                    #Renew thread because terminated threads cannot be called twice
                    self.Automaticthread = threading.Thread(target=self.OnAutomaticThread)
                    #Try to start the new Thread. If an error occurs, end the function
                    try:
                        self.Automaticthread.start()
                    except Exception as ex:
                        self.error = ex
        else:
            self.error = "Internal error. Recreate component (Invalid Automaticthread)"
            #self.AutomaticList[0].RunAutomatic()

    def OnAutomaticThread(self):
        print("Thread started")             

        if(self.CheckConnection() == True):
            #Part of reading out if connected
            if(self.AutomaticList != None):
                if(len(self.AutomaticList) > 0):  
                    i = 0
                    while(i < len(self.AutomaticList)):
                        #self.AutomaticList[i].Whooho()
                        try:
                            self.AutomaticList[i].ReadDB()
                            #print(self.AutomaticList[i].Value)

                        except Exception as ex:
                            self.error = ex
                            print(ex)
                            break;
                        except:
                            print("Unbekannte Fehlermeldung")
                            break;
                    
                        if(self.__automaticEnabled == True):
                            i = i + 1
                            if(i >= len(self.AutomaticList)):
                                i = 0
                                sleep(1)  
                        else:
                            break;
                    else:
                        self.error = "No components to automatic readout"
                else:
                    self.error = "No components to automatic readout"
                    self.__automaticEnabled = False

            #End of reading out
        else:
            print("Device is not connected")
            
        #time.sleep(2)
        print("Thread End")  

    def StopAutomatic(self):
        print("Device.StopAllAutomatic")
        self.__automaticEnabled = False

    def PrintAutomaticList(self):
        return self.AutomaticList
     

    #
        
    #"""    
    ## Funktion zur Anzeige der Netzauslast, ggf. später implementieren
    #def Utilization()         
    #    FreeBits = 608 - this.NumberOfBitsPUTGET;
    #    FreeByte = SIGMAPLC.Functions.BitsToByte(Return.FreeBits);
    #    UsedBits = this.NumberOfBitsPUTGET;
    #    UsedByte = SIGMAPLC.Functions.BitsToByte(Return.UsedBits);
    #    Percent = this.NumberOfBitsPUTGET * 100 / 608;

    #    return FreeBits, FreeByte, UsedBits, UsedByte, Percent;
          
    #"""