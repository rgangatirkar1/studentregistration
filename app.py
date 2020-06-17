import json
from flask import Flask, render_template, request
from pymongo import MongoClient
from random import randint
from bson.objectid import ObjectId


app = Flask(__name__)

mongoDBConnectionString = "mongodb+srv://apollo21daboss:Welcome123@cluster0-976zt.mongodb.net/test?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true";

@app.route('/')
def index():
    return render_template('registeration.html')


@app.route('/getRecords', methods=['GET'])
def getRecords():
    client = MongoClient(mongoDBConnectionString)
    db = client.get_database('bookdb')
    records = db.book_col
    return  render_template('viewall.html', records=records.find({'student_info':{ '$exists':True}}))



@app.route('/', methods=['POST'])
def getValue():
    fname = request.form['first']
    lname = request.form['last']
    lettergrade = request.form['grade']
    school = request.form['schools']
    email = request.form['mail']
    gender = request.form['gender']
    for i in range(100000, 999999):
        value = randint(100000, 999999)
    client = MongoClient(mongoDBConnectionString)
    db = client.get_database('bookdb')
    records = db.book_col
    query = {"student_info":
        {
            "fname": fname,
            "lname": lname,
            "id": value,
            "grade": lettergrade,
            "school":school,
            "email":email,
            "gender":gender
        }
    }
    result = records.insert_one(query)
    if (result.inserted_id):
        return render_template('success.html', f=fname, l=lname, a=value, g=lettergrade,yourid=value,   id=result.inserted_id)
    else:
        return render_template('error.html', f=fname, l=lname, a=value, g=lettergrade,)

@app.route('/getRecord',methods=['GET'])
def displayValues():
    studentId = request.args.get('student_id')
    client = MongoClient(mongoDBConnectionString)
    db = client.get_database('bookdb')
    records = db.book_col
    students = records.find({"student_info.id": int(studentId)})
    for student in students:
        print(student)
    return render_template('student.html',si=student)

@app.route('/deleted')
def returnwebsite():
    arbitrary=request.args.get('student_id')
    return render_template('deleted.html',arb=arbitrary)

@app.route('/deletedsuccess',methods=['POST'])
def deleteinfo():
    studentId = request.args.get('student_id')
    client = MongoClient(mongoDBConnectionString)
    db = client.get_database('bookdb')
    records = db.book_col
    query3 = {"student_info.id": int(studentId)}
    records.delete_one(query3)
    return render_template('deletedsuccess.html')

@app.route('/editStudent', methods=['GET'])
def editInfo():
    studentId= request.args.get('student_id')
    student = findStudent(studentId)
    return render_template('update.html',si=student)


def findStudent(studentId):
    client = MongoClient(mongoDBConnectionString)
    db = client.get_database('bookdb')
    records = db.book_col
    students = records.find({"student_info.id": int(studentId)})
    for student in students:
        print(student)
    return student


@app.route('/updateStudent', methods=['POST'])
def updateInfo():
    studentId = request.args.get('student_id')
    student = findStudent(studentId)
    fname = request.form['first']
    lname = request.form['last']
    lettergrade = request.form['grade']
    school = request.form['schools']
    email = request.form['mail']
    gender = request.form['gender']

    client = MongoClient(mongoDBConnectionString)
    db = client.get_database('bookdb')
    records = db.book_col
    # existingdoc = {"_id": ObjectId(student['_id'])}
    existingdoc = {"student_info.id": int(studentId)}
    newdoc={"$set":{
                     "student_info.fname":fname,
                     "student_info.lname":lname,
                     "student_info.grade":lettergrade,
                     "student_info.school":school,
                     "student_info.email":email,
                     "student_info.gender":gender
                     }}
    records.update(existingdoc, newdoc)
    return render_template('updatedsuccess.html')

@app.route('/updatedsuccess')
def returnsuccess():
    return render_template('updatedsuccess.html')
if __name__ == '__main__':
    app.run(debug=True)