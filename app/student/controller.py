from flask import render_template, redirect, request, jsonify, flash
from . import student_bp
import app.models as models
from app.student.forms import StudentForm, CourseForm, CollegeForm
from app import mysql
import cloudinary
import cloudinary.uploader

@student_bp.route('/')
@student_bp.route('/student')
@student_bp.route('/index')
def index():
    student = models.Student.all()
    return render_template('index.html', data=student,title='Home',something='something')

@student_bp.route('/course')
def course():
    course = models.course.all()
    return render_template('course.html', data=course,title='Home',something='something')

@student_bp.route('/college')
def college():
    college = models.college.all()
    return render_template('college.html', data=college,title='Home',something='something')

@student_bp.route('/student/add_student', methods=['POST','GET'])
def add_student():
    available_courses = []
    for element in models.course.all():
         available_courses.append(element[0])
    form = StudentForm(request.form)
    form.course_code.choices = available_courses
    if form.validate():
        student = models.Student(school_id=form.id.data, first_name=form.first_name.data, last_name=form.last_name.data, course_code=form.course_code.data, year = form.year.data, gender = form.gender.data, prof_url=form.prof_url.data)
        student.add()
        return redirect('/student')
  
    return render_template('add_student.html', form=form, title = 'Add Student')

@student_bp.route('/course/add_course', methods=['POST','GET'])
def add_course():
    form = CourseForm(request.form)
    if request.method == 'POST' and form.validate():
        course = models.course(course_code=form.course_code.data, course_name=form.course_name.data, college_code=form.college_code.data)
        course.add()
        return redirect('/course')
    else:
        return render_template('add_course.html', form=form)

@student_bp.route('/college/add_college', methods=['POST','GET'])
def add_college():
    form = CollegeForm(request.form)
    if request.method == 'POST' and form.validate():
        college = models.college(college_code=form.college_code.data, college_name=form.college_name.data)
        college.add()
        return redirect('/college')
    else:
        return render_template('add_college.html', form=form)


@student_bp.route('/student/edit/<id_number>', methods=['POST','GET'])
def edit(id_number):
    form = StudentForm(request.form)

    details = models.Student.open(id_number)
    available_courses = []
    for element in models.course.all():
        available_courses.append(element[0])
    if request.method == 'GET':
        form.id.data = details[0][0]    
        form.first_name.data = details[0][1]
        form.last_name.data = details[0][2]
        form.course_code.data = details[0][3]
        form.year.data = details[0][4]
        form.gender.data = details[0][5]
        form.prof_url.data = details[0][6]
    
        return render_template('edit_student1.html', form = form ,title = 'Edit Student')
    
    elif request.method == 'POST' and form.validate():

        Student = models.Student(first_name=form.first_name.data, last_name=form.last_name.data, course_code=form.course_code.data, year=form.year.data, gender=form.gender.data, prof_url = form.prof_url.data)
        Student.edit(id_number)
        flash('Student info has been updated!')
        return redirect('/student')

@student_bp.route('/course/edit/<course_code>', methods=['POST','GET'])
def edit_course(course_code):
    form = CourseForm(request.form)
    details = models.course.open(course_code)
    available_colleges = []
    for element in models.college.all():
         available_colleges.append(element[0])

    if request.method == 'GET':
        form.course_code.data = details[0][0]    
        form.course_name.data = details[0][1]
        form.college_code.data = details[0][2]

    
        return render_template('edit_course.html',  form = form, title = 'Edit Course')
    
    elif request.method == 'POST' and form.validate():
        course = models.course(  course_name=  form.course_name.data, college_code = form.college_code.data)
        course.edit(course_code)  
        flash('Course info has been updated!')
        return redirect('/course')

@student_bp.route('/college/edit/<college_code>', methods=['POST','GET'])
def edit_college(college_code):
    form = CollegeForm(request.form)
    details = models.college.open(college_code)
    if request.method == 'GET':
        form.college_code.data = details[0][0]    
        form.college_name= details[0][1]


    
        return render_template('edit_college.html', form = form, title = 'Edit College')
    
    elif request.method == 'POST' and form.validate():
        college = models.college( college_name=  form.college_name.data)
        college.edit(college_code)  
        flash('College info has been updated!')
        return redirect('/college')

@student_bp.route("/student/delete/<string:school_id>", methods=['GET','POST'])
def delete(school_id):
    cursor = mysql.connection.cursor()
    sql = f"DELETE from `student` where `student`.`school_id`= '{school_id}'"
    cursor.execute(sql)
    mysql.connection.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/student')
    
    

@student_bp.route("/course/delete/<string:course_code>", methods=['GET','POST'])
def delete_course(course_code):
    cursor = mysql.connection.cursor()
    sql = f"DELETE from `course` where `course`.`course_code`= '{course_code}'"
    cursor.execute(sql)
    mysql.connection.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/course')

@student_bp.route("/college/delete/<string:college_code>", methods=['GET','POST'])
def delete_college(college_code):
    cursor = mysql.connection.cursor()
    sql = f"DELETE from `college` where `college`.`college_code`= '{college_code}'"
    cursor.execute(sql)
    mysql.connection.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/college')

