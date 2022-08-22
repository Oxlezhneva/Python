nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f'],
	[1, 2, None],
]

def flat_generator(nested_list):
    for el in nested_list:
        for item in el:
            yield  item    

for item in  flat_generator(nested_list):
	print(item)

