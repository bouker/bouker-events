import logging.config
from flask import request
from flask_restful import Resource

from app.logging import default_handler
from app.database import db
from app.models import Event
from app.schemas import EventSchema, EventBookSchema


logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)
logger.addHandler(default_handler)


def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
    return response


class EventListResource(Resource):

    def get(self):
        """
        Returns all events list
        """
        events = Event.query.all()
        logger.info("Returning all events, count: %s items", Event.query.count())
        return EventSchema().dump(events, many=True).data

    def post(self):
        """
        Creates new event
        """
        data, errors = EventSchema().load(request.get_json())
        logger.info("Creating new event, data: %s", request.get_json())
        if errors:
            logger.info("Cannot create event, data: %s", request.get_json())
            return errors, 400
        event = Event(name=data['name'],
                      start_time=data['start_time'])
        for key, value in data.items():
            setattr(event, key, value)
        db.session.add(event)
        db.session.commit()
        logger.info("Event created, data: %s", request.get_json())
        return


class EventResource(Resource):

    def get(self, event_id):
        """
        Returns specific event data
        :param event_id:
        """
        logger.info("Returning event data, event_id: %s", event_id)
        event = Event.query.get(event_id)
        if not event:
            logger.warning("Returning event data, event_id: %s. Event not found.", event_id)
            return {'id': ['event not found']}, 404
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
        logger.info("Modifying event data, event_id: %s, data: %s", event_id, request.get_json())
        data, errors = EventBookSchema().load(request.get_json())
        if errors:
            return errors, 400
        event = Event.query.get(event_id)
        if not event:
            logger.warning("Modifying event data, event_id: %s, data: %s. Event not found.",
                           event_id, request.get_json())
            return {'id': ['event not found']}, 404
        event.taken += data['number']
        if event.taken > event.total:
            logger.warning("Modifying event data, event_id: %s, data: %s. Number cannot exceed event total count.",
                           event_id, request.get_json())
            return {'number': ['number cannot exceed event total count']}, 422
        elif event.taken < 0:
            logger.warning("Modifying event data, event_id: %s, data: %s. Number cannot be less than zero.",
                           event_id, request.get_json())
            return {'number': ['number cannot be less than zero']}, 422
        db.session.commit()
        return

    def delete(self, event_id):
        """
        Returns specific event data
        :param event_id:
        """
        logger.warning("Removing event, event_id: %s", event_id)
        event = Event.query.get(event_id)
        if not event:
            logger.warning("Removing event, event_id: %s. Event not found.", event_id, request.get_json())
            return {'id': ['event not found']}, 404
        db.session.delete(event)
        db.session.commit()
        return None, 204
