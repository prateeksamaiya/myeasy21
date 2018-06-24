import sys
import numpy as np

def initial():
		return np.random.random_integers(1,10)

class state():
	def __init__(self,dealer_first = initial() ,sum_player = initial()):
		self.dealer_first = sum_player
		self.sum_player = sum_player

	


class environment():

	def step(self,s,a):
		if a == "hit":
			s.sum_player += self.hit()
			if s.sum_player < 1 or s.sum_player >21:
				return "terminal",-1
			else:
				return s,0
		else:
			while s.dealer_first < 17 :
				s.dealer_first += self.hit()
			if s.dealer_first<1 or s.dealer_first >21:
				return "terminal",1
			if s.dealer_first == s.sum_player:
				return "terminal",0
			elif s.dealer_first > s.sum_player:
				return "terminal",-1
			else:
				return "terminal",1

	
		# self.sum_player = np.random.random_integers(1,10)

	def hit(self):
		a = np.random.random_integers(-10,0)
		b = np.random.random_integers(1,10)
		arr = [a,b]
		return np.random.choice(arr,p=[1/3,2/3],replace = True)

envir = environment()
s = state()



envir.step(s,"hit")
envir.step(s,"hit")
envir.step(s,"hit")
print(s.sum_player)
print(s.dealer_first)
print(envir.step(s,"stick"))
