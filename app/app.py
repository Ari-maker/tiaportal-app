from flask import Flask, render_template, request, url_for, redirect, jsonify
from flaskwebgui import FlaskUI # import FlaskUI
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
import openpyxl
import json
app = Flask(__name__)

  
#from openness import startTiaPortal
#startTiaPortal()
#from openness import startProcess
from tkinter.filedialog import askopenfilename


#_type = '6SL3210-1KE11-8AF2/4.7.13';
#_name = 'Device_1';

_typeArr = []
_nameArr = []
_consoleArr = []

myproject = ''

mypath = ''

counter = 2 # 3

dllpath = ''

libpath = ''

interface = True

tia = []
project = []
dlist = []

directory = [['project'],['tagit','Drives','DrivesData']]

  
@app.route("/openproject/", methods=["GET"])
def openproject():
    print('project path')
    global mypath
    mypath = askopenfilename(filetypes=(("Project file", "*.ap18"),("All files", "*.*") ))


    return jsonify({'project':mypath})


@app.route("/selectdll/", methods=["GET"])
def selectdll():
    print('dll path')
    global dllpath
    dllpath = askopenfilename(filetypes=(("Siemens.Engineering file", "*.dll"),("All files", "*.*") ))


    return jsonify({'dll':dllpath})


@app.route("/selectlib/", methods=["GET"])
def selectlib():
    print('lib path')
    global libpath
    libpath = askopenfilename(filetypes=(("al file", "*.al18"),("All files", "*.*") ))


    return jsonify({'lib':libpath})


@app.route("/delete/", methods=["POST"])
def delete():
 
    name = request.form['name']
    name = name.capitalize()
    index = _nameArr.index(name)
    _nameArr.remove(name)
    _typeArr.pop(index)


    return jsonify({'type':_typeArr, 'name':_nameArr})


@app.route("/load/")
def load():


    global mypath 
    global dllpath
    global libpath

    # Opening JSON file
    with open('paths.json', 'r') as openfile:
       # Reading from json file
        json_object = json.load(openfile)
        mypath = json_object['project']
        dllpath = json_object['dll']
        libpath = json_object['lib']

   
    return jsonify({'project':mypath, 'dll':dllpath,'lib':libpath})


@app.route("/add/", methods=["POST"])
def add():

    if request.method == "POST":
            _type =  request.form['type']
            _name =  request.form['name']
 

    if _type == '' or _name == '':
        return 400
    

    _name = _name.replace(" ", "")
    _name = _name.capitalize()

    global _typeArr
    global _nameArr
    if _name in _nameArr:
       return 400
 
    _typeArr.append(_type)
    _nameArr.append(_name)
 
    print(_typeArr)
    
    print(_nameArr)

    tex = "Inst"+_name
    directory[0].append(tex)

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
    global interface
    interface = True
   

    return render_template("index.html")

def getXML():

    print('XML')

    global _nameArr
    global counter

    from openness import writeXML
    writeXML(_nameArr, counter)

    return render_template("index.html")

@app.route("/add")
def addFunc():
   
    #return jsonify(directory)
    name = request.args.get('name')
    print(name)

    directory.append([name])

    return render_template('device.html', mylist=directory)




@app.route("/tia/")
def tiafunc():
    if len(tia) != 0:
        return jsonify({'tia':1,'dlist:':dlist})

    return jsonify({'tia':0})

@app.route("/tiaportal/", methods=["POST"])
def initTia():
    global _typeArr
    global _nameArr
    global mypath
    global _consoleArr
    global dllpath
    global libpath
    global interface
   
    print(_typeArr)
    print(_nameArr)
    print(mypath)
    

    if not _typeArr: 
        return 400
    
    if not _nameArr:
        return 400
   
    if not dllpath:
        return 400
    
    if not libpath:
       return 400
    
    if not tia:
        return 400
    
    if not project:
        return 400
    
    getXML()

    from openness import startProcess
    startProcess(_typeArr, _nameArr, _consoleArr, dllpath, libpath, tia[0], project[0], directory)

    #return redirect('/')
    return render_template("device.html")


