from tests.base_tests import BaseTest, TestInsertAdmin
import time


class SystemTestAuth(BaseTest):
    def test_login_and_create_session_with_valid_user(self):
        with self.app_context:
            TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                request = client.post('/admins/login',
                                      json={
                                          'username': 'admin',
                                          'password': 'admin'
                                      })

                response = request.get_json()
                self.assertEqual(request.status_code, 200)
                self.assertIsNotNone(response.get('access_token'))
                self.assertEqual(response.get('message'), "login has success")

    def test_login_with_invalid_user(self):
        with self.app_context:
            TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                request = client.post('/admins/login',
                                      json={
                                          'username': 'not admin',
                                          'password': 'admin'
                                      })

                response = request.get_json()
                self.assertEqual(request.status_code, 401)
                self.assertEqual(response.get('message'), "Could not find the requested user")
                self.assertEqual(response.get('error'), "MissingUserError")

    def test_logout(self):
        with self.app_context:
            TestInsertAdmin.insert_admin()
            with self.app.test_client() as client:
                login = client.post('/admins/login',
                                    json={
                                        'username': 'admin',
                                        'password': 'admin'
                                    })

                response_login = login.get_json()

                request = client.post('/logout',
                                      headers={'Authorization': 'Bearer {}'.format(response_login.get('access_token'))}
                                      )

                print(request.data)


    # def test_refresh_token(self):
    #     TestInsertAdmin.insert_admin()
    #     with self.app.test_client() as client:
    #         print(self.app.config['JWT_ACCESS_LIFESPAN'])
    #
    #         login = client.post('/admins/login',
    #                             json={
    #                                 'username': 'admin',
    #                                 'password': 'admin'
    #                             })
    #         print(self.app.config['SECRET_KEY'])
    #         response = login.get_json()
    #
    #         time.sleep(3)
    #         request = client.post('/refresh/token',
    #                               headers={'Authorization': 'Bearer {}'.format(response.get('access_token'))}
    #                               )
    #
    #         print("ini responnya /n", request.data)
