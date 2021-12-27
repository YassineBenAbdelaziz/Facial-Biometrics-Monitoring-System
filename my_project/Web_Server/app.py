from flask import Flask,render_template,request,redirect,url_for,session
import os
import cv2 as cv
import numpy as np
from ..Database import BaseManager as dm

f = open("compteur.txt","r")
i = int(f.read())
f.close()
db=dm.Base()
app = Flask(__name__)
app.secret_key = '_kyG#IO5pD9(oS0_X'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page route function
    """
    if request.method == 'POST':
        if request.form['user']== 'admin' and request.form['pass'] =='123456' :
            session['username'] = 'admin'
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route("/addface",methods=['GET','POST'])
def add_to_data_set() :
    """
    Route function that adds new faces to data set.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not (file.filename.endswith(".jpg")):
            return redirect(request.url)
        name = request.form['name']
        if os.path.exists("My_project/Live_Recognizer/DataSet/"+name) :
            f = open(os.path.join("My_project/Live_Recognizer/DataSet",name,"counter.txt"),"r+")
            counter = int(f.read())
            file.save(os.path.join("My_project/Live_Recognizer/DataSet",name,"{}{}.jpg".format(name,counter) ))
            counter +=1
            f.seek(0,0)
            f.write(str(counter))
            f.close()
        else :
            os.makedirs("My_project/Live_Recognizer/DataSet/"+name)
            f = open(os.path.join("My_project/Live_Recognizer/DataSet",name,"counter.txt"),"w")
            f.write("1")
            f.close()
            file.save(os.path.join("My_project/Live_Recognizer/DataSet",name,name + "0" + ".jpg" ))
        return redirect(url_for('homepage'))
    return render_template("addface.html")

@app.route("/")
def homepage(): 
    """
    Home page route function
    """     
    global db 
    db.connect()
    unknowns=db.selectUnknows()
    knowns=db.selectAll()
    liste_information=[]
    liste_information.append(len(unknowns))
    liste_information.append(len(knowns))
    liste_information.append(len(knowns)+len(unknowns))
    for r,d ,f in os.walk("my_project\Live_Recognizer\DataSet") :
        break
    knowns=len(d)
    if 'username' in session:
        return render_template('home.html',liste_information=liste_information,knowns=knowns)
    return redirect(url_for('login'))
     

@app.route('/logout')
def logout():
    """
    Logout page route function
    """
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/upload/",methods=['POST'])
def uploadFile():
    """
    Route function that handles uploaded images from the raspberry
    """
    global i
    global db   
    db.connect()
    if request.method == 'POST':
        number_faces = int(request.files['file'].filename)
        file = request.files['file'].read()        
        arr = np.frombuffer(file,dtype="uint8")
        im = cv.imdecode(arr,1)       
        cv.imwrite('my_project/Web_Server/uploads/image{}.jpg'.format(i),im)           
        for j in range(number_faces) :
            db.insert("image{}_{}.jpg".format(i,j))
        i=i+1
        return "..."

@app.route("/forme",methods=['get','post'])
def traitement_form():
    """
    Admin form page route function
    """
    return(render_template('choice.html'))

@app.route("/show",methods=['POST'])
def affichage():
    """
    Handles view visitors page , select required data from database
    """
    global db 
    db.connect()
    if(request.form["person_type"]=="all"):
        if(request.form["date"]!=""): 
            date_requested=request.form["date"]
            liste=db.selectAll(date=date_requested)
            for user_info in liste:
                if ("unknown" not in user_info): 
                    id,date,person=user_info
                    a = id.index("_")
                    b = id.index(".")
                    liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,"knowns",person)
                else :
                    id,date,person=user_info
                    a = id.index("_")
                    b = id.index(".")
                    liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,person)
                
            return(render_template('show.html',liste=liste))
        else:
            liste=db.selectAll()
            for user_info in liste:
                if ("unknown" not in user_info): 
                    id,date,person=user_info
                    a = id.index("_")
                    b = id.index(".")
                    liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,"knowns",person)
                else :
                    id,date,person=user_info
                    a = id.index("_")
                    b = id.index(".")
                    liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,person)
                
            return(render_template('show.html',liste=liste))
    elif(request.form["person_type"]=="unknown"):
        if(request.form["date"]!=""): 
            date_requested=request.form["date"]
            liste=db.selectUnknows(date=date_requested)
            for user_info in liste:
                id,date,person=user_info
                a = id.index("_")
                b = id.index(".")
                liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,person)
            return(render_template('show.html',liste=liste))
        else: 
            liste=db.selectUnknows()
            for user_info in liste:
                id,date,person=user_info
                a = id.index("_")
                b = id.index(".")
                liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,person)
            return(render_template('show.html',liste=liste))

    elif(request.form["person_type"]=="known"):
            if(request.form["date"]!=""): 
                date_requested=request.form["date"]
                liste=db.selectVerified(date=date_requested)
                for user_info in liste:
                    id,date,person=user_info
                    a = id.index("_")
                    b = id.index(".")
                    liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,"knowns",person)
                return(render_template('show.html',liste=liste))
            else: 
                liste=db.selectVerified()
                for user_info in liste:
                    id,date,person=user_info
                    a = id.index("_")
                    b = id.index(".")
                    liste[liste.index(user_info)] = (id.replace(id[a:b],""),date,"knowns",person)
                return(render_template('show.html',liste=liste))
            

    return("here")


app.run(host= 'xxx.xxx.xxx.xxx',port=5000)
f=open("compteur.txt","w")
f.write(str(i))
f.close()