from auth.utils import account_activation_token
from users.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class TestUserApp(APITestCase):
    """
        TEST USER MODEL CLASS
    """
    
    @classmethod
    def setUpTestData(cls):
        """
            Set up test data in the database or others
        """
        test_super_user = User.objects.create_superuser(email="laurent.gina@oasis.com", username="Orangina", password="oasisisgood")
        test_user = User.objects.create_user(email="harry.covert@bomduel.com", username="Aricot", password="sicestboncestbomduel")
        test_user_1 = User.objects.create(email="test.user@bomduel.com", username="Whoao", password="sicestboncestbomduel")
        
    def test_model_user(self):
        """
            Test if new created user has a default permission and isn't confirmed
        """
        user = User.objects.get(id=2)

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.email_verified)

    def test_model_super_user(self):
        """
            test if user is super user
        """
        superuser = User.objects.get(id=1)
        user = User.objects.get(id=2)

        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        self.assertNotEqual(superuser.slug, user.slug)
        self.assertNotEqual(superuser.uuid, user.uuid)

    def test_add_user_with_dummy_email(self):
        """
            Test if user can be add without email field
        """
        with self.assertRaises(ValueError):
            email = "labodruche du 78"
            password = 'testpass1'
            username = 'mudi'

            user = User.objects.create_user(
                email=email,
                username = username,
                password = password,)

    def test_add_user_without_email(self):
        """
            Test if user can be add without email field
        """
        user = User.objects.create(username="mbrouk", password="heyman")
        self.assertEqual(user.email, '')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_str_return(self):
        """
            Test if user can be add without email field
        """
        user = User.objects.create_user(email="jeanyvelafesse@hotmail.com", username="mbrouk", password="heyman")
        self.assertIsInstance(user, User)
        self.assertEqual(user.__str__(), user.email)

    def test_user_has_perm(self):
        """
            Test if user can be add without email field
        """
        user = User.objects.create_user(email="jeanyvelafesse@hotmail.com", username="mbrouk", password="heyman")
        self.assertIsInstance(user, User)
        self.assertFalse(user.has_perm())

    def test_user_has_module_perm(self):
        """
            Test if user can be add without email field
        """
        user = User.objects.create_user(email="jeanyvelafesse@hotmail.com", username="mbrouk", password="heyman")
        self.assertIsInstance(user, User)
        self.assertTrue(user.has_module_perms())

    def test_login_endpoint(self):
        """
            Test login endpoint
        """
        context = {
            "email": "laurent.gina@oasis.com",
            "password": "oasisisgood"
        }

        response = self.client.post(reverse('api-login'), data=context, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_endpoint(self):
        """
            Create user through the API Endpoint
        """
        context = {
            "email": 'lapas.tech@oasis.com',
            'username': 'Pasteque',
            "password": 'oasisisgood',
        }
        response = self.client.post(reverse('api-register'), data=context)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_invalid_email_endpoint(self):
        """
            Test if user can be add without email field
        """
        context = {
            "email" : 'testpass1',
            "password" : 'testpass1',
            "username" : 'mudi'
        }

        response = self.client.post(reverse('api-register'), data=context)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_user_profile_endpoint(self):
        """
            Test profile access for authenticated users
        """
        context = {
            "email": 'laurent.gina@oasis.com',
            "password": 'oasisisgood'
        }
        response = self.client.post(reverse('api-login'), data=context, format='json')
        access_token = response.data['access'] if response.status_code == 200 else None

        if access_token is not None:
            auth_headers = {
                'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
            }
            profile_response = self.client.get(path=reverse('api-user-profile'), **auth_headers)
            self.assertEqual(profile_response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_profile_endpoint(self):
        """
            Test if unauthorized user can't access to profile endpoint
        """
        profile_response = self.client.get(path=reverse('api-user-profile'))
        self.assertEqual(profile_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_and_activate_account(self):
        """
            Test if user can activate account
        """
        context = {
            "email": 'lapas.tech@oasis.com',
            'username': 'Pasteque',
            "password": 'oasisisgood',
        }
        response = self.client.post(reverse('api-register'), data=context)

        user = User.objects.get(id=3)
        self.assertFalse(user.is_active)

        token = account_activation_token.make_token(user)

        activate_response = self.client.get(reverse('api-activate', kwargs={'uidb64': user.uuid, 'token': token}))
        self.assertEqual(activate_response.status_code, status.HTTP_202_ACCEPTED)
        
        updated_user = User.objects.get(id=3)
        self.assertTrue(updated_user.is_active)

    def test_forgot_password_endpoit(self):
        """
            Test forgot password API Endpoint
        """
        context = {
            "email":"laurent.gina@oasis.com"
        }
        response = self.client.post(reverse('api-forgot-password'), data=context)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_reset_password_endpoint(self):
        """
            test Reset password API Endpoint
        """
        user = User.objects.get(id=1)

        token = account_activation_token.make_token(user)

        context = {
            "password1" : "silaconfianceexistaitleaunecuiraitpaslepoisson",
            "password2" : "silaconfianceexistaitleaunecuiraitpaslepoisson"
        }

        response = self.client.post(reverse('api-confirm-reset-password', kwargs={'uidb64': user.uuid, 'token': token}), data=context)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_with_dumb_uuid_endpoint(self):
        """
            Test reset password with a wrong UUID API EndPoint
        """
        user = User.objects.get(id=1)

        token = account_activation_token.make_token(user)

        context = {
            "password1" : "silaconfianceexistaitleaunecuiraitpaslepoisson",
            "password2" : "cestcaquiestlaveriter"
        }

        response = self.client.post(reverse('api-confirm-reset-password', kwargs={'uidb64': user.uuid, 'token': token}), data=context)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_logout_endpoint(self):
        """
            Test logout API Endpoint
        """
        context = {
            "email": 'laurent.gina@oasis.com',
            "password": 'oasisisgood'
        }
        response = self.client.post(reverse('api-login'), data=context, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access'] if response.status_code == 200 else None
        refresh_token = response.data['refresh'] if response.status_code == 200 else None
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
        }
        context = {
            "refresh_token": refresh_token
        }
        logout_response = self.client.post(reverse('api-blacklist'), data=context, **auth_headers)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)


