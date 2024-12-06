from csp_solver import CSP
from dataclasses import dataclass
from typing import List, Tuple, Dict
from datetime import datetime, timedelta

@dataclass
class Course:
    name: str
    duration: int
    teacher: str
    required_room_type: str

@dataclass
class Room:
    name: str
    room_type: str

@dataclass
class TimeSlot:
    start_time: datetime
    end_time: datetime

class ScheduleCSP:
    def __init__(self, courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot]):
        self.csp = CSP()
        self.courses = courses
        self.rooms = rooms
        self.time_slots = time_slots
        
        for course in courses:
            var_name = course.name
            domain = [
                (room, slot) 
                for room in rooms 
                if room.room_type == course.required_room_type
                for slot in time_slots
            ]
            self.csp.add_variable(var_name, domain)
        
        self._add_time_conflict_constraints()
        self._add_room_conflict_constraints()
        self._add_teacher_conflict_constraints()
        
    def _add_time_conflict_constraints(self):
        def time_conflict(assignment1, assignment2):
            room1, slot1 = assignment1
            room2, slot2 = assignment2
            if room1 == room2:
                return (slot1.end_time <= slot2.start_time or 
                       slot2.end_time <= slot1.start_time)
            return True
            
        for i, course1 in enumerate(self.courses):
            for course2 in self.courses[i + 1:]:
                self.csp.add_constraint(
                    (course1.name, course2.name),
                    time_conflict
                )
                
    def _add_room_conflict_constraints(self):
        def room_conflict(assignment1, assignment2):
            room1, slot1 = assignment1
            room2, slot2 = assignment2
            if room1 == room2:
                return (slot1.end_time <= slot2.start_time or 
                       slot2.end_time <= slot1.start_time)
            return True
            
        for i, course1 in enumerate(self.courses):
            for course2 in self.courses[i + 1:]:
                self.csp.add_constraint(
                    (course1.name, course2.name),
                    room_conflict
                )
                
    def _add_teacher_conflict_constraints(self):
        def teacher_conflict(assignment1, assignment2):
            _, slot1 = assignment1
            _, slot2 = assignment2
            return (slot1.end_time <= slot2.start_time or 
                   slot2.end_time <= slot1.start_time)
            
        for i, course1 in enumerate(self.courses):
            for course2 in self.courses[i + 1:]:
                if course1.teacher == course2.teacher:
                    self.csp.add_constraint(
                        (course1.name, course2.name),
                        teacher_conflict
                    )
    
    def solve(self) -> Dict[str, Tuple[Room, TimeSlot]]:
        return self.csp.backtracking_search() 