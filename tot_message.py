from enum import Enum
from werkzeug.datastructures import MultiDict
from utils import Location, Channel


class Radius(Enum):
    SAY = "Say"
    SHOUT = "Shout"
    MUMBLE = "Mumble"
    WHISPER = "Whisper"


class TotMessage:

    def __init__(self, dictionary: MultiDict):
        self.character = dictionary.get("character")
        self.sender = dictionary.get("sender")
        self.message = dictionary.get("message")
        self.radius = Radius(dictionary.get("radius"))
        self.location = Location.from_string(dictionary.get("location"))
        self.channel = Channel(int(dictionary.get("channel")))

    def __str__(self):
        return f"Character: {self.character} Sender: {self.sender} Message: {self.message} Radius: {self.radius.name}"+ \
               f"Location: {self.location} Channel: {self.channel.name} "
