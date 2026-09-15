CREATE TABLE Departments(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    Phone TEXT NOT NULL
);

CREATE TABLE Employees(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    DepartmentId INTEGER NOT NULL REFERENCES Departments(Id)
);

CREATE TABLE Projects(
    Id INTEGER PRIMARY KEY,
    Code TEXT NOT NULL UNIQUE,
    Name TEXT NOT NULL,
    Budget DECIMAL(18, 2) NOT NULL
);

CREATE TABLE EmployeeProject(
    Id INTEGER PRIMARY KEY,
    EmployeeId INTEGER NOT NULL REFERENCES Employees(Id),
    ProjectId INTEGER NOT NULL REFERENCES Projects(Id),
    UNIQUE(EmployeeId, ProjectId)
);

-- Create indexes to improve performance
CREATE INDEX IX_Employees_DepartmentId ON Employees(DepartmentId);
CREATE INDEX IX_EmployeeProject_ProjectId ON EmployeeProject(ProjectId);