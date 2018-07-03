import environment
from environment import *
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

qfunc = {}
envir = environment()
N = 100
def monteControl(s):
    qfunc.setdefault((s.dealer_first,s.sum_player,0), {'value':0,'count':0})
    qfunc.setdefault((s.dealer_first,s.sum_player,1), {'value':0,'count':0})
    

    if qfunc[(s.dealer_first,s.sum_player,0)]['value'] > qfunc[(s.dealer_first,s.sum_player,1)]['value']:
        maxi = 0
    elif qfunc[(s.dealer_first,s.sum_player,0)]['value'] < qfunc[(s.dealer_first,s.sum_player,1)]['value']:
        maxi = 1
    else:
        maxi = np.random.choice([0,1],p=[0.5,0.5])
        
    other = np.random.choice([0,1],p=[0.5,0.5])

    s_count = qfunc[(s.dealer_first,s.sum_player,0)]['count'] + qfunc[(s.dealer_first,s.sum_player,1)]['count']
    e = N/(N+s_count)
    a = np.random.choice([maxi,other],p=[1-e,e])

    qfunc[(s.dealer_first,s.sum_player,a)]['count'] += 1

    snext,reward = envir.step(s,a)

    # print("snext",(snext.dealer_first,snext.sum_player))
    if snext == "terminal":
        gt = reward
    else:
        gt = reward +   monteControl(snext)

    # print((s.dealer_first,s.sum_player),a,s_count,e)

    
    a_count = qfunc[(s.dealer_first,s.sum_player,a)]['count']
    alpha = 1/ a_count 
    qfunc[(s.dealer_first,s.sum_player,a)]['value'] += alpha * (gt - qfunc[(s.dealer_first,s.sum_player,a)]['value']) 
    return gt

for x in range(1,10000):
    for i in range(1,11):
        for j in range(1,11):
            monteControl(state(i,j))


# print(qfunc.keys())

# for i in range(1,100000):
#     print(s.dealer_first,s.sum_player)
#     monteControl(state())
# print(len(qfunc))

keys = qfunc.keys()
# print(keys)

v = np.zeros((10,21))
v_a = np.zeros((10,21))
for key in keys:
    dealer = key[0]
    player = key[1]
    v[dealer-1][player-1] = max(qfunc[(dealer,player,0)]['value'],qfunc[(dealer,player,1)]['value'])
    if qfunc[(dealer,player,0)]['value']>=qfunc[(dealer,player,1)]['value']:
        v_a[dealer-1][player-1] = 0
    else:
        v_a[dealer-1][player-1] = 1
#     entry
# print(v)

# def f(x, y):
#     return v[x][y]

np.save("montecarlo.npy",v)

np.save("montecarloaction.npy",v_a)

x = np.linspace(0, 9, 10)
y = np.linspace(0, 20, 21)

# print(x)
# print(y)
Y,X = np.meshgrid(y,x)
print(X)
print(Y)
# print(Y)
Z = v

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y,Z, color='black')
ax.set_title('wireframe');
ax.set_xlabel('dealer first')
ax.set_ylabel('player sum')
ax.set_zlabel('value')
plt.show()

# # plot monte-carlo value func
# bestval = np.amaxi(testlooking,axis=0)
# bestval = np.amaxi(testlooking,axis=0)
# fig = plt.figure()
# ha = fig.add_subplot(111, projection='3d')
# x = range(10)
# y = range(21)
# X, Y = np.meshgrid(y, x)
# ha.plot_wireframe(X+1, Y+1, bestval[1:,1:])
# ha.set_ylabel("dealer starting card")
# ha.set_xlabel("player current sum")
# ha.set_zlabel("value of state")

