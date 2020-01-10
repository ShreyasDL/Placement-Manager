import pyrebase
import os

from flask import Flask,render_template, request, redirect, session, url_for, flash
from datetime import date
#from firebase_admin import db
#from firebase import firebase

app = Flask(__name__)
app.secret_key = 'random string'

config = {
    "apiKey": "AIzaSyCAwWLzDUZ0dOT2PmeoMfaDi6P1KConsfY",
    "authDomain": "placement-maintenance.firebaseapp.com",
    "databaseURL": "https://placement-maintenance.firebaseio.com",
    "projectId": "placement-maintenance",
    "storageBucket": "placement-maintenance.appspot.com",
    "messagingSenderId": "462647699028",
    "appId": "1:462647699028:web:1e564d98447ec9a286afc1",
    "measurementId": "G-W39CEJ0LYT"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
#database = firebase.database()

db = firebase.database()
personal_details=dict()
academic_details=dict()
comp_list=dict()
email=""
t_date = date.today().strftime("%Y-%m-%d")
today_date=t_date.split('-')
sel_comp=''
#import firebase_admin
#from firebase_admin import credentials

'''if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('path/to/serviceAccountKey.json') 
    default_app = firebase_admin.initialize_app(cred)'''


@app.route("/")
def home():
        if session.get('email',False):
		return render_template('home3.html')
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	try:
		if (request.method == 'POST'):
			email = request.form['name']
			password = request.form['password']
			global company_details
			company_details=dict()
			data3=db.child("Companies").get()
                        for value3 in data3.each() :
                                company_details[value3.key()]=value3.val()
			if email == 'dlshreyas30@gmail.com' and password == '123456789' :
                                return render_template('admin_dashboard.html',company_details=company_details)
			#global usn
			#usn=request.form['f_usn']
			user = auth.sign_in_with_email_and_password(email, password)
			session['email'] = email
                        
			data=db.child("Student Details").get()
                        for value in data.each() :
                                st_data=db.child("Student Details").child(value.key()).child("Personal Details").get()
                                if st_data.val()['Email'] == email :
                                        for v in st_data.each() :
                                                personal_details[v.key()]=v.val()
                                        global usn
                                        usn=value.key()
                                        data2=db.child("Student Details").child(usn).child("Academic Details").get()
                                        for value2 in data2.each() :
                                                academic_details[value2.key()]=value2.val()
                        return redirect(url_for('dashboard'))

	except:
		#flash('Something went wrong!!')
                pass
	flash('Incorrect Mail or Password')
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

	if (request.method == 'POST'):
		email = request.form['email']
		password1 = request.form['password']
		password2 = request.form['confirm_password']
                
		if password1 == password2 and password1!="" and email!="":
                        try :
                                user = auth.create_user_with_email_and_password(email, password1)
                                user = auth.refresh(user['refreshToken'])
                                auth.send_email_verification(user['idToken'])
                                user = auth.sign_in_with_email_and_password(email, password1)
                                session['email'] = email
                        except :
                                flash("Email ID already exists")
                                return render_template('register.html')
			global usn
			usn=request.form['usn']
			db.child("Student Details").child(usn).child("Personal Details").set({"First Name" : request.form['fname'].upper(),
                                                                                       "Last Name" : request.form['lname'].upper(),
                                                                                       "Father's Name" : request.form['f_fname'].upper(),
                                                                                       "DOB" : request.form['dd'],
                                                                                       "Gender" : request.form['gen'],
                                                                                       "Phone" : request.form['no'],
                                                                                       "Address" : request.form['add'],
                                                                                       "City" : request.form['city'].upper(),
                                                                                       "State" : request.form['state'].upper(),
                                                                                        "Email" : request.form['email']})
			db.child("Student Details").child(usn).child("Academic Details").child("10th Details").set(
                                                                                                           {
                                                                                                            "Board" : request.form['board'].upper(),
                                                                                                            "Aggregate" : request.form['aggregate'],
                                                                                                            "YOP" : request.form['yop']
                                                                                                            }
                                                                                                           )
                        db.child("Student Details").child(usn).child("Academic Details").child("12th Details").set(
                                                                                                            {
                                                                                                                "Board" : request.form['board2'].upper(),
                                                                                                               "Aggregate" : request.form['aggregate2'],
                                                                                                               "YOP" : request.form['yop2']
                                                                                                             }
                                                                                                           )
                        db.child("Student Details").child(usn).child("Academic Details").child("UG Details").set(
                                                                                                          {
                                                                                                                "USN":request.form['usn'],
                                                                                                                "Branch":request.form['branch'].upper(),
                                                                                                                "Sem":request.form['sem'],
                                                                                                                "CGPA":request.form['cgpa']
                                                                                                           }
                                                                                                        )
                        data=db.child("Student Details").child(usn).child("Personal Details").get()
                        for value in data.each() :
                                personal_details[value.key()]=value.val()

                        data2=db.child("Student Details").child(usn).child("Academic Details").get()
                        for value2 in data2.each() :
                                academic_details[value2.key()]=value2.val()
                        data3=db.child("Companies").get()
                        for value3 in data3.each() :
                                global company_details
                                company_details=dict()
                                company_details[value3.key()]=value3.val()
                        return redirect(url_for('dashboard'))
	return render_template('register.html')

@app.route("/forgot_password")
def forgot_password():
	return render_template('forgot_password.html')

@app.route("/forgot_form",methods=['GET', 'POST'])
def forgot_form():
	if (request.method == 'POST'):
		email = request.form['name']

		if email!="":
			auth.send_password_reset_email(email)

	return render_template('login.html')

@app.route("/logout")
def logout():
	session.pop(email,None)
	return render_template('login.html')

@app.route("/home")
def h():
        return render_template("home3.html")        


@app.route("/profile")
def profile():     
        return render_template('profile.html',personal_details=personal_details,academic_details=academic_details)

@app.route("/news")
def news():
        global company_details
	company_details=dict()
	data3=db.child("Companies").get()
        for value3 in data3.each() :
                company_details[value3.key()]=value3.val()
        global c_list
        c_list=[]
        d=db.child("Companies").get()
        for each_data in d.each():
            try :
                if usn in each_data.val()["Students"]:
                    c_list.append(each_data.key())
            except :
                pass
        #today_date=t_date.split('-')
        return render_template('news.html',company_details=company_details,academic_details=academic_details,c_list=c_list,today_date=today_date)


@app.route("/update",methods=['GET','POST'])
def update():
        db.child("Companies").child(request.form['comp_name']).child("Students").child(usn).set({"Name":personal_details['First Name']+" "+personal_details['Last Name']})
        flash("Applied for "+request.form['comp_name'])
        c_list.append(request.form['comp_name'])
        
        return render_template('news.html',company_details=company_details,academic_details=academic_details,c_list=c_list,today_date=today_date)

@app.route("/adminlogin")
def adminlogin():
        return render_template('adminlogin.html')

@app.route("/view_companies")
def view_companies():
        global company_details
        company_details=dict()
        data3=db.child("Companies").get()
        for value3 in data3.each() :
                company_details[value3.key()]=value3.val()
        return render_template('view_comp.html',company_details=company_details)

@app.route("/add_company",methods=['GET','POST'])
def add_company():
        if (request.method == 'POST') :
                db.child("Companies").child(request.form['comp_name']).set(
                                           { "Eligibility":
                                             { "Branch":request.form['comp_bran'],
                                               "GPA":request.form['comp_gpa'],
                                               "JOB ROLE":request.form['job_role'],
                                               "DRIVE DATE":request.form['drive_date']
                                                }})
                flash(request.form['comp_name']+" added")
                return render_template('add_comp.html',t_date=t_date)
        return render_template('add_comp.html',t_date=t_date)


@app.route("/reg_students",methods=['GET','POST'])
def reg_students():
        try:
                st_list=dict()
                reg_st=db.child("Companies").child(request.form['comp_name']).child("Students").get()
                for each_st in reg_st.each():
                        st_list[each_st.key()]=each_st.val()
                company_name=request.form['comp_name']
                return render_template('reg_students.html',st_list=st_list,company_name=company_name)
        except:
                flash("No Students registered for "+request.form['comp_name'])
                return render_template('view_comp.html',company_details=company_details)

@app.route("/dashboard")
def dashboard():
        global c_list
        c_list=[]
        global s_list
        s_list = []
        d=db.child("Companies").get()
        for each_data in d.each():
            try :
                if usn in each_data.val()["Students"]:
                    c_list.append(each_data.key())
                if usn in each_data.val()['Selected Students'] :
                	s_list.append(each_data.key())
            except :
                pass
        return render_template('dashboard.html',c_list=c_list,company_details=company_details,s_list = s_list)

@app.route("/upload",methods=['GET','POST'])
def upload():
        firebase_storage=firebase.storage()
        firebase_storage.child("Resume/"+usn+".pdf").put(request.files['fileToUpload'])
        return render_template("dashboard.html")
@app.route("/pro_update",methods=['GET','POST'])
def pro_update():
        if (request.method == 'POST') :
                global usn
		usn=request.form['usn']
		db.child("Student Details").child(usn).child("Personal Details").set({"First Name" : request.form['fname'].upper(),
                                                                                       "Last Name" : request.form['lname'].upper(),
                                                                                       "Father's Name" : request.form['f_fname'].upper(),
                                                                                       "DOB" : request.form['dd'],
                                                                                       "Gender" : request.form['gen'],
                                                                                       "Phone" : request.form['no'],
                                                                                       "Address" : request.form['add'],
                                                                                       "City" : request.form['city'].upper(),
                                                                                       "State" : request.form['state'].upper(),
                                                                                        "Email" : request.form['email']})
		db.child("Student Details").child(usn).child("Academic Details").child("10th Details").set(
                                                                                                           {
                                                                                                            "Board" : request.form['board'].upper(),
                                                                                                            "Aggregate" : request.form['aggregate'],
                                                                                                            "YOP" : request.form['yop']
                                                                                                            }
                                                                                                           )
                db.child("Student Details").child(usn).child("Academic Details").child("12th Details").set(
                                                                                                            {
                                                                                                                "Board" : request.form['board2'].upper(),
                                                                                                               "Aggregate" : request.form['aggregate2'],
                                                                                                               "YOP" : request.form['yop2']
                                                                                                             }
                                                                                                           )
                db.child("Student Details").child(usn).child("Academic Details").child("UG Details").set(
                                                                                                          {
                                                                                                                "USN":request.form['usn'],
                                                                                                                "Branch":request.form['branch'].upper(),
                                                                                                                "Sem":request.form['sem'],
                                                                                                                "CGPA":request.form['cgpa']
                                                                                                           }
                                                                                                        )
                data=db.child("Student Details").child(usn).child("Personal Details").get()
                for value in data.each() :
                        personal_details[value.key()]=value.val()

                data2=db.child("Student Details").child(usn).child("Academic Details").get()
                for value2 in data2.each() :
                        academic_details[value2.key()]=value2.val()
                data3=db.child("Companies").get()
                for value3 in data3.each() :
                        global company_details
                        company_details=dict()
                        company_details[value3.key()]=value3.val()
                        
                return render_template('profile.html',personal_details=personal_details,academic_details=academic_details)
        return render_template('profile.html',personal_details=personal_details,academic_details=academic_details)

@app.route('/add_selected_students',methods=['GET','POST'])
def add_selected_students():
    try :
        if request.method == 'POST' :
            global sel_comp
            sel_comp = request.form['sel_comp']
            data = db.child("Companies").child(sel_comp).child("Students").get()
            reg_students=dict()
            for value in data.each() :
                reg_students[value.key()] = value.val()
            return render_template('add_selected_students2.html',reg_students=reg_students)
    except:
        flash('No Students Registered!!!')
    return render_template('add_selected_students.html',company_details=company_details)

@app.route('/up_selected_students',methods=['GET','POST'])
def up_selected_students():
    if request.method == 'POST' :
        data = request.form.getlist('sel_students')
        sel_students = dict() 
        for value in data :
            data2 = value.split('|')
            sel_students[data2[0]] = data2[1]
        for key,value in sel_students.items() :
            db.child('Companies').child(sel_comp).child('Selected Students').child(key).set(
                                                                                            {
                                                                                                'Name' : value
                                                                                            }
                                                                                        )
        flash('Selected students for '+sel_comp+' added')
        return redirect(url_for('add_selected_students'))
    return redirect(url_for('add_selected_students'))

@app.route('/view_graph')
def view_graph():
    return render_template('view_graph.html')
                        
@app.route('/admin_dashboard')
def admin_dashboard() :
	global company_details
	company_details = dict()
	data3=db.child("Companies").get()
	for value3 in data3.each() :
		company_details[value3.key()]=value3.val()
	return render_template('admin_dashboard.html',company_details=company_details)

@app.route('/get_sel_students',methods=['GET','POST'])
def get_sel_students() :
	try:
		st_list=dict()
		reg_st = db.child("Companies").child(request.form['comp_name']).child('Selected Students').get()
		for each_st in reg_st.each():
			st_list[each_st.key()]=each_st.val()
		company_name=request.form['comp_name']
		return render_template('sel_comp_students.html',st_list=st_list,company_name=company_name)
	except:
		flash("No Students selected for "+request.form['comp_name'])
		return render_template('admin_dashboard.html',company_details=company_details)


app.run(debug=True)
app.do_teardown_appcontext()
