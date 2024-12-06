"""
Example Usage of CSP Scheduler

Input Examples:
--------------
1. Courses:
   - Course("Math 101", 2, "Dr. Smith", "Lecture Hall")
     Format: name, duration in hours, teacher, required room type
   
2. Rooms:
   - Room("Room 101", "Classroom")
     Format: name, room type
   
3. Time Slots:
   - TimeSlot(datetime(2024, 1, 1, 9, 0), datetime(2024, 1, 1, 11, 0))
     Format: start_time, end_time

Output Example:
--------------
Schedule found!

Math 101:
Room: Hall 1
Time: Monday 09:00 AM - 11:00 AM

Physics 101:
Room: Lab A
Time: Monday 09:00 AM - 11:00 AM

Constraints Satisfied:
1. No teacher teaches two classes at the same time
2. No room hosts two classes at the same time
3. Each course is assigned to a room of the correct type
"""

from schedule_csp import ScheduleCSP, Course, Room, TimeSlot
from datetime import datetime, timedelta

def example1_simple():
    print("\nExample 1: Simple Schedule")
    print("-" * 50)
    
    courses = [
        Course("Math 101", 2, "Dr. Smith", "Classroom"),
        Course("Physics 101", 2, "Dr. Smith", "Classroom"),
    ]
    
    rooms = [
        Room("Room 101", "Classroom"),
    ]
    
    # Only Monday morning slots
    time_slots = []
    current_time = datetime(2024, 1, 1, 9, 0)  # Monday 9 AM
    for _ in range(2):
        time_slots.append(TimeSlot(
            current_time,
            current_time + timedelta(hours=2)
        ))
        current_time += timedelta(hours=2)
    
    scheduler = ScheduleCSP(courses, rooms, time_slots)
    solution = scheduler.solve()
    print_solution(solution)

def example2_complex():
    print("\nExample 2: Complex Schedule")
    print("-" * 50)
    
    courses = [
        Course("Math 101", 2, "Dr. Smith", "Lecture Hall"),
        Course("Physics 101", 2, "Dr. Johnson", "Lab"),
        Course("Chemistry 101", 2, "Dr. Brown", "Lab"),
        Course("English 101", 2, "Dr. Davis", "Classroom"),
        Course("History 101", 2, "Dr. Wilson", "Classroom")
    ]
    
    rooms = [
        Room("Room 101", "Classroom"),
        Room("Room 102", "Classroom"),
        Room("Lab A", "Lab"),
        Room("Lab B", "Lab"),
        Room("Hall 1", "Lecture Hall")
    ]
    
    time_slots = []
    for day in range(5):  # Monday to Friday
        current_time = datetime(2024, 1, 1 + day, 9, 0)
        while current_time.hour < 17:
            time_slots.append(TimeSlot(
                current_time,
                current_time + timedelta(hours=2)
            ))
            current_time += timedelta(hours=2)
    
    scheduler = ScheduleCSP(courses, rooms, time_slots)
    solution = scheduler.solve()
    print_solution(solution)

def example3_conflict():
    print("\nExample 3: Conflict Example")
    print("-" * 50)
    print("Attempting to schedule two courses with the same teacher in one time slot...")
    
    courses = [
        Course("Math 101", 2, "Dr. Smith", "Classroom"),
        Course("Physics 101", 2, "Dr. Smith", "Classroom"),
    ]
    
    rooms = [
        Room("Room 101", "Classroom"),
        Room("Room 102", "Classroom"),
    ]
    
    # Only one time slot - should create a conflict
    time_slots = [TimeSlot(
        datetime(2024, 1, 1, 9, 0),
        datetime(2024, 1, 1, 11, 0)
    )]
    
    scheduler = ScheduleCSP(courses, rooms, time_slots)
    solution = scheduler.solve()
    print_solution(solution)

def print_solution(solution):
    if solution:
        print("\nSchedule found!")
        for course_name, (room, time_slot) in solution.items():
            print(f"\n{course_name}:")
            print(f"Room: {room.name}")
            print(f"Time: {time_slot.start_time.strftime('%A %I:%M %p')} - "
                  f"{time_slot.end_time.strftime('%I:%M %p')}")
    else:
        print("\nNo solution found! Constraints cannot be satisfied.")

def main():
    example1_simple()
    example2_complex()
    example3_conflict()

if __name__ == "__main__":
    main() 