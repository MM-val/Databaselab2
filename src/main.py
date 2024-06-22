import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import io


# 连接到数据库
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button, END
from tkinter.filedialog import askopenfilename
import mysql.connector
from mysql.connector import Error

# 数据库连接配置
db_config = {
    'user': 'root',
    'password': 'mimeng',
    'host': '127.0.0.1',
    'database': 'SchoolDB',
}

# 连接到数据库
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

# 选择照片路径
def select_photo(entry):
    photo_path = askopenfilename()
    if photo_path:
        entry.delete(0, END)
        entry.insert(0, photo_path)

# 插入学生信息
def insert_student():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                # 获取输入值
                studentid = studentid_entry.get()
                name = name_entry.get()
                gender = gender_entry.get()
                birth_date = birth_date_entry.get()
                hometown = hometown_entry.get()
                ethnicity = ethnicity_entry.get()
                major_id = major_id_entry.get()
                photo_path = photo_path_entry.get()

                # 检查空输入
                if not studentid or not name or not gender or not birth_date or not hometown or not ethnicity or not major_id or not photo_path:
                    messagebox.showerror("Error", "All fields must be filled out.")
                    return

                studentid = int(studentid)
                major_id = int(major_id)

                # 读取照片
                with open(photo_path, 'rb') as file:
                    photo = file.read()

                # 检查重复输入
                cursor.execute("SELECT COUNT(*) FROM Student WHERE studentid = %s", (studentid,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Student ID already exists.")
                    return

                # 插入数据
                cursor.callproc('AddStudent', (studentid, name, gender, birth_date, hometown, ethnicity, major_id, photo))
                conn.commit()
                messagebox.showinfo("Success", "Student information inserted successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Insert Student")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Name:").grid(row=1, column=0)
    name_entry = Entry(window)
    name_entry.grid(row=1, column=1)

    Label(window, text="Gender:").grid(row=2, column=0)
    gender_entry = Entry(window)
    gender_entry.grid(row=2, column=1)

    Label(window, text="Birth Date (YYYY-MM-DD):").grid(row=3, column=0)
    birth_date_entry = Entry(window)
    birth_date_entry.grid(row=3, column=1)

    Label(window, text="Hometown:").grid(row=4, column=0)
    hometown_entry = Entry(window)
    hometown_entry.grid(row=4, column=1)

    Label(window, text="Ethnicity:").grid(row=5, column=0)
    ethnicity_entry = Entry(window)
    ethnicity_entry.grid(row=5, column=1)

    Label(window, text="Major ID:").grid(row=6, column=0)
    major_id_entry = Entry(window)
    major_id_entry.grid(row=6, column=1)

    Label(window, text="Photo Path:").grid(row=7, column=0)
    photo_path_entry = Entry(window)
    photo_path_entry.grid(row=7, column=1)
    Button(window, text="Browse", command=lambda: select_photo(photo_path_entry)).grid(row=7, column=2)

    Button(window, text="Submit", command=submit).grid(row=8, column=0, columnspan=2)



# 删除学生信息
def delete_student():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                if not studentid:
                    messagebox.showerror("Error", "All fields must be filled out.")
                    return
                cursor.callproc('DeleteStudent', (studentid,))
                conn.commit()
                messagebox.showinfo("Success", "Student information deleted successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Delete Student")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2)

# 更新学生信息
# 获取学生信息并填充到输入框中

# 更新学生信息
def update_student():
    def get_student_info():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                cursor.execute("SELECT name, gender, birthdate, hometown, ethnicity, majorid, photo FROM Student WHERE studentid = %s", (studentid,))
                student = cursor.fetchone()
                if student:
                    name_entry.delete(0, END)
                    name_entry.insert(0, student[0])
                    gender_entry.delete(0, END)
                    gender_entry.insert(0, student[1])
                    birth_date_entry.delete(0, END)
                    birth_date_entry.insert(0, student[2])
                    hometown_entry.delete(0, END)
                    hometown_entry.insert(0, student[3])
                    ethnicity_entry.delete(0, END)
                    ethnicity_entry.insert(0, student[4])
                    major_id_entry.delete(0, END)
                    major_id_entry.insert(0, student[5])
                    photo_path_entry.delete(0, END)
                    photo_path_entry.insert(0, "Photo loaded")  # 这里只是提示，无法显示二进制数据的路径
                else:
                    messagebox.showerror("Error", "Student not found.")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                name = name_entry.get()
                gender = gender_entry.get()
                birth_date = birth_date_entry.get()
                hometown = hometown_entry.get()
                ethnicity = ethnicity_entry.get()
                major_id = int(major_id_entry.get())
                photo_path = photo_path_entry.get()
                
                with open(photo_path, 'rb') as file:
                    photo = file.read()
                
                cursor.callproc('UpdateStudent', (studentid, name, gender, birth_date, hometown, ethnicity, major_id, photo))
                conn.commit()
                messagebox.showinfo("Success", "Student information updated successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Update Student")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)
    Button(window, text="Get", command=get_student_info).grid(row=0, column=2)

    Label(window, text="Name:").grid(row=1, column=0)
    name_entry = Entry(window)
    name_entry.grid(row=1, column=1)

    Label(window, text="Gender:").grid(row=2, column=0)
    gender_entry = Entry(window)
    gender_entry.grid(row=2, column=1)

    Label(window, text="Birth Date (YYYY-MM-DD):").grid(row=3, column=0)
    birth_date_entry = Entry(window)
    birth_date_entry.grid(row=3, column=1)

    Label(window, text="Hometown:").grid(row=4, column=0)
    hometown_entry = Entry(window)
    hometown_entry.grid(row=4, column=1)

    Label(window, text="Ethnicity:").grid(row=5, column=0)
    ethnicity_entry = Entry(window)
    ethnicity_entry.grid(row=5, column=1)

    Label(window, text="Major ID:").grid(row=6, column=0)
    major_id_entry = Entry(window)
    major_id_entry.grid(row=6, column=1)

    Label(window, text="Photo Path:").grid(row=7, column=0)
    photo_path_entry = Entry(window)
    photo_path_entry.grid(row=7, column=1)
    Button(window, text="Browse", command=lambda: select_photo(photo_path_entry)).grid(row=7, column=2)

    Button(window, text="Submit", command=submit).grid(row=8, column=0, columnspan=3)


