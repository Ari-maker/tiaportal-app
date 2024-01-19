import threading
import ipaddress
import os 
import xml.etree.ElementTree as ET
ET.register_namespace("", "http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v4")

# PROJECT PAGE
# The function is called when the 'Start TIA Portal' button is clicked.
# The purpose of the function is to start a TIA Portal project. 
# "_console" parameter can be used to send logs to the ui console
#  "_path" parameter is the project path.
# "dllPath" parameter is the path to "Siemens.Engineering.dll"
# "If the "ui" parameter is true, TIA Portal starting "WithUserInterface"; otherwise, "WithoutUserInterface".
# "project" parameter is the project instance.
# "tiaportal" parameter is the TIA instance.
# "dlist" parameter is the device list.
def init_func(_console, _path, dllPath, ui, tiaportal, project, dlist):
    try:
      # If the path to the 'Siemens.Engineering.dll' is valid, Siemens libraries are imported.
      import clr
      clr.AddReference(dllPath)
      from System.IO import FileInfo
      import Siemens.Engineering as tia
      import Siemens.Engineering.HW.Features as hwf
      import Siemens.Engineering.SW.Units as units
      import Siemens.Engineering.Compiler as comp
      import Siemens.Engineering.Library as lib
      import os

      # Add to the console.
      print("tiaportal")
      _console.append("tiaportal")

      # "If the "ui" parameter is true, TIA Portal starting "WithUserInterface"; otherwise, "WithoutUserInterface".
      if ui is True:
        mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)
      else:
        mytia = tia.TiaPortal(tia.TiaPortalMode.WithoutUserInterface)

      # Making a list of all running processes
      processes = tia.TiaPortal.GetProcesses() 
      # Add to the console.
      print (processes)
      _console.append("process: "+str(processes))

      # "tiaportal" parameter is now "mytia"
      tiaportal.append(mytia)

      try:
        # For loop for iterating over the 'HardwareCatalog' list
        for deviceList in mytia.HardwareCatalog.Find("G120C PN"):
           d = deviceList.TypeIdentifier
           d = d.replace("OrderNumber:", "")
           print(d)
           # Add the device to the 'dlist' list.
           dlist.append(d)

        # Add to the console.
        print(_path)
        _console.append("project path: "+_path)
    
        # "project_path" is now "_path"
        project_path = FileInfo (_path)
        # "myproject" is now an instance of the project.
        myproject = mytia.Projects.OpenWithUpgrade(project_path)
        # "project" parameter is now "myproject"
        project.append(myproject)

        # Add to the console.
        _console.append("project opened")
           
      except Exception as e:
        # Add an error to the console.
        print (e)
        _console.append(e)
        pass

    except Exception as e:
        # Add an error to the console.
        _console.append('An unexpected error has occurred. Please try again!!')
        _console.append('An exception occurred: {}'.format(e))


