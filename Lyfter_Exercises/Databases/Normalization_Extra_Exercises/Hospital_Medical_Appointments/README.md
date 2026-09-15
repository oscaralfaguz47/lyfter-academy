## HOSPITAL AND MEDICAL APPOINTMENTS

**Original table:**
| Appointment ID | Patient Name | Patient Phone | Doctor Name | Specialty    | Date       | Time     |
| A01	         | Diana Vargas | 8888-1111	    | Dr. Soto	  | Pediatría	 | 2024-08-01 | 10:00 AM |
| A02	         | Diana Vargas | 8888-1111	    | Dr. Soto	  | Pediatría	 | 2024-08-10 | 10:00 AM |
| A03	         | Edwin Mora   | 8999-2222	    | Dr. Mora	  | Cardiología	 | 2024-08-05 | 01:00 PM |

**1NF**
The table is already in 1NF. The only change is defining the primary key. (PK: Appointment ID)
Appointments: (no changes)
| Appointment ID | Patient Name | Patient Phone | Doctor Name | Specialty    | Date       | Time     |
| A01	         | Diana Vargas | 8888-1111	    | Dr. Soto	  | Pediatría	 | 2024-08-01 | 10:00 AM |
| A02	         | Diana Vargas | 8888-1111	    | Dr. Soto	  | Pediatría	 | 2024-08-10 | 10:00 AM |
| A03	         | Edwin Mora   | 8999-2222	    | Dr. Mora	  | Cardiología	 | 2024-08-05 | 01:00 PM |

**2NF:**
- Is the table in 1NF?, Yes.
- Is the key composite?, No, the key is only Appointment ID.

Appointments: (no changes)
| Appointment ID | Patient Name | Patient Phone | Doctor Name | Specialty    | Date       | Time     |
| A01	         | Diana Vargas | 8888-1111	    | Dr. Soto	  | Pediatría	 | 2024-08-01 | 10:00 AM |
| A02	         | Diana Vargas | 8888-1111	    | Dr. Soto	  | Pediatría	 | 2024-08-10 | 10:00 AM |
| A03	         | Edwin Mora   | 8999-2222	    | Dr. Mora	  | Cardiología	 | 2024-08-05 | 01:00 PM |

**3NF:**
- Is the table in 2NF?, Yes.

Patients:
| Patient ID     | Patient Name | Patient Phone | 
| P01	         | Diana Vargas | 8888-1111	    | 
| P02	         | Edwin Mora   | 8999-2222	    | 

Specialties:
| Specialty ID | Specialty   | 
| S01	       | Pediatría	 | 
| S02	       | Cardiología |

Doctors:
| Doctor ID | Doctor Name | Specialty ID |
| D001	    | Dr. Soto	  | S01          |
| D002	    | Dr. Mora	  | S02          |

Appointments:
| Appointment ID | Patient ID   | Doctor ID   | Date       | Time     |
| A01	         | P01          | D001    	  | 2024-08-01 | 10:00 AM |
| A02	         | P01          | D001   	  | 2024-08-10 | 10:00 AM |
| A03	         | P02          | D002   	  | 2024-08-05 | 01:00 PM |




