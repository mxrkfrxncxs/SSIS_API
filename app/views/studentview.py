from flask import Flask, Blueprint, request, render_template, redirect, flash, jsonify
import requests, json

students_bp = Blueprint('students', __name__)

@students_bp.route('/students/')
def students():
    students = []
    response = requests.get('http://127.0.0.1:5000/students')
    if response.status_code == 200:
        students = response.json()
    print(students)
    return render_template('students.html', students=students)

@students_bp.route('/students/search', methods=['GET', 'POST'])
def search_student():
    students = None
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('studentsearch')
        if search_query:
            response = requests.get(f'http://127.0.0.1:5000/student/{search_query}')
            if response.status_code == 200:
                data = response.json()
                if data.get('message'):
                    students = [data['message']]
    return render_template('students.html', students=students, search_query=search_query)

@students_bp.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
       name = request.form['name'].title()
       course = request.form['course']
       data = {
            'student': name,
            'course_id': course
       }
       response = requests.post('http://127.0.0.1:5000/student', json=data)
       if response.status_code == 200:
            print(response.json())
            flash('Student added successfully!', 'success')
            return redirect('/students/') 
    response2 = requests.get('http://127.0.0.1:5000/courses')
    if response2.status_code == 200:
        courses = response2.json()
        print(courses)
    return render_template('addstudent.html', courses=courses)

@students_bp.route('/edit_student/<string:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name'].title()
        course = request.form['course']
        data = {
            'student': name,
            'course_id': course
        }
        response = requests.put(f'http://127.0.0.1:5000/student/{id}', json=data)
        if response.status_code == 200:
            flash('Student updated successfully!', 'success')
            return redirect('/students/') 

    # Retrieve student info
    student_info = find_student(id)
    name = student_info['student_name']
    curr_course = student_info['course_name']

    # Retrieve courses
    courses = []
    curr_course_id = None
    response2 = requests.get('http://127.0.0.1:5000/courses')
    if response2.status_code == 200:
        courses_data = response2.json()
        courses = courses_data.get('message', [])
        print(courses)
        for item in courses:
            if item.get('course_name') == curr_course:
                curr_course_id = item.get('course_id')
                break

    return render_template('editstudent.html', name=name, curr_course=curr_course, courses=courses, curr_course_id=curr_course_id)

@students_bp.route('/delete_student/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if request.method == 'DELETE':
        response = requests.delete(f'http://127.0.0.1:5000/student/{student_id}')
        if response.status_code == 200:
            flash('Student deleted successfully!', 'success')
            return jsonify({'message': 'Student deleted successfully'}), 200

def find_student(id):
    response = requests.get(f'http://127.0.0.1:5000/student/{id}')
    if response.status_code == 200:
        data = response.json()
        if data.get('message'):
            students = data['message']
            print(students)
    return students