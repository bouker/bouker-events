from flask_restful import Resource


# TODO: all input/output fields in camelCase

class EventListResource(Resource):
    def get(self):
        """
        Returns all events list
        """
        return {'message': 'hello'}

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
        return {'message': event_id}

    def post(self, event_id):
        """
        Modifies specific event id (changes is available/taken counters).
        Request message: { ‘number’: reverseDelta }
        :param event_id:
        """
        return
