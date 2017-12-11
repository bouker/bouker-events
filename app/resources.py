from flask_restful import Resource
from app.models import Event
from app.schemas import EventSchema


class EventListResource(Resource):

    def get(self):
        """
        Returns all events list
        """
        events = Event.query.all()
        return EventSchema().dump(events, many=True).data

    def post(self):
        """
        Creates new event
        """
        return


class EventResource(Resource):

    def get(self, event_id):
        """
        Returns specific event data
        :param event_id:
        """
        event = Event.query.get(event_id)
        return EventSchema().dump(event).data

    def post(self, event_id):
        """
        Modifies specific event id (changes is available/taken counters).
        Request message: { ‘number’: reverseDelta }
        :param event_id:
        """
        return
