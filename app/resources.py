from flask import request
from flask_restful import Resource

from app.database import db
from app.models import Event
from app.schemas import EventSchema, EventBookSchema


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
        data, errors = EventSchema().load(request.get_json())
        if errors:
            return errors, 400
        event = Event(name=data['name'],
                      description=data['description'],
                      start_time=data['start_time'],
                      end_time=data['end_time'],
                      total=data['total'])
        db.session.add(event)
        db.session.commit()
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

        On error returns different codes:
        - 400 if fields are missing or incorrect format
        - 404 if event was not found
        - 422 if number booked is too big
        :param event_id:
        """
        data, errors = EventBookSchema().load(request.get_json())
        if errors:
            return errors, 400
        event = Event.query.get(event_id)
        if not event:
            return {'id': ['event not found']}, 404
        event.taken += data['number']
        if event.taken > event.total:
            return {'number': ['number cannot exceed event total count']}, 422
        elif event.taken < 0:
            return {'number': ['number cannot be less than zero']}, 422
        db.session.commit()
        return
