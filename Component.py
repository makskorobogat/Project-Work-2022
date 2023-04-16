import snap7
from snap7.types import*
from snap7.util import*
from time import sleep

class Component(object):
    #A component represents a value on a plc. 

    def __init__(self, Plc, Name, Datatype, OffsetByte, OffsetBit, DBNumber):
        self.Name = Name
        self.Device = Plc
        self.OffsetBit = OffsetBit
        self.OffsetByte = OffsetByte
        self.DBNumber = DBNumber
        self.Datatype = Datatype
        self.Bytearray = None
        self.error = None
        self.Value = None
        self.__Counter = 0
        
        self.Initvalue()

        print("Component " + self.Name + " created!")
    
    def SetBit(self):
        #Function to set a boolean value
        if(self.Device.CommunicationBusy == False):
            self.Device.CommunicationBusy = True
            if(self.Datatype != Datatypes.Bool):
                self.error = "SetBit only if datatype == Boolean"
                return self.error
            else:
                try:
                    self.Bytearray = self.Device.S7Device.db_read(self.DBNumber, self.OffsetByte, snap7.types.S7WLBit)
                
                    set_bool(self.Bytearray, 0, self.OffsetBit, True)
                    self.Value = True

                    self.Device.S7Device.db_write(self.DBNumber, self.OffsetByte, self.Bytearray)
                except Exception as ex:
                    self.error = ex
                    return self.error

                #Writing Data completed
                self.Device.CommunicationBusy = False
                self.__Counter = 0

        else:            
            print(self.Name + ": System is busy")
            sleep(0.1)  #Sleep 100ms
            self.__Counter = self.__Counter + 1
            if(self.__Counter <= 3):
                self.ReadDB()
            else:
                print("System is to busy now")
                self.__Counter = 0
            
    def ResetBit(self):
        #Function to set a boolean value
        
        if(self.Device.CommunicationBusy == False):
            self.Device.CommunicationBusy = True
            if(self.Datatype != Datatypes.Bool):
                self.error = "ResetBit only if datatype == Boolean"
                return self.error
            else:
                try:
                    self.Bytearray = self.Device.S7Device.db_read(self.DBNumber, self.OffsetByte, snap7.types.S7WLByte)
            
                    set_bool(self.Bytearray,  0, self.OffsetBit, False)
                    self.Value = False

                    self.Device.S7Device.db_write(self.DBNumber, self.OffsetByte, self.Bytearray)
                except Exception as ex:
                    self.error = ex
                    return self.error

            #Writing Data completed
            self.Device.CommunicationBusy = False
            self.__Counter = 0

        else:            
            print(self.Name + ": System is busy")
            sleep(0.1)  #Sleep 100ms
            self.__Counter = self.__Counter + 1
            if(self.__Counter <= 3):
                self.ReadDB()
            else:
                print("System is to busy now")
                self.__Counter = 0
                self.Device.CommunicationBusy = False
    
    def ReadDB(self):
        #print("ReadDB")
        if(self.Device.CommunicationBusy == False):
            try:
                self.Device.CommunicationBusy = True
                self.ReadBytearray()
            
                #if(self.Bytearray == None):
                #    print("Bytearray empty @ " + self.Name + ".ReadDB")
                #    return self.error
                #print(self.Datatype)
                if self.Datatype == Datatypes.Real:
                    #print("ReadDB Real")
                    try:
                        self.Value = get_real(self.Bytearray, 0)
                        #print("Ergebnis:")
                        #print(str(self.Value))
                    except Exception as ex:
                        print("Exception:")
                        print(ex)
                        self.error = ex
                elif self.Datatype == Datatypes.Byte:
                    #print("ReadDB Byte")
                    self.Value = get_byte(self.Bytearray, 0)
                    #print(self.Value)
                elif self.Datatype == Datatypes.DWord:
                    #print("ReadDB DWord")
                    self.Value = get_dword(self.Bytearray, 0)
                    #print(self.Value)
                elif self.Datatype == Datatypes.Word:
                    #print("ReadDB Word")
                    self.Value = get_word(self.Bytearray, 0)
                    #print(self.Value)
                elif self.Datatype == Datatypes.Int16:
                    #print("ReadDB Int16")
                    try:
                        self.Value = get_int(self.Bytearray, 0)
                        #print("Ergebnis:")
                        #print(str(TestValue))
                    except Exception as ex:
                        print("Exception:")
                        print(ex)
                        self.error = ex
                elif self.Datatype == Datatypes.Bool:
                    #print("ReadDB Bool")
                    try:
                        self.Value = get_bool(self.Bytearray, 0, self.OffsetBit)
                        #print("Ergebnis:")
                        #print(str(TestValue))
                    except Exception as ex:
                        print("Exception:")
                        print(ex)
                        self.error = ex

                else:
                    self.error = "Invalid datatype set @ " + self.Name
                    print(str(self.error))
                    return self.error
                        
                #Reading out completed
                self.Device.CommunicationBusy = False
                self.__Counter = 0
                return self.Value

            except Exception as ex:
                self.error = ex
                print(str(self.error))
                return self.error                
        else:
            print(self.Name + ": System is busy")
            sleep(0.1)  #Sleep 100ms
            self.__Counter = self.__Counter + 1
            if(self.__Counter <= 3):
                self.ReadDB()
            else:
                print("System is to busy now")
                self.__Counter = 0
            

    def WriteDB(self, value):
        
        #print()
        #print("WriteDB")
        #print(value)
        #print(type(value))
        #print(self.Datatype)
        
        if(self.Device.CommunicationBusy == False):
            self.Device.CommunicationBusy = True
            if(type(value) != self.Datatype):
                #print("Converting datatype of value")
                if self.Datatype == Datatypes.Int16:
                    value = int(value)
                elif self.Datatype == Datatypes.Word:
                    value = word(int(value))
                elif self.Datatype == Datatypes.Byte:
                    value = value.encode('utf-8')
                elif self.Datatype == Datatypes.Real or Datatypes.DWord:
                    value = float(value)
                else:
                    self.error = "Invalid value given at WriteDB @ " + self.Name + ". " + ex
                    return self.error
                    
            #print(value)
            #print(type(value))
            #print(self.Datatype)

            try:
                #Get Dataarray from Plc. Maybe unnessesary?
                self.ReadBytearray()
            
                #Choose Datatype
                if self.Datatype == Datatypes.Real:
                    #print("WriteDB Real")
                    set_real(self.Bytearray, 0, value) 
                elif self.Datatype == Datatypes.Byte:
                    #print("WriteDB Byte")
                    set_byte(self.Bytearray, 0, value) 
                elif self.Datatype == Datatypes.DWord:
                    #print("WriteDB DWord")
                    set_dword(self.Bytearray, 0, value)
                elif self.Datatype == Datatypes.Word:
                    #print("WriteDB Word")
                    set_word(self.Bytearray, 0, value) 
                elif self.Datatype == Datatypes.Int16:
                    #print("WriteDB Int16")
                    set_int(self.Bytearray, 0, value) 
                else:
                    self.error = "Invalid Datatype set @ " + self.Name
                    return self.error

                #Write Data into Plc
                self.Device.S7Device.db_write(self.DBNumber, self.OffsetByte, self.Bytearray)
            except Exception as ex:
                self.error = ex
                return self.error

            #Writing Data completed
            self.Device.CommunicationBusy = False
            self.__Counter = 0

        else:            
            print(self.Name + ": System is busy")
            sleep(0.1)  #Sleep 100ms
            self.__Counter = self.__Counter + 1
            if(self.__Counter <= 3):
                self.ReadDB()
            else:
                print("System is to busy now")
                self.__Counter = 0
                self.Device.CommunicationBusy = False

    def ReadBytearray(self):
        if self.Datatype == Datatypes.Real:
            self.Bytearray = self.Device.S7Device.db_read(self.DBNumber, self.OffsetByte, S7WLReal) 
        elif self.Datatype == Datatypes.Bool:
            self.Bytearray = self.Device.S7Device.db_read(self.DBNumber, self.OffsetByte, S7WLBit)
        elif self.Datatype == Datatypes.Byte:
            self.Bytearray = self.Device.S7Device.db_read(self.DBNumber, self.OffsetByte, S7WLByte)
        elif self.Datatype == Datatypes.Int16 or Datatypes.Word:
            self.Bytearray = self.Device.S7Device.db_read(self.DBNumber, self.OffsetByte, S7WLWord)
        else:
            self.error = "Invalid Datatype set @ " + self.name
            print(str(self.error))
            return self.error

    def SetAutomatic(self,run):
        #Set the component on the List of the device to read out automatically
        if(run==True):
            self.Device.AutomaticList.append(self)
        else:
            self.Device.AutomaticList.remove(self)

    def Whooho(self):
        print(self.Name + " says Whooho")

    def Initvalue(self):
        if self.Datatype == Datatypes.Real:
            self.Value = 0.0
        if self.Datatype == Datatypes.Int16 or Datatypes.Byte:
            self.Value = 0
        if self.Datatype == Datatypes.Bool:
            self.Value = False
        if self.Datatype == Datatypes.Word or Datatypes.DWord:
            self.Value = 0
            

class Datatypes(Enum):
    Int16 = 1
    Real = 2
    Bool = 3
    Byte = 4
    Word = 5
    DWord = 6  
