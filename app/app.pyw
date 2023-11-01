from flask import Flask, render_template, request, url_for, redirect, jsonify
from flaskwebgui import FlaskUI # import FlaskUI
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
import openpyxl
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


@app.route("/load/", methods=["POST"])
def load():
 
    project = request.form['project']
    dll = request.form['dll']
    lib = request.form['lib']

    global mypath 
    mypath = project
    global dllpath
    dllpath = dll
    global libpath
    libpath = lib
   
    return render_template("index.html")


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

@app.route("/tiaportal/", methods=["POST"])
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

    if not _typeArr: 
        return 400
    
    if not _nameArr:
        return 400
   
    if not dllpath:
        return 400
    
    if not libpath:
       return 400
    
    getXML()

    from openness import startProcess
    startProcess(_typeArr, _nameArr, mypath, _consoleArr, dllpath, libpath, interface)
    
     
    #return redirect('/')
    return render_template("index.html")

@app.route("/console/")
def console():
     return render_template("console.html")


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


@app.route("/shutdown/")
def shutdown():
      
      print("shutdown")
      return RuntimeError("Server going down")


@app.route("/interface/")
def interfaceUser():

    global interface

    if interface is True:
        interface = False
    else:
        interface = True

    return render_template("index.html")

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