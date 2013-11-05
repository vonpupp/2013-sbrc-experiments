import scipy.stats
#x = [[1,3,2,5,7], [2,8,1,6,9,4], [12,5,7,9,11]]
x = [1,3,2,5,7, 2,8,1,6,9,4, 12,5,7,9,11]
a2, critical, sig = scipy.stats.anderson(x)
print('a2={}'.format(a2))
print('critical={}'.format(critical))
print('sig={}'.format(sig))

