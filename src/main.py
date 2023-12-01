# encoding: utf-8
import sys
import random
import math

def vrp(data,popsize,iterations):
	def distance(n1, n2):
		dx = n2['posX'] - n1['posX']
		dy = n2['posY'] - n1['posY']
		return math.sqrt(dx * dx + dy * dy)

	def fitness(p):
		# The first distance is from depot to the first node of the first route
		s = distance(data['nodes'][0], data['nodes'][p[0]])
		# Then calculating the distances between the nodes
		for i in range(len(p) - 1):
			prev = data['nodes'][p[i]]
			next = data['nodes'][p[i + 1]]
			s += distance(prev, next)
		# The last distance is from the last node of the last route to the depot
		s += distance(data['nodes'][p[len(p) - 1]], data['nodes'][0])
		return s

	def adjust(p):
		# Adjust repeated
		repeated = True
		while repeated:
			repeated = False
			for i1 in range(len(p)):
				for i2 in range(i1):
					if p[i1] == p[i2]:
						haveAll = True
						for nodeId in range(len(data['nodes'])):
							if nodeId not in p:
								p[i1] = nodeId
								haveAll = False
								break
						if haveAll:
							del p[i1]
						repeated = True
					if repeated: break
				if repeated: break
		# Adjust capacity exceed
		i = 0
		s = 0.0
		cap = data['capacity']
		while i < len(p):
			s += data['nodes'][p[i]]['demand']
			if s > cap:
				p.insert(i, 0)
				s = 0.0
			i += 1
		i = len(p) - 2
		# Adjust two consective depots
		while i >= 0:
			if p[i] == 0 and p[i + 1] == 0:
				del p[i]
			i -= 1



	pop = []

	# Generating random initial population
	for i in range(popsize):
		p = list(range(1, len(data['nodes'])))
		random.shuffle(p)
		pop.append(p)
	for p in pop:
		adjust(p)

	# Running the genetic algorithm
	for i in range(iterations):
		nextPop = []
		# Each one of this iteration will generate two descendants individuals. Therefore, to guarantee same population size, this will iterate half population size times
		for j in range(int(len(pop) / 2)):
			# Selecting randomly 4 individuals to select 2 parents by a binary tournament
			parentIds = set()
			while len(parentIds) < 4:
				parentIds |= {random.randint(0, len(pop) - 1)}
			parentIds = list(parentIds)
			# Selecting 2 parents with the binary tournament
			parent1 = pop[parentIds[0]] if fitness(pop[parentIds[0]]) < fitness(pop[parentIds[1]]) else pop[parentIds[1]]
			parent2 = pop[parentIds[2]] if fitness(pop[parentIds[2]]) < fitness(pop[parentIds[3]]) else pop[parentIds[3]]
			# Selecting two random cutting points for crossover, with the same points (indexes) for both parents, based on the shortest parent
			cutIdx1, cutIdx2 = random.randint(1, min(len(parent1), len(parent2)) - 1), random.randint(1, min(len(parent1), len(parent2)) - 1)
			cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)
			# Doing crossover and generating two children
			child1 = parent1[:cutIdx1] + parent2[cutIdx1:cutIdx2] + parent1[cutIdx2:]
			child2 = parent2[:cutIdx1] + parent1[cutIdx1:cutIdx2] + parent2[cutIdx2:]
			nextPop += [child1, child2]
		# Doing mutation: swapping two positions in one of the individuals, with 1:15 probability
		if random.randint(1, 15) == 1:
			ptomutate = nextPop[random.randint(0, len(nextPop) - 1)]
			i1 = random.randint(0, len(ptomutate) - 1)
			i2 = random.randint(0, len(ptomutate) - 1)
			ptomutate[i1], ptomutate[i2] = ptomutate[i2], ptomutate[i1]
		# Adjusting individuals
		for p in nextPop:
			adjust(p)
		# Updating population generation
		pop = nextPop

	# Selecting the best individual, which is the final solution
	better = None
	bf = float('inf')
	for p in pop:
		f = fitness(p)
		if f < bf:
			bf = f
			better = p


	## After processing the algorithm, now outputting it ##

	result = ''
	# Printing the solution
	print(' route:')
	result += 'depot'
	for nodeIdx in better:
		result +=data['nodes'][nodeIdx]['label']
	result += 'depot'
	return result,float(bf)
