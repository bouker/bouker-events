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

    def test_event_list_post(self):
        event_dict = {
            'name': 'Day of Pizza Concert',
            'description': 'Great fun!',
            'startTime': '2018-01-30T20:00:00+00:00',
            'endTime': '2018-01-31T6:00:00+00:00',
            'total': 200,
        }
        resp = self.app_client.post('/events', data=json.dumps(event_dict), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        with self.app.app_context():
            event_count = Event.query.count()
            self.assertEqual(event_count, 3)
            event = Event.query.all()[2]
            self.assertEqual(event.name, "Day of Pizza Concert")
            self.assertEqual(event.start_time, datetime(year=2018, month=1, day=30, hour=20))
            self.assertEqual(event.taken, 0)

    def test_event_list_post_error_missing_start_time(self):
        event_dict = {
            'name': 'Day of Pizza Concert',
        }
        resp = self.app_client.post('/events', data=json.dumps(event_dict), content_type='application/json')
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(resp.status_code, 400)
        self.assertIn('startTime', data)

    def test_event_list_post_error_invalid_total(self):
        event_dict = {
            'name': 'Day of Pizza Concert',
            'startTime': '2018-01-30T20:00:00+00:00',
            'total': 'Something but not a number',
        }
        resp = self.app_client.post('/events', data=json.dumps(event_dict), content_type='application/json')
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(resp.status_code, 400)
        self.assertIn('total', data)

    def test_event_post(self):
        event_dict = {
            'number': '5',
        }
        resp = self.app_client.post('/events/%s' % self.event_id,
                                    data=json.dumps(event_dict),
                                    content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        with self.app.app_context():
            self.assertEqual(Event.query.get(self.event_id).taken, 5)

    def test_event_post_number_too_big(self):
        event_dict = {
            'number': '100',
        }
        resp = self.app_client.post('/events/%s' % self.event_id,
                                    data=json.dumps(event_dict),
                                    content_type='application/json')
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(resp.status_code, 422)
        self.assertIn('number', data)

    def test_event_post_number_decreases_to_negative_taken(self):
        event_dict = {
            'number': '-30',
        }
        resp = self.app_client.post('/events/%s' % self.event_id,
                                    data=json.dumps(event_dict),
                                    content_type='application/json')
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(resp.status_code, 422)
        self.assertIn('number', data)

    def test_event_post_event_does_not_exist(self):
        event_dict = {
            'number': '5',
        }
        resp = self.app_client.post('/events/%s' % 10000,
                                    data=json.dumps(event_dict),
                                    content_type='application/json')
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(resp.status_code, 404)
        self.assertIn('id', data)
