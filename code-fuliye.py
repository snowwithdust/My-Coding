'''
这篇代码的积分使用的是scipy,在运行中可能出现由于细分数过大而报错，
这种情况下就需要使用sympy进行积分，尽管sympy计算速度慢的多
'''


import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
import time
t1 = time.time()


#定义函数
N = 50
f = 20e3
E = 5
T = 1/f
def f(x):
    if x>=-T/2 and x<0:
        return -E/2
    else:
        return E/2


#y用列表存放函数的值
y = []
for x in np.arange(-T/2,T/2,1e-7):
    y.append(f(x))

w = 2*np.pi/T
a0 = integrate.quad(f,-T/2,T/2)[0]/T
a = []
b = []
fi = []
wn = []
c = []


for n in range(N):
    def ccos(x):
        return f(x)*np.cos(n*w*x)
	#计算an
    an = (integrate.quad(ccos,-T/2,0)[0]+ integrate.quad(ccos,0,T/2)[0])*2/T
    def ssin(x):
        return f(x)*np.sin(n*w*x)
	#计算bn
    bn = (integrate.quad(ssin,-T/2,0)[0]+ integrate.quad(ssin,0,T/2)[0])*2/T

    a.append(an)
    b.append(bn)
	#计算幅度
    c.append(np.sqrt(np.square(an)+np.square(bn)))
	#计算频率
    wn.append(n*w)
	
	#an和bn等于0的特殊情况需要另外考虑
    if an == 0:
        if bn > 0:
            fi.append(np.pi/2)
        elif bn < 0:
            fi.append(-np.pi/2)
        else:
            fi.append(0)
    else:
        fi.append(np.arctan(-bn/an))

a[0] = a0
b[0] = 0

ys = []
for x in np.arange(-T/2,T/2,1e-7):
    s = 0
    for n in range(N):
        s = s + a[n]*np.cos(n*w*x) + b[n]*np.sin(n*w*x)
	#计算傅里叶变换的函数值
    ys.append(s)

def f2(x):
    return np.square(f(x))

#奇函数特殊，只含有bn，偶函数只有an
b2= []
for i in b:
    b2.append(np.square(i))
#傅里叶拟合的误差
err = integrate.quad(f2,-T/2,T/2)[0]/T-np.cumsum(b2)/2
#误差百分比
errs = err/(integrate.quad(f2,-T/2,T/2)[0]/T)

#原函数图像和傅里叶拟合图像
plt.figure()
plt.plot(np.arange(-T/2,T/2,1e-7),y)
plt.xlabel('t')
plt.ylabel('y')

plt.plot(np.arange(-T/2,T/2,1e-7),ys)
plt.xlabel('t')
plt.ylabel('y')

#n取值不同时产生的对应误差图像和误差百分比图像
plt.figure()
plt.subplot(211)
plt.plot(np.arange(0,len(b)),err)
plt.xlabel('n')
plt.ylabel('err')

plt.subplot(212)
plt.plot(np.arange(0,len(b)),errs)
plt.xlabel('n')
plt.ylabel('errs')

#幅度谱
plt.figure()
plt.subplot(211)
markerline, stemlines, baseline = plt.stem(np.arange(0,len(c)), c, linefmt='-', markerfmt='C0.', bottom=0, use_line_collection=True)
markerline.set_markerfacecolor('none')
plt.xlabel('w')
plt.ylabel('c')
#频谱
plt.subplot(212)
markerline, stemlines, baseline = plt.stem(np.arange(0,len(fi)), fi, linefmt='-', markerfmt='C0.', bottom=0, use_line_collection=True)
markerline.set_markerfacecolor('none')
plt.xlabel('w')
plt.ylabel('fi')
'''
print(integrate.quad(f2,-T/2,T/2))
print(err)
print(errs)
print([n for n in range(len(errs)) if errs[n]<0.002])
print(b)
'''
t2 = time.time()
print(f"历时{t2-t1}")


plt.show()