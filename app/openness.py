import time
import threading
import ipaddress
import os 

import xml.etree.ElementTree as ET
ET.register_namespace("", "http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v4")


def async_func(_type, _name, _path, _consoleArr, dllPath, libPath):  
    
    import clr
    #clr.AddReference('C:\\Program Files\\Siemens\\Automation\\Portal V18\PublicAPI\\V18\\Siemens.Engineering.dll')
    clr.AddReference(dllPath)
    from System.IO import DirectoryInfo, FileInfo
    import Siemens.Engineering as tia
    import Siemens.Engineering.HW.Features as hwf
    import Siemens.Engineering.SW.Units as units
    import Siemens.Engineering.Compiler as comp
    import Siemens.Engineering.Library as lib
    import os

    
    print("tiaportal")
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
       #global myproject
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
            ioSystem = n_interfaces[0].IoControllers[0].CreateIoSystem("PNIO")
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


    # global library
    #availableLibraries = mytia.GlobalLibraries.GetGlobalLibraryInfos()

    #for libInfo in availableLibraries:
          #print(" Library Name: {0}", libInfo.Name)
          #print(" Library Path: {0}", libInfo.Path)
          #print(" Library Type: {0}", libInfo.LibraryType)
          #print(" Library IsOpen: {0}", libInfo.IsOpen)
      
          #if libInfo.Name == "testLib":
                  #libraryOpenedWithInfo = mytia.GlobalLibraries.Open(libInfo)
                  #masterCopy = libraryOpenedWithInfo.MasterCopyFolder.MasterCopies.Find("SinaSpeedTest")               
                  #libBlock = software_base.BlockGroup.Blocks.CreateFrom(masterCopy)
     

    userLib = mytia.GlobalLibraries.Open(FileInfo(libPath), tia.OpenMode.ReadWrite)
    masterCopy = userLib.MasterCopyFolder.MasterCopies.Find("SinaSpeedTest")               
    libBlock = software_base.BlockGroup.Blocks.CreateFrom(masterCopy)


    #plc_block = software_base.BlockGroup.Blocks.Find("Drives")
    #plc_block.Export(FileInfo('C:\\export\\tulos\\Drives.xml'), tia.ExportOptions.WithDefaults)
    #plc_block0 = software_base.BlockGroup.Blocks.Find("sinaSpeed2_DB")
    #plc_block0.Export(FileInfo('C:\\export\\tulos\\sinaSpeed2_DB.xml'), tia.ExportOptions.WithDefaults)




    # DrivesData

    tree = ET.parse('./xmltemplate/DrivesData.xml')
    root = tree.getroot()

    for item in root.findall('SW.Blocks.GlobalDB'):
        attributeList=item.find('AttributeList')
        Interface=attributeList.find('Interface')
        Sections=Interface.find('Sections')
        Section=Sections.find('Section')

     
        db_array = _name
        loopMax = len(_name)

        for i in range(loopMax):
            
            # plc tags
            plcTagTableSystemGroup = software_base.TagTableGroup
            constant1 = plcTagTableSystemGroup.TagTables[0].SystemConstants.Find(db_array[i]+"~PROFINET_interface~ModuleAccessPoint")
            constant2 = plcTagTableSystemGroup.TagTables[0].SystemConstants.Find(db_array[i]+"~PROFINET_interface~Standard_telegram_1")



            member = f"""
      <Member Name="{db_array[i]}" Datatype="&quot;typeSinaSpeedInterface&quot;" Remanence="NonRetain" Accessibility="Public">
            <AttributeList>
              <BooleanAttribute Name="ExternalAccessible" SystemDefined="true">true</BooleanAttribute>
              <BooleanAttribute Name="ExternalVisible" SystemDefined="true">true</BooleanAttribute>
              <BooleanAttribute Name="ExternalWritable" SystemDefined="true">true</BooleanAttribute>
              <BooleanAttribute Name="SetPoint" SystemDefined="true">false</BooleanAttribute>
            </AttributeList>
            <Sections>
              <Section Name="None">
                <Member Name="control" Datatype="Struct">
                  <Member Name="enableAxis" Datatype="Bool" />
                  <Member Name="ackError" Datatype="Bool" />
                  <Member Name="speedSp" Datatype="Real" />
                  <Member Name="refSpeed" Datatype="Real" />
                  <Member Name="configAxis" Datatype="Word" />
                  <Member Name="hwidStw" Datatype="HW_SUBMODULE">
                    <StartValue>{constant1.Value}</StartValue>
                  </Member>
                  <Member Name="hwidZsw" Datatype="HW_SUBMODULE">
                    <StartValue>{constant2.Value}</StartValue>
                  </Member>
                </Member>
                <Member Name="status" Datatype="Struct">
                  <Member Name="axisEnabled" Datatype="Bool" />
                  <Member Name="lockout" Datatype="Bool" />
                  <Member Name="actVelocity" Datatype="Real" />
                  <Member Name="error" Datatype="Bool" />
                  <Member Name="status" Datatype="Int" />
                  <Member Name="diagId" Datatype="Word" />
                </Member>
              </Section>
            </Sections>
          </Member>
            """
            
            new_field = ET.fromstring(member)
            Section.insert(1, new_field)


    tree.write("C:\\openness-app\\DrivesData.xml", encoding='unicode')

    with open("C:\\openness-app\\DrivesData.xml") as f:
      lines = f.readlines()


    lines[0] = "<Document>\n"

    index = 0
    for toisto in lines:
        if lines[index].find('linkki'):
          lines[index] = lines[index].replace('linkki', 'xmlns')
          index = index + 1


    with open("C:\\openness-app\\DrivesData.xml", "w") as f:
        f.writelines(lines)




    # EXPORT

    plc_block2 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\\openness-app\\Drives.xml'), tia.ImportOptions.Override)
    unit_block1 = software_base.TypeGroup.Types.Import(FileInfo('C:\\openness-app\\typeSinaSpeedInterface.xml'), tia.ImportOptions.Override)
    plc_block1 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\\openness-app\\DrivesData.xml'), tia.ImportOptions.Override)
  
    



    #unit = software_base.TypeGroup.Types.Find("typeSinaSpeedInterface")
    #unit.Export(FileInfo('C:\\export\\tulos\\typeSinaSpeedInterface.xml'), tia.ExportOptions.WithDefaults)


    blockComposition = software_base.BlockGroup.Blocks
    isAutoNumber = True
    instanceOfName = "SinaSpeedTest"
    number = 1

    # sinaSpeedTest
    index = 0
    for i in range(len(_name)):
      iDBName = f"Inst{_name[i]}"    
      iDbBlock = blockComposition.CreateInstanceDB(iDBName, isAutoNumber, number, instanceOfName)
      index = index + 1


    print('Demo complete!')
    _consoleArr.append('Demo complete!')


