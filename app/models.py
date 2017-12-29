import logging.config
from sqlalchemy import String, Integer, Text, DateTime
from .database import db

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(256), nullable=False)
    description = db.Column(Text)
    start_time = db.Column(DateTime, nullable=False)
    end_time = db.Column(DateTime)
    total = db.Column(Integer)
    taken = db.Column(Integer, default=0)

    def book(self, amount):
        """
        Marks chosen amount of spots as taken.
        Returns True when completed, False in case it's not possible
        :param amount:
        :return:
        """
        status = False
        if amount < self.available:
            self.taken += amount
            status = True
            logger.info("Event %s: booked %s items, %s left", self.id, amount, self.available)
        logger.warning("Event %s: cannot book %s items, %s left", self.id, amount, self.available)
        return status

    @property
    def available(self):
        if self.total:
            return self.total - self.taken
        return None
