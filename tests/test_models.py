from datetime import datetime, timedelta
from unittest import TestCase

from app.database import db
from app.models import Event


class EventTest(TestCase):

    def setUp(self):
        self.event = Event(
            name="Mum's Birthday", description="Great party!",
            start_time=datetime.now() + timedelta(days=5),
            end_time=datetime.now() + timedelta(days=5, hours=3),
            total=10, taken=0,
        )

    def test_available(self):
        self.assertEqual(self.event.taken, 0)
        self.assertEqual(self.event.total, 10)
        self.assertEqual(self.event.available, 10)
        self.event.taken = 4
        self.assertEqual(self.event.available, 6)

    def test_book(self):
        self.assertEqual(self.event.taken, 0)
        result = self.event.book(4)
        self.assertEqual(self.event.taken, 4)
        self.assertTrue(result)
        result = self.event.book(10)
        self.assertEqual(self.event.taken, 4)
        self.assertFalse(result)
