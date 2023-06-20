# Point #
class Point:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __str__(self):
		return '(' + str(self.x) + ':' + str(self.y) + ')'

	def __eq__(self, p):
		res = False
		res = (self.x == p.x) and (self.y == p.y)
		return res
