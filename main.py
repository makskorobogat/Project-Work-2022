# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 10:04:04 2021

@author: weixin87167
@info: Main function
"""

##from _typeshed import FileDescriptor
import Device
import Component
from snap7.types import*
from snap7.util import*
from Device import*
from Component import*

global plc
global Exit

print("Hallo")
Exit = False
   
plc = Device("Pumpenversuchsstand", "192.168.1.1", 0, 2)
#print(plc.error)

Testcomponente = Component(plc, "Test", Datatypes.Int16, 33, 0, 520)
#print(Testcomponente.error)


def switcher(status):
    match status:
        case "name":
            return plc.name
        case "info":
            return plc.GetDeviceInformation()
        case "exit":
            return "Exit"
        case "check":
            return plc.CheckConnection()
        case "connect":
            return plc.Connect()
        case "error":
            return plc.error
        case "device":
            return plc.S7Device
        case "component":
            return Testcomponente.error
        case "read":
            return Testcomponente.ReadDB()
        case "write":
            print("Value:")
            Valuetowrite = input()
            if(Valuetowrite == "TRUE"):
                Valuetowrite = True
            elif(Valuetowrite == "FALSE"):
                Valuetowrite = False
            return Testcomponente.WriteDB(Valuetowrite)
        case "setbit":
            return Testcomponente.SetBit()
        case "resetbit":
            return Testcomponente.ResetBit()
    print("Eingabe: " + status)
    
while Exit == False:
    print("Eingabe")
    Eingabe = switcher(input())
    print(Eingabe)
    if Eingabe == "Exit":
        break
    
print("Program exit")




