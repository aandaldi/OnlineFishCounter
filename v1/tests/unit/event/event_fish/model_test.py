from tests.base_tests import BaseTest
from app.event.event_fish.models import EventFishModel
from datetime import datetime as dt
from uuid import uuid4


class TestEventFishModel(BaseTest):
    def test_create_event_fish(self):
        event = EventFishModel(
            created_by=str(uuid4()),
            date_modified=dt.now(),
            modified_by=str(uuid4()),
            stick_number=3,
            fish_weight=43.03,
            usermanagement_uuid=str(uuid4()),
            event_uuid=str(uuid4())
        )

        self.assertEqual(event.stick_number, 3)
        self.assertEqual(event.fish_weight, 43.03)
        self.assertIsInstance(event, EventFishModel)

