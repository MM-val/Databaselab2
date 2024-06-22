USE SchoolDB;
DELIMITER //

CREATE PROCEDURE AddStudent(
    IN p_StudentID INT,
    IN p_Name VARCHAR(100),
    IN p_Gender VARCHAR(10),
    IN p_BirthDate DATE,
    IN p_Hometown VARCHAR(100),
    IN p_Ethnicity VARCHAR(50),
    IN p_MajorID INT,
    IN p_Photo BLOB
)
BEGIN
    DECLARE majorExists INT;

    SELECT COUNT(*) INTO majorExists
    FROM Major
    WHERE MajorID = p_MajorID;

    IF majorExists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Major does not exist';
    ELSE
        INSERT INTO Student (StudentID, Name, Gender, BirthDate, Hometown, Ethnicity, MajorID, Photo)
        VALUES (p_StudentID, p_Name, p_Gender, p_BirthDate, p_Hometown, p_Ethnicity, p_MajorID, p_Photo);
    END IF;
END //

DELIMITER ;
DELIMITER //
DROP PROCEDURE if EXISTS DeleteStudent

CREATE PROCEDURE DeleteStudent(IN p_StudentID INT)
BEGIN
    DELETE FROM grades WHERE Student_ID = p_StudentID;
    DELETE FROM majorchange WHERE Student_ID = p_StudentID;
    DELETE FROM courseenrollment WHERE StudentID = p_StudentID;
    DELETE FROM Student WHERE StudentID = p_StudentID;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE UpdateStudent(
    IN p_StudentID INT,
    IN p_Name VARCHAR(100),
    IN p_Gender VARCHAR(10),
    IN p_BirthDate DATE,
    IN p_Hometown VARCHAR(100),
    IN p_Ethnicity VARCHAR(50),
    IN p_MajorID INT,
    IN p_Photo BLOB
)
BEGIN
    DECLARE majorExists INT;

    SELECT COUNT(*) INTO majorExists
    FROM Major
    WHERE MajorID = p_MajorID;

    IF majorExists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Major does not exist';
    ELSE
        UPDATE Student
        SET Name = p_Name, Gender = p_Gender, BirthDate = p_BirthDate, Hometown = p_Hometown, Ethnicity = p_Ethnicity, MajorID = p_MajorID, Photo = p_Photo
        WHERE StudentID = p_StudentID;
    END IF;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE GetStudent(IN p_StudentID INT)
BEGIN
    SELECT * FROM Student WHERE StudentID = p_StudentID;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE EnrollCourse(
    IN p_StudentID INT,
    IN p_CourseID INT
)
BEGIN
    DECLARE courseExists INT;
    start TRANSACTION;
    SELECT COUNT(*) INTO courseExists
    FROM Course
    WHERE CourseID = p_CourseID;

    IF courseExists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course does not exist';
    ELSE
        INSERT INTO CourseEnrollment (StudentID, CourseID)
        VALUES (p_StudentID, p_CourseID);
    END IF;
    COMMIT;
END //

DELIMITER ;
DELIMITER //
drop procedure if EXISTS DropCourse

CREATE PROCEDURE DropCourse(
    IN p_StudentID INT,
    IN p_CourseID INT
)
BEGIN
    DELETE FROM grades WHERE Student_ID = p_StudentID AND Course_ID = p_CourseID;
    DELETE FROM CourseEnrollment WHERE StudentID = p_StudentID AND CourseID = p_CourseID;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE GetStudentGrades(IN p_StudentID INT)
BEGIN
    SELECT Course.CourseName, CourseEnrollment.Grade
    FROM CourseEnrollment
    JOIN Course ON CourseEnrollment.CourseID = Course.CourseID
    WHERE CourseEnrollment.StudentID = p_StudentID;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE ApplyMajorChange(
    IN p_StudentID INT,
    IN p_OldMajorID INT,
    IN p_NewMajorID INT,
    IN p_ChangeDate DATE,
    IN p_ApplicationStatus VARCHAR(50)
)
BEGIN
    INSERT INTO MajorChange (StudentID, OldMajorID, NewMajorID, ChangeDate, ApplicationStatus)
    VALUES (p_StudentID, p_OldMajorID, p_NewMajorID, p_ChangeDate, p_ApplicationStatus);
END //

DELIMITER //
drop trigger IF EXISTS StudentmajorAfterInsertUpdate

CREATE TRIGGER StudentmajorAfterInsertUpdate
AFTER INSERT ON majorchange
FOR EACH ROW
BEGIN
    UPDATE student set MajorID = NEW.oldMajorID WHERE StudentID = NEW.StudentID;
END //

DELIMITER ;

DELIMITER //
drop PROCEDURE if EXISTS GetCourseSchedule
DELIMITER //
-- 查询课表
CREATE PROCEDURE GetCourseSchedule(IN p_studentid INT)
BEGIN
    SELECT c.courseid, c.coursename, c.credits 
    FROM courseenrollment e
    JOIN Course c ON e.courseid = c.courseid
    WHERE e.studentid = p_studentid;
END //

DELIMITER //
-- 查询平均成绩

CREATE FUNCTION calculate_average_grade(student_id INT)
RETURNS DECIMAL(5,2)
READS SQL DATA
BEGIN
    DECLARE avg_grade DECIMAL(5,2);
    
    SELECT AVG(grade) INTO avg_grade
    FROM Grades
    WHERE student_id = student_id;
    
    RETURN IFNULL(avg_grade, 0);
END //

DELIMITER ;


DELIMITER ;


-- 查询成绩
CREATE PROCEDURE GetStudentGrade(IN p_studentid INT, IN p_courseid INT)
BEGIN
    SELECT grade 
    FROM Grades 
    WHERE studentid = p_studentid AND courseid = p_courseid;
END //

-- 添加成绩
CREATE PROCEDURE AddStudentGrade(IN p_studentid INT, IN p_courseid INT, IN p_grade DECIMAL(5, 2))
BEGIN
    INSERT INTO Grades (studentid, courseid, grade) 
    VALUES (p_studentid, p_courseid, p_grade);
END //

-- 修改成绩
CREATE PROCEDURE UpdateStudentGrade(IN p_studentid INT, IN p_courseid INT, IN p_grade DECIMAL(5, 2))
BEGIN
    UPDATE Grades 
    SET grade = p_grade 
    WHERE studentid = p_studentid AND courseid = p_courseid;
END //

DELIMITER ;
