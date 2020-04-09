import numpy as np
import matplotlib.pyplot as plt


x=np.linspace(0,10,100)
yorg=np.sin(x)
y=np.sin(x)+np.random.randn(100)*0.2

num=5#移動平均の個数
b=np.ones(num)/num

y2=np.convolve(y, b, mode='same')#移動平均

plt.plot(x,yorg,'r',label='original sin')
plt.plot(x,y,'k-',label='元系列')
plt.plot(x,y2,'b--', label='移動平均')
plt.legend()
plt.show()
