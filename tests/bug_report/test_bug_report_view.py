from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_user_with_token_no_admin


class BugReportViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, token = create_user_with_token()
        cls.access_token = str(token.access_token)

        cls.user, token_no_admin = create_user_with_token_no_admin()
        cls.access_token_no_admin = str(token_no_admin.access_token)

        cls.BASE_URL = f"/api/bug_report/"

        cls.maxDiff = None

    def test_create_bug_report_without_required_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL, data={}, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_400_BAD_REQUEST
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_fields = {
            "description",
        }
        returned_fields = set(returned_data.keys())
        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar um bug report sem dados"
        self.assertSetEqual(expected_fields, returned_fields, msg)

    def test_create_bug_report_without_token(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem token "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_create_bug_report(self):
        bug_report_data = {
            "page": "Login",
            "description":"A página de login está com um bug, onde demora muito a logar."
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL, data=bug_report_data, format="json")
        resulted_data = response.json()

        resulted_keys = set(resulted_data.keys())
        expected_keys = {"id", "page", "description", "created_at", "user_id"}
        msg = "Verifique se as chaves estão sendo retornadas corretamente"
        self.assertSetEqual(expected_keys, resulted_keys, msg)

    def test_list_bug_report_without_token(self):
        response = self.client.get(self.BASE_URL)

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET sem token "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)
    
    def test_list_bug_report_user_not_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_no_admin)
        response = self.client.get(self.BASE_URL)

        with self.subTest():
            expected_status_code = status.HTTP_403_FORBIDDEN
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do GET sem usuário ser admin "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_list_bug_report(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get(self.BASE_URL)
        resulted_data = response.json()
        
        msg = "Verifique se as bug report estão sendo retornadas corretamente"
        self.assertEqual(len(resulted_data), 0, msg)

    def test_delete_bug_report_without_token(self):
        response = self.client.delete(self.BASE_URL)

        with self.subTest():
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE sem token "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)
    
    def test_delete_bug_report_user_not_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_no_admin)
        response = self.client.delete(self.BASE_URL)

        with self.subTest():
            expected_status_code = status.HTTP_403_FORBIDDEN
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE sem usuário ser admin "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_delete_bug_report(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get(self.BASE_URL)

        with self.subTest():
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do DELETE "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)