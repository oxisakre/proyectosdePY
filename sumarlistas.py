def repeat_sum(l):
    list_number = -1
    sumar = []
    if len(l) == 1:
        return 0
    else:
        for i in l:
            list_number += 1
            for j in l[list_number]:
                for t in range(0, len(l) - 1):
                    if t == (list_number):
                        continue
                    elif j in l[t] and j not in sumar:
                        sumar.append(j)
    return sum(sumar)

repeat_sum([[16, 14, 7], [5, 7, 12, 7, 15], [10, 14, 3, 9, 13], [18, 13, 7, 17]])