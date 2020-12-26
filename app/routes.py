# events
from .events.api import EventsAPI, EventList


def initialize_routes(api):
    # events
    api.add_resource(EventsAPI, "/events", "/events/<string:title>")
    api.add_resource(EventList, "/events/list")
