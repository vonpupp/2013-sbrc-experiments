def possible_solution(remaining, sol=None):
    sol = sol or []
    if not remaining:
        yield sol
    else:
        for i, candidate in enumerate(remaining):
            if not sol or abs(sol[-1] - candidate) != 1:
                new_sol = sol + [candidate]
                new_remaining = remaining[:i] + remaining[i+1:]
                for x in possible_solution(new_remaining, new_sol):
                    yield x


def possible_solutions(neighbors):
    for solution in possible_solution(neighbors):
        print solution

print '-' * 30
possible_solutions([1, 2, 3])

print '-' * 30
possible_solutions([1, 2, 3, 4])

print '-' * 30
possible_solutions([1, 2, 3, 4, 5])