# The function is called when the 'compile' button is clicked
# The purpose of the function is to generate program blocks in the project.
# "_type" is a list of OrderNumbers.
# "_name" is a list of device names.
# "_consoleArr" parameter can be used to send logs to the ui console.
# "dllPath" parameter is the path to "Siemens.Engineering.dll".
# "libPath" is the path to the library.
# "mytia" parameter is the TIA instance.
# "myproject" parameter is the project instance.
def async_func(_type, _name, _consoleArr, dllPath, libPath, mytia, myproject, directory):  

  # Using try/except in case project allready exists
  try:
      # If the path to the 'Siemens.Engineering.dll' is valid, Siemens libraries are imported.
      import clr
      clr.AddReference(dllPath)
      from System.IO import FileInfo
      import Siemens.Engineering as tia
      import Siemens.Engineering.HW.Features as hwf
      import Siemens.Engineering.SW.Units as units
      import Siemens.Engineering.Compiler as comp
      import Siemens.Engineering.Library as lib
      import os

      # Check if any PLC exists, if not, create a new PLC
      count = 0
      for device in myproject.Devices:
          count+=1

      # Add to the console.
      print('Devices: '+ str(count))
      _consoleArr.append('Devices: '+ str(count))

      if count == 0:
          print ('Creating PLC1')
          _consoleArr.append('Creating PLC1')
          PLC1_mlfb = 'OrderNumber:6ES7 511-1AL03-0AB0/V3.0'
          # creating a new PLC
          PLC1 = myproject.Devices.CreateWithItem(PLC1_mlfb, 'PLC1', 'PLC1')
    
      # For loop for iterating over the added devices
      for i in range(len(_type)):
          print(i, _type[i])
          _consoleArr.append(str(_type[i]))
          print(i, _name[i])
          _consoleArr.append(str(_name[i]))
          PN_mlfb = 'OrderNumber:'+ str(_type[i])
          # Creating a new device in the TIA Portal project.
          PN = myproject.Devices.CreateWithItem(PN_mlfb,  str(_name[i]), None)

      # Adding IO cards to the PLC and IO station
      # This is basic to show how it works, using loops with checks (CanPlugNew) to see if the slot is available
      # Creating network, iosytem and setting IP adresses
      # creating a list of all found network interfaces on all stations in the station list
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

      # Assigning an IP to each item in the list
      if count == 0:
          n_interfaces[0].Nodes[0].SetAttribute('Address','192.168.0.130')

      add = n_interfaces[0].Nodes[0].GetAttribute('Address')
      
      # Add to the console.
      print(add)
      _consoleArr.append("IP Address: "+str(add))

      # Creating subnet and IO system on the first item in the list
      # Connects to subnet for remaining devices, if IO device it gets assigned to the IO system
      for n in n_interfaces:
          if count == 0:
              count = 1
              subnet = n_interfaces[0].Nodes[0].CreateAndConnectToSubnet("Profinet")
              ioSystem = n_interfaces[0].IoControllers[0].CreateIoSystem("PNIO")
          if n_interfaces.index(n) != 0:
              
              t = str(ipaddress.ip_address(add) + 256)
              n_interfaces[n_interfaces.index(n)].Nodes[0].SetAttribute('Address', t)
              add = t
              subnet = ''

              for subnets in myproject.Subnets:
                  subnet = subnets

              try:

                  ioSystem = subnet.IoSystems[0]
                  n_interfaces[n_interfaces.index(n)].Nodes[0].ConnectToSubnet(subnet)
                  if (n_interfaces[n_interfaces.index(n)].IoConnectors.Count) >> 0:
                      n_interfaces[n_interfaces.index(n)].IoConnectors[0].ConnectToIoSystem(ioSystem)
              
              except Exception:
                  pass    

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

          #compiling all devices
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

      # PLC
      deviceItem = myproject.Devices[0].DeviceItems[1]
      
      # Software container
      software_container = tia.IEngineeringServiceProvider(deviceItem).GetService[hwf.SoftwareContainer]()
    
      # Software
      software_base = software_container.Software

      print(str(deviceItem.Name))  
      print(str(software_base.Name))  
      _consoleArr.append(str(deviceItem.Name))  
      _consoleArr.append(str(software_base.Name))  

      # The command opens the selected library
      userLib = mytia.GlobalLibraries.Open(FileInfo(libPath), tia.OpenMode.ReadWrite)
      # Get 'SinaSpeedTest' block from library
      typesLib = userLib.TypeFolder.Types.Find("SinaSpeedTest")   
      typeVersion = typesLib.Versions[0]
      # Import 'SinaSpeedTest' block into the project.       
      libBlock = software_base.BlockGroup.Blocks.CreateFrom(typeVersion)

      _consoleArr.append("SinaSpeedTest")

      # DrivesData
      # Open the DrivesData.xml file
      tree = ET.parse('./xml/DrivesData.xml')
      root = tree.getroot()

      # For loop for iterating over 'SW.Blocks.GlobalDB' from the file.
      for item in root.findall('SW.Blocks.GlobalDB'):
          attributeList=item.find('AttributeList')
          Interface=attributeList.find('Interface')
          Sections=Interface.find('Sections')
          Section=Sections.find('Section')

          # List of device names.
          db_array = _name
          loopMax = len(_name)

          # For loop for iterating over device names
          for i in range(loopMax):
              
              # System constants
              plcTagTableSystemGroup = software_base.TagTableGroup
              constant1 = plcTagTableSystemGroup.TagTables[0].SystemConstants.Find(db_array[i]+"~PROFINET_interface~ModuleAccessPoint")
              constant2 = plcTagTableSystemGroup.TagTables[0].SystemConstants.Find(db_array[i]+"~PROFINET_interface~Standard_telegram_1")


              # Add the XML structure below to the 'Section'.
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


      # Write the file.
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

      _consoleArr.append("DrivesData")

      # Import typeSinaSpeedInterface
      unit_block1 = software_base.TypeGroup.Types.Import(FileInfo('C:\\openness-app\\typeSinaSpeedInterface.xml'), tia.ImportOptions.Override)

      # Function to convert the UI tree structure to be compatible with the Openness interface.
      # 'array' is the current folder/file.
      # If 'nest' is false, root folder; otherwise, not a root folder.
      # 'usergroup' is a program block instance.
      def treeToOpenness(array, nest, usergroup):
        
          for node in array:

              if isinstance(node, dict):
                  # groups
                  currentkey = ''
                  for key in node.keys(): 
                      currentkey = key

                  print("created: " + currentkey)   
                  _consoleArr.append("created folder: " + currentkey) 
                  # check if root
                  if nest is False:
                      usergroup = software_base.BlockGroup.Groups.Create(currentkey)
                  else:
                      usergroup = usergroup.Groups.Create(currentkey)


                  for file in node[currentkey]["children"]:
                      if isinstance(file, dict):
                          # once!
                          for key in file.keys(): 
                      
                              treeToOpenness(node[currentkey]["children"], True, usergroup)
                      else:
                          if file == "Drives [OB]":
                              print("_Drives")
                              _consoleArr.append("Drives") 
                              # import Drives
                              usergroup.Blocks.Import(FileInfo('C:\\openness-app\\Drives.xml'), tia.ImportOptions.Override) 

                          if file == "DrivesData [DB]":
                              print("_DrivesData")
                              _consoleArr.append("DrivesData") 
                              # import DrivesData
                              usergroup.Blocks.Import(FileInfo('C:\\openness-app\\DrivesData.xml'), tia.ImportOptions.Override) 
                          if "Inst" in file:
                              blockComposition = usergroup.Blocks
                              isAutoNumber = True
                              instanceOfName = "SinaSpeedTest"
                              number = 1
                              file = file.replace(" [DB]", "")
                              _consoleArr.append(file) 
                              iDbBlock = blockComposition.CreateInstanceDB(file, isAutoNumber, number, instanceOfName)

              elif nest is False: 
                  # main directory (no groups)
                  if node == "Drives [OB]":
                      print("Drives")
                      _consoleArr.append("Drives") 
                      # import Drives
                      plc_block2 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\\openness-app\\Drives.xml'), tia.ImportOptions.Override)
                  if node == "DrivesData [DB]":
                      print("DrivesData")
                      _consoleArr.append("DrivesData") 
                      # import DrivesData
                      plc_block1 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\\openness-app\\DrivesData.xml'), tia.ImportOptions.Override)
                  if "Inst" in node:
                      blockComposition = software_base.BlockGroup.Blocks
                      isAutoNumber = True
                      instanceOfName = "SinaSpeedTest"
                      number = 1
                      node = node.replace(" [DB]", "")
                      _consoleArr.append(node) 
                      iDbBlock = blockComposition.CreateInstanceDB(node, isAutoNumber, number, instanceOfName)
              
      usergroup = 0        
      treeToOpenness(directory["Parent"]["children"], False, usergroup)

      _consoleArr.append("export xml")
      _consoleArr.append("CreateInstanceDB")

      # Program block generation completed.
      print('Demo complete!')
      _consoleArr.append('Demo complete!')

      # Dispose
      mytia.Dispose()

  except Exception as e:
     _consoleArr.append('An unexpected error has occurred. Please try again!!')
     _consoleArr.append('An exception occurred: {}'.format(e))

