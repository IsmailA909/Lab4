import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QMessageBox, QComboBox,
    QTabWidget, QHBoxLayout, QFormLayout
)

DATABASE = 'university.db'

def create_connection():
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(e)
    return conn

def init_db():
    """ Create tables in the SQLite database according to the SQL schema above """
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                subject TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                code TEXT NOT NULL,
                instructor_id INTEGER,
                FOREIGN KEY (instructor_id) REFERENCES teachers (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollment (
                student_id INTEGER,
                course_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (course_id) REFERENCES courses (id)
            );
        ''')
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Management System")
        self.resize(1000, 800)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_students_tab(), "Students")
        self.tabs.addTab(self.create_teachers_tab(), "Teachers")
        self.tabs.addTab(self.create_courses_tab(), "Courses")
        self.tabs.addTab(self.create_assignments_tab(), "Assignments")
        self.tabs.addTab(self.create_all_records_tab(), "All Records")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        init_db()

    def create_students_tab(self):
        layout = QVBoxLayout()
        self.students_table = QTableWidget(0, 4)
        self.students_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email"])

        self.refresh_students_table()

        form_layout = QFormLayout()
        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()
        form_layout.addRow("Name:", self.student_name_input)
        form_layout.addRow("Age:", self.student_age_input)
        form_layout.addRow("Email:", self.student_email_input)

        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        form_layout.addWidget(add_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_students_table)
        form_layout.addWidget(refresh_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.students_table)

        container = QWidget()
        container.setLayout(layout)
        return container

    def add_student(self):
        name = self.student_name_input.text()
        age = self.student_age_input.text()
        email = self.student_email_input.text()

        if not name or not age.isdigit() or not email:
            QMessageBox.warning(self, "Input Error", "Please enter valid data for all fields")
            return

        student = (name, int(age), email)
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO students (name, age, email) VALUES (?, ?, ?)', student)
            conn.commit()
            conn.close()

        self.refresh_students_table()
        self.student_name_input.clear()
        self.student_age_input.clear()
        self.student_email_input.clear()

    def refresh_students_table(self):
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            conn.close()

            self.students_table.setRowCount(0)
            for row in rows:
                row_position = self.students_table.rowCount()
                self.students_table.insertRow(row_position)
                for i, item in enumerate(row):
                    self.students_table.setItem(row_position, i, QTableWidgetItem(str(item)))

    def create_teachers_tab(self):
        layout = QVBoxLayout()
        self.teachers_table = QTableWidget(0, 3)
        self.teachers_table.setHorizontalHeaderLabels(["ID", "Name", "Subject"])

        self.refresh_teachers_table()

        form_layout = QFormLayout()
        self.teacher_name_input = QLineEdit()
        self.teacher_subject_input = QLineEdit()
        form_layout.addRow("Name:", self.teacher_name_input)
        form_layout.addRow("Subject:", self.teacher_subject_input)

        add_button = QPushButton("Add Teacher")
        add_button.clicked.connect(self.add_teacher)
        form_layout.addWidget(add_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_teachers_table)
        form_layout.addWidget(refresh_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.teachers_table)

        container = QWidget()
        container.setLayout(layout)
        return container

    def add_teacher(self):
        name = self.teacher_name_input.text()
        subject = self.teacher_subject_input.text()

        if not name or not subject:
            QMessageBox.warning(self, "Input Error", "Please enter valid data for all fields")
            return

        teacher = (name, subject)
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO teachers (name, subject) VALUES (?, ?)', teacher)
            conn.commit()
            conn.close()

        self.refresh_teachers_table()
        self.teacher_name_input.clear()
        self.teacher_subject_input.clear()

    def refresh_teachers_table(self):
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teachers")
            rows = cursor.fetchall()
            conn.close()

            self.teachers_table.setRowCount(0)
            for row in rows:
                row_position = self.teachers_table.rowCount()
                self.teachers_table.insertRow(row_position)
                for i, item in enumerate(row):
                    self.teachers_table.setItem(row_position, i, QTableWidgetItem(str(item)))

    def create_courses_tab(self):
        layout = QVBoxLayout()
        self.courses_table = QTableWidget(0, 4)
        self.courses_table.setHorizontalHeaderLabels(["ID", "Title", "Code", "Instructor ID"])

        self.refresh_courses_table()

        form_layout = QFormLayout()
        self.course_title_input = QLineEdit()
        self.course_code_input = QLineEdit()
        self.course_instructor_id_input = QLineEdit()
        form_layout.addRow("Title:", self.course_title_input)
        form_layout.addRow("Code:", self.course_code_input)
        form_layout.addRow("Instructor ID:", self.course_instructor_id_input)

        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)
        form_layout.addWidget(add_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_courses_table)
        form_layout.addWidget(refresh_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.courses_table)

        container = QWidget()
        container.setLayout(layout)
        return container

    def add_course(self):
        title = self.course_title_input.text()
        code = self.course_code_input.text()
        instructor_id = self.course_instructor_id_input.text()

        if not title or not code or not instructor_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter valid data for all fields")
            return

        course = (title, code, int(instructor_id))
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO courses (title, code, instructor_id) VALUES (?, ?, ?)', course)
            conn.commit()
            conn.close()

        self.refresh_courses_table()
        self.course_title_input.clear()
        self.course_code_input.clear()
        self.course_instructor_id_input.clear()

    def refresh_courses_table(self):
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            rows = cursor.fetchall()
            conn.close()

            self.courses_table.setRowCount(0)
            for row in rows:
                row_position = self.courses_table.rowCount()
                self.courses_table.insertRow(row_position)
                for i, item in enumerate(row):
                    self.courses_table.setItem(row_position, i, QTableWidgetItem(str(item)))

    def create_assignments_tab(self):
        layout = QVBoxLayout()
        self.assignments_table = QTableWidget(0, 3)
        self.assignments_table.setHorizontalHeaderLabels(["ID", "Assignment Name", "Course ID"])

        self.refresh_assignments_table()

        form_layout = QFormLayout()
        self.assignment_name_input = QLineEdit()
        self.assignment_course_id_input = QLineEdit()
        form_layout.addRow("Assignment Name:", self.assignment_name_input)
        form_layout.addRow("Course ID:", self.assignment_course_id_input)

        add_button = QPushButton("Add Assignment")
        add_button.clicked.connect(self.add_assignment)
        form_layout.addWidget(add_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_assignments_table)
        form_layout.addWidget(refresh_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.assignments_table)

        container = QWidget()
        container.setLayout(layout)
        return container

    def add_assignment(self):
        name = self.assignment_name_input.text()
        course_id = self.assignment_course_id_input.text()

        if not name or not course_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter valid data for all fields")
            return

        assignment = (name, int(course_id))
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO assignments (name, course_id) VALUES (?, ?)', assignment)
            conn.commit()
            conn.close()

        self.refresh_assignments_table()
        self.assignment_name_input.clear()
        self.assignment_course_id_input.clear()

    def refresh_assignments_table(self):
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assignments")
            rows = cursor.fetchall()
            conn.close()

            self.assignments_table.setRowCount(0)
            for row in rows:
                row_position = self.assignments_table.rowCount()
                self.assignments_table.insertRow(row_position)
                for i, item in enumerate(row):
                    self.assignments_table.setItem(row_position, i, QTableWidgetItem(str(item)))

    def create_all_records_tab(self):
        layout = QVBoxLayout()
        self.all_records_table = QTableWidget(0, 5)
        self.all_records_table.setHorizontalHeaderLabels(["Type", "ID", "Name", "Details", "Email/Subject"])

        self.refresh_all_records_table()

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_all_records_table)
        layout.addWidget(refresh_button)
        layout.addWidget(self.all_records_table)

        container = QWidget()
        container.setLayout(layout)
        return container

    def refresh_all_records_table(self):
        conn = create_connection()
        if conn is not None:
            self.all_records_table.setRowCount(0)

            # Students
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            students_rows = cursor.fetchall()
            for student in students_rows:
                row_position = self.all_records_table.rowCount()
                self.all_records_table.insertRow(row_position)
                self.all_records_table.setItem(row_position, 0, QTableWidgetItem("Student"))
                self.all_records_table.setItem(row_position, 1, QTableWidgetItem(str(student[0])))
                self.all_records_table.setItem(row_position, 2, QTableWidgetItem(student[1]))
                self.all_records_table.setItem(row_position, 3, QTableWidgetItem(str(student[2])))
                self.all_records_table.setItem(row_position, 4, QTableWidgetItem(student[3]))

            # Teachers
            cursor.execute("SELECT * FROM teachers")
            teachers_rows = cursor.fetchall()
            for teacher in teachers_rows:
                row_position = self.all_records_table.rowCount()
                self.all_records_table.insertRow(row_position)
                self.all_records_table.setItem(row_position, 0, QTableWidgetItem("Teacher"))
                self.all_records_table.setItem(row_position, 1, QTableWidgetItem(str(teacher[0])))
                self.all_records_table.setItem(row_position, 2, QTableWidgetItem(teacher[1]))
                self.all_records_table.setItem(row_position, 3, QTableWidgetItem(teacher[2]))
                self.all_records_table.setItem(row_position, 4, QTableWidgetItem(""))

            # Courses
            cursor.execute("SELECT * FROM courses")
            courses_rows = cursor.fetchall()
            for course in courses_rows:
                row_position = self.all_records_table.rowCount()
                self.all_records_table.insertRow(row_position)
                self.all_records_table.setItem(row_position, 0, QTableWidgetItem("Course"))
                self.all_records_table.setItem(row_position, 1, QTableWidgetItem(str(course[0])))
                self.all_records_table.setItem(row_position, 2, QTableWidgetItem(course[1]))
                self.all_records_table.setItem(row_position, 3, QTableWidgetItem(course[2]))
                self.all_records_table.setItem(row_position, 4, QTableWidgetItem(str(course[3])))

            # Assignments
            cursor.execute("SELECT * FROM assignments")
            assignments_rows = cursor.fetchall()
            for assignment in assignments_rows:
                row_position = self.all_records_table.rowCount()
                self.all_records_table.insertRow(row_position)
                self.all_records_table.setItem(row_position, 0, QTableWidgetItem("Assignment"))
                self.all_records_table.setItem(row_position, 1, QTableWidgetItem(str(assignment[0])))
                self.all_records_table.setItem(row_position, 2, QTableWidgetItem(assignment[1]))
                self.all_records_table.setItem(row_position, 3, QTableWidgetItem(str(assignment[2])))
                self.all_records_table.setItem(row_position, 4, QTableWidgetItem(""))

            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
