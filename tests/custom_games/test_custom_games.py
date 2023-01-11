from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_user_with_token_no_admin
from custom_games.models import CustomGames
from users.models import User

class CustomGameViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, token_no_admin = create_user_with_token_no_admin()
        cls.access_token_no_admin = str(token_no_admin.access_token)

        cls.user_2, token = create_user_with_token()
        cls.access_token = str(token.access_token)

        cls.BASE_URL_GET_PTCH_DEL = "/api/custom_games/" 
        cls.BASE_URL_POST = "/api/custom_games/create/" 

    def test_list_all_custom_games_without_token(self):  
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/")


        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET sem token "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_list_all_custom_games_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get(self.BASE_URL_GET_PTCH_DEL)

        with self.subTest():
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        msg = "Verifique se os jogos customizados estão sendo retornados corretamente"
        self.assertEqual(len(returned_data), 0, msg)

    def test_list_specific_custom_game_without_token(self):  
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET sem token "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_list_specific_custom_game_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        response = self.client.get(f"{self.BASE_URL_GET_PTCH_DEL}{self.user.id}/")

        with self.subTest():
            expected_status_code = status.HTTP_404_NOT_FOUND
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{self.user.id}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Not found."}
        msg = "Verifique se a mensagem de jogo customizado não encotrando está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_list_specific_custom_game_success(self):
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        response = self.client.get(f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_keys = set(response.json().keys())
        expected_keys = {"id", "name", "image_url", "platform", "user_id"}
        msg = "Verifique se o body está sendo retornado corretamente"
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_create_custom_game_without_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer ")
        response = self.client.post(self.BASE_URL_POST, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem token "
                + f"em `{self.BASE_URL_POST}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authorization header must contain two space-delimited values","code": "bad_authorization_header"}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)
        
    def test_create_custom_game_without_required_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL_POST, data={}, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_400_BAD_REQUEST
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL_POST}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {
	            "name": [
		            "This field is required."
	        ],
	            "image_url": [
		            "This field is required."
	        ],
	            "platform": [
		            "This field is required."
	        ]
        }
        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar o jogo customizado"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_create_custom_game_successfully(self):
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL_POST, data=custom_game_data, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_201_CREATED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL_POST}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_keys = set(response.json().keys())
        expected_keys = {"id", "name", "image_url", "platform", "user_id"}
        msg = "Verifique se o body está sendo retornado corretamente"
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_create_custom_game_with_existing_name_and_platform(self):
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL_POST, data=custom_game_data, format="json")
        response = self.client.post(self.BASE_URL_POST, data=custom_game_data, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_400_BAD_REQUEST
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL_POST}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"non_field_errors": [
		        "The fields name, platform must make a unique set."
	    ]}
        msg = "Verifique se a mensagem de criação do jogo customizado está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_update_custom_game_without_token(self):  
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.patch(f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do PATCH sem token "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_update_custom_game_without_admin(self):
        custom_game_data1 = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game1 = self.client.post(
            self.BASE_URL_POST, data=custom_game_data1, format="json").json()

        custom_game_data2 = {
	        "name": "God of War Ragnarök",
            "image_url": "https://image.api.playstation.com/vulcan/ap/rnd/202207/1210/4xJ8XB3bi888QTLZYdl7Oi0s.png",
            "platform": "Epic Games",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_no_admin)
        added_custom_game2 = self.client.post(
            self.BASE_URL_POST, data=custom_game_data2, format="json").json()

        response = self.client.patch(
            f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game1['id']}/", format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH "
            + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game1['id']}/` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do PATCH em `{self.BASE_URL_GET_PTCH_DEL}{self.user.pk}/` está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_update_custom_game_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        response = self.client.patch(f"{self.BASE_URL_GET_PTCH_DEL}{self.user.id}/")

        with self.subTest():
            expected_status_code = status.HTTP_404_NOT_FOUND
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do PATCH "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{self.user.id}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Not found."}
        msg = "Verifique se a mensagem de jogo customizado não encotrando está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_update_custom_game_success(self):
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        response = self.client.patch(f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do PATCH "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_keys = set(response.json().keys())
        expected_keys = {"id", "name", "image_url", "platform", "user_id"}
        msg = "Verifique se o body está sendo retornado corretamente"
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_delete_custom_game_without_token(self):  
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.delete(f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE sem token "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Authentication credentials were not provided."}
        msg = "Verifique se a mensagem de credenciais inválidas está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_delete_custom_game_without_admin(self):
        custom_game_data1 = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game1 = self.client.post(
            self.BASE_URL_POST, data=custom_game_data1, format="json").json()

        custom_game_data2 = {
	        "name": "God of War Ragnarök",
            "image_url": "https://image.api.playstation.com/vulcan/ap/rnd/202207/1210/4xJ8XB3bi888QTLZYdl7Oi0s.png",
            "platform": "Epic Games",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_no_admin)
        added_custom_game2 = self.client.post(
            self.BASE_URL_POST, data=custom_game_data2, format="json").json()

        response = self.client.delete(
            f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game1['id']}/", format="json"
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE "
            + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game1['id']}/` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do DELETE em `{self.BASE_URL_GET_PTCH_DEL}{self.user.pk}/` está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_delete_custom_game_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        response = self.client.delete(f"{self.BASE_URL_GET_PTCH_DEL}{self.user.id}/")

        with self.subTest():
            expected_status_code = status.HTTP_404_NOT_FOUND
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{self.user.id}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Not found."}
        msg = "Verifique se a mensagem de jogo customizado não encotrando está correta"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_delete_custom_game_success(self):
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        response = self.client.delete(f"{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/")

        with self.subTest():
            expected_status_code = status.HTTP_204_NO_CONTENT
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE "
                + f"em `{self.BASE_URL_GET_PTCH_DEL}{added_custom_game['id']}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)