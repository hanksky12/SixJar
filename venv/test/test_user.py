
from flask import url_for

from setting_base import SettingBase

class UserTest(SettingBase):
    def test_login(self):
        response = self.client.post(url_for('api.userloginapi'),
                                    use_cookies=True,
                                    json={
                                        "email": self.user_email,
                                        "password": self.user_password,
                                        "remember_me": True
                                    })

        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_info(self):
        response = self.client.get(url_for('api.userapi', user_id=1),
                                   headers={"X-CSRF-TOKEN": "1"},
                                   use_cookies=True
                                   )

        print(response)
        print(response.json)
        self.assertEqual(response.status_code, 200)


