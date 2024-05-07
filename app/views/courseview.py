from flask import *

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses/')
def courses():
    courses = get_courses()
    return render_template('courses.html', courses=courses)

@courses_bp.route('/courses/search', methods=['GET', 'POST'])
def search_course():
    courses = []
    if request.method == 'POST':
        search_query = request.form.get('coursesearch')
        if search_query:
            courses = find_courses(search_query)
    return render_template('courses.html', courses=courses, search_query=search_query)

@courses_bp.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']
        if check(course_code):
            flash('Course Code already exists!', 'error')
        elif len(course_code)> 20:
            flash('Course Code too long!', 'error')
        else:
            insert_course(course_code, course_name, college_code)
            flash('Course added successfully!', 'success')
            return redirect('/courses') 
    colleges = get_college_codes()
    return render_template('addcourse.html', colleges=colleges)

@courses_bp.route('/edit_course', methods=['GET', 'POST'])
def edit_course():
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        college_code = request.form.get('college_code')
        update_course(course_code, course_name, college_code)
        flash('Course updated successfully!', 'success')
        return redirect('/courses/') 
    course_code = request.args.get('course_code')
    course_name = request.args.get('course_name')
    college_code = request.args.get('college_code')
    colleges = get_college_codes()
    return render_template('editcourse.html', course_code=course_code, course_name=course_name, college_code=college_code, colleges=colleges)

@courses_bp.route('/delete_course/<string:course_code>', methods=['DELETE'])
def delete_course(course_code):
    if request.method == 'DELETE':
        remove_course(course_code)
        flash('Course deleted successfully!', 'success')
        return jsonify({'success': True})
    
@courses_bp.route('/view_course/<string:course_code>', methods=['GET'])
def view_course(course_code):
    data = read_course(course_code)
    return render_template('courseinfo.html', data=data)