## EMPLOYEES AND PROJECTS
**EXPLANATION:**
    ### 1NF: 
    1.Does the table have more than one value in a single cell?, **No.**
    2.Are the same repeated columns for the same data (project 1, project 2)?, **No.**
    3.Is there a key that identifies each row without repeating?, **Yes** (Employee Id, Project Id)

    The table is already in 1NF.

    ### 2NF:
    1.Is the table in 1NF?, **Yes**
    2.When part of the key repeats, does other data repeat with it?, **Yes**
      EmployeeId 201 repeats, and "Ana Rivera", "IT" and "2222-2222" repeat with it.
    
    Partial dependencies:
    - EmployeeName, Department, DepartmentPhone: depend only on EmployeeId.
    - ProjectName, ProjectBudget: depend only on ProjectId.

    The table was split into:
    - Employees: (EmployeeId, EmployeeName, Department, DepartmentPhone)
    - Projects: (ProjectId, ProjectName, ProjectBudget)
    - EmployeeProject: (EmployeeId, ProjectId)

    Employees:
    | EmployeeId | EmployeeName | Department | DepartmentPhone |
    | 201 | Ana Rivera | IT | 2222-2222 |
    | 202 | Luis Mendez | Marketing | 1111-1111 | 

    Projects:
    | ProjectId | ProjectName | ProjectBudget |
    | P001 | Web App | 50000 |
    | P002 | API REST | 25000 |
    | P003 | Campaña TV | 30000 |

    EmployeeProjects:
    | EmployeeId | ProjectId |
    | 201 | P001 |
    | 201 | P002 |
    | 202 | P003 |

    ### 3NF
    1. Are the tables in 2NF? **Yes**
    2. Does any non-key column depend on another non-key column? **Yes**
       In Employees: EmployeeId (Department, DepartmentPhone)
       The phone describes the department, not the employee.

    The department data was moved to its own table:
    - Departments: (DepartmentId, Name, Phone)
    - Employees: (EmployeeId, Name, DepartmentId)
    - Projects and EmployeeProject stay the same.

    Departments:
    | DepartmentId | DepartmentName | DepartmentPhone |
    | D01 | IT | 2222-2222 | 
    | D02 | Marketing | 1111-1111 |

    Employees:
    | EmployeeId | EmployeeName | DepartmentId |
    | 201 | Ana Rivera | D01 | 
    | 202 | Luis Mendez | D02 |

    Projects: 
    | ProjectId | ProjectName | ProjectBudget |
    | P001 | Web App | 50000 | 
    | P002 | API REST | 25000 | 
    | P003 | Campaña TV | 30000 |

    EmployeeProject:
    | EmployeeId | ProjectId |
    | 201 | P001 | 
    | 201 | P002 | 
    | 202 | P003 |

    All tables are now in 3NF.