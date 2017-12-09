from flask_restful import Resource, fields, marshal_with

from app.models import Event

event_fields = {
    'id': fields.Integer,           # read only
    'name': fields.String,          # required
    'description': fields.String,
    'startTime': fields.DateTime(
        dt_format='iso8601', attribute='start_time'),  # required
    'endTime': fields.DateTime(
        dt_format='iso8601', attribute='end_time'),
    'total': fields.Integer,        # required
    'taken': fields.Integer,        # read only
    'available': fields.Integer,    # read only
}


class EventListResource(Resource):

    @marshal_with(event_fields)
    def get(self):
        """
        Returns all events list
        """
        return Event.query.all()

    def post(self):
        """
        Creates new event
        """
        return


class EventResource(Resource):

    @marshal_with(event_fields)
    def get(self, event_id):
        """
        Returns specific event data
        :param event_id:
        """
        return Event.query.get(event_id)

    def post(self, event_id):
        """
        Modifies specific event id (changes is available/taken counters).
        Request message: { ‘number’: reverseDelta }
        :param event_id:
        """
        return
