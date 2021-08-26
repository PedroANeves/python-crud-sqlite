#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
python-crud-sqlite.py
manage students names,classes an emails using CRUD conventions
inserts, selects, updates and deletes entries on student.db
using sqlite3 and python3
"""
import sqlite3
from csv import reader

DATABASE = "students.db"

##############################################################################
# CRUD backend
##############################################################################

def connect_to_students_db(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    return(connection,cursor)

def create_empty_student_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS STUDENT")
    cursor.execute("""
        CREATE TABLE STUDENT(
        ID          INTEGER     PRIMARY KEY     NOT NULL,
        FIRST_NAME  TEXT                        NOT NULL,
        LAST_NAME   TEXT                        NOT NULL,
        CLASS       TEXT,
        EMAIL       TEXT
        )
    """)

def add_student(studentData: dict):
    with con:
        cursor.execute("""
            INSERT INTO STUDENT (FIRST_NAME,LAST_NAME,CLASS)
            VALUES(:first,:last,:class)
        """,studentData)

def add_muliple_students(studentList: list):
    with con:
        cursor.executemany("""
            INSERT INTO STUDENT (FIRST_NAME,LAST_NAME,CLASS,EMAIL)
            VALUES(?,?,?,?)
        """,studentList)

def delete_student(studentId: int):
    with con:
        cursor.execute("""
            DELETE FROM STUDENT
            WHERE ID=?
        """,(studentId,))

def fetch_student_by_name(firstName: str="",lastName: str=""):
    cursor.execute("""
        SELECT ID,FIRST_NAME,LAST_NAME,CLASS,EMAIL FROM STUDENT
        WHERE FIRST_NAME=? OR LAST_NAME=?
    """,(firstName,lastName))
    return(cursor.fetchall())

def fetch_student_by_id(studentId: int):
    cursor.execute("""
        SELECT ID,FIRST_NAME,LAST_NAME,CLASS,EMAIL FROM STUDENT
        WHERE ID=?
    """,(studentId,))
    return(cursor.fetchone())

def change_student_class(studentId: int,newClass: str):
    with con:
        cursor.execute("""
            UPDATE STUDENT SET CLASS=? WHERE ID=?    
        """,(newClass,studentId))

def create_student_email(studentId: int):
    cursor.execute("""
        SELECT FIRST_NAME,LAST_NAME FROM STUDENT
        WHERE ID=?
    """,(studentId,))
    first,last = cursor.fetchone()
    email = "{}.{}@school.edu".format(first,last)

    student = {
        "id": studentId,
        "first": first,
        "last": last,
        "email": email
    }
    with con:
        cursor.execute("""
            UPDATE STUDENT set EMAIL=:email
            WHERE ID=:id
        """,student)

def database_fill(csvfile):

    with open(csvfile,"r") as read_obj:
        csv_reader = reader(read_obj)
        listOfMockStudents = list(map(tuple,csv_reader))
        add_muliple_students(listOfMockStudents)

##############################################################################
# terminal user inverface
##############################################################################

def start_tui():
    
    while True:
        print("""
        1 - (s)earch student
        2 - (r)egister student
        3 - (d)elete student
        4 - change student (c)lass
        5 - generate student (e)-mail

        9 - manage student data(b)ase

        0 - (q)uit program
        """)
        option = input("select option: ").lower()

        if option in ("1", "s"):
            search_one_tui()
        elif option in ("2", "r"):
            register_one_student_tui()
        elif option in ("3", "d"):
            delete_student_tui()
        elif option in ("4", "c"):
            change_student_class_tui()
        elif option in ("5", "e"):
            generate_student_email_tui()
        elif option in ("9", "b"):
            manage_database_tui()
        elif option in ("0", "q"):
            close_tui()

def hold_tui():
    _ = input("press Enter to continue")

def search_one_tui():
    firstNameInput = input("enter first name(leave blank for any): ")
    lastNameInput = input("enter last name(leave blank for any): ")

    student = fetch_student_by_name(firstNameInput,lastNameInput)

    studentId, firstName, lastName, className, email = student[0]

    print("""

        student id: {}
        full name: {} {}
        registered class: {}
        student e-mail: {}

    """.format(studentId, firstName, lastName, className, email)
    )
    hold_tui()

def register_one_student_tui():

    firstNameInput = input("enter first name: ")
    while firstNameInput == "":
        firstNameInput = input("please enter first name: ")
    
    lastNameInput = input("enter last name: ")
    while lastNameInput == "":
        lastNameInput = input("please enter last name: ")
    
    classNameInput = input("enter class name(leave blank for none): ")

    studentData = {
        "first": firstNameInput,
        "last": lastNameInput,
        "class": classNameInput
    }

    add_student(studentData)

    option = input("generate student email? (y/n) ").lower()
    if option in ("y","yes"):
        generate_student_email_tui()
    else:
        print("no e-mail generated")

def delete_student_tui():
    studentIdInput = input("enter student id ('0' to cancel): ")
    while studentIdInput == "":
        studentIdInput = input("please enter student id ('0' to cancel): ")
    if studentIdInput == "0":
        print("deletion canceled")
    else:
        studentId  = int(studentIdInput)
        student = fetch_student_by_id(studentId)
        studentId, firstName, lastName, className, email = student
        print("""

            student id: {}
            full name: {} {}
            registered class: {}
            student e-mail: {}

        """.format(studentId, firstName, lastName, className, email)
        )

        print("[THIS IS INRREVERSABLE]")
        option = input("delete student? (y/n): ").lower()
        if option in ("y","yes"):
            delete_student(studentIdInput)
        else:
            print("deletion canceled")

def change_student_class_tui():
    studentIdInput = input("enter student id ('0' to cancel): ")
    while studentIdInput == "":
        studentIdInput = input("please enter student id ('0' to cancel): ")
    if studentIdInput == "0":
        print("transfer canceled")
    else:
        studentId  = int(studentIdInput)
        student = fetch_student_by_id(studentId)
        studentId, firstName, lastName, className, email = student
        print("""

            student id: {}
            full name: {} {}
            registered class: {}
            student e-mail: {}

        """.format(studentId, firstName, lastName, className, email)
        )

        newClassInput = input("enter new class ('0' to cancel): ")
        if newClassInput == "0":
            print("transfer canceled")
        else:
            change_student_class(studentId,newClassInput)

def generate_student_email_tui():
    studentIdInput = input("enter student id ('0' to cancel): ")
    while studentIdInput == "":
        studentIdInput = input("please enter student id ('0' to cancel): ")

    if studentIdInput != "0":
        create_student_email(studentIdInput)

def manage_database_tui():
    while True:
        print("""
        1 - (f)ill database with mock data
        9 - (e)mpty database [IRREVERSABLE]

        0 - (q)uit this menu and return to main menu
        """)
        option = input("select option: ").lower()

        if option in ("1", "f"):
            database_fill_tui()
        elif option in ("9","e"):
            database_empty_tui()
        elif option in ("0","q"):
            break

def database_fill_tui():
    name = input("enter filename with .csv sufix: (default: mockdata.csv)")
    if name == "": name = "mockdata.csv"
    database_fill(name)

def database_empty_tui():
    print("[WARNING: THIS IS IRREVERSABLE!]")
    option = input("Are you sure you want to empty the database? (y/n)").lower()
    if option in ("y","yes"):
        create_empty_student_table(cursor)

def close_tui():
    option = input("Are you sure you want to quit? (y/n)").lower()
    if option in ("y","yes"):
        con.close()
        quit()

##############################################################################
# main
##############################################################################

con,cursor = connect_to_students_db(DATABASE)

start_tui()
