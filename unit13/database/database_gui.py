import tkinter as tk
import sqlite3
from sqlite3 import Error

class GUI:
    '''GUI Class creates a GUI that allows a user to input person and student information into a database'''
    def __init__(self, root):
        self.root = root
        self.conn = None
        self.database = 'gui_database.db'
        self.error = tk.Label(self.root)
        self.person_labels = []
        self.student_labels = []

    '''Creates buttons, labels, and entries for the GUI'''
    def set_up(self):
        self.create_db_button = tk.Button(self.root, text='Make database and table', command=lambda : self.create_connection_and_tables(self.database))
        self.create_db_button.grid(row=1, column=1, pady=5, padx=5)

        self.view_all_student = tk.Button(self.root, text='View Student Table', command=lambda: self.select_all_students())
        self.view_all_student.grid(row=1, column=2, padx=5, pady=5)

        self.view_all_people = tk.Button(self.root, text='View Person Table', command=lambda: self.select_all_persons())
        self.view_all_people.grid(row=1, column=3, pady=5, padx=5)

        self.exit = tk.Button(self.root, text='Exit', command=lambda: self.root.quit())
        self.exit.grid(row=1, column=4)

        '''Creating Person'''
        self.first_name = tk.Label(self.root, text='First name')
        self.first_name.grid(row=2, column=1, pady=5, padx=5)

        self.first_name_entry = tk.Entry(self.root)
        self.first_name_entry.grid(row=2, column=2, pady=5, padx=5)

        self.last_name = tk.Label(self.root, text='Last name')
        self.last_name.grid(row=3, column=1, pady=5, padx=5)

        self.last_name_entry = tk.Entry(self.root)
        self.last_name_entry.grid(row=3, column=2, pady=5, padx=5)

        self.add_person_button = tk.Button(self.root, text='Add Person', command=lambda: self.create_person())
        self.add_person_button.grid(row=3, column=3, padx=5, pady=5)

        '''Creating Student'''
        self.major = tk.Label(self.root, text='Major')
        self.major.grid(row=5, column=1, padx=5, pady=5)

        self.major_entry = tk.Entry(self.root)
        self.major_entry.grid(row=5, column=2, padx=5, pady=5)

        self.start_date = tk.Label(self.root, text='Start Date')
        self.start_date.grid(row=6, column=1, padx=5, pady=5)

        self.start_date_entry = tk.Entry(self.root)
        self.start_date_entry.grid(row=6, column=2, padx=5, pady=5)

        self.add_student_button = tk.Button(self.root, text='Add Student', command=lambda: self.create_student())
        self.add_student_button.grid(row=6, column=3, padx=5, pady=5)

    '''Creates a person in the database using the user input'''
    def create_person(self):
        if self.first_name_entry.get() == '' or self.last_name_entry.get() == '':

            self.error.config(text='Some person info left blank')
            self.error.grid(row=7, column=2, pady=5, padx=5)
        else:
            self.error.grid_forget()
            firstname = self.first_name_entry.get()
            lastname = self.last_name_entry.get()

            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()

            cursor.execute('INSERT INTO person (firstname, lastname) VALUES(?, ?)', (firstname, lastname))
            conn.commit()

            cursor.close()
            conn.close()

            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)

    '''Displays database rows of person table'''
    def select_all_persons(self):
        """Query all rows of person table
        :param conn: the connection object
        :return:
        """
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM person")

        rows = cur.fetchall()

        if len(self.student_labels) > 0:
            for student in self.student_labels:
                student.grid_forget()

        curr_row = 8
        for person in rows:
            person_label = tk.Label(self.root, text=person)
            person_label.grid(row=curr_row, column=1)
            self.person_labels.append(person_label)
            curr_row += 1

        cur.close()
        conn.close()

    '''Creates a student in the student table using person_id as a foreign key'''
    def create_student(self):
        if self.first_name_entry.get() == '' or self.last_name_entry.get() == '' or self.major_entry.get() == '' or self.start_date_entry.get() == '':
            self.error.config(text='Some student information left blank')
            self.error.grid(row=7, column=2, pady=5, padx=5)
        else:
            firstname = self.first_name_entry.get()
            lastname = self.last_name_entry.get()
            major = self.major_entry.get()
            startdate = self.start_date_entry.get()

            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            cur.execute('SELECT id FROM person WHERE firstname=? and lastname=?', (firstname, lastname))
            try:
                personid = cur.fetchone()[0]

                cur.execute('INSERT INTO student (major, begin_date, person_id) VALUES(?, ?, ?)', (major, startdate, personid))
                conn.commit()
            except TypeError:
                self.error.config(text="Person isn't set first")

            cur.close()
            conn.close()

            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.major_entry.delete(0, tk.END)
            self.start_date_entry.delete(0, tk.END)

    '''Displays database rows of student table'''
    def select_all_students(self):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()

        cur.execute('SELECT * FROM student')

        rows = cur.fetchall()

        if len(self.person_labels) > 0:
            for person in self.person_labels:
                person.grid_forget()

        curr_row = 8
        for student in rows:
            student_label = tk.Label(self.root, text=student)
            student_label.grid(row=curr_row, column=1)
            self.student_labels.append(student_label)
            curr_row += 1

        cur.close()
        conn.close()

    '''Makes Database and Tables'''
    def create_connection_and_tables(self, db):
        """ Connect to a SQLite database """
        try:
            conn = sqlite3.connect(db)
            self.create_tables(conn, db)
            conn.close()

        except Error as err:
            print(err)
        finally:
            conn.close()

    '''Takes in sql query to make a table and executes it'''
    def create_table(self, conn, sql_create_table):
        """ Creates table with give sql statement
        :param conn: Connection object
        :param sql_create_table: a SQL CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(sql_create_table)
        except Error as e:
            print(e)

    '''Contains tables to be made and calls create_table def to create specified tables'''
    def create_tables(self, conn, database):

        sql_create_person_table = """ CREATE TABLE IF NOT EXISTS person (
                                            id integer PRIMARY KEY,
                                            firstname text NOT NULL,
                                            lastname text NOT NULL
                                        ); """

        sql_create_student_table = """CREATE TABLE IF NOT EXISTS student (
                                        id integer PRIMARY KEY,
                                        major text NOT NULL,
                                        begin_date text NOT NULL,
                                        person_id integer,
                                        FOREIGN KEY (person_id) REFERENCES person (id)
                                    );"""

        # create a database connection
        if conn is not None:
            # create person table
            self.create_table(conn, sql_create_person_table)
            # create student table
            self.create_table(conn, sql_create_student_table)
        else:
            print("Unable to connect to " + str(database))

    '''Starts setup and mainloop'''
    def start_gui(self):
        self.root.title('Database GUI')
        self.set_up()
        self.root.mainloop()

if __name__ == '__main__':
    window = tk.Tk()
    db_gui = GUI(window)
    db_gui.start_gui()
