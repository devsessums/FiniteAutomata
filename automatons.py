# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 23:11:54 2021

@author: Sam

"""



import sys
import os
from os.path import exists
import random
import time
import signal

E = ''
SPACE = '~'

# System call - reference in the Docs for colored printing
os.system("")


# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BLINK = '\033[05m'

class Automaton():
        def __init__(self, Q, E, D, q, F, t):
            try:
                if isinstance(Q, int):
                    self.Q = Q # int representing the amount of states in automaton
                else:
                    raise TypeError("Automaton.Q requires a type int")

                if isinstance(E, list):
                    self.E = E # sigma(Σ) or alphabet for the automaton
                else:
                    raise TypeError("Automaton.E requires a type list")

                if isinstance(D, dict):
                    self.D = D # state transition table {state:{transition:[toStates]}}
                else:
                    raise TypeError("Automaton.D requires type dict")

                if isinstance(q, int):
                    self.q = q # starting state or 0, useless more for aethestics
                else:
                    raise TypeError("Automaton.q requires a type int")

                if isinstance(F, list):
                    self.F = F # list of accepted states
                else:
                    raise TypeError("Automaton.F requires a type list")

                if isinstance(t, str):
                    self.t_ = t # type of automaton either 'NFA' or 'DFA'
                else:
                    raise TypeError("Automaton.t_ requires a type str")

                signal.signal(signal.SIGINT, self.end)
            except TypeError as e:
                print(e)

        """
        Recursive Go Figure!
        #
        """
        def run(self, w, path, transitions):
            try:
                cycle = False
                count = 0

                # before taking any epsilon transitions check that we haven't made
                # a complete cycle of epsilon transitions from current state to current state
                for i in range(len(transitions)):
                            #print(len(transitions))
                            if transitions[i] == E:
                                count += 1
                                if count >= 1:
                                    if path[count] == path[0]:
                                        return (False, path, transitions)


                # Base Case:
                # w is an empty string check if its in the list of accepted states
                if len(w) == 0:

                    # no more input to parse and current state is in accepted states
                    if path[0] in self.F:
                        return (True, path, transitions)

                    # no more input to parse and not in accepted state, but at least one
                    # epsilon transition exists from current state
                    if (path[0] not in self.F and E in self.D[path[0]].keys() and not cycle):

                        for i in range(len(self.D[path[0]][E])):
                            newPath = path.copy()
                            newTransitions = transitions.copy()
                            newPath.insert(0, self.D[path[0]][E][i])
                            newTransitions.insert(0, E)

                            truth, aPath, t = self.run(w, newPath, newTransitions)

                            #pop out here after recursive call

                            # if the call ends in the accept state then exit
                            if truth:
                                return (True, aPath, t)

                            # if we are at the end of all possible epsilon transitions
                            # then return false
                            elif i == len(self.D[path[0]][E]) - 1:
                                return (False, aPath, t)

                    # not in accept state
                    else:
                        return (False, path, transitions)

                else:
                    # can't parse input anymore
                    if (w[0] not in self.D[path[0]].keys() and E not in self.D[path[0]].keys()):
                        return (False, path, transitions)

                    # take all epsilon paths if no epsilon cycle has happened
                    elif (w[0] not in self.D[path[0]].keys() and E in self.D[path[0]].keys() and not cycle):

                        for i in range(len(self.D[path[0]][E])):
                            newPath = path.copy()
                            newTransitions = transitions.copy()
                            newPath.insert(0, self.D[path[0]][E][i])
                            newTransitions.insert(0, E)

                            truth, aPath, t = self.run(w, newPath, newTransitions)

                            # pop out of recursion
                            if truth:
                                return (True, aPath, t)

                            elif i == ((len(self.D[path[0]][E])) - 1 ):
                                return (False, aPath, t)


                    # this is where DFAs will run, but NFAs can run here too
                    else:
                        # if only one state exists on the transition
                        if len(self.D[path[0]][w[0]]) == 1:
                            newPath = path.copy()
                            newTransitions = transitions.copy()
                            newPath.insert(0,self.D[path[0]][w[0]][0])
                            newTransitions.insert(0, w[0])

                            # right before base case
                            if len(w) == 1:
                                return self.run('', newPath, newTransitions)
                            # still more input to parse
                            else:
                                return self.run(w[1:], newPath, newTransitions)


                        else:
                            # more than one state exists for that transition
                            for i in range(len(self.D[path[0]][w[0]])):
                                newPath = path.copy()
                                newTransitions = transitions.copy()
                                newPath.insert(0,self.D[path[0]][w[0]][i])
                                newTransitions.insert(0, w[0])

                                # right before base case
                                if len(w) == 1:
                                    truth, aPath, t = self.run('', newPath, newTransitions)

                                # still more input to parse
                                else:
                                    truth, aPath, t = self.run(w[1:], newPath, newTransitions)

                                # recursive out
                                if truth:
                                    # path taken is accepted
                                    return (True, aPath, t)

                                # path taken is rejected
                                elif i == (len(self.D[path[0]][w[0]]) - 1):
                                    return (False, aPath, t)

            except Exception as e:
                print(e)


        def end(self, signum, f):
            try:
                print(style.RED + "\nUser has hit Ctrl + C to exit!"+style.RESET)
                sys.exit(0)
            except Exception as e:
                print(e)


class automata_sim():
    def __init__(self, file):

        try:
            self.automaton = self.setup(file)
            #print(__name__)
            if __name__ == "__main__":
                self.main()
            else:
                return self.automaton
        except Exception as err:
            print(err)

    def main(self):
        try:
            word = None
            end = False

            while not end:
                #path always starts at start state state
                path = [self.automaton.q]
                word = input(style.YELLOW + "Please input a word: " + style.RESET)

                accepted, newPath, t = self.automaton.run(word, path, [])

                path = newPath[::-1]

                if accepted:
                    print("String Accepted. Path:")
                    for i in range(len(path)):
                        if i % 2 != 0:
                            print(style.WHITE + "Q{}".format(path[i]),end=' ')
                        else:
                            print(style.WHITE + "Q{}".format(path[i]),end=' ')

                    print(style.RESET)

                else:
                    print("String Rejected. Path:")
                    for i in range(len(path)):
                        if i % 2 != 0:
                            print(style.WHITE + "Q{}".format(path[i]),end=' ')
                        else:
                            print(style.WHITE + "Q{}".format(path[i]),end=' ')
                    print(style.RESET)
        except Exception as e:
            print(e)


    def setup(self, file):

        try:
            states = 0
            state_table = {}
            sigma = []
            accepts = []
            t_Automaton = 'DFA' # assume until otherwise

            raw_data = []
            with open(file,'r') as f:
                for l in f:
                    raw_data.append(l)


                if len(raw_data) == 0:
                    print("File Rejected: Empty File")
                    sys.exit(0)

                # check that raw data would have an acceptable minimum of data entries
                if len(raw_data) <= 4:
                    print("File Rejected: Possibly no rules included")
                    sys.exit(0)


                #########################################################
                # extract header & check for format & value errors
                #########################################################
                if raw_data[0] == 'NFA\n':
                    t_Automaton = raw_data.pop(0)


                    if raw_data[0] == '\n':
                        sigma.append('')
                        raw_data.pop(0)
                    else:
                        # get alphabet of NFA
                        sigma = raw_data.pop(0).split()

                        # Automaton needs at least one input symbol
                        if len(sigma) < 1:
                            print("File Rejected: Needs at least one input symbol")
                            sys.exit(0)

                else:
                    # get alphabet of DFA
                    sigma = raw_data.pop(0).split()
                    # Automaton needs at least one input symbol
                    if len(sigma) < 1:
                        print("File Rejected: Needs at least one input symbol")
                        sys.exit(0)

                # strip rest of the data of '\n'
                for i in range(len(raw_data)):
                        raw_data[i] = raw_data[i].strip()




                # get amount of states
                states = raw_data.pop(0).split()

                # should be a number
                if len(states) > 1 or len(states) == 0:
                    print("File Rejected: Amount of States need to be an integer greater than zero")
                    sys.exit(0)

                # check to see if states is a number
                if not states[0].isdigit():
                    print("File Rejected: Amount of States need to be an integer greater than zero")
                    sys.exit(0)

                # cast to int
                states = int(states[0])

                # check if number is non-negative
                if states <= 0:
                    print("Amount of States need to be a single integer greater than zero")
                    sys.exit(0)

                # add states to state transition table
                for i in range(states):
                    state_table[i] = {}

                # get accept states
                accepts = raw_data.pop(0)

                if accepts == '---':
                    accepts = []
                else:
                    accepts = accepts.split()


                for i in range(len(accepts)):
                    # check that each accept state starts with a Q
                    if accepts[i][0] != 'Q':
                        print("File Rejected: Accept states need to be prefixed with 'Q'")
                        sys.exit(0)

                    # check that successive chars after 'Q' represent an integer
                    if not accepts[i][1:].isdigit():
                        print("File Rejected: State not suffixed with an integer")
                        sys.exit(0)

                    # if it is, make sure it is not negative
                    if accepts[i][1:].isdigit():
                        if int(accepts[i][1:]) < 0:
                            print("File Rejected: State suffixed with a negative integer")
                            sys.exit(0)

                    # replace 'Qx' as int('x')
                    accepts[i] = int(accepts[i][1:])


                # pop off '---'
                raw_data.pop(0)

                # raw data remaining are rules for each state

                for r in raw_data:
                    rule = r.split()

                    if len(rule) < 2 or len(rule) > 3:
                        print("File Rejected: Rule is not formatted by 2 or \
                              more parts 'Q# Q#' or 'Q# t Q#'")
                        sys.exit(0)

                    if rule[0][0] != 'Q':
                        print("File Rejected: State not prefixed with 'Q'")
                        sys.exit(0)

                    if not rule[0][1:].isdigit():
                        print("File Rejected: State not suffixed with an integer")
                        sys.exit(0)


                    if rule[0][1:].isdigit():
                        if int(rule[0][1:]) < 0:
                            print("File Rejected: State suffixed with a negative integer")
                            sys.exit(0)
                    if len(rule) == 3:
                        if len(rule[1]) > 1:
                            print("File Rejected: Rule has more than one symbol")
                            sys.exit(0)

                        if rule[1] not in sigma:
                            print("File Rejected: Rule uses a symbol not in sigma(Σ)")
                            sys.exit(0)

                        if rule[2][0] != 'Q':
                            print("File Rejected: State not prefixed with 'Q'")
                            sys.exit(0)

                        if not rule[2][1:].isdigit():
                            print("File Rejected: State not suffixed with an integer")
                            sys.exit(0)

                        if rule[2][1:].isdigit():
                            if int(rule[2][1:]) < 0:
                                print("File Rejected: State suffixed with a negative integer")
                                sys.exit(0)

                    if len(rule) == 2:
                        if rule[1][0] != 'Q':
                            print("File Rejected: State not prefixed with 'Q'")
                            sys.exit(0)

                        if not rule[1][1:].isdigit():
                            print("File Rejected: State not suffixed with an integer")
                            sys.exit(0)

                        if rule[1][1:].isdigit():
                            if int(rule[1][1:]) < 0:
                                print("File Rejected: State suffixed with a negative integer")
                                sys.exit(0)

                    q = int(rule[0][1:]) # in current state

                    if len(rule) == 2:
                        t = ''
                        if t not in sigma:
                            sigma.append(t)
                        p = int(rule[1][1:]) # state transition 't' goes to
                    else:
                        t = rule[1]          # transition available in current state
                        p = int(rule[2][1:]) # state transition 't' goes to

                    # special character tilda(~) to represent a space
                    if t == SPACE:
                        t = ' '

                    # state does not exist
                    if (q not in state_table.keys() or p not in state_table.keys()):
                        print("File Rejected: Rule uses a state number not in Q.")
                        sys.exit(0)


                    # transition not added to state's dict of transitions
                    # If file represents a dfa then each list will have one entry
                    if t not in state_table[q].keys():
                        state_table[q][t] = [p]

                    # redundant now but I'm leaving it in
                    elif t in state_table[q].keys():
                        t_Automaton = 'NFA'
                        state_table[q][t].append(p)


                # Close File
                f.close()

                # To run NFAs comment out lines below (lines: 344 - 346)
    ###############################################################################
    #           if t_Automaton == 'NFA':
    #               print("File Rejected: Automaton is a NFA")
    #               sys.exit(0)
    ###############################################################################

                return Automaton(states, sigma, state_table, 0, accepts, t_Automaton)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("No Input File Found")

        else:
            print(style.YELLOW + "Looking for {}".format(sys.argv[1]) + style.RESET)
            if exists(sys.argv[1]):
                print("{} Found!".format(sys.argv[1]))
                automata_sim((sys.argv[1]))
            else:
                print(style.RED + "{} does not exist!".format(sys.argv[1]) + style.RESET)
        print(style.RESET)

    except Exception as e:
        print(e,style.Reset)
