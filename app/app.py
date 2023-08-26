from flask import Flask, render_template, request, url_for, redirect, jsonify
from flaskwebgui import FlaskUI # import FlaskUI
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
app = Flask(__name__)

  
  
import clr
clr.AddReference('C:\\Program Files\\Siemens\\Automation\\Portal V18\PublicAPI\\V18\\Siemens.Engineering.dll')
from System.IO import DirectoryInfo, FileInfo
import Siemens.Engineering as tia
import Siemens.Engineering.HW.Features as hwf
import Siemens.Engineering.SW.Units as units
import Siemens.Engineering.Compiler as comp
import os

import time
import threading
from tkinter.filedialog import askopenfilename
import ipaddress
import xml.etree.ElementTree as ET

ET.register_namespace("", "http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v4")

#_type = '6SL3210-1KE11-8AF2/4.7.13';
#_name = 'Device_1';

_typeArr = []
_nameArr = []
_consoleArr = []

myproject = ''

mypath = ''

counter = 3

def async_func(_type, _name, _path):  
    print("tiaportal")
    global _consoleArr
    _consoleArr.append("tiaportal")
    mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)
    processes = tia.TiaPortal.GetProcesses() # Making a list of all running processes
    print (processes)
    _consoleArr.append(str(processes))
    # Creating a new project. Using try/except in case project allready exists
 
    #project_path = DirectoryInfo ('C:\\Openness\\PKI')
    
 
    try:
       print(_path)
       _consoleArr.append(_path)
       #myproject = mytia.Projects.Create(project_path, project_name)
       project_path = FileInfo (_path)
       global myproject
       myproject = mytia.Projects.OpenWithUpgrade(project_path)
       #print(myproject)
    except Exception as e:
       print (e)
       _consoleArr.append(e)
       pass

    #Adding the main components

    #print ('Creating PLC1')
    #PLC1_mlfb = 'OrderNumber:6ES7 513-1AL02-0AB0/V2.6'
    #PLC1 = myproject.Devices.CreateWithItem(PLC1_mlfb, 'PLC1', 'PLC1')


    #print ('Creating IOnode1')
    #IOnode1_mlfb = 'OrderNumber:6ES7 155-6AU01-0BN0/V4.1'
    #IOnode1 = myproject.Devices.CreateWithItem(IOnode1_mlfb, 'IOnode1', 'IOnode1')


    #print ('Creating HMI1')
    #HMI1_mlfb = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
    #HMI1 = myproject.Devices.CreateWithItem(HMI1_mlfb, 'HM1', None)

    #ToDo Add start screen to avoid compilation error fo the HMI


        #print ('Creating PN')
        #print(str(_name.index(n)))
        #PN_mlfb = 'OrderNumber:'+ str(_type.index(n));
        #PN = myproject.Devices.CreateWithItem(PN_mlfb,  str(_name.index(n)), None)

    # tsekataan onko yhtakaan laitetta olemassa jos ei ole niin luodaan PLC
    count = 0
    for device in myproject.Devices:
        count+=1

    print('Devices: '+ str(count))
    _consoleArr.append('Devices: '+ str(count))

    if count == 0:
        print ('Creating PLC1')
        _consoleArr.append('Creating PLC1')
        PLC1_mlfb = 'OrderNumber:6ES7 511-1AL03-0AB0/V3.0'
        PLC1 = myproject.Devices.CreateWithItem(PLC1_mlfb, 'PLC1', 'PLC1')
  

    # display indices in the list
    for i in range(len(_type)):
        print(i, _type[i])
        _consoleArr.append(str(_type[i]))
        print(i, _name[i])
        _consoleArr.append(str(_name[i]))
        PN_mlfb = 'OrderNumber:'+ str(_type[i])
        PN = myproject.Devices.CreateWithItem(PN_mlfb,  str(_name[i]), None)

    # Adding IO cards to the PLC and IO station
    # This is basic to show how it works, use loops with checks (CanPlugNew) to see if the slot is available
    # CanPlugnew is not mandatory, but usefull in real code

    #if (PLC1.DeviceItems[0].CanPlugNew('OrderNumber:6ES7 521-1BL00-0AB0/V2.1','IO1',2)): 
       # PLC1.DeviceItems[0].PlugNew('OrderNumber:6ES7 521-1BL00-0AB0/V2.1','IO1', 2)

        
    #if (IOnode1.DeviceItems[0].CanPlugNew('OrderNumber:6ES7 131-6BH01-0BA0/V0.0','IO1',1)):
       # IOnode1.DeviceItems[0].PlugNew('OrderNumber:6ES7 131-6BH01-0BA0/V0.0','IO1', 1)



    #
    # # Creating network, iosytem and setting IP adresses
    # 

   
    #creating a list of all found network interfaces on all stations in the station list
    n_interfaces = []
    for device in myproject.Devices:
        
        deviceItemComposition = device.DeviceItems
      
        for deviceItem in deviceItemComposition:
            for info in deviceItem.GetAttributeInfos():
                print(str(device.Name)+': '+str(info.Name))
                _consoleArr.append(str(device.Name)+': '+str(info.Name))
            
        
        device_item_aggregation = device.DeviceItems[1].DeviceItems
        for deviceitem in device_item_aggregation:
            network_service = tia.IEngineeringServiceProvider(deviceitem).GetService[hwf.NetworkInterface]()
            if type(network_service) is hwf.NetworkInterface:
                n_interfaces.append(network_service)




    # Assigning an IP to each item in the list (dirty code, but to demonstrate how theAPI works)

    #n_interfaces[0].Nodes[0].SetAttribute('Address','192.168.0.130')
   # n_interfaces[1].Nodes[0].SetAttribute('Address','192.168.0.131')
   # n_interfaces[2].Nodes[0].SetAttribute('Address','192.168.0.132')
    #n_interfaces[len(n_interfaces)-1].Nodes[0].SetAttribute('Address','140.80.0.204')
    #n_interfaces[0].Nodes[0].SetAttribute('Address','140.80.0.200')
    #n_interfaces[1].Nodes[0].SetAttribute('Address','140.80.0.202')
    #n_interfaces[0].Nodes[0].SetAttribute('Address','192.168.0.130')

    if count == 0:
        n_interfaces[0].Nodes[0].SetAttribute('Address','192.168.0.130')

    
    add = n_interfaces[0].Nodes[0].GetAttribute('Address')
    
    print(add)
    _consoleArr.append(str(add))

    #n_interfaces[1].Nodes[0].SetAttribute('Address', a)

    # Creating subnet and IO system on the first item in the list
    # Connects to subnet for remaining devices, if IO device it gets assigned to the IO system
    for n in n_interfaces:
        if count == 0:
            count = 1
            subnet = n_interfaces[0].Nodes[0].CreateAndConnectToSubnet("Profinet")
            #subnet = n_interfaces[0].Nodes[0].CreateAndConnectToSubnet("PN/IE_1")
            ioSystem = n_interfaces[0].IoControllers[0].CreateIoSystem("PNIO");
        if n_interfaces.index(n) != 0:
            
            t = str(ipaddress.ip_address(add) + 256)
            n_interfaces[n_interfaces.index(n)].Nodes[0].SetAttribute('Address', t)
          
            add = t
          
            #subnet = myproject.Subnets.Find("Profinet");
            subnet = ''

            for subnets in myproject.Subnets:
                subnet = subnets


            try:

                ioSystem = subnet.IoSystems[0]
                n_interfaces[n_interfaces.index(n)].Nodes[0].ConnectToSubnet(subnet)
                if (n_interfaces[n_interfaces.index(n)].IoConnectors.Count) >> 0:
                    n_interfaces[n_interfaces.index(n)].IoConnectors[0].ConnectToIoSystem(ioSystem);
            
            except Exception:
                pass    


    #
    # # Compiling HW & SW
    # 

   
  



    # Defining method to recursively print error messages
    def print_comp(messages):
        for msg in messages:
            print(f'Path: {msg.Path}')
            print(f'DateTime: {msg.DateTime}')
            print(f'State: {msg.State}')
            print(f'Description: {msg.Description}')
            print(f'Warning Count: {msg.WarningCount}')
            print(f'Error Count: {msg.ErrorCount}\n')
            print_comp(msg.Messages)
  
            _consoleArr.append(str(f'Path: {msg.Path}'))
            _consoleArr.append(str(f'DateTime: {msg.DateTime}'))
            _consoleArr.append(str(f'State: {msg.State}'))
            _consoleArr.append(str(f'Description: {msg.Description}'))
            _consoleArr.append(str(f'Warning Count: {msg.WarningCount}'))
            _consoleArr.append(str(f'Error Count: {msg.ErrorCount}\n'))
            _consoleArr.append(str(msg.Messages))


    try:
 
        # Compiling all devices
        for device in myproject.Devices:
            compile_service =  device.GetService[comp.ICompilable]()
            result = compile_service.Compile()
                        
            #Printing results from compiler
            print(f'State: {result.State}')
            print(f'Warning Count: {result.WarningCount}')
            print(f'Error Count: {result.ErrorCount}')
            print_comp(result.Messages)   

            
            _consoleArr.append(str(f'State: {result.State}'))
            _consoleArr.append(str(f'Warning Count: {result.WarningCount}'))
            _consoleArr.append(str(f'Error Count: {result.ErrorCount}'))
            _consoleArr.append(str(result.Messages)) 

    except Exception:
        pass       


    #
    # # Option to compile SW only
    # 



    # Defining method to recursively print error messages
    def print_comp(messages):
        for msg in messages:
            print(f'Path: {msg.Path}')
            print(f'DateTime: {msg.DateTime}')
            print(f'State: {msg.State}')
            print(f'Description: {msg.Description}')
            print(f'Warning Count: {msg.WarningCount}')
            print(f'Error Count: {msg.ErrorCount}\n')
            print_comp(msg.Messages)

         
            _consoleArr.append(str(f'Path: {msg.Path}'))
            _consoleArr.append(str(f'DateTime: {msg.DateTime}'))
            _consoleArr.append(str(f'State: {msg.State}'))
            _consoleArr.append(str(f'Description: {msg.Description}'))
            _consoleArr.append(str(f'Warning Count: {msg.WarningCount}'))
            _consoleArr.append(str(f'Error Count: {msg.ErrorCount}\n'))
            _consoleArr.append(str(msg.Messages))

    try:

            #compiling all sw in all devices
        for device in myproject.Devices:
            device_item_aggregation = device.DeviceItems
            for deviceitem in device_item_aggregation:   
                    software_container = tia.IEngineeringServiceProvider(deviceitem).GetService[hwf.SoftwareContainer]()
                    if (software_container != None):
                        print(f'compiling: {deviceitem.Name}')
                        _consoleArr.append(f'compiling: {deviceitem.Name}')
                        software_base = software_container.Software
                        
                        compile_service =  software_base.GetService[comp.ICompilable]()
                        result = compile_service.Compile()
                        
                        #Printing results from compiler
                        print(f'State: {result.State}')
                        print(f'Warning Count: {result.WarningCount}')
                        print(f'Error Count: {result.ErrorCount}')
                        print_comp(result.Messages)   

                        

                        _consoleArr.append(str(f'State: {result.State}'))
                        _consoleArr.append(str(f'Warning Count: {result.WarningCount}'))
                        _consoleArr.append(str(f'Error Count: {result.ErrorCount}'))
                        _consoleArr.append(str(result.Messages))  

    except Exception:
        pass  


    #myproject.Save()

    #myproject.Close()

    #mytia.Dispose()


    # lohkojen luonti
    deviceItem = myproject.Devices[0].DeviceItems[1]

    software_container = tia.IEngineeringServiceProvider(deviceItem).GetService[hwf.SoftwareContainer]()
   
    software_base = software_container.Software
    print(str(deviceItem.Name))  
    print(str(software_base.Name))  

    _consoleArr.append(str(deviceItem.Name))  
    _consoleArr.append(str(software_base.Name))  

    #plc_block = software_base.BlockGroup.Blocks.Find("Drives")
    #plc_block.Export(FileInfo('C:\\export\\tulos\\Drives.xml'), tia.ExportOptions.WithDefaults)
    #plc_block0 = software_base.BlockGroup.Blocks.Find("sinaSpeed2_DB")
    #plc_block0.Export(FileInfo('C:\\export\\tulos\\sinaSpeed2_DB.xml'), tia.ExportOptions.WithDefaults)



    plc_block2 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\export\\result\\XMLtest.xml'), tia.ImportOptions.Override)
    unit_block1 = software_base.TypeGroup.Types.Import(FileInfo('C:\export\\result\\typeSinaSpeedInterface.xml'), tia.ImportOptions.Override)
    plc_block1 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\export\\result\\DrivesData.xml'), tia.ImportOptions.Override)
  
    



    #unit = software_base.TypeGroup.Types.Find("typeSinaSpeedInterface")
    #unit.Export(FileInfo('C:\\export\\tulos\\typeSinaSpeedInterface.xml'), tia.ExportOptions.WithDefaults)


    blockComposition = software_base.BlockGroup.Blocks
    isAutoNumber = True
    iDBName="SinaSpeed_DB"
    instanceOfName = "SinaSpeed"
    number = 1

    iDbBlock = blockComposition.CreateInstanceDB(iDBName, isAutoNumber, number,instanceOfName)


    iDBName="SinaParaS_DB"
    instanceOfName = "SinaParaS"
    iDbBlock2 = blockComposition.CreateInstanceDB(iDBName, isAutoNumber, number,instanceOfName)

    # SinaParaS

    # loop

   # index = 0
    #for device in myproject.Devices:
     # if index != 0:
          



    print('Demo complete!')
    _consoleArr.append('Demo complete!')

  
