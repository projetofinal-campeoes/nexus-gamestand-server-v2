from rest_framework.test import APITestCase
from rest_framework.views import status

from tests.factories import create_user_with_token, create_user_with_token_no_admin
from friends.models import Friend


class FriendViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, token = create_user_with_token()
        cls.access_token = str(token.access_token)

        cls.user, token_no_admin = create_user_with_token_no_admin()
        cls.access_token_no_admin = str(token_no_admin.access_token)

        cls.BASE_URL = "/api/friends/"

        cls.maxDiff = None

    def test_add_friend_without_token(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem token "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_add_friend_own_user(self):
        friend_data = {
            "username": "nexus_teste",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL, data=friend_data, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_400_BAD_REQUEST
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Not able to add own account."}
        msg = "Verifique se a mensagem de adicão do próprio usuário está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_add_friend_invalid_user(self):
        friend_data = {
            "username": "testError",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL, data=friend_data, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_404_NOT_FOUND
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "User not found."}
        msg = "Verifique se a mensagem de adição do usuário inválido está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_add_friend_success(self):
        friend_data = {
            "username": "nexus_teste_no_admin",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL, data=friend_data, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_201_CREATED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_keys = set(response.json().keys())
        expected_keys = {"id", "friend_id", "friend_name", "user_id"}
        msg = "Verifique se o body está sendo retornado corretamente"
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_list_friends_of_logged_user_without_token(self):
        response = self.client.get(self.BASE_URL)

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET sem token "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_list_friends_of_logged_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get(self.BASE_URL)

        with self.subTest():
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        msg = "Verifique se os amigos do usuário logado estão sendo retornadas corretamente"
        self.assertEqual(len(returned_data), 0, msg)

    def test_list_especific_friend_without_token(self):
        friend_data = {
            "username": "nexus_teste_no_admin",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_friend = self.client.post(
            self.BASE_URL, data=friend_data, format="json"
        ).json()

        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(f"{self.BASE_URL}{added_friend['friend_id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET sem token "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_list_especifc_friend_with_invalid_user_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get(f"{self.BASE_URL}{self.user.id}/")

        with self.subTest():
            expected_status_code = status.HTTP_404_NOT_FOUND
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "This user is not added."}
        msg = "Verifique se a mensagem de usuário inválido está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_list_especifc_friend_success(self):
        friend_data = {"username": "nexus_teste_no_admin"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_friend = self.client.post(
            self.BASE_URL, data=friend_data, format="json"
        ).json()

        response = self.client.get(f"{self.BASE_URL}{added_friend['friend_id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_keys = set(response.json().keys())
        expected_keys = {"id", "friend_id", "friend_name", "user_id"}
        msg = "Verifique se o body está sendo retornado corretamente"
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_delete_especific_friend_without_token(self):
        friend_data = {
            "username": "nexus_teste_no_admin",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_friend = self.client.post(
            self.BASE_URL, data=friend_data, format="json"
        ).json()

        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.delete(f"{self.BASE_URL}{added_friend['friend_id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE sem token "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_delete_especific_friend_with_invalid_user_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.delete(f"{self.BASE_URL}{self.user.id}/")

        with self.subTest():
            expected_status_code = status.HTTP_404_NOT_FOUND
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "User not Found."}
        msg = "Verifique se a mensagem usuário inválido está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_delete_especific_friend_success(self):
        friend_data = {
            "username": "nexus_teste_no_admin",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_friend = self.client.post(
            self.BASE_URL, data=friend_data, format="json"
        ).json()

        response = self.client.delete(f"{self.BASE_URL}{added_friend['friend_id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_204_NO_CONTENT
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)
