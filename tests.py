from ruobr_api import Ruobr, AsyncRuobr
from datetime import datetime, timedelta
import unittest
import asyncio
import os

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

ruobr = Ruobr(username, password)
aruobr = AsyncRuobr(username, password)
loop = asyncio.get_event_loop()


class RuobrTests(unittest.TestCase):
    def test_1_getUser(self):
        self.assertIsNotNone(ruobr.getUser())

    def test_getChildren(self):
        self.assertGreater(len(ruobr.getChildren()), 0)

    def test_getMail(self):
        self.assertIsNotNone(ruobr.getMail())

    def test_getControlmarks(self):
        self.assertIsNotNone(ruobr.getControlmarks())

    def test_getTimetable(self):
        self.assertIsNotNone(
            ruobr.getTimetable(datetime.now() - timedelta(weeks=2), datetime.now())
        )

    def test_getProgress(self):
        self.assertIsNotNone(ruobr.getProgress(datetime.now()))

    def test_getMarks(self):
        self.assertIsNotNone(
            ruobr.getMarks(datetime.now() - timedelta(weeks=2), datetime.now())
        )

    def test_getAttendance(self):
        self.assertIsNotNone(
            ruobr.getAttendance(datetime.now() - timedelta(weeks=2), datetime.now())
        )

    def test_getFoodInfo(self):
        self.assertIsNotNone(ruobr.getFoodInfo())

    def test_getFoodHistory(self):
        now = datetime.now()
        self.assertIsNotNone(
            ruobr.getFoodHistory(datetime(now.year, 1, 1), datetime(now.year, 12, 31))
        )

    def test_getNews(self):
        self.assertIsNotNone(ruobr.getNews())


class AsyncRuobrTests(unittest.TestCase):
    def test_1_getUser(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.getUser()))

    def test_getChildren(self):
        self.assertGreater(len(loop.run_until_complete(aruobr.getChildren())), 0)

    def test_getMail(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.getMail()))

    def test_getControlmarks(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.getControlmarks()))

    def test_getTimetable(self):
        self.assertIsNotNone(
            loop.run_until_complete(
                aruobr.getTimetable(datetime.now() - timedelta(weeks=2), datetime.now())
            )
        )

    def test_getProgress(self):
        self.assertIsNotNone(
            loop.run_until_complete(aruobr.getProgress(datetime.now()))
        )

    def test_getMarks(self):
        self.assertIsNotNone(
            loop.run_until_complete(
                aruobr.getMarks(datetime.now() - timedelta(weeks=2), datetime.now())
            )
        )

    def test_getAttendance(self):
        self.assertIsNotNone(
            loop.run_until_complete(
                aruobr.getAttendance(
                    datetime.now() - timedelta(weeks=2), datetime.now()
                )
            )
        )

    def test_getFoodInfo(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.getFoodInfo()))

    def test_getFoodHistory(self):
        now = datetime.now()
        self.assertIsNotNone(
            loop.run_until_complete(
                aruobr.getFoodHistory(
                    datetime(now.year, 1, 1), datetime(now.year, 12, 31)
                )
            )
        )

    def test_getNews(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.getNews()))


if __name__ == "__main__":
    unittest.main()
    loop.close()