from tests.base_tests import BaseTest
from app.event.models import EventModel
from datetime import datetime as dt


class UnitEventTest(BaseTest):
    def test_create_event(self):
        event = EventModel(
            name='Launching',
            created_by="admin",
            date_modified=dt.now(),
            modified_by="admin",
            date=dt.strptime('2020-10-20 10:10:10', '%Y-%m-%d %H:%M:%S'),
            max_stick=60
        )
        self.assertEqual(event.name, "Launching")
        self.assertEqual(event.max_stick, 60)
        self.assertIsInstance(event, EventModel)


    def test_to_json(self):
        event = EventModel(
            name='Launching',
            created_by="admin",
            date_modified=dt.now(),
            modified_by="admin",
            date=dt.strptime('2020-10-20 10:10:10', '%Y-%m-%d %H:%M:%S'),
            max_stick=60
        )


        expected = {'uuid': event.uuid,
                    'date_created': event.date_created,
                    'created_by': 'admin',
                    'date_modified': event.date_modified,
                    'modified_by': 'admin',
                    'name': 'Launching',
                    'date': dt.strptime('2020-10-20 10:10:10', '%Y-%m-%d %H:%M:%S'),
                    'max_stick': 60}

        self.assertEqual(event.to_json(), expected)
