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

autNonComplet = automaton.automaton(
	epsilons = ['0'],
	states = [1,2,3],
	initials = [1],
	finals = [3],
	transitions = [
		(1, 'a', 2), (2, 'b', 3), (1, 'c', 3)
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
	Aut.renumber_the_states()
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

	#Ajout des nouveaux etats
	i = 0
	while i < len(states):
		setState = list(states)[i]
		if type(setState).__name__ == 'int':
			setState = [setState]


		for alpha in alphabet:
			new_state = tuple()
			for state in setState:
				for access_state in Aut.delta(alpha, [state], True):
					if access_state not in new_state:
						new_state = new_state + (access_state,)
				
			if len(new_state) > 0:
				if len(new_state) == 1:
					new_state = new_state[0]

				states.add(new_state)

		i += 1

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
	Aut = determinisation(Aut)
	Aut = completer(Aut)
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
		classIterator = 0
		while classIterator < len(c):
			s=c[classIterator]
			classIterator+=1
			for a in alphabet:
				l1=list()
				l2=list()
				l1.append(s)
				l2.append(list(c)[0])
				if list(Aut.delta(a, l1))[0] in classeDe(list(Aut.delta(a, l2))[0], classes):
					continue
				else:
					c.remove(s)
					if len(newclass) > 0:
						classes.remove(newclass)
					newclass.append(s)
					classes.append(newclass)
					classIterator-=1
					break
	realStates = automaton.pretty_set()
	realIni = automaton.pretty_set()
	realFin = automaton.pretty_set()
	realTrans = automaton.pretty_set()
	realAut = automaton.automaton(alphabet, automaton.pretty_set(), realStates, realIni, realFin, realTrans)
	for c in classes:
		if len(c)>1:
			cp = tuple(c)
		else:
			cp = list(c)[0]
		if Aut.state_is_final(list(c)[0]):
			realAut.add_final_state(cp)
		else:
			if Aut.state_is_initial(list(c)[0]):
				realAut.add_initial_state(cp)
			else:
				realAut.add_state(cp)
		for a in alphabet:
			if len(classeDe(list(Aut.delta(a, c))[0], classes))>1:
				cpd = tuple(classeDe(list(Aut.delta(a, c))[0], classes))
			else:
				cpd = classeDe(list(Aut.delta(a, c))[0], classes)[0]
			realAut.add_transition((cp, a, cpd))
	return realAut

def thomson_union(aut1, aut2):
	new_aut1 = aut1.clone()
	new_aut1 = new_aut1.get_renumbered_automaton()
	new_aut2 = aut2.clone()
	new_aut2 = new_aut2.get_renumbered_automaton()

	#Renumerote aut2 pour eviter des conflits si des etats ont le meme nom
	def renumber(obj):
		return obj+new_aut1.get_maximal_id()

	new_aut2.map(renumber)

	new_initial = new_aut2.get_maximal_id()+1
	new_final = new_aut2.get_maximal_id()+2

	new_aut = automaton.automaton(epsilons = ['0'],
									states = [],
									initials = [new_initial],
									finals = [new_final],
									transitions = [])

	#Ajout des etats de aut1 et aut2 dans new_aut
	new_aut.add_states(new_aut1.get_states())
	new_aut.add_states(new_aut2.get_states())

	#Ajout des transitions de aut1 et aut2 dans new_aut
	new_aut.add_transitions(new_aut1.get_transitions())
	new_aut.add_transitions(new_aut2.get_transitions())

	#Epsilon transition du nouvel initial vers les anciens initiaux de aut1 et aut2
	new_aut.add_transition((new_initial, '0', list(new_aut1.get_initial_states())[0]))
	new_aut.add_transition((new_initial, '0', list(new_aut2.get_initial_states())[0]))

	#Epsilon transition des anciens finaux de aut1 et aut2 vers new_aut
	new_aut.add_transition((list(new_aut1.get_final_states())[0], '0', new_final))
	new_aut.add_transition((list(new_aut2.get_final_states())[0], '0', new_final))

	return new_aut

def thomson_produit(aut1, aut2):
	new_aut1 = aut1.clone()
	new_aut1 = new_aut1.get_renumbered_automaton()
	new_aut2 = aut2.clone()
	new_aut2 = new_aut2.get_renumbered_automaton()

	#Renumerote aut2 pour eviter des conflits si des etats ont le meme nom
	def renumber(obj):
		return obj+new_aut1.get_maximal_id()

	new_aut2.map(renumber)

	new_aut = automaton.automaton(epsilons = ['0'],
									states = [],
									initials = [list(new_aut1.get_initial_states())[0]],
									finals = [list(new_aut2.get_final_states())[0]],
									transitions = [])


	#Ajout des etats de aut1 et aut2 dans new_aut
	new_aut.add_states(new_aut1.get_states())
	new_aut.add_states(new_aut2.get_states())

	#Ajout des transitions de aut1 et aut2 dans new_aut
	new_aut.add_transitions(new_aut1.get_transitions())
	new_aut.add_transitions(new_aut2.get_transitions())
	
	new_aut1_final = list(new_aut1.get_final_states())[0]
	new_aut2_initial = list(new_aut2.get_initial_states())[0]

	#Epsilon transition new_aut1_final vers new_aut2_initial
	new_aut.add_transition((new_aut1_final, '0', new_aut2_initial))

	return new_aut



def thomson_etoile(aut):
	aut = aut.get_renumbered_automaton()

	new_initial = aut.get_maximal_id()+1
	new_final = aut.get_maximal_id()+2

	new_aut = automaton.automaton(epsilons = ['0'],
									states = [],
									initials = [new_initial],
									finals = [new_final],
									transitions = [])

	ancien_final = list(aut.get_final_states())[0]
	ancien_initial = list(aut.get_initial_states())[0]

	#Ajout epsilon transition du final vers l'initial
	new_aut.add_transition((ancien_final, '0', ancien_initial))

	#Ajout epsilon transition nouvel initial vers ancien initial
	new_aut.add_transition((new_initial, '0', ancien_initial))

	#Ajout epsilon transition ancien final vers nouveau final
	new_aut.add_transition((ancien_final, '0', new_final))
	
	#Ajout epsilon transition nouvel initial vers nouveau final
	new_aut.add_transition((new_initial, '0', new_final))

	#Copie des etats
	new_aut.add_states(aut.get_states())

	#Copie des transitions
	new_aut.add_transitions(aut.get_transitions())

	return new_aut


def thomson_char(expr):
	return automaton.automaton(
		epsilons = ['0'],
		states = [1,2],
		initials = [1],
		finals = [2],
		transitions = [(1, expr, 2)])


# def thomson_epsilon():
# 	return automaton.automaton(
# 		epsilons = ['0'],
# 		states = [1,2],
# 		initials = [1],
# 		finals = [2],
# 		transitions = [(1, '0', 2)])


def expression_vers_automate(expr):
	i = 1

	for item in expr:
		if type(item) != list:
			if item == "*":
				"""
				Traitement de l'etoile
				"""
				aut = expression_vers_automate(expr[i:][0])
				return thomson_etoile(aut)
			elif item == "+":
				"""
				Traitement de l'union
				"""
				arg = expr[i:][0]

				aut = expression_vers_automate(arg[0])

				"""
				Parcours la liste pour unir les elements deux a deux
				"""
				for j in range(1, len(arg)):
					if type(arg[j]) == list:
						p_aut = expression_vers_automate(arg[j])
					else:
						p_aut = thomson_char(arg[j])

					aut = thomson_union(aut, p_aut)

				return aut
			elif item == ".":
				#Traitement du produit
				arg = expr[i:][0]

				aut = expression_vers_automate(arg[0])

				#Parcours la liste des elements pour effectuer le produit des automates deux a deux
				for j in range(1, len(arg)):
					if type(arg[j]) == list:
						p_aut = expression_vers_automate(arg[j])
					else:
						p_aut = thomson_char(arg[j])

					aut = thomson_produit(aut, p_aut)
				return aut
			else:
				return thomson_char(item)

		i += 1

"""
Exemple 1.
Rendre un automate complet
"""
# autNonComplet.display()
# autCompleter = completer(autNonComplet)
# autCompleter.display()

"""
Exemple 2.
Faire l'union de 2 automates
"""
# aut1.display()
# aut2.display()
# autUnion = union(aut1, aut2)
# autUnion.display()

"""
Exemple 3.
Faire l'intersection de 2 automates
"""
# aut1.display()
# aut2.display()
# autIntersect = intersection(aut1, aut2)
# autIntersect.display()

"""
Exemple 4.
Calcul de l'automate miroir
"""
# aut1.display()
# autMiroir = miroir(aut1)
# autMiroir.display()


"""
Exemple 5.
Determinisation d'un automate
"""
# autNonDeter.display()
# autDeterministe = determinisation(autNonDeter)
# autDeterministe.display()


"""
Exemple 6.
Complement du langage reconnu par un automate
"""
# complementAut.display()
# complementAut = complement(complementAut)
# complementAut.display()


"""
Exemple 7.
Minimisation d'un automate
"""
# autNonMini.display()
# autMini = minimiser(autNonMini)
# autMini.display()


"""
Exemple 8.1
Expression vers automate (a+b*a)*
"""
# expr = ["*", ["+", ["a", [".", [["*", "b"], "a"]]]]]  #(a+b*a)*
# t = expression_vers_automate(expr)
# t.display()

"""
Exemple 8.2
Expression vers automate a*(b+cd)*
"""
# expr2 = [".", [["*", "a"], ["*", ["+", ["b", [".", ["c", "d"]]]]]]]  #a*(b+cd)*
# t = expression_vers_automate(expr2)
# t.display()

"""
Exemple 8.3
Expression vers automate ab+cd
"""
# expr3 = ["+", [[".", ["a", "b"]], [".", ["c", "d"]]]]
# t = expression_vers_automate(expr3)
# t.display()

"""
Exemple 8.4
Expression vers automate a+b+(cd)*
"""
# expr4 = ["+", ["a", "b", ["*", [".", ["c", "d"]]]]]
# t = expression_vers_automate(expr4)
# t.display()



#aut3 = union(aut1, aut2)
#aut4 = intersection(aut1, aut2)
#aut5 = miroir(aut1)
# aut6 = minimiser(autNonMini)
#aut7 = determinisation(autNonDeter)

#aut11fig3 = determinisation(aut11fig3)
#aut11fig3.display()

#complementAut = complement(complementAut)
#complementAut.display()

#aut1.display()

#autNonMini.display()
# aut6.display()

#aut5.display()