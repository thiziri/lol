from numpy import *
import math
import matplotlib.pyplot as plt
import numpy as np

#t = linspace(0,2*math.pi,400)
print("begin:")
t = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
#a = sin(t)
a = [0.2048,0.231,0.2375,0.2389,0.2387,0.2386,0.2385,0.2384,0.2381]
#b = cos(t)
b = [0.2222,
0.2385,
0.2403,
0.2403,
0.24,
0.2399,
0.2398,
0.2396,
0.2393
]
#c = a + b

plt.plot(t,a,'r') # plotting t,a separately
plt.plot(t,b,'b') # plotting t,b separately  
#plt.ylabel('MAP') 
plt.title("map developpement")
#plt.xlabel('\u0391')
#plt.plot(t,c,'g') # plotting t,c separately 
plt.show()