import numpy
a = (['1 1 1'], ['1 1 1'], ['1 0 0'], ['0 1 0'], ['0 1 0'])

list_a = list(a)

list_a =numpy.array(list_a)
b = numpy.zeros((5,3),numpy.int)

for i in range(len(list_a)):
	b[i] = list_a[i][0].split(' ')
print (b)

for i in range(3):
	k = [example[i] for example in b]
	print k