@app.route("/initPortal/", methods=["POST"])
def tiaportal():
    
    global _typeArr
    global _nameArr
    global mypath
    global _consoleArr
    global dllpath
    global libpath
    global interface

    _consoleArr = []

    print(_typeArr)
    print(_nameArr)
    print(mypath)
    
    if not mypath:
        return 400
   
    if not dllpath:
        return 400
    
    if not libpath:
       return 400
    
 
    
    getXML()

    #from openness import startProcess
    #startProcess(_typeArr, _nameArr, mypath, _consoleArr, dllpath, libpath, tia)


    from openness import initProcess
    initProcess(_consoleArr, mypath,dllpath,interface, tia, project, dlist)
     
    #return redirect('/')

    if len(tia) != 0:
        return jsonify({'tia':1, 'dlist':dlist})

    return jsonify({'tia':0})

@app.route("/console/")
def console():
     return render_template("console.html")

@app.route("/device/")
def device():

    return render_template('device.html', mylist=directory)


@app.route("/importExcel/")
def importExcel():

    excelPath = askopenfilename(filetypes=(("Excel file", "*.xlsx"),("All files", "*.*") ))

    if excelPath is None or excelPath == "":
        return render_template("index.html")

    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(excelPath)
    
    # Define variable to read sheet
    dataframe1 = dataframe.active
    
    foundPaths = True
    foundDevices = False
    pathsRow = -1

    # Iterate the loop to read the cell values
    for row in range(0, dataframe1.max_row):
        index = 0

        for col in dataframe1.iter_cols(1, dataframe1.max_column):
        

            # paths
            if col[row].value != None and foundPaths == True:

                pathsRow = row+1

                if(index == 0):
                    global mypath
                    mypath = col[pathsRow].value
                if(index == 1):
                    global dllpath
                    dllpath = col[pathsRow].value
                if(index == 2):
                    global libpath
                    libpath = col[pathsRow].value
                    foundPaths = False
                    foundDevices = True

       # devices
            elif col[row].value != None and foundDevices == True and row > (pathsRow+1):
              
                if(index == 0):
                    _nameArr.append(col[row].value)
                if(index == 1):
                    _typeArr.append(col[row].value)
              

            index = index + 1

    return jsonify({'type':_typeArr, 'name':_nameArr})


@app.route("/interface/")
def interfaceUser():

    global interface

    if interface is True:
        interface = False
    else:
        interface = True

    return jsonify({'interface':str(interface)})


@app.route("/updateDirectory/", methods=["POST"])
def updateDirectoryFunc():
     _name = request.form['folderName']

     #directory.update({_name:[]})

     return jsonify(directory)

@app.route("/updateFile/", methods=["POST"])
def updateDIR():
       _folder = request.form['folder']
       _file = request.form['file']

       print(_folder)
       print(_file)


        
       for folder in directory:
           for file in folder:
               if file == _file:
                   folder.remove(file)

           if folder[0] == _folder:
               folder.append(_file)


       if _folder == "":
           directory[0].append(_file)
          

       return render_template('device.html', mylist=directory) 



@app.route("/saveFile/", methods=["POST"])
def saveFile():
    _project = request.form['project']
    _dll = request.form['dll']
    _lib = request.form['lib']

    filedata = {
    "project": _project,
    "dll": _dll,
    "lib": _lib
    }

    # Serializing json
    json_object = json.dumps(filedata, indent=3)

    # Writing to sample.json
    with open("paths.json", "w") as outfile:
        outfile.write(json_object)

    return jsonify({'file':str(filedata)})  


@app.route("/getConsoleData/")
def consoleData():
   
     global _consoleArr

     print(_consoleArr)

     return jsonify({'consoleArr':str(_consoleArr)})
    

if __name__ == "__main__":
    #app.run(debug=True)
    #ui.run()
    FlaskUI(app=app, width=1280 , height=800, server="flask").run()
     #ui = FlaskUI(app, width=500, height=500) # add app and parameters