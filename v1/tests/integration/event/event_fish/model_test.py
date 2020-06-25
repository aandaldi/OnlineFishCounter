from tests.base_tests import BaseTest
from app.event.event_fish.models import EventFishModel
from uuid import uuid4
from datetime import datetime as dt


class TestEventFishModel(BaseTest):
    def test_create_event_fish_and_get_by_id(self):
        with self.app_context:
            event = EventFishModel(
                created_by=str(uuid4()),
                date_modified=dt.now(),
                modified_by=str(uuid4()),
                stick_number=3,
                fish_weight=43.03,
                usermanagement_uuid=str(uuid4()),
                event_uuid=str(uuid4())
            )
            self.assertIsNone(EventFishModel.lookup_by_id(event.uuid))
            event.save_to_db()
            self.assertIsNotNone(EventFishModel.lookup_by_id(event.uuid))
            self.assertEqual(EventFishModel.lookup_by_id(event.uuid).stick_number, 3)

    def test_get_event_fish_by_user_id(self):
        event = EventFishModel(
            created_by=str(uuid4()),
            date_modified=dt.now(),
            modified_by=str(uuid4()),
            stick_number=3,
            fish_weight=43.03,
            usermanagement_uuid=str(uuid4()),
            event_uuid=str(uuid4())
        )
        self.assertIsNone(EventFishModel.lookup_by_usermanagement_id(event.usermanagement_uuid))
        event.save_to_db()
        self.assertIsNotNone(EventFishModel.lookup_by_usermanagement_id(event.usermanagement_uuid))
        self.assertEqual(EventFishModel.lookup_by_usermanagement_id(event.usermanagement_uuid).stick_number, 3)

    def test_get_event_fish_by_event_id(self):
        event = EventFishModel(
            created_by=str(uuid4()),
            date_modified=dt.now(),
            modified_by=str(uuid4()),
            stick_number=3,
            fish_weight=43.03,
            usermanagement_uuid=str(uuid4()),
            event_uuid=str(uuid4())
        )
        self.assertIsNone(EventFishModel.lookup_by_event_id(event.event_uuid))
        event.save_to_db()
        self.assertIsNotNone(EventFishModel.lookup_by_event_id(event.event_uuid))
        self.assertEqual(EventFishModel.lookup_by_event_id(event.event_uuid).stick_number, 3)