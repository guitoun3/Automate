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

aut11fig3 = automaton.automaton(
	epsilons = ['0'],
	states = [1,2,4],
	initials = [1,4],
	finals = [2,4],
	transitions = [
		(1, 'a', 2), (1, 'b', 4),
		(2, 'a', 4),
		(4, 'a', 4)
		]
	)

complementAut = automaton.automaton(
	epsilons = ['0'],
	states = [1,2],
	initials = [1],
	finals = [1],
	transitions = [
		(1, 'a', 2), (1, 'c', 1),
		(2, 'b', 1)
		]
	)

autNonMini = automaton.automaton(
	epsilons =[],
	states = [2,4,5,6,7,8],
	initials = [1],
	finals = [3],
	transitions = [(1,'a',2), (1,'b',6), (2,'b',3), (3,'a',4), (3,'b',3), (4,'b',7), (5,'a',8), (5,'b',6), (6,'a',3), (6,'b',7), (7,'a',8), (8,'b',3)]
	)

# Le puits n'est cree que si l'automate n'est pas deja complet
def completer(Aut):
	puits = Aut.get_maximal_id()+1
	isComplet = True

	for state in Aut.get_states():
		for alpha in Aut.get_alphabet():
			if not Aut.delta(alpha, [state]):

				#Ne cree le puits que si necessaire
				if isComplet == True:
					isComplet = False

					Aut.add_state(puits)

				Aut.add_transition((state, alpha, puits))

	#Ajout des transitions du puits
	for alpha in Aut.get_alphabet():
		Aut.add_transition((puits, alpha, puits))

	return Aut
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
	initial = []
	finaux = []
	alphabet = Aut.get_alphabet()
	transitions = []
	epsilons = Aut.get_epsilons()

	#Creation de l'etat initial
	my_initial = ()
	for initState in Aut.get_initial_states():
		my_initial = my_initial +(initState,)
	
	if len(my_initial) > 1:
		initial.append(my_initial)
	else:
		initial.append(my_initial[0])
	
	#Copie la variable de initial au lieu d'utiliser un pointeur
	states = set(initial[:])
	print states
	#Ajout des nouveaux etats
	i = 0
	while i < len(states):
		setState = list(states)[i]
		if type(setState).__name__ == 'int':
			setState = [setState]

		print "setState = ", setState

		for alpha in alphabet:
			new_state = tuple()
			for state in setState:
				for access_state in Aut.delta(alpha, [state], True):
					print "\t\t\taccess = ", access_state
					if access_state not in new_state:
						new_state = new_state + (access_state,)
						print "\t\t\tOK"
				
			if len(new_state) > 0:
				if len(new_state) == 1:
					new_state = new_state[0]

				states.add(new_state)

		"""for state in setState:
			print "\tstate = ", state
			for alpha in alphabet:
				print "\t\tal = ", alpha
				new_state = tuple()

				for access_state in Aut.delta(alpha, [state], True):
					print "\t\t\taccess = ", access_state
					if access_state not in new_state:
						new_state = new_state + (access_state,)
						print "\t\t\tOK"
				
				if len(new_state) > 0:
					if len(new_state) == 1:
						new_state = new_state[0]

					states.add(new_state)"""

		i += 1

	print states	
	#Ajout des etats finaux
	for setState in states:
		if type(setState).__name__ == 'int':
			if setState in Aut.get_final_states():
				finaux.append(setState)

			continue

		for state in setState:
			if state in Aut.get_final_states():
				finaux.append(setState)

	#Ajout des transitions
	for setState in states:
		setStateC = setState
		if type(setState).__name__ == 'int':
			setStateC = [setState]
		for alpha in alphabet:
			state_arrive = []

			for state in setStateC:
				for access_state in Aut.delta(alpha, [state], True):
					if access_state not in state_arrive:
						state_arrive.append(access_state)

			if len(state_arrive) > 0:
				#Evite d'avoir un state_arrive de la forme (1,) quand l'etat n'est pas un etat "compose"
				if len(state_arrive) > 1:
					state_arrive = tuple(state_arrive)
				else:
					state_arrive = state_arrive[0]
				transitions.append((setState, alpha, state_arrive))

	return automaton.automaton(alphabet, epsilons, states, initial, finaux, transitions)

def complement(Aut):
	Aut = determinisation(Aut)
	Aut = completer(Aut)

	finaux = []
	
	for state in Aut.get_states():
		if state not in Aut.get_final_states():
			finaux.append(state)

	return automaton.automaton(Aut.get_alphabet(), Aut.get_epsilons(), Aut.get_states(), Aut.get_initial_states(), finaux, Aut.get_transitions())

def classeDe(state, classes):
	for c in classes:
		if state in c:
			return c

def minimiser(Aut):
	#Aut = determinisation(Aut)
	#Aut = completer(Aut)
	classes = list()
	finaux = list()
	nf = list()
	alphabet = Aut.get_alphabet()
	for e in Aut.get_states():
		if Aut.state_is_final(e):
			finaux.append(e)
		else:
			nf.append(e)
	classes.append(finaux)
	classes.append(nf)
	for c in classes:
		newclass = list()
		for s in c:
			for a in alphabet:
				l1=list()
				l2=list()
				l1.append(s)
				l2.append(list(c)[0])
				if Aut.delta(a, l1) in classeDe(Aut.delta(a, l2), classes):
					continue
				else:
					c.remove(s)
					newclass.append(s)
					break
		if newclass.len() > 0:
			classes.append(newclass)
	realStates = automaton.pretty_set()
	realIni = automaton.pretty_set()
	realFin = automaton.pretty_set()
	realTrans = automaton.pretty_set()
	for c in classes:
		if Aut.state_is_final(list(c)[0]):
			realFin.append(tuple(c))
		else:
			if Aut.state_is_initial(list(c)[0]):
				realIni.append(tuple(c))
			else:
				realStates.append(tuple(c))
		for a in alphabet:
			realTrans.append(tuple(c), a, tuple(classeDe(Aut.delta(a, list(c)[0]), classes)))
	return automaton.automaton(alphabet, set(), realStates, realIni, realFin, realTrans)

aut3 = union(aut1, aut2)
aut4 = intersection(aut1, aut2)
aut5 = miroir(aut1)
aut6 = minimiser(autNonMini)
#aut7 = determinisation(autNonDeter)

#aut11fig3 = determinisation(aut11fig3)
#aut11fig3.display()

#complementAut = complement(complementAut)
#complementAut.display()

#aut1.display()

autNonMini.display()
#aut6.display()

#aut5.display()