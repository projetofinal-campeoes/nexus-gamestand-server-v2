from rest_framework.test import APITestCase
from rest_framework.views import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from tests.factories import create_user_with_token, create_user_with_token_no_admin

User: AbstractUser = get_user_model()


class UserCreationViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/"

        cls.user, token_no_admin = create_user_with_token_no_admin()
        cls.access_token_no_admin = str(token_no_admin.access_token)

        cls.user_2, token = create_user_with_token()
        cls.access_token = str(token.access_token)

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_user_creation(self):
        user_data = {
            "username": "marchi",
            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFrCAT0yddSLR1q64m5s2bLUkMgFUaFamivJ5E3pUVWX_AY6fOgfJHyDP9haXSHB5WgjE&usqp=CAU",
            "email": "kenzie@kenzie.com",
            "password": "bergamota",
            "status": True,
            "steam_user": "yMarKxy",
            "gamepass": True,
        }

        response = self.client.post(self.BASE_URL, data=user_data, format="json")

        added_user = User.objects.last()
        # # RETORNO JSON
        returned_keys = set(response.json().keys())

        expected_keys = {
            "id",
            "username",
            "avatar_url",
            "email",
            "status",
            "steam_user",
            "gamepass",
        }

        msg = (
            "Verifique se as informações do usuário retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertSetEqual(expected_keys, returned_keys, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_user_creation_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        # RETORNO JSON
        resulted_data: dict = response.json()
        expected_data = {
            "email": ["This field is required."],
            "password": ["This field is required."],
            "steam_user": ["This field is required."],
            "username": ["This field is required."],
        }
        msg = "\nVerifique as chaves obrigatórias ao tentar criar um usuário."
        self.assertDictEqual(expected_data, resulted_data, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
            + f"em `{self.BASE_URL}` é {expected_status_code}."
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_non_unique_username_or_email_user_creation(self):
        user_data = {
            "username": "marchi",
            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFrCAT0yddSLR1q64m5s2bLUkMgFUaFamivJ5E3pUVWX_AY6fOgfJHyDP9haXSHB5WgjE&usqp=CAU",
            "email": "kenzie@kenzie.com",
            "password": "bergamota",
            "status": True,
            "steam_user": "yMarKxy",
            "gamepass": True,
        }

        # Populando o banco pré testagem
        User.objects.create_superuser(**user_data)
        response = self.client.post(self.BASE_URL, data=user_data, format="json")

        # RETORNO JSON
        resulted_data = response.json()
        expected_fields = {"username", "email"}
        resulted_fields = set(resulted_data.keys())
        msg = (
            "Verifique se as informações do usuário retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertSetEqual(expected_fields, resulted_fields, msg)

        # ERROR MESSAGES
        resulted_username_message = resulted_data["username"][0]
        resulted_email_message = resulted_data["email"][0]

        expected_username_message = "A user with that username already exists."
        expected_email_message = "This field must be unique."

        msg = (
            "Verifique a mensagem de erro quando criando usuário com username repetido"
        )
        self.assertEqual(expected_username_message, resulted_username_message, msg)

        msg = "Verifique a mensagem de erro quando criando usuário com email repetido"
        self.assertEqual(expected_email_message, resulted_email_message, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_retrieve_users(self):
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = [
            {
                "id": str(self.user.pk),
                "username": "nexus_teste_no_admin",
                "email": "nexus_teste_no_admin@nexus.com",
                "avatar_url": "",
                "status": True,
                "steam_user": "",
                "gamepass": False,
            },
            {
                "id": str(self.user_2.pk),
                "username": "nexus_teste",
                "email": "nexus_teste@nexus.com",
                "avatar_url": "",
                "status": True,
                "steam_user": "",
                "gamepass": False,
            },
        ]

        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertEqual(expected_data, resulted_data, msg)

    def test_update_user_with_correct_user_token(self):
        info_to_patch = {
            "username": "marchi",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.patch(
            f"{self.BASE_URL}{self.user.pk}/", data=info_to_patch, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token correto "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": str(self.user.pk),
            "username": "marchi",
            "email": "nexus_teste_no_admin@nexus.com",
            "avatar_url": "",
            "status": True,
            "steam_user": "",
            "gamepass": False,
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token correto em "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_user_without_token(self):
        response = self.client.patch(f"{self.BASE_URL}{self.user.pk}/", format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_user_with_correct_user_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_no_admin
        )
        response = self.client.delete(f"{self.BASE_URL}{self.user.pk}/", format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_delete_user_without_token(self):
        response = self.client.delete(f"{self.BASE_URL}{self.user.pk}/", format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_another_user_without_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_no_admin
        )
        response = self.client.delete(
            f"{self.BASE_URL}{self.user_2.pk}/", format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token correto "
            + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do DELETE em `{self.BASE_URL}{self.user.pk}/` está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)
