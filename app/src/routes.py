from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    events = EventFileManager.read_events_from_file()
    return events


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    
    events = EventFileManager.read_events_from_file()

    filtered_events = events
    if date:
        filtered_events = [event for event in filtered_events if event.date == date]
    if organizer:
        filtered_events = [event for event in filtered_events if event.organizer.email == organizer]
    if status:
        filtered_events = [event for event in filtered_events if event.status == status]
    if event_type:
        filtered_events = [event for event in filtered_events if event.type == event_type]

    return filtered_events


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    
    events = EventFileManager.read_events_from_file()

    for event in events:
        if event.id == event_id:
            return event

    raise HTTPException(status_code=404, detail="Event not found")
    


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    
    events = EventFileManager.read_events_from_file()

    for existing_event in events:
        if existing_event.id == event.id:
            raise HTTPException(status_code=400, detail="Event ID already exists")

    events.append(event)

    EventFileManager.write_events_to_file(events)

    return event
    


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    
    events = EventFileManager.read_events_from_file()

    for existing_event in events:
        if existing_event.id == event_id:
            existing_event.date = event.date
            existing_event.organizer.email = event.organizer.email
            existing_event.status = event.status
            existing_event.type = event.type
            existing_event.joiners = event.joiners  
            existing_event.location = event.location   
            existing_event.max_attendees = event.max_attendees 
            EventFileManager.write_events_to_file(events)
            return existing_event
    
    
    raise HTTPException(status_code=404, detail="Event Not found")
    

@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    events = EventFileManager.read_events_from_file()

    for event in events:
        if event.id == event_id:
            events.remove(event)
            EventFileManager.write_events_to_file(events)
            return {"message": "Event deleted successfully"}

    
    raise HTTPException(status_code=404, detail="Event Not found")


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    
    events = EventFileManager.read_events_from_file()
    
    event_analyzer = EventAnalyzer()
    
    multiple_meeting_joiners = event_analyzer.get_joiners_multiple_meetings_method(events)
    
    if not multiple_meeting_joiners:
        return "No joiners attending at least 2 meetings"
    
    return multiple_meeting_joiners
    