def get_student():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                cursor.callproc('GetStudent', (studentid,))
                for result in cursor.stored_results():
                    student = result.fetchall()
                    if student:
                        student_info = student[0]
                        result_text.delete(1.0, END)
                        result_text.insert(END, f"ID: {student_info[0]}\n")
                        result_text.insert(END, f"Name: {student_info[1]}\n")
                        result_text.insert(END, f"Gender: {student_info[2]}\n")
                        result_text.insert(END, f"Birth Date: {student_info[3]}\n")
                        result_text.insert(END, f"Hometown: {student_info[4]}\n")
                        result_text.insert(END, f"Ethnicity: {student_info[5]}\n")
                        result_text.insert(END, f"Major ID: {student_info[6]}\n")
                        photo_data = student_info[7]
                        if photo_data:
                            image = Image.open(io.BytesIO(photo_data))
                            image.thumbnail((200, 200))
                            photo_image = ImageTk.PhotoImage(image)
                            photo_label.config(image=photo_image)
                            photo_label.image = photo_image
                        else:
                            photo_label.config(image='')
                            photo_label.image = None
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    window = Toplevel(root)
    window.title("Get Student")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2)

    result_text = Text(window, height=10, width=50)
    result_text.grid(row=2, column=0, columnspan=2)

    photo_label = Label(window)
    photo_label.grid(row=3, column=0, columnspan=2)

# 学生选课
def enroll_course():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                course_id = int(course_id_entry.get())
                cursor.callproc('EnrollCourse', (studentid, course_id))
                conn.commit()
                messagebox.showinfo("Success", "Course enrollment successful")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Enroll Course")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Course ID:").grid(row=1, column=0)
    course_id_entry = Entry(window)
    course_id_entry.grid(row=1, column=1)

    Button(window, text="Submit", command=submit).grid(row=2, column=0, columnspan=2)

# 学生退课
def drop_course():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                course_id = int(course_id_entry.get())
                cursor.callproc('DropCourse', (studentid, course_id))
                conn.commit()
                messagebox.showinfo("Success", "Course drop successful")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Drop Course")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Course ID:").grid(row=1, column=0)
    course_id_entry = Entry(window)
    course_id_entry.grid(row=1, column=1)

    Button(window, text="Submit", command=submit).grid(row=2, column=0, columnspan=2)

