from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_user_with_token_no_admin
from custom_games.models import CustomGames
from users.models import User

class CustomGameGetViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, token = create_user_with_token()
        cls.access_token = str(token.access_token)
        cls.BASE_URL = "/api/custom_games/" 
        cls.BASE_URL_POST = "/api/custom_games/create/" 
        
    def test_list_all_custom_game_without_token(self):  
        custom_game_data = {
	        "name": "Horizon Forbidden West",
			"image_url":"https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/ki0STHGAkIF06Q4AU8Ow4OkV.png",
            "platform": "Epic Games"
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        added_custom_game = self.client.post(
            self.BASE_URL_POST, data=custom_game_data, format="json").json()

        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(f"{self.BASE_URL}{added_custom_game['id']}/")

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
        response = self.client.get(f"{self.BASE_URL}{added_custom_game['id']}/")

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

    def test_list_specific_custom_game_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        response = self.client.get(f"{self.BASE_URL}{self.user.id}/")

        with self.subTest():
            expected_status_code = status.HTTP_404_NOT_FOUND
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET "
                + f"em `{self.BASE_URL}{self.user.pk}/` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "Not found."}
        msg = "Verifique se a mensagem de jogo customizado não encotrando está correta"
        self.assertDictEqual(expected_data, returned_data, msg)