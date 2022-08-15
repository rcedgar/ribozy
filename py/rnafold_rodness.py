#!/usr/bin/python3

import sys

# Input is .fold file from RNAfold, format is fasta-like with
# sequence label followed by sequence followed by one or more lines
# of ss in ((.)) format.

FileName = sys.argv[1]

def SetPairs():
	global L, Pairs, ItoJ, Parens

	Pairs = []
	L = len(Parens)
	Stack = []
	for i in range(0, L):
		c = Parens[i]
		if c == '(':
			Stack.append(i)
		elif c == ')':
			i2 = Stack.pop()
			Pair = (i2, i)
			Pairs.append(Pair)
	assert len(Stack) == 0

def GetDist12(i, j):
	global L, Pairs, ItoJ, Parens

	assert i < j
	d1 = j - i
	assert d1 >= 0 and d1 < L

	d2 = L + i - j
	assert d2 >= 0 and d2 < L

	return min(d1, d2)

def GetDist(i, j):
	global L, Pairs, ItoJ, Parens

	if i < j:
		return GetDist12(i, j)
	elif i > j:
		return GetDist12(j, i)
	else:
		return 0

def SetItoJ():
	global L, Pairs, ItoJ

	ItoJ = [ None ] * (L+1)

	for Pair in Pairs:
		i, j = Pair
		assert i <= L and j <= L
		if ItoJ[i] == None:
			ItoJ[i] = j
		else:
			assert ItoJ[i] == j

def Output():
	global L, Pairs, ItoJ, Parens, Label
	global Label

	Maxd = 0
	Max_i = 0
	Max_j = 0
	Ds = L*[ 0 ]
	for i in range(0, L):
		j = ItoJ[i]
		if j == None:
			continue
		d = GetDist(i, j)
		Ds[i] = d
		if d > Maxd:
			Maxd = d
			Max_i = i
			Max_j = j

	Equator1 = min(Max_i, Max_j)
	Equator2 = max(Max_i, Max_j)
	Pole1 = (Equator1 + Equator2)//2
	Pole2 = (Pole1 + L//2)%L

	K = 0
	k = 0
	L8 = L//8
	for Offset in range(0, L8):
		i = (Equator1 + Offset)%L
		j = ItoJ[i]
		if j != None:
			k += 1
		i = (Equator1 + L - Offset)%L
		j = ItoJ[i]
		if j != None:
			k += 1

	M = 0
	Good = 0
	for i in range(0, L):
		j = ItoJ[i]
		if j == None:
			continue
		M += 1

		Actual_d = GetDist(i, j)

		DistPole1_i = GetDist(i, Pole1)
		DistPole2_i = GetDist(i, Pole2)
		MinDistPole_i = min(DistPole1_i, DistPole2_i)

		Perfect_d = MinDistPole_i*2
		Error = abs(Actual_d - Perfect_d)
		if Error < L/10:
			Good += 1

	#	print("i=%d j=%d d=%d perfd=%d" % (i, j, Actual_d, Perfect_d))

	if M == 0:
		assert Good == 0
		Rodness = 0
		Intensity = 0
	else:
		assert Good <= M
		assert M <= L
		Rodness = float(Good)/M
		Intensity = float(k)/(2*L8)

	s = Label
	s += "\trodness=%.2f" % Rodness
	print(s)

FirstLine = False
SecondLine = False
for Line in open(FileName):
	if Line.startswith(">"):
		Label = Line[1:-1]
		if Label.endswith("_0001"):
			Label = Label.replace("_0001", "")
		else:
			break
		FirstLine = True
		continue
	elif FirstLine:
		Seq = Line[:-1]
		SecondLine = True
		FirstLine = False
	elif SecondLine:
		Parens = Line[:-1].split()[0]
		L = len(Parens)
		SetPairs()
		SetItoJ()
		Output()
		SecondLine = False
