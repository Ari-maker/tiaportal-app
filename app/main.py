from flask import Flask, render_template, request, url_for, redirect, jsonify
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
app = Flask(__name__)
  
  
import clr
clr.AddReference('C:\\Program Files\\Siemens\\Automation\\Portal V18\PublicAPI\\V18\\Siemens.Engineering.dll')
from System.IO import DirectoryInfo, FileInfo
import Siemens.Engineering as tia
import Siemens.Engineering.HW.Features as hwf
import Siemens.Engineering.Compiler as comp
import os

import time
import threading

from tkinter.filedialog import askopenfilename
import ipaddress

#_type = '6SL3210-1KE11-8AF2/4.7.13';
#_name = 'Device_1';

_typeArr = []
_nameArr = []

myproject = ''

mypath = ''

def async_func(_type, _name, _path):  
    print("tiaportal")
    mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)
    processes = tia.TiaPortal.GetProcesses() # Making a list of all running processes
    print (processes)
    # Creating a new project. Using try/except in case project allready exists
 
    #project_path = DirectoryInfo ('C:\\Openness\\PKI')
    
 
    try:
       print(_path)
       #myproject = mytia.Projects.Create(project_path, project_name)
       project_path = FileInfo (_path)
       global myproject
       myproject = mytia.Projects.OpenWithUpgrade(project_path)
       #print(myproject)
    except Exception as e:
       print (e)
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

    if count == 0:
        print ('Creating PLC1')
        PLC1_mlfb = 'OrderNumber:6ES7 513-1AL02-0AB0/V2.6'
        PLC1 = myproject.Devices.CreateWithItem(PLC1_mlfb, 'PLC1', 'PLC1')
  

    # display indices in the list
    for i in range(len(_type)):
        print(i, _type[i])
        print(i, _name[i])
        PN_mlfb = 'OrderNumber:'+ str(_type[i]);
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
        
        deviceItemComposition = device.DeviceItems;
      
        for deviceItem in deviceItemComposition:
            for info in deviceItem.GetAttributeInfos():
                print(str(device.Name)+': '+str(info.Name))
            
        
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

                ioSystem = subnet.IoSystems[0];
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


    try:

            #compiling all sw in all devices
        for device in myproject.Devices:
            device_item_aggregation = device.DeviceItems
            for deviceitem in device_item_aggregation:   
                    software_container = tia.IEngineeringServiceProvider(deviceitem).GetService[hwf.SoftwareContainer]()
                    if (software_container != None):
                        print(f'compiling: {deviceitem.Name}')
                        software_base = software_container.Software
                        
                        compile_service =  software_base.GetService[comp.ICompilable]()
                        result = compile_service.Compile()
                        
                        #Printing results from compiler
                        print(f'State: {result.State}')
                        print(f'Warning Count: {result.WarningCount}')
                        print(f'Error Count: {result.ErrorCount}')
                        print_comp(result.Messages)   

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
    #plc_block = software_base.BlockGroup.Blocks.Find("sinaSpeed2")
    #plc_block.Export(FileInfo('C:\\export\\tulos\\sinaSpeed2.xml'), tia.ExportOptions.WithDefaults)
    #plc_block0 = software_base.BlockGroup.Blocks.Find("sinaSpeed2_DB")
    #plc_block0.Export(FileInfo('C:\\export\\tulos\\sinaSpeed2_DB.xml'), tia.ExportOptions.WithDefaults)


    plc_block2 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\export\\result\\Drives.xml'), tia.ImportOptions.Override)
    plc_block4 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\export\\result\\sinaSpeed2.xml'), tia.ImportOptions.Override)
    plc_block5 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\export\\result\\sinaSpeed2_DB.xml'), tia.ImportOptions.Override)

    PlcTagTableGroup = software_base.TagTableGroup
    PlcTagTableGroup.TagTables.Import(FileInfo('C:\export\\result\\example.xml'), tia.ImportOptions.Override)

    plc_block3 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\export\\result\\DrivesData.xml'), tia.ImportOptions.Override)

    print('Demo complete!')
  

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
 
 
@app.route("/tiaportal/", methods=["POST"])
def tiaportal():
    
    global _typeArr
    global _nameArr
    global mypath

    print(_typeArr)
    print(_nameArr)
    print(mypath)
    
    if not mypath:
        return 400

    if not _typeArr: 
        return 400
    
    if not _nameArr:
        return 400
   
    
    x = threading.Thread(target=async_func, args=(_typeArr,_nameArr,mypath,))
    x.start()
     
    #return redirect('/')
    return render_template("index.html")

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

  
if __name__ == "__main__":
    app.run(debug=True)