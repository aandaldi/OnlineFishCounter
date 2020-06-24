from tests.base_tests import BaseTest, TestInsertAdmin


class TestEvent(BaseTest):
    def test_create_event(self):
        with self.app_context:
            TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                login = client.post('/admins/login', json={'username': 'admin', 'password': 'admin'})
                token = login.get_json().get('access_token')
                request = client.post('/events/',
                                      json={
                                          "name": "Launching",
                                          "date": "2020-10-10 20:20:20",
                                          "max_stick": 30
                                      },
                                      headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.get_json().get('message'), "success add new event")

    def test_create_event_with_duplicate_name(self):
        with self.app_context:
            TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                login = client.post('/admins/login', json={'username': 'admin', 'password': 'admin'})
                token = login.get_json().get('access_token')
                event = client.post('/events/',
                                    json={
                                        "name": "Launching",
                                        "date": "2020-10-10 20:20:20",
                                        "max_stick": 30
                                    },
                                    headers={'Authorization': 'Bearer {}'.format(token)})
                self.assertEqual(event.status_code, 201)

                request = client.post('/events/',
                                      json={
                                          "name": "Launching",
                                          "date": "2020-10-21 20:20:20",
                                          "max_stick": 30
                                      },
                                      headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.get_json().get('message'), "event already exists")

    def test_get_event(self):
        with self.app_context:
            TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                login = client.post('/admins/login', json={'username': 'admin', 'password': 'admin'})
                token = login.get_json().get('access_token')
                post_event = client.post('/events/',
                                      json={
                                          "name": "Launching",
                                          "date": "2020-10-10 20:20:20",
                                          "max_stick": 30
                                      },
                                      headers={'Authorization': 'Bearer {}'.format(token)})

                eventId = post_event.get_json().get('event').get('uuid')

                request = client.get('/events/{}'.format(eventId),
                                      headers={'Authorization': 'Bearer {}'.format(token)})

                self.assertEqual(request.status_code, 200)
                self.assertEqual(request.get_json().get('message'), "success get event data")
                self.assertEqual(request.get_json().get('event').get('uuid'), eventId)