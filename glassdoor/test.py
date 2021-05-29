def test(n):
	if n >= 10:
		print(n)
	else:
		raise Exception("Less than 10")

test(10)