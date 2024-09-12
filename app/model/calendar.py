from datetime import datetime, date, time, timedelta

# Simulamos las dependencias externas con simples funciones de error
def slot_not_available_error():
    raise ValueError("Slot not available.")

def event_not_found_error():
    raise ValueError("Event not found.")

def date_lower_than_today_error():
    raise ValueError("Date is lower than today's date.")

def reminder_not_found_error(index):
    raise IndexError(f"Reminder at index {index} not found.")

def generate_unique_id():
    return "unique-event-id"

class Reminder:
    EMAIL: str = "email"
    SYSTEM: str = "system"

    def __init__(self, date_time: datetime, type_: str = EMAIL):
        self.date_time = date_time
        self.type = type_

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"

class Event:
    def __init__(self, title: str, description: str, date_: date, start_at: time, end_at: time, id: str = None):
        self.title = title
        self.description = description
        self.date_ = date_
        self.start_at = start_at
        self.end_at = end_at
        self.id = id or generate_unique_id()
        self.reminders = []

    def add_reminder(self, date_time, type_="email"):
        reminder = Reminder(date_time=date_time, type_=type_)
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
    def __init__(self, date_: date):
        self.date_ = date_
        self.slots = {}
        self._init_slots()

    def _init_slots(self):
        current_time = time(0, 0)
        while current_time < time(23, 45):
            self.slots[current_time] = None
            current_time = (datetime.combine(self.date_, current_time) + timedelta(minutes=15)).time()
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

class Calendar:
    def __init__(self):
        self.days = {}
        self.events = {}

    def add_event(self, title: str, description: str, date_: date, start_at: time, end_at: time) -> str:
        if date_ < datetime.now().date():
            date_lower_than_today_error()

        if date_ not in self.days:
            self.days[date_] = Day(date_)
        event = Event(title=title, description=description, date_=date_, start_at=start_at, end_at=end_at)
        self.days[date_].add_event(event.id, start_at, end_at)
        self.events[event.id] = event
        return event.id

    def add_reminder(self, event_id: str, date_time: datetime, type_: str):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        event.add_reminder(date_time, type_)

    def find_available_slots(self, date_: date) -> list[time]:
        if date_ not in self.days:
            return []
        return [slot for slot, event_id in self.days[date_].slots.items() if event_id is None]

    
