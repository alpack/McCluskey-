import itertools

def validate(strMinterms, strDontcare, strVarNum):
    valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    if strMinterms == '' or strVarNum == '':
        return False
    for i in strMinterms:
        if i not in valid:
            return False
    for i in strDontcare:
        if i not in valid:
            return False
    for i in strVarNum:
        if i not in valid:
            return False
    minterms = strMinterms.split(' ')
    dontcare = strDontcare.split(' ')
    minterms = [int(i) for i in minterms]
    if dontcare == ['']:
        dontcare = []
    else:
        dontcare = [int(i) for i in dontcare]
    varNum = int(strVarNum)
    if varNum == 1 or varNum > 26:
        return False
    if len(set(minterms)) != len(minterms):
        return False
    if len(dontcare) != 0:
        if len(set(dontcare)) != len(dontcare):
            return False
        if len(set(minterms) & set(dontcare)) != 0:
            return False
        if (2**varNum) <= max(dontcare):
            return False

    if (2**varNum) <= max(minterms):
        return False
    return minterms, dontcare

# compare two binary strings, check where there is one difference
def compBinary(s1, s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count += 1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None

# compare if the number is same as implicant term
# s1 should be the term
def compBinarySame(term, number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False

    return True

# combine pairs and make new group
def combinePairs(group, unchecked):
    # define length
    l = len(group) - 1

    # check list
    check_list = []

    # create next group
    next_group = [[] for x in range(l)]

    # go through the groups
    for i in range(l):
        # first selected group
        for elem1 in group[i]:
            # next selected group
            for elem2 in group[i+1]:
                b, pos = compBinary(elem1, elem2)
                if b == True:
                    # append the ones used in check list
                    check_list.append(elem1)
                    check_list.append(elem2)
                    # replace the different bit with '-'
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked

# remove redundant lists in 2d list
def remove_redundant(group):
    new_group = []
    for j in group:
        new = []
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group

# remove redundant in 1d list
def remove_redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list

# return True if empty
def check_empty(group):

    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count += 1
        if count == 0:
            return True
    return False

# find essential prime implicants ( col num of ones = 1)
def find_prime(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            # find essential
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime

def check_all_zero(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True

# Find max value in list
def find_max(l):
    max = -1
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index

# Multiply two terms (ex. (p1 + p2)(p1+p4+p5) )..it returns the product
def multiplication(list1, list2):
    list_result = []

    if len(list1) == 0 and len(list2) == 0:
        return list_result

    elif len(list1) == 0:
        return list2

    elif len(list2) == 0:
        return list1

    else:
        for i in list1:
            for j in list2:
                if i == j:
                    # list_result.append(sorted(i))
                    list_result.append(i)
                else:
                    # list_result.append(sorted(list(set(i+j))))
                    list_result.append(list(set(i+j)))

        list_result.sort()
        return list(list_result for list_result, _ in itertools.groupby(list_result))

# Petrick's Method
def petrick_method(Chart):
    P = []
    for col in range(len(Chart[0])):
        p = []
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                p.append([row])
        P.append(p)

    for l in range(len(P)-1):
        P[l+1] = multiplication(P[l], P[l+1])

    P = sorted(P[len(P)-1], key=len)
    final = []

    min = len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        else:
            break

    return final

def find_minimum_cost(Chart, unchecked, flag):
    P_final = []
    essential_prime = find_prime(Chart)
    essential_prime = remove_redundant_list(essential_prime)

    # Essential Prime Implicants
    if len(essential_prime) > 0:
        s = " "
        for i in range(len(unchecked)):
            for j in essential_prime:
                if j == i:
                    s = s+binary_to_letter(unchecked[i])+' , '
        if (flag == 2):
            return s[:(len(s)-3)]

    # modifiy the chart to exclude the covered terms
    for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0

    # if all zero, no need for petrick method
    if check_all_zero(Chart) == True:
        P_final = [essential_prime]
    else:
        P = petrick_method(Chart)
        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count + cal_efficient(unchecked[i])
            P_cost.append(count)

        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])

        # append prime implicants to the solution of Petrick's method
        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)
    return P_final

# calculate the number of literals
def cal_efficient(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count += 1
    return count

# print the binary code to letter
def binary_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        # if it is a range a-zA-Z
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c+'\''

        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n += 1
        # conditions for next operations
        if c == 'z' and more == False:
            c = 'A'
        elif c == 'Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1)
    return out

def solve(mintermsList, varsNum, flag):
    # put the numbers in list in int form
    minterms = list(map(int, mintermsList))
    group = [[] for x in range(varsNum+1)]

    # convert to binary
    for i in range(len(minterms)):
        minterms[i] = bin(minterms[i])[2:]
        if len(minterms[i]) < varsNum:
            # add zeros to fill the n-bits
            for j in range(varsNum - len(minterms[i])):
                minterms[i] = '0' + minterms[i]

        elif len(minterms[i]) > varsNum:
            print('\nError : Selecione o número correto de variáveis(bits)\n')
            return

        index = minterms[i].count('1')
        group[index].append(minterms[i])

    all_group = []
    unchecked = []
    # combine the pairs in series until nothing new can be combined
    while check_empty(group) == False:
        all_group.append(group)
        next_group, unchecked = combinePairs(group, unchecked)
        group = remove_redundant(next_group)

    s = ""
    for i in unchecked:
        s = s + binary_to_letter(i) + " , "
    
    if flag == 1:
        return(s[:(len(s)-3)])

    # make the prime implicant chart
    Chart = [[0 for x in range(len(minterms))] for x in range(len(unchecked))]

    for i in range(len(minterms)):
        for j in range(len(unchecked)):
            # term is same as number
            if compBinarySame(unchecked[j], minterms[i]):
                Chart[j][i] = 1
    
    if (flag == 2):
        return (remove_redundant_list(find_minimum_cost(Chart, unchecked, flag)))
    
    primes = remove_redundant_list(find_minimum_cost(Chart, unchecked, flag))
    
    for prime in primes:
        s = ''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s = s+binary_to_letter(unchecked[i])+' + '
        return s[:(len(s)-3)]
