from tests.base_tests import BaseTest, TestInsertAdmin
from datetime import datetime as dt


class EventFishTests(BaseTest):
    def insert_admin_user_and_event(self):
        """ run when need insert admin, user and event"""
        with self.app_context:
            TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                login = client.post('/login', json={'username': 'admin', 'password': 'admin'})
                token = login.get_json().get('access_token')
                headers = {'Authorization': 'Bearer {}'.format(token)}

                create_event = client.post('/events', headers=headers,
                                           json={
                                               "name": "Launching",
                                               "date": "2020-10-10 20:20:20",
                                               "max_stick": 30
                                           })

                register_user = client.post('/users', headers=headers,
                                            json={
                                                "username": "siapa",
                                                "password": "siapasih",
                                                "roles": "admin",
                                            })

                event_id = create_event.get_json().get('event').get('uuid')
                user_id = register_user.get_json().get('usermanagement').get('uuid')
                return dict(headers=headers, event_id=event_id, user_id=user_id)

    def test_create_event_fish(self):
        with self.app_context:
            # TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                insert = EventFishTests.insert_admin_user_and_event(self)
                request = client.post('/events/{}/customers/{}'.format(insert.get('event_id'), insert.get('user_id')),
                                      headers=insert.get('headers'),
                                      json={
                                          "stick_number": "32",
                                          "fish_weight": 34.09
                                      })
                response = request.get_json()
                self.assertEqual(request.status_code, 201)
                self.assertEqual(response.get('message'), "success add new event fish obtained by user")
                self.assertEqual(response.get('event_fish').get('usermanagement_uuid'), insert.get('user_id'))
                self.assertEqual(response.get('event_fish').get('stick_number'), 32)
                self.assertEqual(response.get('event_fish').get('fish_weight'), 34.09)

    def test_get_event_fish_by_id(self):
        with self.app_context:
            with self.app.test_client() as client:
                insert = self.insert_admin_user_and_event()
                insert_event_fish = client.post(
                    '/events/{}/customers/{}'.format(insert.get('event_id'), insert.get('user_id')),
                    headers=insert.get('headers'),
                    json={
                        "stick_number": "32",
                        "fish_weight": 34.09
                    })
                event_fish_id = insert_event_fish.get_json().get('event_fish').get('uuid')

                request = client.get(
                    '/events/{}/customers/{}/{}'.format(insert.get('event_id'), insert.get('user_id'), event_fish_id),
                    headers=insert.get('headers'))

                response = request.get_json()
                self.assertEqual(request.status_code, 200)
                self.assertEqual(response.get('message'),
                                 "success get event fish obtained by user {} on {} event".format(insert.get('user_id'),
                                                                                                 insert.get(
                                                                                                     'event_id')))
                self.assertEqual(response.get('event_fish').get('usermanagement_uuid'), insert.get('user_id'))
                self.assertEqual(response.get('event_fish').get('stick_number'), 32)
                self.assertEqual(response.get('event_fish').get('fish_weight'), 34.09)

    def test_update_event_fish_obtained_by_user(self):
        with self.app_context:
            with self.app.test_client() as client:
                insert = self.insert_admin_user_and_event()
                insert_event_fish = client.post(
                    '/events/{}/customers/{}'.format(insert.get('event_id'), insert.get('user_id')),
                    headers=insert.get('headers'),
                    json={
                        "stick_number": "32",
                        "fish_weight": 34.09
                    })

                event_fish_id = insert_event_fish.get_json().get('event_fish').get('uuid')

                request = client.patch(
                    '/events/{}/customers/{}/{}'.format(insert.get('event_id'), insert.get('user_id'), event_fish_id),
                    headers=insert.get('headers'),
                    json={
                        "stick_number": "32",
                        "fish_weight": 34.04
                    })

                response = request.get_json()
                self.assertEqual(request.status_code, 200)
                self.assertEqual(response.get('event_fish').get('usermanagement_uuid'), insert.get('user_id'))
                self.assertEqual(response.get('event_fish').get('stick_number'), 32)
                self.assertEqual(response.get('event_fish').get('fish_weight'), 34.04)
