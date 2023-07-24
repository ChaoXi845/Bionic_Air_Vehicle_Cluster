# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 19:09:13 2022

@author: 10208
"""
import matplotlib.pyplot as plt

fig=plt.figure()
ax=fig.add_subplot(projection='3d')
ax.quiver(0, 0,0, 0.5, -0.5,0.5,color='b') #画箭头
ax.grid()
ax.set_xlabel('X')
ax.set_xlim3d(-1, 1)
ax.set_ylabel('Y')
ax.set_ylim3d(-1, 1)
ax.set_zlabel('Z')
ax.set_zlim3d(-1, 1)
plt.show()