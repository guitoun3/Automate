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
		(2, 'a', 2), (2, 'a', 2), (2, 'a', 2)
		]

	)


# Le puit n'est cree que si l'automate n'est pas deja complet

def completer(Aut):
	puit = Aut.get_maximal_id()+1
	isComplet = True

	for state in Aut.get_states():
		for alpha in Aut.get_alphabet():
			if alpha not in Aut.delta(state):

				#Ne cree le puit que si necessaire
				if isComplet == True:
					isComplet = False

					Aut.add_state(puit)

				Aut.add_transition((state, alpha, puit))


# Aut1 et Aut2 doivent etre complet et deterministe 
def union(Aut1, Aut2):

	epsilons = Aut1.get_epsilons().union(Aut2.get_epsilons())
	states = ()
	initiaux = ()
	finaux = ()
	transitions = ()
	
	print states

	AutUnion = automaton.automaton(epsilons, states, initiaux, finaux, transitions)

	#Ajout des etats
	for x in Aut1.get_states():
		for y in Aut2.get_states():
			AutUnion.add_state((x,y))

			#Ajout des etats finaux
			if x in Aut1.get_final_states():
				AutUnion.add_final_state((x,y))
			if y in Aut2.get_final_states():
				AutUnion.add_final_state((x,y))

	#Ajout des etats initiaux
	AutUnion.add_initial_state((Aut1.get_initial_states(), Aut2.get_initial_states()))


	#Ajout des transitions
	for state in AutUnion.get_states():
		for alpha in AutUnion.get_alphabet():
			successeur = (Aut1.delta(alpha), Aut2.delta(alpha))
			AutUnion.add_transition((state, alpha, successeur))

	return AutUnion

aut3 = union(aut1, aut2)



aut3.display()