import json
from datetime import datetime, timedelta
from app.models import Event
from tests.utils import TestCase


class EventResourceTest(TestCase):

    def setUp(self):
        super(EventResourceTest, self).setUp()
        with self.app.app_context():
            self.event = Event(
                name="Mum's Birthday", description="Great party!",
                start_time=datetime.now() + timedelta(days=5),
                end_time=datetime.now() + timedelta(days=5, hours=3),
                total=10, taken=0,
            )
            self.db.session.add(self.event)
            self.db.session.commit()

    def test_events(self):
        resp = self.app_client.get('/events')
        data = json.loads(resp.get_data(as_text=True))
        self.assertDictEqual({'message': 'hello'}, data)