def writeXML(_nameArr, counter):

    print('XML')

        
    # path 
    path = 'C:\\openness-app'
        
    # Create the directory 
    # 'GeeksForGeeks' in 
    # '/home / User / Documents' 
    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error)  

    tree = ET.parse('./xmltemplate/Drives.xml')
    root = tree.getroot()

    def counterFunc():
        nonlocal  counter
        counter = len(_nameArr)+(counter+1)
        return str(counter)
    
  
    for item in root.findall('SW.Blocks.OB'):
        itemid=item.find('ObjectList')
        
        
        db_array = _nameArr
        loop = (2 + len(db_array)) # default 2
        loopMax = len(_nameArr)
        index = int(len(_nameArr)-1)
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
      </Symbol>
    </Access>
    <Call UId="22">
      <CallInfo Name="SinaSpeedTest" BlockType="FB">
        <Instance Scope="GlobalVariable" UId="23">
          <Component Name="Inst{db_array[i]}" />
        </Instance>
        <Parameter Name="data" Section="InOut" Type="&quot;typeSinaSpeedInterface&quot;" />
      </CallInfo>
    </Call>
  </Parts>
  <Wires>
    <Wire UId="24">
      <Powerrail />
      <NameCon UId="22" Name="en" />
    </Wire>
    <Wire UId="25">
      <IdentCon UId="21" />
      <NameCon UId="22" Name="data" />
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
          index = index - 1


    tree.write("C:\\openness-app\\Drives.xml", encoding='unicode')
    #tree.write("XMLtest.xml", encoding='unicode')


    with open("C:\\openness-app\\Drives.xml") as f:
      lines = f.readlines()


    lines[0] = "<Document>\n"

    index = 0
    for toisto in lines:
        if lines[index].find('linkki'):
          lines[index] = lines[index].replace('linkki', 'xmlns')
          index = index + 1


    with open("C:\\openness-app\\Drives.xml", "w") as f:
        f.writelines(lines)



    # sinaSpeedInterface
    tree = ET.parse('./xmltemplate/typeSinaSpeedInterface.xml')
    tree.write("C:\\openness-app\\typeSinaSpeedInterface.xml", encoding='unicode')

    with open("C:\\openness-app\\typeSinaSpeedInterface.xml") as f:
      lines = f.readlines()


    lines[0] = "<Document>\n"

    index = 0
    for toisto in lines:
        if lines[index].find('linkki'):
          lines[index] = lines[index].replace('linkki', 'xmlns')
          index = index + 1


    with open("C:\\openness-app\\typeSinaSpeedInterface.xml", "w") as f:
        f.writelines(lines)



def startProcess(_type, _name, _path, _console, dllPath, libPath):
   


   x = threading.Thread(target=async_func, args=(_type,_name,_path,_console,dllPath,libPath,))
   x.start()