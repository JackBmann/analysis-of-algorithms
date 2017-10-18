# Homework 1 - Jack Baumann - Sept. 7, 2017
from sys import stdin
from math import floor, sqrt

# Problem 1 Part A
print("Problem 1 Part A")
print("Enter the number of integers to tensor against each other: ")
k = int(stdin.readline())
# If k > 10 the tensor product is somewhat useless because products will have different numbers of digits.
A, B = [], []
for j in range(k):
    A.append(j)
    B.append(j)

print("Enter the number of iterations of the tensor product on " + str(B) + " to print: ")
n = int(stdin.readline())

# Recursively applies the tensor product for a given number of iterations
def tensorRecursive(vs, ws, num):
    temp = []
    # Base case: n = 0, return the singular strings to be concatenated
    if num == 0:
        return vs
    else:
        # Concatenate each number from ws onto the recursively generated vs
        for v in vs:
            for w in ws:
                temp.append(str(v) + str(w))
        # Recursively call giving the built list, base list, and num-1
        return tensorRecursive(temp, ws, num-1)

print(tensorRecursive(A, B, n))


# Problem 2 Part A
print("\nProblem 2 Part A")
print("Enter the number of pairs to enumerate up to: ")
p = int(stdin.readline())

# Solves for x and y given z as detailed on the Wikipedia Pairing Function article
def solve(z):
    w = floor((sqrt(8 * z + 1) - 1) / 2)
    t = (w * w + w) / 2
    y = z - t
    x = w - y
    return x, y

pairs = []
# Solve for x and y for each point up until point p and append each one to a list to be printed
for i in range(p):
    x, y = solve(i * 1.0)
    pairs.append(str(int(i)) + ": (" + str(int(x)) + ", " + str(int(y)) + ")")
print(pairs)


# Problem 3 Part A
print("\nProblem 3 Part A")
# Recursively applies the tensor product for a given number of iterations by the Divide and Conquer strategy
def tensorDivideAndConquer(vs, num):
    # Base case: n = 0, return the singular strings to be concatenated
    if num == 0:
        return vs
    # If n is odd then there are an even number of divisions needed
    elif num % 2 == 1:
        temp = []
        # Find the tensors of the num/2 iteration
        divided = tensorDivideAndConquer(vs, floor(num / 2))
        # Concatenate the tensors of the num/2 iteration together, add them to a list, and return the list
        for w in divided:
            for v in divided:
                temp.append(str(w) + str(v))
        return temp
    # If n is even then there are an odd number of divisions need and the permutations must be divided into even parts
    # and the tensor product must be applied one last time to the result.
    else:
        temp1, temp2 = [], []
        # Find the tensors of the (num-1)/2 iteration
        divided = tensorDivideAndConquer(vs, floor((num - 1) / 2))
        # Concatenate the tensors of the (num-1)/2 iteration together and add them to a list
        for w in divided:
            for v in divided:
                temp1.append(str(w) + str(v))
        # Do one last tensor product on the results because the number of divisions is odd, then return the result
        for w in temp1:
            for v in vs:
                temp2.append(str(w) + str(v))
        return temp2

print(tensorDivideAndConquer(A, n))
