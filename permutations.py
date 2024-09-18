def permutations(s):
    if len(s) == 1:
        return [s]
    perms = set()
    for i, char in enumerate(s):
        rest = s[:i] + s[i+1:]
        for p in permutations(rest):
            perms.add(char + p)
    return list(perms)