@app.route("/openproject/", methods=["GET"])
def openproject():
    print('project path')
    global mypath
    mypath = askopenfilename(filetypes=(("Project files", "*.ap18"),("All files", "*.*") ))


    return render_template("index.html")


@app.route("/add/", methods=["POST"])
def add():

    if request.method == "POST":
            _type =  request.form['type']
            _name =  request.form['name']
 

    if _type == '' or _name == '':
        return 400
 
    global _typeArr
    _typeArr.append(_type)
    
    global _nameArr
    _nameArr.append(_name)
 
    print(_typeArr)
    
    print(_nameArr)

    return jsonify({'type':_typeArr, 'name':_nameArr})
 
 

@app.route("/")
def index(): 
    # resetoidaan
    global myproject
    myproject = ''
    global mypath 
    mypath = ''
    global _typeArr
    _typeArr = []
    global _nameArr
    _nameArr = []
   

    return render_template("index.html")


#@app.route("/xml/")
def getXML():

    print('XML')

    tree = ET.parse('test.xml')
    root = tree.getroot()

    #root = ET.fromstring(fields)
    #new_field = ET.Element("field")

    

    def counterFunc():
        global counter
        counter = counter+1
        return str(counter)
    
  
    for item in root.findall('SW.Blocks.OB'):
        itemid=item.find('ObjectList')
        
        global _nameArr
        db_array = _nameArr
        loop = 3
        loopMax = len(_nameArr)
        for i in range(loopMax):

          if loopMax == 1:
            num = loop 
          else:
            num = loop - i


          objectList = f"""
              <SW.Blocks.CompileUnit ID="{num}" CompositionName="CompileUnits">
          <AttributeList>
            <NetworkSource><FlgNet linkki="http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v4">
    <Parts>
      <Access Scope="GlobalVariable" UId="21">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="control" />
          <Component Name="enableAxis" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="22">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="control" />
          <Component Name="ackError" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="23">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="control" />
          <Component Name="speedSp" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="24">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="control" />
          <Component Name="refSpeed" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="25">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="control" />
          <Component Name="configAxis" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="26">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="control" />
          <Component Name="hwidStw" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="27">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="control" />
          <Component Name="hwidZsw" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="28">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="status" />
          <Component Name="axisEnabled" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="29">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="status" />
          <Component Name="lockout" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="30">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="status" />
          <Component Name="actVelocity" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="31">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="status" />
          <Component Name="error" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="32">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="status" />
          <Component Name="status" />
        </Symbol>
      </Access>
      <Access Scope="GlobalVariable" UId="33">
        <Symbol>
          <Component Name="DrivesData" />
          <Component Name="{db_array[i]}" />
          <Component Name="status" />
          <Component Name="diagId" />
        </Symbol>
      </Access>
      <Part Name="SinaSpeed" Version="1.0" UId="34">
        <Instance Scope="GlobalVariable" UId="35">
          <Component Name="SinaSpeed_DB" />
        </Instance>
      </Part>
    </Parts>
    <Wires>
      <Wire UId="36">
        <Powerrail />
        <NameCon UId="34" Name="en" />
      </Wire>
      <Wire UId="37">
        <IdentCon UId="21" />
        <NameCon UId="34" Name="EnableAxis" />
      </Wire>
      <Wire UId="38">
        <IdentCon UId="22" />
        <NameCon UId="34" Name="AckError" />
      </Wire>
      <Wire UId="39">
        <IdentCon UId="23" />
        <NameCon UId="34" Name="SpeedSp" />
      </Wire>
      <Wire UId="40">
        <IdentCon UId="24" />
        <NameCon UId="34" Name="RefSpeed" />
      </Wire>
      <Wire UId="41">
        <IdentCon UId="25" />
        <NameCon UId="34" Name="ConfigAxis" />
      </Wire>
      <Wire UId="42">
        <IdentCon UId="26" />
        <NameCon UId="34" Name="HWIDSTW" />
      </Wire>
      <Wire UId="43">
        <IdentCon UId="27" />
        <NameCon UId="34" Name="HWIDZSW" />
      </Wire>
      <Wire UId="44">
        <NameCon UId="34" Name="AxisEnabled" />
        <IdentCon UId="28" />
      </Wire>
      <Wire UId="45">
        <NameCon UId="34" Name="Lockout" />
        <IdentCon UId="29" />
      </Wire>
      <Wire UId="46">
        <NameCon UId="34" Name="ActVelocity" />
        <IdentCon UId="30" />
      </Wire>
      <Wire UId="47">
        <NameCon UId="34" Name="Error" />
        <IdentCon UId="31" />
      </Wire>
      <Wire UId="48">
        <NameCon UId="34" Name="Status" />
        <IdentCon UId="32" />
      </Wire>
      <Wire UId="49">
        <NameCon UId="34" Name="DiagId" />
        <IdentCon UId="33" />
      </Wire>
    </Wires>
  </FlgNet></NetworkSource>
            <ProgrammingLanguage>LAD</ProgrammingLanguage>
          </AttributeList>
          <ObjectList>
            <MultilingualText ID="{counterFunc()}" CompositionName="Comment">
              <ObjectList>
                <MultilingualTextItem ID="{counterFunc()}" CompositionName="Items">
                  <AttributeList>
                    <Culture>en-US</Culture>
                    <Text />
                  </AttributeList>
                </MultilingualTextItem>
              </ObjectList>
            </MultilingualText>
            <MultilingualText ID="{counterFunc()}" CompositionName="Title">
              <ObjectList>
                <MultilingualTextItem ID="{counterFunc()}" CompositionName="Items">
                  <AttributeList>
                    <Culture>en-US</Culture>
                    <Text />
                  </AttributeList>
                </MultilingualTextItem>
              </ObjectList>
            </MultilingualText>
          </ObjectList>
        </SW.Blocks.CompileUnit>
          """

          objectList2 = f"""
              <SW.Blocks.CompileUnit ID="{counterFunc()}" CompositionName="CompileUnits">
        <AttributeList>
          <NetworkSource><FlgNet linkki="http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v4">
  <Parts>
    <Access Scope="LiteralConstant" UId="21">
      <Constant>
        <ConstantType>UInt</ConstantType>
        <ConstantValue>2000</ConstantValue>
      </Constant>
    </Access>
    <Access Scope="GlobalVariable" UId="22">
      <Symbol>
        <Component Name="DrivesData" />
        <Component Name="{db_array[i]}" />
        <Component Name="control" />
        <Component Name="hwidStw" />
      </Symbol>
    </Access>
    <Access Scope="GlobalVariable" UId="23">
      <Symbol>
        <Component Name="DrivesData" />
        <Component Name="{db_array[i]}" />
        <Component Name="control" />
        <Component Name="refSpeed" />
      </Symbol>
    </Access>
    <Part Name="SinaParaS" Version="1.1" UId="24">
      <Instance Scope="GlobalVariable" UId="25">
        <Component Name="SinaParaS_DB" />
      </Instance>
    </Part>
  </Parts>
  <Wires>
    <Wire UId="41">
      <Powerrail />
      <NameCon UId="24" Name="en" />
    </Wire>
    <Wire UId="42">
      <OpenCon UId="26" />
      <NameCon UId="24" Name="Start" />
    </Wire>
    <Wire UId="43">
      <OpenCon UId="27" />
      <NameCon UId="24" Name="ReadWrite" />
    </Wire>
    <Wire UId="44">
      <IdentCon UId="21" />
      <NameCon UId="24" Name="Parameter" />
    </Wire>
    <Wire UId="45">
      <OpenCon UId="28" />
      <NameCon UId="24" Name="Index" />
    </Wire>
    <Wire UId="46">
      <OpenCon UId="29" />
      <NameCon UId="24" Name="ValueWrite1" />
    </Wire>
    <Wire UId="47">
      <OpenCon UId="30" />
      <NameCon UId="24" Name="ValueWrite2" />
    </Wire>
    <Wire UId="48">
      <OpenCon UId="31" />
      <NameCon UId="24" Name="AxisNo" />
    </Wire>
    <Wire UId="49">
      <IdentCon UId="22" />
      <NameCon UId="24" Name="hardwareId" />
    </Wire>
    <Wire UId="50">
      <NameCon UId="24" Name="Ready" />
      <OpenCon UId="32" />
    </Wire>
    <Wire UId="51">
      <NameCon UId="24" Name="Busy" />
      <OpenCon UId="33" />
    </Wire>
    <Wire UId="52">
      <NameCon UId="24" Name="Done" />
      <OpenCon UId="34" />
    </Wire>
    <Wire UId="53">
      <NameCon UId="24" Name="ValueRead1" />
      <IdentCon UId="23" />
    </Wire>
    <Wire UId="54">
      <NameCon UId="24" Name="ValueRead2" />
      <OpenCon UId="35" />
    </Wire>
    <Wire UId="55">
      <NameCon UId="24" Name="Format" />
      <OpenCon UId="36" />
    </Wire>
    <Wire UId="56">
      <NameCon UId="24" Name="ErrorNo" />
      <OpenCon UId="37" />
    </Wire>
    <Wire UId="57">
      <NameCon UId="24" Name="Error" />
      <OpenCon UId="38" />
    </Wire>
    <Wire UId="58">
      <NameCon UId="24" Name="ErrorId" />
      <OpenCon UId="39" />
    </Wire>
    <Wire UId="59">
      <NameCon UId="24" Name="DiagId" />
      <OpenCon UId="40" />
    </Wire>
  </Wires>
</FlgNet></NetworkSource>
          <ProgrammingLanguage>LAD</ProgrammingLanguage>
        </AttributeList>
        <ObjectList>
          <MultilingualText ID="{counterFunc()}" CompositionName="Comment">
            <ObjectList>
              <MultilingualTextItem ID="{counterFunc()}" CompositionName="Items">
                <AttributeList>
                  <Culture>en-US</Culture>
                  <Text />
                </AttributeList>
              </MultilingualTextItem>
            </ObjectList>
          </MultilingualText>
          <MultilingualText ID="{counterFunc()}" CompositionName="Title">
            <ObjectList>
              <MultilingualTextItem ID="{counterFunc()}" CompositionName="Items">
                <AttributeList>
                  <Culture>en-US</Culture>
                  <Text />
                </AttributeList>
              </MultilingualTextItem>
            </ObjectList>
          </MultilingualText>
        </ObjectList>
      </SW.Blocks.CompileUnit>
          """
     
          new_field = ET.fromstring(objectList)
          itemid.insert(1, new_field)

          new_field2 = ET.fromstring(objectList2)
          itemid.insert(2, new_field2)


    tree.write("C:\\export\\result\XMLtest.xml", encoding='unicode')
    #tree.write("XMLtest.xml", encoding='unicode')


    with open("C:\\export\\result\XMLtest.xml") as f:
      lines = f.readlines()


    lines[0] = "<Document>\n"

    index = 0
    for toisto in lines:
        if lines[index].find('linkki'):
          lines[index] = lines[index].replace('linkki', 'xmlns')
          index = index + 1


    with open("C:\\export\\result\XMLtest.xml", "w") as f:
        f.writelines(lines)

  
    return render_template("index.html")

@app.route("/tiaportal/", methods=["POST"])
def tiaportal():
    
    global _typeArr
    global _nameArr
    global mypath
    global _consoleArr
    _consoleArr = []

    print(_typeArr)
    print(_nameArr)
    print(mypath)
    
    if not mypath:
        return 400

    if not _typeArr: 
        return 400
    
    if not _nameArr:
        return 400
   
    
    getXML()

    x = threading.Thread(target=async_func, args=(_typeArr,_nameArr,mypath,))
    x.start()

   
     
    #return redirect('/')
    return render_template("index.html")

@app.route("/console/")
def console():
     return render_template("console.html")

@app.route("/getConsoleData/")
def consoleData():
   
     global _consoleArr

     print(_consoleArr)

     return jsonify({'consoleArr':str(_consoleArr)})
    

if __name__ == "__main__":
    #app.run(debug=True)
    #ui.run()
     FlaskUI(app=app, port=3000, width=1280 , height=800, server="flask").run()
     #ui = FlaskUI(app, width=500, height=500) # add app and parameters