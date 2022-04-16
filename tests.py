import ruobr_api
from datetime import datetime, timedelta
import unittest
import asyncio
import os

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

ruobr = ruobr_api.Ruobr(username, password)
aruobr = ruobr_api.AsyncRuobr(username, password)

loop = asyncio.get_event_loop()


class RuobrTests(unittest.TestCase):
    def test_getUser(self):
        self.assertIsNotNone(ruobr.get_user())

    def test_getChildren(self):
        self.assertGreater(len(ruobr.get_children()), 0)

    def test_getMessage(self):
        mail = ruobr.get_mail()
        self.assertIsNotNone(mail)
        self.assertIsNotNone(ruobr.get_message(mail[0]["id"]))

    def test_getRecipients(self):
        self.assertIsNotNone(ruobr.get_recipients())

    def test_getAchievements(self):
        self.assertIsNotNone(ruobr.get_achievements())

    def test_getAllMarks(self):
        controlmarks = ruobr.get_control_marks()
        self.assertIsNotNone(controlmarks)
        period = controlmarks[0]
        if len(period["marks"]) != 0:
            subject = period["marks"][0]
            self.assertIsNotNone(
                ruobr.get_all_marks(period["period"], subject["subject_id"])
            )

    def test_getEvents(self):
        self.assertIsNotNone(ruobr.get_events())

    def test_getBirthdays(self):
        self.assertIsNotNone(ruobr.get_birthdays())

    def test_getFoodInfo(self):
        self.assertIsNotNone(ruobr.get_food_info())

    def test_getClassmates(self):
        self.assertIsNotNone(ruobr.get_classmates())

    def test_getBooks(self):
        self.assertIsNotNone(ruobr.get_books())

    def test_getUsefulLinks(self):
        self.assertIsNotNone(ruobr.get_useful_links())

    def test_getGuide(self):
        self.assertIsNotNone(ruobr.get_guide())

    def test_getTimetable(self):
        self.assertIsNotNone(
            ruobr.get_timetable(datetime.now() - timedelta(weeks=2), datetime.now())
        )


class NewAsyncRuobrTests(unittest.TestCase):
    def test_getUser(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_user()))

    def test_getChildren(self):
        self.assertGreater(len(loop.run_until_complete(aruobr.get_children())), 0)

    def test_getMessage(self):
        mail = loop.run_until_complete(aruobr.get_mail())
        self.assertIsNotNone(mail)
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_message(mail[0]["id"])))

    def test_getRecipients(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_recipients()))

    def test_getAchievements(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_achievements()))

    def test_getAllMarks(self):
        controlmarks = loop.run_until_complete(aruobr.get_control_marks())
        self.assertIsNotNone(controlmarks)
        period = controlmarks[0]
        if len(period["marks"]) != 0:
            subject = period["marks"][0]
            self.assertIsNotNone(
                loop.run_until_complete(
                    aruobr.get_all_marks(period["period"], subject["subject_id"])
                )
            )

    def test_getEvents(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_events()))

    def test_getBirthdays(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_birthdays()))

    def test_getFoodInfo(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_food_info()))

    def test_getClassmates(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_classmates()))

    def test_getBooks(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_books()))

    def test_getUsefulLinks(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_useful_links()))

    def test_getGuide(self):
        self.assertIsNotNone(loop.run_until_complete(aruobr.get_guide()))

    def test_getTimetable(self):
        self.assertIsNotNone(
            loop.run_until_complete(
                aruobr.get_timetable(
                    datetime.now() - timedelta(weeks=2), datetime.now()
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
    loop.close()
