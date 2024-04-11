from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import os
from matrix2 import run, write, missing, read

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/About")
def about():
    return render_template("aboutus.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        if email == "admin" and password == "admin":
            return redirect(url_for('admin'))
        else:
            error = "INVALID DETAILS"
    return render_template("login.html", error=error)

@app.route("/admin")
def admin():
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
        data = cursor.execute("SELECT * FROM room")
        data = cursor.fetchall()
    return render_template("admin.html", data=data)

@app.route("/addroom", methods=['GET', 'POST'])
def addroom():
    data = None
    error = None
    if request.method == 'POST':
        room_no = request.form['room_no']
        row = request.form['row']
        col = request.form['col']
        seat = request.form['seat']
        myconn = sqlite3.connect("room_details.db")
        if (int(seat) <= int(row) * int(col)):
            with myconn:
                cursor = myconn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
                temp_no = cursor.execute("SELECT room_no from room where room_no=?", [room_no])
                temp_no = cursor.fetchone()
            if temp_no is None:
                with myconn:
                    cursor = myconn.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
                    cursor.execute("INSERT INTO room VALUES(?,?,?,?)", [room_no, col, row, seat])
                    error = room_no + " is added"
            else:
                error = room_no + " is already exist"
        else:
            error = "Invalid number of seat"
    return render_template("addroom.html", error=error, data=data)

@app.route("/Generate", methods=['GET', 'POST'])
def generate():
    error = None
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
        temp_no = cursor.execute("SELECT room_no from room ")
        temp_no = cursor.fetchall()
    if request.method == 'POST':
        room_no = request.form['room']
        cm_start = request.form['cm_start']
        cm_end = request.form['cm_end']
        sc_start = request.form['sc_start']
        sc_end = request.form['sc_end']
        el_start = request.form['el_start']
        el_end = request.form['el_end']
        r_missing = request.form['missing']
        with myconn:
            cursor = myconn.cursor()
            row = cursor.execute("SELECT row FROM room WHERE room_no = ?", [room_no])
            row = cursor.fetchone()
            row = row[0]
            col = cursor.execute("SELECT col FROM room WHERE room_no = ?", [room_no])
            col = cursor.fetchone()
            col = col[0]
            seat = cursor.execute("SELECT seat FROM room WHERE room_no = ?", [room_no])
            seat = cursor.fetchone()
            seat = seat[0]
        cm_start = int(cm_start)
        cm_end = int(cm_end)
        sc_start = int(sc_start)
        sc_end = int(sc_end)
        el_start = int(el_start)
        el_end = int(el_end)
        r_missing = r_missing.split()
        for i in range(len(r_missing)):
            r_missing[i] = int(r_missing[i])
        cm_list = list(range(cm_start, cm_end + 1))
        cm_list = missing(r_missing, cm_list)
        sc_list = list(range(sc_start, sc_end + 1))
        sc_list = missing(r_missing, sc_list)
        el_list = list(range(el_start, el_end + 1))
        el_list = missing(r_missing, el_list)
        check = len(el_list) + len(sc_list) + len(cm_list)
        if (check <= int(seat)):
            data = run(el_list, sc_list, cm_list, row, col)
            write(data, room_no)
            error = "Seating Arrangment For " + room_no + " Is generated "
        else:
            error = " Total Number of student is Not More than " + str(seat) + " " + str(check)
    return render_template("generate.html", room_no=temp_no, error=error)

@app.route('/result', methods=['GET', 'POST'])
def show():
    data = None
    filename = None
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
        temp_no = cursor.execute("SELECT room_no from room ")
        temp_no = cursor.fetchall()
    if request.method == 'POST':
        room_no = request.form['room']
        data = read(room_no)
        data = data.to_html()
        filename = '/static/execl/' + room_no + '.xlsx'
    return render_template("show_result.html", data=data, room_no=temp_no, filename=filename)

@app.route('/resultview', methods=['GET', 'POST'])
def showresult():
    data = None
    filename = None
    room_number = None
    not_found_message = None
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
        temp_no = cursor.execute("SELECT room_no from room ")
        temp_no = cursor.fetchall()
    if request.method == 'POST':
        if 'room' in request.form:  # Check if room selection form is submitted
            room_no = request.form['room']
            data = read(room_no)
            data = data.to_html()
            filename = f'/static/excel/{room_no}.xlsx'
        elif 'roll_number' in request.form:  # Check if roll number search form is submitted
            roll_number = request.form['roll_number']
            room_number, not_found_message = search_roll_number(roll_number)
            if room_number:
                data = read(room_number)
                data = data.to_html()
                filename = f'/static/excel/{room_number}.xlsx'
    return render_template("view_result.html", data=data, room_no=temp_no, filename=filename, room_number=room_number, not_found_message=not_found_message)

def search_roll_number(roll_number):
    room_number = None
    not_found_message = None
    # Iterate through each Excel file in the directory
    for filename in os.listdir('static/excel'):
        if filename.endswith('.xlsx'):
            filepath = os.path.join('static/excel', filename)
            df = pd.read_excel(filepath)

            # Check if any roll number in the DataFrame contains the entered roll number
            matching_roll_numbers = [str(r) for r in df.values.flatten() if str(r).startswith(roll_number)]
            if matching_roll_numbers:
                room_number = filename.split('.')[0]
                break
    else:
        not_found_message = f"Roll number {roll_number} not found in any room."
    return room_number, not_found_message

@app.route('/delete/<id>')
def delete(id):
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
        cursor.execute("DELETE FROM room WHERE room_no=?", [id])
    return redirect(url_for('admin'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    error = None  # Initialize error variable
    if request.method == 'POST':
        room_no = request.form['room_no']
        row = request.form['row']
        col = request.form['col']
        seat = request.form['seat']
        
        myconn = sqlite3.connect("room_details.db")
        with myconn:
            cursor = myconn.cursor()
            if (int(seat) <= int(row) * int(col)):
                cursor.execute("UPDATE room SET col=?, row=?, seat=? WHERE room_no=?", [col, row, seat, room_no])
                error = room_no + " is updated"
            else:
                error = "Invalid number of seats"
    
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        data = cursor.execute("SELECT * FROM room WHERE room_no = ?", [id])
        data = cursor.fetchmany()
    
    room_no = data[0][0]
    col = data[0][1]
    row = data[0][2]
    seat = data[0][3]
    
    return render_template("addroom.html", error=error, room=room_no, col=col, row=row, seat=seat)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345)