# 查询学生成绩
def get_student_grades():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                cursor.callproc('GetStudentGrades', (studentid,))
                for result in cursor.stored_results():
                    grades = result.fetchall()
                    result_text.delete(1.0, END)
                    result_text.insert(END, grades)
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    window = Toplevel(root)
    window.title("Get Student Grades")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2)

    result_text = Text(window, height=10, width=50)
    result_text.grid(row=2, column=0, columnspan=3)

# 申请专业变更
def apply_major_change():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                old_major_id = int(old_major_id_entry.get())
                new_major_id = int(new_major_id_entry.get())
                change_date = change_date_entry.get()
                application_status = application_status_entry.get()
                cursor.callproc('ApplyMajorChange', (studentid, old_major_id, new_major_id, change_date, application_status))
                conn.commit()
                messagebox.showinfo("Success", "Major change application successful")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Apply Major Change")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Old Major ID:").grid(row=1, column=0)
    old_major_id_entry = Entry(window)
    old_major_id_entry.grid(row=1, column=1)

    Label(window, text="New Major ID:").grid(row=2, column=0)
    new_major_id_entry = Entry(window)
    new_major_id_entry.grid(row=2, column=1)

    Label(window, text="Change Date (YYYY-MM-DD):").grid(row=3, column=0)
    change_date_entry = Entry(window)
    change_date_entry.grid(row=3, column=1)

    Label(window, text="Application Status:").grid(row=4, column=0)
    application_status_entry = Entry(window)
    application_status_entry.grid(row=4, column=1)

    Button(window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2)

# 选择照片文件
def select_photo(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    entry.delete(0, END)
    entry.insert(0, file_path)

# 查询课表
def get_course_schedule():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                cursor.callproc('GetCourseSchedule', (studentid,))
                for result in cursor.stored_results():
                    courses = result.fetchall()
                    result_text.delete(1.0, END)
                    
                    # 表头
                    result_text.insert(END, f"{'Course ID':<10} {'Course Name':<30} {'Credits':<10}\n")
                    result_text.insert(END, "-" * 50 + "\n")
                    
                    # 课程信息
                    for course in courses:
                        result_text.insert(END, f"{course[0]:<10} {course[1]:<30} {course[2]:<10}\n")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    window = Toplevel(root)
    window.title("Get Course Schedule")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2)

    result_text = Text(window, height=15, width=50)
    result_text.grid(row=2, column=0, columnspan=2)


# 查询成绩
def get_student_grade():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                course_id = int(course_id_entry.get())
                cursor.callproc('GetStudentGrade', (studentid, course_id))
                for result in cursor.stored_results():
                    grade = result.fetchall()
                    result_text.delete(1.0, END)
                    if grade:
                        result_text.insert(END, f"Grade: {grade[0][0]}\n")
                    else:
                        result_text.insert(END, "No grade found.\n")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    window = Toplevel(root)
    window.title("Get Student Grade")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Course ID:").grid(row=1, column=0)
    course_id_entry = Entry(window)
    course_id_entry.grid(row=1, column=1)

    Button(window, text="Submit", command=submit).grid(row=2, column=0, columnspan=2)

    result_text = Text(window, height=10, width=50)
    result_text.grid(row=3, column=0, columnspan=3)

# 计算学生平均成绩
# 调用存储函数计算学生的平均成绩
def calculate_student_avg_grade():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor(buffered=True)
            try:
            # 调用存储函数
                studentid = int(studentid_entry.get())
                cursor.execute("SELECT calculate_average_grade(%s)", (studentid,))
                records = cursor.fetchone()
                if records:
                    result_text.insert(END, f"avg_score: {records[0]}\n")
                else:
                    result_text.insert(END, "No records found")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    window = Toplevel(root)
    window.title("Calculate Student Average Grade")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2)

    result_text = Text(window, height=10, width=50)
    result_text.grid(row=2, column=0, columnspan=3)
