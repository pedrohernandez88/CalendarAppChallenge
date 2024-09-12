from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar
from datetime import date, time, timedelta
from app.services.util import slot_not_available_error, event_not_found_error

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error

class Reminder:
    EMAIL: str = "email"
    SYSTEM: str = "system"
    date_time: datetime
    type: str = EMAIL  

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"
    
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    id: str = field(default_factory=generate_unique_id)
    reminders: list ['Reminder'] = field(default_factory=list)

    def add_reminder(self, date_time, type_="email"):
        reminder = Reminder(date_time=date_time, type=type_)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            self.reminders.pop(reminder_index)
        else:
            reminder_not_found_error(reminder_index)

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"Event title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Time: {self.start_at} - {self.end_at}")

class Day:
    def _init_(self, date_: date):
        self.date_ = date_
        self.slots = {}
        self._init_slots()

    def _init_slots(self):
        current_time = time(0, 0)
        while current_time < time(23, 45):
            self.slots[current_time] = None
            current_time = (datetime.combine(self.date_, current_time)+timedelta(minutes=15)).time()
        self.slots[time(23, 45)] = None

    def add_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot] is not None: 
                    slot_not_available_error()  
        for slot in self.slots:
            if start_at <= slot < end_at:
                self.slots[slot] = event_id

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error() 

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None  
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                 slot_not_available_error()
            else:
                self.slots[slot] = event_id

              