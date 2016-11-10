import pickle as pk
from sets import Set

#find the inversion count:
def SortCount(A):
    l = len(A)
    if l > 1:
        n = l//2
        C = A[:n]
        D = A[n:]
        C, c = SortCount(A[:n])
        D, d = SortCount(A[n:])
        B, b = MergeCount(C,D)
        return B, b+c+d
    else:
        return A, 0

def MergeCount(A,B):
    count = 0
    M = []
    while A and B:
        if A[0] <= B[0]: 
            M.append(A.pop(0)) 
        else:
            count += len(A)
            M.append(B.pop(0)) 
    M  += A + B     
    return M, count 

if __name__ == "__main__":
    k = 100

    exact_list = pk.load(open('exact_100_5.p', 'rb'))
    estimate_list = pk.load(open('exp1_05.p', 'rb'))

    exact_list = [key for (key, val) in exact_list[:k]]
    estimate_list = [key for (key, val) in estimate_list[:k]]


    exact_list_set = Set(exact_list)
    estimate_list_set = Set(estimate_list)

    false_positive = estimate_list_set.difference(exact_list_set)
    false_negative = exact_list_set.difference(estimate_list_set)

    estimate_list_elm_idx= []

    for elm in estimate_list:
        if not elm in false_positive:
            estimate_list_elm_idx.append(exact_list.index(elm))
    _, count = SortCount(estimate_list_elm_idx[:40])

    print len(false_positive)
    print len(false_negative)
    print count
