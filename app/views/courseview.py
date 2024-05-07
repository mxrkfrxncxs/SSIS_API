from flask import Flask, Blueprint, request, render_template, redirect, flash, jsonify
import requests, json

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses/')
def courses():
    courses = []
    response = requests.get('http://127.0.0.1:5000/courses')
    if response.status_code == 200:
        courses = response.json()
    print(courses)
    return render_template('courses.html', courses=courses)

@courses_bp.route('/courses/search', methods=['GET', 'POST'])
def search_course():
    courses = None
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('coursesearch')
        if search_query:
            response = requests.get(f'http://127.0.0.1:5000/course/{search_query}')
            if response.status_code == 200:
                data = response.json()
                if data.get('message'):
                    courses = [data['message']]
                    print(courses)
    return render_template('courses.html', courses=courses, search_query=search_query)

@courses_bp.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name'].title()
        data = {
            'course': course_name
        }
        response = requests.post('http://127.0.0.1:5000/course', json=data)
        if response.status_code == 200:
            print(response.json())
            flash('Course added successfully!', 'success')
            return redirect('/courses/') 
    return render_template('addcourse.html')

@courses_bp.route('/edit_course/<string:id>', methods=['GET', 'POST'])
def edit_course(id):
    if request.method == 'POST':
        course_name = request.form['course_name'].title()
        data = {
            'course': course_name
        }
        response = requests.put(f'http://127.0.0.1:5000/course/{id}', json=data)
        if response.status_code == 200:
            print(response.json())
            flash('Course edited successfully!', 'success')
            return redirect('/courses/') 
    
    course_info = find_course(id)
    course_name = course_info['course_name']    
    
    return render_template('editcourse.html', course_name=course_name)

@courses_bp.route('/delete_course/<string:course_id>', methods=['DELETE'])
def delete_course(course_id):
    if request.method == 'DELETE':
        response = requests.delete(f'http://127.0.0.1:5000/course/{course_id}')
        if response.status_code == 200:
            flash('Course deleted successfully!', 'success')
            return jsonify({'message': 'Course deleted successfully'}), 200
    
def find_course(id):
    response = requests.get(f'http://127.0.0.1:5000/course/{id}')
    if response.status_code == 200:
        data = response.json()
        if data.get('message'):
            courses = data['message']
            print(courses)
    return courses