# 添加成绩
def add_student_grade():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                course_id = int(course_id_entry.get())
                grade = float(grade_entry.get())
                cursor.callproc('AddStudentGrade', (studentid, course_id, grade))
                conn.commit()
                messagebox.showinfo("Success", "Grade added successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Add Student Grade")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Course ID:").grid(row=1, column=0)
    course_id_entry = Entry(window)
    course_id_entry.grid(row=1, column=1)

    Label(window, text="Grade:").grid(row=2, column=0)
    grade_entry = Entry(window)
    grade_entry.grid(row=2, column=1)

    Button(window, text="Submit", command=submit).grid(row=3, column=0, columnspan=2)

# 修改成绩
def update_student_grade():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                course_id = int(course_id_entry.get())
                grade = float(grade_entry.get())
                cursor.callproc('UpdateStudentGrade', (studentid, course_id, grade))
                conn.commit()
                messagebox.showinfo("Success", "Grade updated successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Update Student Grade")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Course ID:").grid(row=1, column=0)
    course_id_entry = Entry(window)
    course_id_entry.grid(row=1, column=1)

    Label(window, text="Grade:").grid(row=2, column=0)
    grade_entry = Entry(window)
    grade_entry.grid(row=2, column=1)

    Button(window, text="Submit", command=submit).grid(row=3, column=0, columnspan=2)

    # 查询奖惩信息
def query_rewards_punishments():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                query = "SELECT * FROM rewardpunishment WHERE studentid = %s"
                cursor.execute(query, (studentid,))
                records = cursor.fetchall()
                result_text.delete(1.0, END)
                if records:
                    for record in records:
                        result_text.insert(END, f"Record ID: {record[0]}\n")
                        result_text.insert(END, f"Student ID: {record[1]}\n")
                        result_text.insert(END, f"Type: {record[2]}\n")
                        result_text.insert(END, f"Description: {record[3]}\n")
                        result_text.insert(END, f"Date: {record[4]}\n")
                        result_text.insert(END, f"DepartmentID: {record[5]}\n\n")
                else:
                    result_text.insert(END, "No records found")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    window = Toplevel(root)
    window.title("Query Rewards and Punishments")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2)

    result_text = Text(window, height=10, width=50)
    result_text.grid(row=2, column=0, columnspan=2)

# 增加奖惩信息
def add_rewards_punishments():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                studentid = int(studentid_entry.get())
                rp_type = rp_type_entry.get()
                description = description_entry.get()
                date = Date_entry.get()
                departmentID = DepartmentID_entry.get()
                query = "INSERT INTO rewardpunishment (studentid, type, description, date, departmentID) VALUES (%s, %s, %s,%s,%s)"
                cursor.execute(query, (studentid, rp_type, description,date, departmentID))
                conn.commit()
                messagebox.showinfo("Success", "Record added successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Add Rewards and Punishments")

    Label(window, text="Student ID:").grid(row=0, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=0, column=1)

    Label(window, text="Type (Reward/Punishment):").grid(row=1, column=0)
    rp_type_entry = Entry(window)
    rp_type_entry.grid(row=1, column=1)

    Label(window, text="Description:").grid(row=2, column=0)
    description_entry = Entry(window)
    description_entry.grid(row=2, column=1)

    Label(window, text="Date:").grid(row=3, column=0)
    Date_entry = Entry(window)
    Date_entry.grid(row=3, column=1)

    Label(window, text="DepartmentID:").grid(row=4, column=0)
    DepartmentID_entry = Entry(window)
    DepartmentID_entry.grid(row=4, column=1)

    Button(window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2)

# 删除奖惩信息
def delete_rewards_punishments():
    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                record_id = int(record_id_entry.get())
                query = "DELETE FROM rewardpunishment WHERE id = %s"
                cursor.execute(query, (record_id,))
                conn.commit()
                messagebox.showinfo("Success", "Record deleted successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    window.title("Delete Rewards and Punishments")

    Label(window, text="Record ID:").grid(row=0, column=0)
    record_id_entry = Entry(window)
    record_id_entry.grid(row=0, column=1)

    Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2)

