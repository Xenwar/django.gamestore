import unittest
from django.test import Client
from django.test import TestCase

class PageTest(unittest.TestCase):
	def test_highlevelpages(self):
		client = Client()
		response = client.get('/gamesite/',)
		self.assertEqual(response.status_code, 200, 'Testing landing page')
	def test_game_url(self):
		client = Client()
		response = client.get('/gamecenter/games/')
		self.assertEqual(response.status_code, 200,'Testing list of games')

		response = client.get('/gamecenter/game/1',)
		self.assertEqual(response.status_code, 200, 'Testing landing page')

		response = client.get("/gamecenter/game/-1")
		self.assertEqual(response.status_code, 404, "Testing that game -1 does not work")

class LoginTestCase(TestCase):
	def test_purchase(self):
		response = self.client.get('/gamecenter/purchase/game999')
		self.assertRedirects(response, '/accounts/login/?next=/gamecenter/purchase/game999')
	def test_edit(self):
		response = self.client.get('/gamecenter/updategame/game999')
		self.assertRedirects(response, '/accounts/login/?next=/gamecenter/updategame/game999')
	def test_delete(self):
		response = self.client.get('/gamecenter/deletegame/game999')
		self.assertRedirects(response, '/accounts/login/?next=/gamecenter/deletegame/game999')
	def test_play(self):
		response = self.client.get('/gamecenter/playgame/game999')
		self.assertRedirects(response, '/accounts/login/?next=/gamecenter/playgame/game999')

	#developers game requiires login
	def test_developerstats(self):
		response = self.client.get('/gamecenter/developergames/game999')
		self.assertRedirects(response, '/accounts/login/?next=/gamecenter/developergames/game999')

	#developers game requiires login
	def test_playersgames(self):
		response = self.client.get('/gamecenter/playergames/game999')
		self.assertRedirects(response, '/accounts/login/?next=/gamecenter/playergames/game999')
	#template test
	def test_templates(self):
		response = self.client.get('/gamecenter/games/')
		self.assertEquals(response.status_code, 200, "Testing for status code 200")
		self.assertTemplateUsed(response, 'gamecenter/game_list.html', "Testing that the correct template (webshop/product_view.html) was rendered")

		response = self.client.get('/gamecenter/game/1')
		self.assertEquals(response.status_code, 200, "Testing for status code 200")
		self.assertTemplateUsed(response, 'gamecenter/game_detail.html', "Testing that the correct template (webshop/product_view.html) was rendered")





#test api