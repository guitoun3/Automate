import automaton

aut1 = automaton.automaton(
	epsilons = ['0'],
	states = ['X', 'Y', 'Z'],
	initials = ['X'],
	finals = ['Z'],
	transitions = [
		('X', 'a', 'X'), ('X', 'b', 'Y'), ('X', 'c', 'X'),
		('Y', 'a', 'Z'), ('Y', 'b', 'Y'), ('Y', 'c', 'X'),
		('Z', 'a', 'Z'), ('Z', 'b', 'Z'), ('Z', 'c', 'Z')
		]

	)

aut2 = automaton.automaton(
	epsilons = ['0'],
	states = [1,2],
	initials = [1],
	finals = [2],
	transitions = [
		(1, 'a', 1), (1, 'b', 1), (1, 'c', 2), 
		(2, 'a', 2), (2, 'b', 2), (2, 'c', 2)
		]

	)

autNonDeter = automaton.automaton(
	epsilons = ['0'],
	states = [1,2],
	initials = [1],
	finals = [2],
	transitions = [
		(1, 'a', 1), (1, 'b', 1),
		(1, 'a', 2)
		]

	)


# Le puits n'est cree que si l'automate n'est pas deja complet
def completer(Aut):
	puits = Aut.get_maximal_id()+1
	isComplet = True

	for state in Aut.get_states():
		for alpha in Aut.get_alphabet():
			if alpha not in Aut.delta(state):

				#Ne cree le puits que si necessaire
				if isComplet == True:
					isComplet = False

					Aut.add_state(puits)

				Aut.add_transition((state, alpha, puits))


# Aut1 et Aut2 doivent etre complets et deterministes 
def union(Aut1, Aut2):

	states = ()
	initiaux = ()
	finaux = ()
	transitions = ()
	
	AutUnion = automaton.automaton((), states, initiaux, finaux, transitions)

	#Definition de l'epsilon
	AutUnion.add_epsilon_character(list(Aut1.get_epsilons())[0])

	#Ajout des caracteres dans l'alphabet
	for a in Aut1.get_alphabet():
		AutUnion.add_character(a)

	#Ajout des etats
	for x in Aut1.get_states():
		for y in Aut2.get_states():
			state = automaton.pretty_set((x,y))
			AutUnion.add_state(state)

			#Ajout des etats finaux
			if x in Aut1.get_final_states() or y in Aut2.get_final_states():
				AutUnion.add_final_state(state)

	#Ajout des etats initiaux
	state = automaton.pretty_set((list(Aut1.get_initial_states())[0], list(Aut2.get_initial_states())[0]))
	AutUnion.add_initial_state(state)


	#Ajout des transitions
	for alpha in AutUnion.get_alphabet():
		#Ne traite pas les epsilons transitions
		if alpha in AutUnion.get_epsilons():
			continue

		for stateA1 in Aut1.get_states():
			for stateA2 in Aut2.get_states():

				#Calcule les etats accessibles depuis les etats stateA1 et stateA2
				successeurA1 = list(Aut1.delta(alpha, [stateA1]))
				successeurA2 = list(Aut2.delta(alpha, [stateA2]))

				#Si pour le meme caractere un etat est accessible dans A1 
				#et un etat est accessible dans A2 on ajoute une transition
				if len(successeurA1) > 0 and len(successeurA2) > 0:

					state = automaton.pretty_set((stateA1, stateA2)) #Etat avant transition
					#A1 et A2 sont deterministes
					#ils ne doivent posseder qu'une valeur => [0]
					successeur = automaton.pretty_set((successeurA1[0], successeurA2[0])) #Etat apres transition

					AutUnion.add_transition((state, alpha, successeur))

	return AutUnion

def intersection(Aut1, Aut2):

	states = ()
	initiaux = ()
	finaux = ()
	transitions = ()
	
	AutInter = automaton.automaton((), states, initiaux, finaux, transitions)

	#Definition de l'epsilon
	AutInter.add_epsilon_character(list(Aut1.get_epsilons())[0])

	#Ajout des caracteres dans l'alphabet
	for a in Aut1.get_alphabet():
		AutInter.add_character(a)

	#Ajout des etats
	for x in Aut1.get_states():
		for y in Aut2.get_states():
			state = automaton.pretty_set((x,y))
			AutInter.add_state(state)

			#Ajout des etats finaux
			if x in Aut1.get_final_states() and y in Aut2.get_final_states():
				AutInter.add_final_state(state)

	#Ajout des etats initiaux
	state = automaton.pretty_set((list(Aut1.get_initial_states())[0], list(Aut2.get_initial_states())[0]))
	AutInter.add_initial_state(state)


	#Ajout des transitions
	for alpha in AutInter.get_alphabet():
		#Ne traite pas les epsilons transitions
		if alpha in AutInter.get_epsilons():
			continue

		for stateA1 in Aut1.get_states():
			for stateA2 in Aut2.get_states():

				#Calcule les etats accessibles depuis les etats stateA1 et stateA2
				successeurA1 = list(Aut1.delta(alpha, [stateA1]))
				successeurA2 = list(Aut2.delta(alpha, [stateA2]))

				#Si pour le meme caractere un etat est accessible dans A1 
				#et un etat est accessible dans A2 on ajoute une transition
				if len(successeurA1) > 0 and len(successeurA2) > 0:

					state = automaton.pretty_set((stateA1, stateA2)) #Etat avant transition
					#A1 et A2 sont deterministes
					#ils ne doivent posseder qu'une valeur => [0]
					successeur = automaton.pretty_set((successeurA1[0], successeurA2[0])) #Etat apres transition

					AutInter.add_transition((state, alpha, successeur))

	return AutInter

def miroir(Aut):
	alphabet = Aut.get_alphabet()
	epsilons = Aut.get_epsilons()
	states = Aut.get_states()
	initiaux = Aut.get_final_states()
	finaux = Aut.get_initial_states()
	transitions = ()
	AutMir = automaton.automaton(alphabet, epsilons, states, initiaux, finaux, transitions)
	for t in Aut.get_transitions():
		AutMir.add_transition((t[2],t[1],t[0]))

	return AutMir


def determinisation(Aut):
	initial = Aut.get_initial_states()
	finaux = ()
	alphabet = Aut.get_alphabet()
	transitions = ()
	epsilons = Aut.get_epsilons()

	#Ajout de l'etat initial
	states = set(initial)
	states.add((1,2))
	print states

	for buildState in states:
		print "\t", buildState
		for st in [buildState]:
			print "\t\t", st
			for alpha in alphabet:
				newState = list()
				print "\t\t\t A = ", alpha , " : " ,Aut.delta(alpha, [st])
				for access_state in list(Aut.delta(alpha, [st])):
					print "\t\t\t\t add = ", access_state
					newState.append(access_state)

				print newState
				print states
					
				#if newState not in states:
				print "insert", newState
				states.add(frozenset(newState))

	print states


	"""
	states = set(initial)
	for buildState in states:
		print "\t", buildState
		for st in [buildState]:
			print "\t\t", st
			for alpha in alphabet:
				newState = list()
				print "\t\t\t A = ", alpha , " : " ,Aut.delta(alpha, [st])
				for access_state in list(Aut.delta(alpha, [st])):
					print "\t\t\t\t add = ", access_state
					newState.append(access_state)

				print newState
				print states
					
				#if newState not in states:
				print "insert", newState
				states.add(frozenset(newState))

	print states
	"""			




aut3 = union(aut1, aut2)
aut4 = intersection(aut1, aut2)
aut5 = miroir(aut1)
aut6 = determinisation(autNonDeter)


#aut1.display()
#aut5.display()