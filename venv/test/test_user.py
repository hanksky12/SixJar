from flask import url_for

from setting_base import SettingBase


class UserTest(SettingBase):
    #api測試
    def test_login(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.__check_cookie_is_set(response)

    def __check_cookie_is_set(self,response):
        cookie_list = ['access_token_cookie',
                       'csrf_access_token',
                       'refresh_token_cookie',
                       'csrf_refresh_token',
                       'user_id',
                       'session']
        check_cookie_list = cookie_list.copy() #自己在迴圈內移除自己，會有問題
        response_cookie_list = response.headers.get_all('Set-Cookie')
        for cookie_name in cookie_list:
            for cookie in response_cookie_list:
                # print(f"檢查{cookie[:8]}")
                if cookie_name in cookie:
                    check_cookie_list.remove(cookie_name)
        self.assertEqual(check_cookie_list, [])

    def test_logout(self):
        response = self.client.get(url_for('api.userlogoutapi'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(url_for('api.userpostapi'),
                                    json={
                                        "name": "test2",
                                        "email": "test2@gmail.com",
                                        "password": "test2",
                                        "password2": "test2"
                                    }
                                    )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], '成功新增')


    def test_check_repeat_register(self):
        response = self.client.post(url_for('api.userpostapi'),
                                    json={
                                        "name": self.user_name,
                                        "email": self.user_email,
                                        "password": self.user_password,
                                        "password2": self.user_password}
                                    )

        data = response.json['messages']['json']['email'][0]
        self.assertEqual(data, 'Mail已被註冊')

    def test_get_info(self):
        csrf_access_token = self.get_csrf_access_token()
        response = self.client.get(url_for('api.userapi', user_id=1),
                                   headers={"X-CSRF-TOKEN": csrf_access_token})
        # print(response.json)
        data = response.json['data']
        self.assertEqual(data["email"], self.user_email)
        self.assertEqual(data["name"], self.user_name)

    def test_wrong_user_id_get_info(self):
        csrf_access_token = self.get_csrf_access_token()
        response = self.client.get(url_for('api.userapi', user_id=2),
                                   headers={"X-CSRF-TOKEN": csrf_access_token})
        # print(response.json['code'])
        self.assertEqual(response.json['code'], 400)

    def test_update_info(self):
        update_user_name = "update_user"
        update_user_password = "update_password"
        csrf_access_token = self.get_csrf_access_token()
        response = self.client.put(url_for('api.userapi', user_id=1),
                                   headers={"X-CSRF-TOKEN": csrf_access_token},
                                   json={
                                       "name": update_user_name,
                                       "password": update_user_password,
                                       "password2": update_user_password
                                   }
                                   )
        print(response.json)
        #
        data = response.json['data']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], update_user_name)
        self.assertEqual(data["password"], update_user_password)
        self.assertEqual(data["password2"], update_user_password)
