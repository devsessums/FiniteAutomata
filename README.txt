             _                        _                                
            | |                      | |                               
  __ _ _   _| |_ ___  _ __ ___   __ _| |_ ___  _ __  ___   _ __  _   _ 
 / _` | | | | __/ _ \| '_ ` _ \ / _` | __/ _ \| '_ \/ __| | '_ \| | | |
| (_| | |_| | || (_) | | | | | | (_| | || (_) | | | \__ \_| |_) | |_| |
 \__,_|\__,_|\__\___/|_| |_| |_|\__,_|\__\___/|_| |_|___(_) .__/ \__, |
                                                          | |     __/ |
                                                          |_|    |___/ 

What is automatons.py?
automatons.py contains a python library to implement nondeterministic and deterministic fintite automata either as a standalone console program or can be imported into other python libraries. 

What does a file look like?
If the file represents a deterministic finite automaton (DFA):
- The first line is the alphabet (sigma) where each char is separated by a space . If one of characters is a tilda '~', then it will be treated as a space ' ' for input. This can be changed from the global variable SPACE.
- The second line is the amount of states in automaton.
- The third line is optional if there no accept states, if there are accept states then each of the states should be prefixed by a 'Q' followed by the state number. Each accept state should be separated by a space.
- The next line should be three consecutive dashes '---'.
- The following lines will indicate a rule on each line, where each rule is in three parts separated by spaces. Parts one and three are prefixed with 'Q' followed by the state number, which represent the in and out states, respectively. The second part of the rule is a single char transition the in state uses to get to the out state.

DFA file example:
	0 1
	3
	Q1
	---
	Q0 0 Q1
	Q0 1 Q2
	Q2 0 Q2
	Q2 1 Q2
	Q1 1 Q2
	Q1 0 Q1


If the file represents a nondeterministic finite automaton (NFA):
- The first line should be 'NFA'
- The second line is the alphabet (sigma) where each char is separated by a space . If one of characters is a tilda '~', then it will be treated as a space ' ' for input. This can be changed from the global variable SPACE.
- The third line is the amount of states in automaton.
- The fourth line is optional if there no accept states, if there are accept states then each of the states should be prefixed by a 'Q' followed by the state number. Each accept state should be separated by a space.
- The next line should be three consecutive dashes '---'.
- The following lines will indicate a rule on each line, where each rule could be in three parts or two parts. If there are three parts, then parts one and three are prefixed with 'Q' followed by the state number, which represent the in and out states, respectively. The second part of the rule is a single char transition the in state uses to get to the out state. If there are two parts to the rule, then parts one and two are prefixed with 'Q' followed by the state number. This means the in state goes to the out state on an epsilon (empty) transition

NFA file example:
	NFA
	0 1
	4
	Q3
	---
	Q0 0 Q1
	Q0 0 Q2
	Q1 1 Q0
	Q1 1 Q3
	Q2 0 Q3
	Q3 0 Q0
	Q3   Q1
	Q3 1 Q0


How do I run automatons.py as a standalone program?
You can run automatons.py in a terminal with a given text (*.txt) file representing the automaton. Then you will be prompted to input a word or sentence until Ctrl + c is pressed. If no file is found or if given an incorrect file format the program will fail to load.

An example of starting automatons.py as a standalone program.

	> python automatons.py someFiniteAutomaton.txt
	< Looking for someFiniteAutomaton.txt
	< someFiniteAutomaton.txt Found!
	> Please input a word :

The program shall output the results as either 'Accepted' meaning the word exists in the language described by the automaton or 'Rejected' meaning the word does not exist in the language described by the automaton. Regardless, of whether the word is 'Accepted' or 'Rejected', the program will output the path taken.

A DFA representing the regular expression of 0+ (one or more zeros in a string):

	> python automatons.py dfaZeroOneOrMore.txt
	< Looking for dfaZeroOneOrMore.txt
	< dfaZeroOneOrMore.txt Found!
	> Please input a word: 00000
	< String Accepted. Path:
	< Q0 Q1 Q1 Q1 Q1 Q1
	> Please input a word: 01010000111 
	< String Rejected
	< Q0 Q1 Q2 Q2 Q2 Q2 Q2 Q2 Q2 Q2 Q2 Q2
	> Please input a word :
	< User has hit Ctrl + C to exit!

How do I use automatons.py in other libraries?
automatons.py has two classes to use: Automaton and automata_sim.


class Automaton
- Default constructor
- automatons.Automaton(int Q, list E, dict D, int q, list F, string t_):

	- Q is the amount of states in Automaton; should be greater than zero. Example: 2 for two states.

	- E is the alphabet (sigma) by a list of chars; should be greater than zero. Example: ['a', 'b'] a possible transition for any state.
	
	- D is the  state transition table (delta) using a dictionary; where keys are the states and the value is another dictionary. The second dictionary stores keys as single char transitions and the value is a list of states(ints). Example: {0:{'a':[1],'b':[0]}, 1:{'a':[1], 'b':[0]}} There are two states 0 and 1. State 0 goes to state 1 on transition 'a' and goes to state 0 on transition 'b'.

	- q is the start state; However, it should always start at 0.

	- F is the list of integer accept states in the automaton. If there are no accept states, then use an empty list([]). Example: [0, 1] states 0 and 1 are accept states .

	- t_ is the finite automaton type. If the automaton is nondeterministic, then use the string 'NFA'. If it is deterministic use the string 'DFA'.

	A default constructor example: 
	a = Automaton(2, ['a','b'], {0:{'a':[1],'b':[0]}, 1:{'a':[1], 'b':[0]}}, 0, [1], 'DFA')

- class Automaton method run
- automatons.Automaton.run(string w, list path, list transitions)

	Returns a 3-tuple (bool, list, list). The boolean is whether the word was accepted (True) or rejected (False). The first list is of integers representing the states taken in reverse order of the path taken. The second list is of single chars in reverse order, the first transition taken is the last index of the list.
 
	- w is a string or word to test for membership in the Automaton. Example: '8675309'

	- path is a list of integers or path taken through the automaton. path should always be a list with a single zero in it. Example: [0]
	
	- transitions is a list of single chars taken for each state. Should always be an empty list ([]).
	
	Automaton.run method example:
	t, p, tr = Automaton.run('00100010',[0],[])

- class Automaton method end
- automatons.Automaton.end(int signum, f)
DO NOT CALL THIS METHOD. This is the for handling the 'Ctrl + c' signal.



class automata_sim
- Default constructor
- automatons.automata_sim(string file)
	
	If running as standalone this calls automata_sim.main() with command line file argument. If importing automatons.py into other libraries, then automata_sim(file) returns an Automaton object representing the file. 

	- file is a string of the name of the file to convert to Automaton object. file must be a text(*.txt) file format. Example: 'dfa1.txt'

	A default constructor example standalone:
	automata_sim('dfa2.txt')

	A default constructor example used in other libraries:
	a = automata_sim('dfa2.txt')

- class automata_sim method main
-automatons.automata_sim.main()
	This should not be called outside of the module driver. automata_sim.main will continually ask for word input for a file automaton. 'Ctrl + c' will interrupt this loop.

- class automata_sim method setup
-automatons.automata_sim.setup(string file)
	Returns an Automaton object after parsing a correct file.

	- file is a string of the name of the file to convert to Automaton object. file must be a text(*.txt) file format. Example: 'dfa1.txt'

