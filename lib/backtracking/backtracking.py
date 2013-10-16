import json

def all_perms(elements):
# http://code.activestate.com/recipes/252178/
# http://stackoverflow.com/questions/104420/how-to-generate-all-permutations-of-a-list-in-python
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                #nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]

def pprint(json_data):
    return json.dumps(json_data, sort_keys=True,
                      indent=4, separators=(',', ': '))

vms = [
{'_id': '1', 'cpu': 10, 'net': 80, 'io': 10},
{'_id': '2', 'cpu': 20, 'net': 35, 'io': 80},
{'_id': '3', 'cpu': 15, 'net': 15, 'io': 20},
{'_id': '4', 'cpu': 12, 'net': 5, 'io': 10},
{'_id': '5', 'cpu': 5, 'net': 25, 'io': 15},
]

hosts = [
{'_id': '1', 'cpu': 0, 'net': 0, 'io': 0},
{'_id': '2', 'cpu': 0, 'net': 0, 'io': 0},
{'_id': '3', 'cpu': 0, 'net': 0, 'io': 0},
{'_id': '4', 'cpu': 0, 'net': 0, 'io': 0},
{'_id': '5', 'cpu': 0, 'net': 0, 'io': 0},
]
pprint(vms)

p = all_perms(vms)

i = 1
end = False
while not end:
    try:
        print('permutation {}: {}'.format(i, pprint(p.next())))
        i += 1
    except:
        end = True
