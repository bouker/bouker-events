from app.resources import EventListResource, EventResource


def configure_routes(api):
    api.add_resource(EventListResource, '/events', endpoint='event_list_ep')
    api.add_resource(EventResource, '/events/<string:event_id>', endpoint='event_ep')
