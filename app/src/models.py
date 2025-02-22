from typing import List, Optional
from pydantic import BaseModel


class Organizer(BaseModel):
    email: str


class Joiner(BaseModel):
    name: str
    country: str


class Event(BaseModel):
    id: Optional[int]
    name: str
    date: str
    organizer: Organizer
    status: str
    type: Optional[str]
    location: Optional[str]
    max_attendees: int
    joiners: Optional[List[Joiner]]