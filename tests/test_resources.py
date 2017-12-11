import json
from datetime import datetime
from app.models import Event
from tests.utils import TestCase


class EventResourcesTest(TestCase):

    def setUp(self):
        super(EventResourcesTest, self).setUp()
        with self.app.app_context():
            self.event = Event(
                name="Mum's Birthday",
                description="Great party",
                start_time=datetime(year=2018, month=4, day=7, hour=15),
                end_time=datetime(year=2018, month=4, day=7, hour=18),
                total=10, taken=0,
            )
            self.db.session.add(self.event)
            another_event = Event(
                name="Dad's Birthday",
                description="Even better party",
                start_time=datetime(year=2018, month=10, day=4, hour=15),
                end_time=datetime(year=2018, month=10, day=4, hour=21),
                total=10, taken=0,
            )
            self.db.session.add(another_event)
            self.db.session.commit()
            self.event_id = self.event.id

    def test_event_list_get(self):
        resp = self.app_client.get('/events')
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], {
            'id': self.event_id,
            'name': "Mum's Birthday",
            'description': "Great party",
            'startTime': '2018-04-07T15:00:00+00:00',
            'endTime': '2018-04-07T18:00:00+00:00',
            'total': 10,
            'taken': 0,
            'available': 10,
        })

    def test_event_get(self):
        resp = self.app_client.get('/events/%s' % self.event_id)
        data = json.loads(resp.get_data(as_text=True))
        self.assertDictEqual(data, {
            'id': self.event_id,
            'name': "Mum's Birthday",
            'description': "Great party",
            'startTime': '2018-04-07T15:00:00+00:00',
            'endTime': '2018-04-07T18:00:00+00:00',
            'total': 10,
            'taken': 0,
            'available': 10,
        })