# Write XML files to 'C:\openness-app'.
def writeXML(_nameArr, counter):

    print('XML')

    # path 
    path = 'C:\\openness-app'
        
    # Create the directory 
    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error)  

    tree = ET.parse('./xml/Drives.xml')
    root = tree.getroot()

    # ID
    def counterFunc():
        nonlocal  counter
        counter = len(_nameArr)+(counter+1)
        return str(counter)
    
  
    for item in root.findall('SW.Blocks.OB'):
        itemid=item.find('ObjectList')
        
        
        db_array = _nameArr
        loop = (2 + len(db_array))
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


    # Drives
    tree.write("C:\\openness-app\\Drives.xml", encoding='unicode')
  
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
    tree = ET.parse('./xml/typeSinaSpeedInterface.xml')
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


def initProcess(_console, path, dllPath, interface, tia, project, dlist):
  try:

    x = threading.Thread(target=init_func, args=(_console,path,dllPath,interface,tia,project,dlist))
    x.start()
    x.join()
    
  except Exception as e:
    _console.append('An unexpected error has occurred. Please try again!!')
    _console.append('An exception occurred: {}'.format(e))

def startProcess(_type, _name, _console, dllPath, libPath, tia, project, directory):
  try:

    x = threading.Thread(target=async_func, args=(_type,_name,_console,dllPath,libPath,tia,project,directory,))
    x.start()

  except Exception as e:
    _console.append('An unexpected error has occurred. Please try again!!')
    _console.append('An exception occurred: {}'.format(e))

