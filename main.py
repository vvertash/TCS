# Depth First Search algorithm. It uses for checking disjoined states and states which are not reachable from the initial state
def dfs(graph, init_st, used):
    used.append(init_st)
    for i in range(len(states)):
        if (graph[states.index(init_st)][i] == 1) and (states[i] not in used):
            dfs(graph, states[i], used)

# function which translate a FSA to a regular expression using formula
def reg_exp(k, i, j):
    result = '(' + str(steps[i][k]) + ')' + '(' + str(steps[k][k]) + ')*' + '(' + str(steps[k][j]) + ')'\
             + '|' + '(' + str(steps[i][j]) + ')'
    return result

# opening an input file
input = open('fsa.txt', 'r')

# opening an output file
output = open('result.txt', 'w+')

# variable for working with different line in input file
lin = 1

# array for states
states = []

# array for alphabet
alpha = []

# variable of initial state
init_st = ''

# array for final states
fin_st = []

first_trans = ()
transit = []

# array for transitions
trans = []

# array for understanding which states are already visited in DFS
used = []

fsa_in = [[], []]
fsa_out = [[], []]

# graph array
graph = [[], []]

# variable of checking - are there final states
empt = 0

# array for understanding is there is an error and which one
errors = [1, 0, 0, 0, 0, 0, 0]

# array to see which states aren't in the set of states
err1 = []

# array to see which transitions aren't in the alphabet
err3 = []

# array for checking if FSA deterministic or not
deterministic_checker = []

# reading and parsing an input file
for line in input:
    if lin == 1:
        if line[0:8] != 'states={':
            errors[5] = 1
        else:
            line = line.replace('states={', '')
            line = line.replace(' ', '')
            line = line.replace('}', '')
            line = line.replace('\n', '')
            states = line.split(',')
            lin += 1
    elif lin == 2:
        if line[0:7] != 'alpha={':
            errors[5] = 1
        else:
            line = line.replace('alpha={', '')
            line = line.replace(' ', '')
            line = line.replace('}', '')
            line = line.replace('\n', '')
            alpha = line.split(',')
            lin += 1
    elif lin == 3:
        if line[0:9] != 'init.st={':
            errors[5] = 1
        else:
            line = line.replace('init.st={', '')
            line = line.replace(' ', '')
            line = line.replace('}', '')
            line = line.replace('\n', '')
            init_st = line
            lin += 1
    elif lin == 4:
        if line[0:8] != 'fin.st={':
            errors[5] = 1
        else:
            line = line.replace('fin.st={', '')
            line = line.replace(' ', '')
            line = line.replace('}', '')
            line = line.replace('\n', '')
            fin_st = line.split(',')
            lin += 1
    elif lin == 5:
        if line[0:7] != 'trans={':
            errors[5] = 1
        else:
            line = line.replace('trans={', '')
            line = line.replace(' ', '')
            line = line.replace('}', '')
            line = line.replace('\n', '')
            transit = line.split(',')
            for q in transit:
                first_trans = q.split('>')
                trans.append(first_trans)

# checking - is array of final states empty
if fin_st == ['']:
    empt = 1

# checking first error - is there an initial state in the set of states
if states.count(init_st) == 0:
    errors[1] = 1
    err1.append(init_st)

# checking first error - are there all final states in the set of states
for i in fin_st:
    if i != '' and states.count(i) == 0:
        errors[1] = 1
        err1.append(fin_st)

# checking first error - are there all states from transitions in the set of states
for i in trans:
    for j in i:
        if i.index(j) != 1:
            if states.count(j) == 0:
                errors[1] = 1
                err1.append(j)

# checking forth error - is there an initial state
if init_st == '':
    errors[4] = 1

# inserting states in a graph
for i in range(len(states)):
    fsa_in.append([])
    fsa_out.append([])
    for j in range(len(states)):
        fsa_in[i].append(0)
        fsa_out[i].append(0)

graph.append([])
graph.append([])
for i in range(len(states)):
    for j in range(len(states)):
        graph[i].append(0)

# checking third error - are there all transitions in the alphabet
for i in trans:
    for j in i:
        x = False
        for k in alpha:
            if (j == k) or (i.index(j) % 2 == 0):
                x = True
        if not x:
            errors[3] = 1
            err3.append(j)

# using DFS see are some states disjoined or not
for i in trans:
    #  indexes of two joined states in transition
    x = i[0]
    y = i[2]
    # filling the graph
    graph[states.index(x)][states.index(y)] = 1
    graph[states.index(y)][states.index(x)] = 1
    # DFS call
    dfs(graph, init_st, used)

# checking second error - are some states disjoined or not
for i in states:
    if i not in used and states.index(i) < 2:
        errors[2] = 1

# checking sixth error - is a FSA deterministic or not
for i in trans:
    for j in trans:
        if (i[0] == j[0]) and (i[1] == j[1]) and (i[2] != j[2]):
            errors[6] = 1

# array for regular expressions of states on every step
steps = []

# filling graphs with states
for i in range(len(states)):
    steps.append([])
    for j in range(len(states)):
        if i != j:
            # every regular expression is empty in the beginning
            steps[i].append('{}')
        else:
            steps[i].append('eps')

# filling matrix with regular expressions by results of the -1 step
for i in range(len(alpha)):
    for j in range(len(states)):
        for l in range(len(trans)):
            if (states[j] == trans[l][2]) and (alpha[i] == trans[l][1]):
                index1 = states.index(trans[l][0])
                index2 = states.index(trans[l][2])
                # if cell is empty then adding an expression
                if (steps[index1][index2]) == '{}':
                    steps[index1][index2] = str(alpha[i])
                else:
                    # add | and second part of an expression
                    steps[index1][index2] = str(steps[index1][index2]) + '|' + str(alpha[i])

                # adding |eps if it is an initial state
                if ((steps[index1][index2]) != '{}') and (trans[l][0] == trans[l][2]):
                    steps[index1][index2] = steps[index1][index2].replace('|eps', '')
                    steps[index1][index2] = steps[index1][index2].replace('eps|', '')
                    steps[index1][index2] += '|eps'

for l in range(len(states)):
    a = 0
    # array for updating the matrix with regular expressions
    new_states = []
    for i in range(len(steps)):
        for j in range(len(steps)):
            # calling function to form a new regular expression
            new_states.append(reg_exp(l, i, j))
    for i in range(len(steps)):
        # updating matrix
        for j in range(len(steps)):
            steps[i][j] = new_states[a]
            a += 1


# writing an output - errors or regular expression
answer = ''
if (errors[1] == 1 or errors[2] == 1 or errors[3] == 1 or errors[4] == 1 or errors[5] == 1 or errors[6] == 1):
    output.write('Error:')
    if (errors[1] == 1):
        for i in err1:
            output.write('\nE1: A state ' + str(i) + ' is not in set of states')
    if (errors[2] == 1):
        output.write('\nE2: Some states are disjoint')
    if (errors[3] == 1):
        for i in err3:
            output.write('\nE3: A transition ' + str(i) + ' is not represented in the alphabet')
    if (errors[4] == 1):
        output.write('\nE4: Initial state is not defined')
    if (errors[5] == 1):
        output.write('\nE5: Input file is malformed')
    if (errors[6] == 1):
        output.write('\nE6: FSA is nondeterministic')
else:
    # if there is no final state
    if empt == 1:
        output.write('{}')
    else:
        # writing a regular expression for every final state
        for i in range(len(fin_st)):
            if i != 0:
                answer += '|'
            answer += steps[states.index(init_st)][states.index(fin_st[i])]
        output.write(answer)