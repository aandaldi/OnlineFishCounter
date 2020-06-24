from tests.base_tests import BaseTest
from app.event.models import EventModel
from datetime import datetime as dt


class EventIntegrationTest(BaseTest):
    def test_crete_and_save_event(self):
        with self.app_context:
            event = EventModel(
                name='Launching',
                created_by="admin",
                date_modified=dt.now(),
                modified_by="admin",
                date=dt.strptime('2020-10-20 10:10:10', '%Y-%m-%d %H:%M:%S'),
                max_stick=60
            )

            self.assertIsNone(EventModel.lookup('Launching'))
            event.save_to_db()
            self.assertIsNotNone(EventModel.lookup('Launching'))

    def test_update_event(self):
        with self.app_context:
            event = EventModel(
                name='Launching',
                created_by="admin",
                date_modified=dt.now(),
                modified_by="admin",
                date=dt.strptime('2020-10-20 10:10:10', '%Y-%m-%d %H:%M:%S'),
                max_stick=60
            )

            event.save_to_db()

            event_db = EventModel.lookup('Launching')
            self.assertIsNotNone(event_db)
            self.assertEqual(event_db.name, "Launching")

            event_db.name = 'Update Launching'
            event_db.update_on_db()

            self.assertIsNone(EventModel.lookup("Launching"))
            self.assertIsNotNone(EventModel.lookup("Update Launching"))