# EXCEL PAGE
# The function is called when the 'Start TIA Portal' button is clicked
# The purpose of the function is to generate program blocks in the project.
# "_type" is a list of OrderNumbers.
# "_name" is a list of device names.
# "_path" is the project path.
# "_consoleArr" parameter can be used to send logs to the ui console.
# "dllPath" parameter is the path to "Siemens.Engineering.dll".
# "libPath" is the path to the library.
 # "If the "ui" parameter is true, TIA Portal starting "WithUserInterface"; otherwise, "WithoutUserInterface".
def async_funcExcel(_type, _name, _path, _consoleArr, dllPath, libPath, ui):  
  # Using try/except in case project allready exists
  try:
      # If the path to the 'Siemens.Engineering.dll' is valid, Siemens libraries are imported.
      import clr
      clr.AddReference(dllPath)
      from System.IO import FileInfo
      import Siemens.Engineering as tia
      import Siemens.Engineering.HW.Features as hwf
      import Siemens.Engineering.SW.Units as units
      import Siemens.Engineering.Compiler as comp
      import Siemens.Engineering.Library as lib
      import os

      # Add to the console.
      print("tiaportal")
      _consoleArr.append("tiaportal")

      mytia = ''

      # "If the "ui" parameter is true, TIA Portal starting "WithUserInterface"; otherwise, "WithoutUserInterface".
      if ui is True:
        mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)
      else:
        mytia = tia.TiaPortal(tia.TiaPortalMode.WithoutUserInterface)

      # Making a list of all running processes
      processes = tia.TiaPortal.GetProcesses() 
      print (processes)
      _consoleArr.append("process: "+str(processes))

      try:
        print(_path)
        _consoleArr.append("project path: "+_path)
        # "project_path" is now "_path"
        project_path = FileInfo (_path)
        # "myproject" is now an instance of the project.
        myproject = mytia.Projects.OpenWithUpgrade(project_path)
      except Exception as e:
        print (e)
        _consoleArr.append(e)
        pass

      # Check if any PLC exists, if not, create a new PLC 
      count = 0
      for device in myproject.Devices:
          count+=1

      print('Devices: '+ str(count))
      _consoleArr.append('Devices: '+ str(count))

      if count == 0:
          print ('Creating PLC1')
          _consoleArr.append('Creating PLC1')
          PLC1_mlfb = 'OrderNumber:6ES7 511-1AL03-0AB0/V3.0'
          # creating a new PLC  
          PLC1 = myproject.Devices.CreateWithItem(PLC1_mlfb, 'PLC1', 'PLC1')
    

      # For loop for iterating over the added devices
      for i in range(len(_type)):
          print(i, _type[i])
          _consoleArr.append(str(_type[i]))
          print(i, _name[i])
          _consoleArr.append(str(_name[i]))
          PN_mlfb = 'OrderNumber:'+ str(_type[i])
          # Creating a new device in the TIA Portal project.
          PN = myproject.Devices.CreateWithItem(PN_mlfb,  str(_name[i]), None)

      # Adding IO cards to the PLC and IO station
      # This is basic to show how it works, use loops with checks (CanPlugNew) to see if the slot is available
      #  Creating network, iosytem and setting IP adresses
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

      # Assigning an IP to each item in the list
      if count == 0:
          n_interfaces[0].Nodes[0].SetAttribute('Address','192.168.0.130')

      add = n_interfaces[0].Nodes[0].GetAttribute('Address')
      print(add)
      _consoleArr.append("IP Address: "+str(add))

      # Creating subnet and IO system on the first item in the list
      # Connects to subnet for remaining devices, if IO device it gets assigned to the IO system
      for n in n_interfaces:
          if count == 0:
              count = 1
              subnet = n_interfaces[0].Nodes[0].CreateAndConnectToSubnet("Profinet")
              ioSystem = n_interfaces[0].IoControllers[0].CreateIoSystem("PNIO")
          if n_interfaces.index(n) != 0:
              
              t = str(ipaddress.ip_address(add) + 256)
              n_interfaces[n_interfaces.index(n)].Nodes[0].SetAttribute('Address', t)
              add = t
              subnet = ''

              for subnets in myproject.Subnets:
                  subnet = subnets


              try:

                  ioSystem = subnet.IoSystems[0]
                  n_interfaces[n_interfaces.index(n)].Nodes[0].ConnectToSubnet(subnet)
                  if (n_interfaces[n_interfaces.index(n)].IoConnectors.Count) >> 0:
                      n_interfaces[n_interfaces.index(n)].IoConnectors[0].ConnectToIoSystem(ioSystem)
              
              except Exception:
                  pass    

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

    
      deviceItem = myproject.Devices[0].DeviceItems[1]
    
      software_container = tia.IEngineeringServiceProvider(deviceItem).GetService[hwf.SoftwareContainer]()
    
      software_base = software_container.Software
      print(str(deviceItem.Name))  
      print(str(software_base.Name))  

      _consoleArr.append(str(deviceItem.Name))  
      _consoleArr.append(str(software_base.Name))  


      userLib = mytia.GlobalLibraries.Open(FileInfo(libPath), tia.OpenMode.ReadWrite)
      typesLib = userLib.TypeFolder.Types.Find("SinaSpeedTest")   
      typeVersion = typesLib.Versions[0]         
      libBlock = software_base.BlockGroup.Blocks.CreateFrom(typeVersion)

      _consoleArr.append("SinaSpeedTest")

      # DrivesData

      tree = ET.parse('./xml/DrivesData.xml')
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


      _consoleArr.append("DrivesData")

      plc_block2 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\\openness-app\\Drives.xml'), tia.ImportOptions.Override)
      unit_block1 = software_base.TypeGroup.Types.Import(FileInfo('C:\\openness-app\\typeSinaSpeedInterface.xml'), tia.ImportOptions.Override)
      plc_block1 = software_base.BlockGroup.Blocks.Import(FileInfo('C:\\openness-app\\DrivesData.xml'), tia.ImportOptions.Override)
    
      _consoleArr.append("export xml")

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


      _consoleArr.append("CreateInstanceDB")


      print('Demo complete!')
      _consoleArr.append('Demo complete!')

      mytia.Dispose()

  except Exception as e:
     _consoleArr.append('An unexpected error has occurred. Please try again!!')
     _consoleArr.append('An exception occurred: {}'.format(e))



def startProcessExcel(_type, _name, _path, _console, dllPath, libPath, interface):
   
  try:

    x = threading.Thread(target=async_funcExcel, args=(_type,_name,_path,_console,dllPath,libPath,interface,))
    x.start()
    

  except Exception as e:
    _console.append('An unexpected error has occurred. Please try again!!')
    _console.append('An exception occurred: {}'.format(e))