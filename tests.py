import ruobr_api
import ruobr_api.new
from datetime import datetime, timedelta
import unittest
import asyncio
import os

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

ruobr = ruobr_api.Ruobr(username, password)
aruobr = ruobr_api.AsyncRuobr(username, password)

new_ruobr = ruobr_api.new.Ruobr(username, password)
new_aruobr = ruobr_api.new.AsyncRuobr(username, password)

loop = asyncio.get_event_loop()


class RuobrTests(unittest.TestCase):
    def test_getUser(self):
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


class NewRuobrTests(unittest.TestCase):
    def test_getUser(self):
        self.assertIsNotNone(new_ruobr.getUser())

    def test_getChildren(self):
        self.assertGreater(len(new_ruobr.getChildren()), 0)

    def test_getMessage(self):
        mail = new_ruobr.getMail()
        self.assertIsNotNone(mail)
        self.assertIsNotNone(new_ruobr.getMessage(mail[0]))

    def test_getRecipients(self):
        self.assertIsNotNone(new_ruobr.getRecipients())

    def test_getAchievements(self):
        self.assertIsNotNone(new_ruobr.getAchievements())

    def test_getAllMarks(self):
        controlmarks = new_ruobr.getControlmarks()
        self.assertIsNotNone(controlmarks)
        period = controlmarks[0]
        subject = period.marks[0]
        self.assertIsNotNone(new_ruobr.getAllMarks(period, subject))

    def test_getEvents(self):
        self.assertIsNotNone(new_ruobr.getEvents())

    def test_getCertificate(self):
        self.assertIsNotNone(new_ruobr.getCertificate())

    def test_getBirthdays(self):
        self.assertIsNotNone(new_ruobr.getBirthdays())

    def test_getFoodInfo(self):
        self.assertIsNotNone(new_ruobr.getFoodInfo())

    def test_getClassmates(self):
        self.assertIsNotNone(new_ruobr.getClassmates())

    def test_getBooks(self):
        self.assertIsNotNone(new_ruobr.getBooks())

    def test_getIos(self):
        self.assertIsNotNone(new_ruobr.getIos())

    def test_getGuide(self):
        self.assertIsNotNone(new_ruobr.getGuide())

    def test_getTimetable(self):
        self.assertIsNotNone(
            new_ruobr.getTimetable(datetime.now() - timedelta(weeks=2), datetime.now())
        )


class NewAsyncRuobrTests(unittest.TestCase):
    def test_getUser(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getUser()))

    def test_getChildren(self):
        self.assertGreater(len(loop.run_until_complete(new_aruobr.getChildren())), 0)

    def test_getMessage(self):
        mail = loop.run_until_complete(new_aruobr.getMail())
        self.assertIsNotNone(mail)
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getMessage(mail[0])))

    def test_getRecipients(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getRecipients()))

    def test_getAchievements(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getAchievements()))

    def test_getAllMarks(self):
        controlmarks = loop.run_until_complete(new_aruobr.getControlmarks())
        self.assertIsNotNone(controlmarks)
        period = controlmarks[0]
        subject = period.marks[0]
        self.assertIsNotNone(
            loop.run_until_complete(new_aruobr.getAllMarks(period, subject))
        )

    def test_getEvents(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getEvents()))

    def test_getCertificate(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getCertificate()))

    def test_getBirthdays(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getBirthdays()))

    def test_getFoodInfo(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getFoodInfo()))

    def test_getClassmates(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getClassmates()))

    def test_getBooks(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getBooks()))

    def test_getIos(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getIos()))

    def test_getGuide(self):
        self.assertIsNotNone(loop.run_until_complete(new_aruobr.getGuide()))

    def test_getTimetable(self):
        self.assertIsNotNone(
            loop.run_until_complete(
                new_aruobr.getTimetable(
                    datetime.now() - timedelta(weeks=2), datetime.now()
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
    loop.close()
