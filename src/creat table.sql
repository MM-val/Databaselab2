DROP DATABASE if  EXISTS schooldb;
CREATE DATABASE SchoolDB;



USE SchoolDB;

CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL
);

CREATE TABLE Major (
    MajorID INT PRIMARY KEY,
    MajorName VARCHAR(100) NOT NULL,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);
DROP TABLE if  EXISTS student;
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Gender VARCHAR(10),
    BirthDate DATE,
    Hometown VARCHAR(100),
    Ethnicity VARCHAR(50),
    MajorID INT,
    Photo LONGBLOB,
    FOREIGN KEY (MajorID) REFERENCES Major(MajorID)
);

CREATE TABLE MajorChange (
    ChangeID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    OldMajorID INT,
    NewMajorID INT,
    ChangeDate DATE,
    ApplicationStatus VARCHAR(50),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (OldMajorID) REFERENCES Major(MajorID),
    FOREIGN KEY (NewMajorID) REFERENCES Major(MajorID)
);

CREATE TABLE RewardPunishment (
    RecordID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    Type VARCHAR(50),
    Description TEXT,
    Date DATE,
    DepartmentID INT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    Credits INT,
    Hours INT
);
CREATE TABLE Grades (
    student_id INT,
    course_id INT,
    grade DECIMAL(5, 2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Student(studentid),
    FOREIGN KEY (course_id) REFERENCES Course(courseid)
);

CREATE TABLE CourseEnrollment (
    EnrollmentID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    CourseID INT,
    Grade VARCHAR(10),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE StudentLog (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    Action VARCHAR(10),
    Timestamp DATETIME
);
ALTER TABLE student MODIFY photo LONGBLOB;
INSERT INTO department (DepartmentID,Departmentname) VALUES (1,'Computer Science');
INSERT INTO department (DepartmentID,Departmentname) VALUES (2,'Math');
INSERT INTO Major (MajorID, MajorName, DepartmentID) VALUES (1, 'Computer Science', 1);
INSERT INTO Major (MajorID, MajorName, DepartmentID) VALUES (2, 'geography', 2);
SELECT DATABASE()


-- 插入Department数据
INSERT INTO Department (DepartmentID, DepartmentName) VALUES
(3, 'Physics');

-- 插入Major数据
INSERT INTO Major (MajorID, MajorName, DepartmentID) VALUES
(3, 'Applied Mathematics', 2),
(4, 'Theoretical Physics', 3);

-- 插入Student数据
INSERT INTO Student (StudentID, Name, Gender, BirthDate, Hometown, Ethnicity, MajorID, Photo) VALUES
(2, 'Bob Johnson', 'Male', '1999-11-22', 'Los Angeles', 'African American', 2, NULL),
(3, 'Carol White', 'Female', '2001-07-30', 'Chicago', 'Hispanic', 3, NULL);

-- 插入MajorChange数据
INSERT INTO MajorChange (StudentID, OldMajorID, NewMajorID, ChangeDate, ApplicationStatus) VALUES
(1, 1, 2, '2023-01-01', 'Approved'),
(2, 2, 1, '2023-02-15', 'Pending');

-- 插入RewardPunishment数据
INSERT INTO RewardPunishment (StudentID, Type, Description, Date, DepartmentID) VALUES
(1, 'Reward', 'Outstanding academic performance', '2023-03-01', 1),
(2, 'Punishment', 'Late submission of assignment', '2023-04-10', 1);

-- 插入Course数据
INSERT INTO Course (CourseID, CourseName, Credits, Hours) VALUES
(1, 'Introduction to Programming', 4, 60),
(2, 'Data Structures', 3, 45),
(3, 'Calculus I', 4, 60);

-- 插入Grades数据
INSERT INTO Grades (student_id, course_id, grade) VALUES
(1, 1, 90.5),
(2, 2, 85.0),
(3, 3, 78.0);

DELETE grades

-- 插入CourseEnrollment数据
INSERT INTO CourseEnrollment (StudentID, CourseID, Grade) VALUES
(1, 1, 'A'),
(2, 2, 'B'),
(3, 3, 'C');

