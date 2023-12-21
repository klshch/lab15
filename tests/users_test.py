from flask import url_for

from flask_login import current_user, login_user
from .base import BaseTestCase

from app.users.models import User

class UserTest(BaseTestCase):
    '''Тест чи відображається реєстраційна сторінка'''
    def test_register(self):
        with self.client:

            response = self.client.get(url_for('users.register'))

            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Register page', response.data)
            self.assertIn(b'Username', response.data)
            self.assertIn(b'Email', response.data)
            self.assertIn(b'Password', response.data)
            self.assertIn(b'Confirm password', response.data)
            self.assertIn(b'Register', response.data)

    '''Тест чи коректно працює реєстрація при правильних даних'''
    def test_registrarion_correct(self):
        with self.client:

            response = self.client.post(url_for('users.register'),
                                        data=dict(username='test', email='test@gmail.com', password='password', confirm_password='password'),
                                        follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Account successfully created', response.data)

        user = User.query.filter_by(email='test@gmail.com').first()
        self.assertIsNotNone(user)


    '''Тест чи коректно працює реєстрація при неправильних даних'''
    def test_registrarion_incorrect(self):
        with self.client:

            response = self.client.post(url_for('users.register'),
                                        data=dict(username='test+', email='testgmail.com', password='password', confirm_password='password1'),
                                        follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Username must have only letters, numbers, dots, or underscores', response.data)
            self.assertIn(b'Invalid email.', response.data)
            self.assertIn(b'Passwords must match.', response.data)


    '''Тест чи відображається сторінка з входом в аккаунт'''
    def test_log(self):
        with self.client:

            response = self.client.get(url_for('users.login'))

            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Login page', response.data)
            self.assertIn(b'Email', response.data)
            self.assertIn(b'Password', response.data)
            self.assertIn(b'Remember me', response.data)
            self.assertIn(b'Login', response.data)


    '''Тест чи коректно працює логін з правильною інформацією'''
    def test_login_correct(self):
        with self.client:

            response = self.client.post(url_for('users.login'),
                                        data=dict(email='user@gmail.com', password='password'),
                                        follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'You have been logged in!', response.data)

            self.assertTrue(current_user.is_authenticated)

    
    '''Тест чи коректно працює логін з неправильною інформацією'''
    def test_login_incorrect(self):
        with self.client:

            response = self.client.post(url_for('users.login'),
                                        data=dict(email='user', password='pass word'),
                                        follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Invalid email.', response.data)

            self.assertFalse(current_user.is_authenticated)


    '''Тест чи коректно працює вихід з аккаунта'''
    def test_logout(self):

        login_user(User.query.filter_by(id=1).first())
                
        response = self.client.get(url_for('users.logout'), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        self.assertIn(b'You have been logged out', response.data)

        self.assertFalse(current_user.is_authenticated)

    
    '''Тест чи відбувається оновлення інформації про користувача'''
    def test_update(self):
    
        login_user(User.query.filter_by(id=1).first())

        with self.client:
            response = self.client.post(url_for('users.account'),
                                        data=dict(username='USER', email='user1@gmail.com', about_me=":)"),
                                        follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Your account has been updated', response.data)

            self.assertEqual(current_user.username, 'USER')
            self.assertEqual(current_user.about_me, ':)')
    

    '''Тест чи відображається сторінка з інформацією користувачів'''
    def test_users(self):

        response = self.client.get(url_for('users.userslist'))

        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Users page', response.data)
        self.assertIn(b'Number of users:', response.data)