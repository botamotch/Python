import matplotlib.pyplot as plt
import numpy as np

class Cube:
    def __init__(self):
        self.p = []
        self.l = []
        self.mapped_p = []
        for i in range(16):
            self.p.append(np.array([(-1)**i, (-1)**(i//2), (-1)**(i//4), (-1)**(i//8)],dtype=float))
            self.mapped_p.append(np.array([(-1)**i, (-1)**(i//2), (-1)**(i//4)],dtype=float))
        for i in range(16):
            for j in range(i+1,16):
                LEN = [0 for m in range(4) if self.p[i][m] != self.p[j][m]]
                if len(LEN) == 1:
                    self.l.append((i,j))

    def rotation(self, ax1=0, ax2=1, angle=0.0):
        '''
        ax1, ax2 = 0 - 3 and ax1 and ax2 must not be equal
        angle [radian]
        '''
        if ax1 != ax2:
            rot_mat = np.identity(n=4,dtype=float)
            rot_mat[ax1%4][ax1%4] =  np.cos(angle*np.pi)
            rot_mat[ax1%4][ax2%4] = -np.sin(angle*np.pi)
            rot_mat[ax2%4][ax1%4] =  np.sin(angle*np.pi)
            rot_mat[ax2%4][ax2%4] =  np.cos(angle*np.pi)
            for i in range(16):
                self.p[i] = np.dot(self.p[i], rot_mat)
                self.mapped_p[i] = self.p[i][0:3]

c = Cube()

# 投影行列の作成
# 透視投影変換を使用、視点はX軸上に限定
def projection(p):
    SIGHT = np.array([ -5., 0., 0.])
    SCREEN = np.array([0., 0., 0.])
    a = (SCREEN[0] - SIGHT[0])/(p[0] - SIGHT[0])
    p_d = np.array([
        SIGHT[1] + (p[1] - SIGHT[1]) * a,
        SIGHT[2] + (p[2] - SIGHT[1]) * a
    ])
    return p_d

# プロットオブジェクトの作成、本当は枠消したい
fig, axs = plt.subplots(1, 1, figsize=(6, 6))
dot, = axs.plot([], [], marker='o', linestyle='None', color='blue')
axs.set_xlim(-2, 2)
axs.set_ylim(-2, 2)
axs.tick_params(labelbottom=False,bottom=False) # x軸の削除
axs.tick_params(labelleft=False,left=False) # y軸の削除
axs.set_xticklabels([]) 
fig.tight_layout()

line = []
for i in c.l:
    l, = axs.plot([], [], marker='None', linestyle='-', color='blue')
    line.append(l)

for j in range(200):
    c.rotation(0, 3, 0.007)
    c.rotation(1, 3, 0.007)
    c.rotation(2, 3, 0.007)

    X_D = [projection(v)[0] for v in c.mapped_p]
    Y_D = [projection(v)[1] for v in c.mapped_p]

    dot.set_data(X_D, Y_D)
    for i, l in enumerate(c.l):
        line[i].set_data([X_D[l[0]], X_D[l[1]]], [Y_D[l[0]], Y_D[l[1]]])

    fig .savefig('./figure/{0:04d}.png'.format(j))

# fig.show()
