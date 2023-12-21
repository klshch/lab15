from flask import url_for
from .base import BaseTestCase

class PortfolioTest(BaseTestCase):
    '''Тест чи відображається головна сторінка, та текст "Вітаю!"'''
    def test_home(self):
        response = self.client.get(url_for('portfolio.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вітаю!'.encode('utf-8'), response.data)

    '''Тест чи відображається сторінка з інформацією про володіння JavaScript, та текст "JavaScript"'''
    def test_page1(self):
        response = self.client.get(url_for('portfolio.page1'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'JavaScript', response.data)

    '''Тест чи відображається сторінка з інформацією про володіння HTML, та текст "HTML"'''
    def test_page2(self):
        response = self.client.get(url_for('portfolio.page2'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HTML', response.data)

    '''Тест чи відображається сторінка з інформацією про навички, та деякий текст'''
    def test_page3(self):
        response = self.client.get(url_for('portfolio.page3'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Skills page', response.data)
        self.assertIn(b'All Skills', response.data)
        self.assertIn(b'Total Skills', response.data)