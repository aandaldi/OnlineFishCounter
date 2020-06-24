# from tests.base_tests import BaseTest
# from app.event.views import create_event, get_event_data, update_event_data, EventModel
# from datetime import datetime as dt
#
# class EventViewsTest(BaseTest):
#     def test_create_event(self):
#         pass
#
#     def test_get_event(self):
#         event = EventModel(
#             name='Launching',
#             created_by="admin",
#             date_modified=dt.now(),
#             modified_by="admin",
#             date=dt.strptime('2020-10-20 10:10:10', '%Y-%m-%d %H:%M:%S'),
#             max_stick=60
#         )
#
#         # event.save_to_db()
#
#         # print(get_event_data(EventModel.lookup("Launching").uuid), header=None)
#
#         pass