# 修改奖惩信息
# 更新奖励惩罚记录
def update_rewards_punishments():
    def get_record_info():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                record_id = int(record_id_entry.get())
                query = "SELECT studentid, type, description, Date, departmentID FROM rewardpunishment WHERE recordid = %s"
                cursor.execute(query, (record_id,))
                record = cursor.fetchone()
                if record:
                    studentid_entry.delete(0, END)
                    rp_type_entry.delete(0, END)
                    description_entry.delete(0, END)
                    Date_entry.delete(0, END)
                    DepartmentID_entry.delete(0, END)
                    studentid_entry.insert(0, record[0])
                    rp_type_entry.insert(0, record[1])
                    description_entry.insert(0, record[2])
                    Date_entry.insert(0, record[3])
                    DepartmentID_entry.insert(0, record[4])
                else:
                    messagebox.showerror("Error", "Record ID not found.")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    def submit():
        conn = connect_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                record_id = int(record_id_entry.get())
                studentid = int(studentid_entry.get())
                rp_type = rp_type_entry.get()
                description = description_entry.get()
                Date = Date_entry.get()
                departmentID = int(DepartmentID_entry.get())
                if not record_id or not studentid or not rp_type or not description or not Date or not departmentID:
                    messagebox.showerror("Error", "All fields must be filled out.")
                    return
                query = "UPDATE rewardpunishment SET studentid = %s, type = %s, description = %s, Date = %s, departmentID = %s WHERE recordid = %s"
                cursor.execute(query, (studentid, rp_type, description, Date, departmentID, record_id))
                conn.commit()
                messagebox.showinfo("Success", "Record updated successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
            window.destroy()

    window = Toplevel(root)
    
    window.title("Update Rewards and Punishments")

    Label(window, text="Record ID:").grid(row=0, column=0)
    record_id_entry = Entry(window)
    record_id_entry.grid(row=0, column=1)
    Button(window, text="Get", command=get_record_info).grid(row=0, column=2)

    Label(window, text="Student ID:").grid(row=1, column=0)
    studentid_entry = Entry(window)
    studentid_entry.grid(row=1, column=1)

    Label(window, text="Type (Reward/Punishment):").grid(row=2, column=0)
    rp_type_entry = Entry(window)
    rp_type_entry.grid(row=2, column=1)

    Label(window, text="Description:").grid(row=3, column=0)
    description_entry = Entry(window)
    description_entry.grid(row=3, column=1)

    Label(window, text="Date:").grid(row=4, column=0)
    Date_entry = Entry(window)
    Date_entry.grid(row=4, column=1)

    Label(window, text="Department ID:").grid(row=5, column=0)
    DepartmentID_entry = Entry(window)
    DepartmentID_entry.grid(row=5, column=1)

    Button(window, text="Submit", command=submit).grid(row=6, column=0, columnspan=2)

# 主窗口
root = Tk()
root.title("Student Management System")

Button(root, text="Insert Student", command=insert_student).grid(row=0, column=0, padx=10, pady=10)
Button(root, text="Delete Student", command=delete_student).grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Update Student", command=update_student).grid(row=1, column=0, padx=10, pady=10)
Button(root, text="Get Student", command=get_student).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Enroll Course", command=enroll_course).grid(row=2, column=0, padx=10, pady=10)
Button(root, text="Drop Course", command=drop_course).grid(row=2, column=1, padx=10, pady=10)
Button(root, text="Cal Student avg grade", command=calculate_student_avg_grade).grid(row=3, column=0, padx=10, pady=10)
Button(root, text="Get Course Schedule", command=get_course_schedule).grid(row=3, column=1, padx=10, pady=10)
Button(root, text="Get Student Grade", command=get_student_grade).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Add Student Grade", command=add_student_grade).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Update Student Grade", command=update_student_grade).grid(row=5, column=0, padx=10, pady=10)
Button(root, text="Apply Major Change", command=apply_major_change).grid(row=5, column=1, padx=10, pady=10)
Button(root, text="Query Rewards and Punishments", command=query_rewards_punishments).grid(row=6, column=0, padx=10, pady=10)
Button(root, text="Add Rewards and Punishments", command=add_rewards_punishments).grid(row=6, column=1, padx=10, pady=10)
Button(root, text="Delete Rewards and Punishments", command=delete_rewards_punishments).grid(row=7, column=0, padx=10, pady=10)
Button(root, text="Update Rewards and Punishments", command=update_rewards_punishments).grid(row=7, column=1, padx=10, pady=10)
root.mainloop()
