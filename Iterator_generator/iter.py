nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f', 'h', False],
	[1, 2, None],
]

class FlatIterator:
    def __init__(self, my_list):
        self.my_list = my_list
 
    def __iter__(self):
        self.cursor = -1
        self.some_list = []
        for item in  self.my_list:
            for el in item:
                self.some_list.append(el)
        return self

    def __next__(self):
        self.cursor += 1
        if self.cursor == len(self.some_list):
            raise StopIteration
        return self.some_list[self.cursor]
        
for item in FlatIterator(nested_list):
    print(item)

flat_list = [item for item in FlatIterator(nested_list)]
print(flat_list)
    
