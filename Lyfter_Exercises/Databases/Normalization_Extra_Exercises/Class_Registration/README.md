## CLASSES REGISTRATION
**EXPLANATION:**

    ### 1NF:
    The table is already in 1FN because it doesn't have any cell with more than one value and it doesn't have more than one columns with the same category of data.

    | StudentId | StudentName |	CourseCode | CourseName | InstructorName |	InstructorEmail |
    | 301 |	Marco Gómez | CS101	| Python I | Juan Pérez | juan@uni.edu |
    | 301 |	Marco Gómez | CS102	| Python II | Laura Rojas |	laura@uni.edu |
    | 302 |	Carla Ruiz | CS101	| Python I | Juan Pérez | juan@uni.edu |

    ### 2NF:

    Students: 
    | StudentId | StudentName |
    | 301       | Marco Gómez |
    | 302       | Carla Ruiz  | 

    Courses:
    | CourseCode | CourseName | InstructorName | InstructorEmail |
    | CS101	     | Python I   | Juan Pérez     | juan@uni.edu    |
    | CS102	     | Python II  | Laura Rojas    | laura@uni.edu   |

    StudentCourses:
    | StudentId | CourseCode |
    | 301       | CS101	     |
    | 301       | CS102	     | 
    | 302       | CS101	     | 

    ### 3NF:
    
    Instructors:
    | InstructorId | InstructorName | InstructorEmail |
    | 102          | Juan Pérez     | juan@uni.edu    |
    | 103          | Laura Rojas    | laura@uni.edu   |

    Courses: 
    | CourseCode | CourseName | InstructorId |
    | CS101	     | Python I   | 101          |
    | CS102	     | Python II  | 102          |

    Students: (No changes)
    | StudentId | StudentName |
    | 301       | Marco Gómez |
    | 302       | Carla Ruiz  |

    StudentCourses: (no changes)
    | StudentId | CourseCode |
    | 301       | CS101	     |
    | 301       | CS102	     | 
    | 302       | CS101	     | 
