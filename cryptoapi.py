from requests import post
from time import sleep
from hashlib import md5 as md
import json

class CryptoAPI():

	def __init__(self, user_id, token):
		self.user_id = user_id
		self.token = str(token)
		self.old_response = False

	def crypto_post(self, method, data):
		urls = 'https://vk-crypto.space/api' + method
		response = post(urls,
			headers = {'Content-Type': 'application/json'},
			json = data)
		return response.json()

	def getUserCoins(self, user_id = None):
		if user_id:
			func_user = int(user_id)
		else:
			func_user = self.user_id
		response = CryptoAPI.crypto_post(self, method='/getUserCoins', data={'user_id': func_user, 'token': self.token})
		if not 'error' in response:
			return response['response']['coins']
		else:
			return response

	def getTransfers(self):
		return CryptoAPI.crypto_post(self, method='/getTransfers', data={'user_id': self.user_id, 'token': self.token})

	def transfer(self, toId, amount):
		toId = int(toId)

		if int(amount) >= 1:
			return CryptoAPI.crypto_post(self, method='/transfer', data={'recipient_id': toId, 'sender_id': self.user_id, 'token': self.token, 'amount': amount})
		else:
			print('amount cannot be less than 1')

	def connectServer(self, url=None):
		if url:
			if url.startswith(('https://', 'http://')):
				return CryptoAPI.crypto_post(self, method='/connectServer', data={'url': url, 'user_id': self.user_id, 'token': self.token})
			else:
				print('Url must start with https:// AND http://')
		else:
			print('Invalid url')

	def listen(self, interval=1):
		if interval >= 0.1:
			while True:
				try:
					response = CryptoAPI.crypto_post(self, method='/getTransfers', data={'user_id': self.user_id, 'token': self.token})[0]
					self.old_response = response if not self.old_response else self.old_response
					if response['recipient_id'] == self.user_id:
						if response != self.old_response:
							self.old_response = response
							yield response
				except Exception as e:
					print(e)
				sleep(interval)
		else:
			print('interval cannot be less then 0.1')

	def md5(self, create_date=None, sender_id=None, json=None):
		if json:
			create_date = json['object']['create_date']
			sender_id = json['object']['sender_id']
		if create_date:
			if sender_id:
				return (md(f"{create_date}@{sender_id}@{self.token}".encode())).hexdigest()
			else:
				print("Invalid parameter sender_id")
		else:
			print('Invalid parameter create_date')