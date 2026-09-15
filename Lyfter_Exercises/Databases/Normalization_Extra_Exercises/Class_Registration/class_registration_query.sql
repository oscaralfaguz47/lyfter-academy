CREATE TABLE Students(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);

CREATE TABLE Instructors(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE
);

CREATE TABLE Courses(
    Id INTEGER PRIMARY KEY,
    Code TEXT NOT NULL UNIQUE,
    Name TEXT NOT NULL,
    InstructorId INTEGER NOT NULL REFERENCES Instructors(Id)
);

CREATE TABLE StudentCourses(
    Id INTEGER PRIMARY KEY,
    StudentId INTEGER NOT NULL REFERENCES Students(Id),
    CourseId INTEGER NOT NULL REFERENCES Courses(Id),
    UNIQUE(StudentId, CourseId)
);

-- Create indexes to improve performance
CREATE INDEX IX_Courses_InstructorId ON Courses(InstructorId);
CREATE INDEX IX_StudentCourse_CourseId ON StudentCourses(CourseId); 