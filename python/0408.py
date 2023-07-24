# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:06:35 2022

@author: 10208
"""

import numpy as np
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from progressbar import ProgressBar as PB


def rotate_towards(vi, vf, theta):
    x = np.cross(vi, vf)
    _x_ = np.linalg.norm(x)
    if _x_ < 1e-15:
        return vi
    else:
        x /= _x_
    A = np.array([[0, -x[2], x[1]],
                  [x[2], 0, -x[0]],

                  [-x[1], x[0], 0]])
    c, s = np.cos(theta), np.sin(theta)
    R = np.eye(3) + s * A + (1 - c) * A.dot(A)

    return R.dot(vi)


def cart2sphere(v):
    """
    Return the spherical angles `theta` and `phi` associated with a unit vector `v`.
    """
    # v needs to be a unit vector
    x, y, z = v
    theta = np.arccos(np.clip(z, -1, 1))
    phi = np.arctan2(x, y)

    return theta, phi


def sphere2cart(theta, phi):
    """
    Return the unit vector `v` associated with angles `theta` and `phi`.
    Adjusts `theta` and `phi` such that the transformation is valid
    """
    if theta < 0:
        theta = np.pi + theta
        phi += np.pi
    elif theta > np.pi:
        theta = theta - np.pi
        phi += np.pi
    st, sp = np.sin(theta), np.sin(phi)
    ct, cp = np.cos(theta), np.cos(phi)
    x = st * sp
    y = st * cp
    z = ct

    return np.array([x, y, z])


class Bird:
    """扑翼机
      
    扑翼机的信息主要包括所处位置和下一步的速度向量

    具体属性
    ----------
        position : numpy.ndarray
            目前扑翼机所处三维空间的具体位置
        direction : numpy.ndarray
            扑翼机下一步的三维单位速度向量
        d_r : numpy.ndarray
            排斥区区域
        n_r : int
            排斥区内扑翼机的数量
        d_o : numpy.ndarray
            取向区区域
        n_o : int
            取向区内扑翼机的数量
        d_a : numpy.ndarray
            吸引区区域
        n_a : int
            吸引区内扑翼机的数量
    """

    def __init__(self, position, direction=None, ID=None, verbose=False):
        """
        Initiate a Bird object

        Parameters
        ----------
        position : numpy.ndarray
            三维空间具体位置
        direction : numpy.ndarray, default : None
            扑翼机的运动方向
            三维单位速度向量
        ID : any type, default : None
            扑翼机编号
        verbose : bool, default : False
            be chatty
        """

        self.position = position

        if direction is None:
            self.direction = np.random.randn(3)
            self.direction /= np.linalg.norm(self.direction)
        else:
            self.direction = direction / np.linalg.norm(direction)

        self.ID = ID
        self.verbose = verbose
        self.reset_direction_influences()

    def reset_direction_influences(self):
        """
        重置下一时间的速度向量
        """

        self.d_r = np.zeros(3, dtype=float)
        self.d_o = np.zeros(3, dtype=float)
        self.d_a = np.zeros(3, dtype=float)
        self.n_r = 0
        self.n_a = 0
        self.n_o = 0

    def zor_update(self, r_ij):
        """
        排斥区内扑翼机的影响

        参数
        ----------
        r_ij : numpy.ndarray
           排斥区指向另一扑翼机的单位速度向量
        """

        self.d_r = self.d_r - r_ij
        self.n_r += 1

    def zoo_update(self, v_j):
        """
        取向区内扑翼机的影响

        参数
        ----------
        v_j : numpy.ndarray
            取向区指向另一扑翼机的单位速度向量
        """

        self.d_o = self.d_o + v_j
        self.n_o += 1

    def zoa_update(self, r_ij):
        """
        吸引区内扑翼机的影响

        参数
        ----------
        r_ij : numpy.ndarray
           吸引区指向另一扑翼机的单位速度向量
        """

        self.d_a = self.d_a + r_ij
        self.n_a += 1

    def evaluate_direction(self, thetatau, sigma):
        """
        按Couzin模型生成下一速度，并添加噪音
        返回新方向的单位速度向量

        参数
        ----------
        thetatau : float
            每个时间步长允许旋转的最大角度
        sigma : float
            噪声的标准偏差将影响生成的新速度

        Returns
        -------
        new_d : numpy.ndarray
           新生成的单位速度向量
        """

        no_new_d = False

        if self.n_r > 0:
            new_d = self.d_r
        elif self.n_o > 0 and self.n_a > 0:
            new_d = 0.5 * (self.d_o + self.d_a)
        elif self.n_o > 0:
            new_d = self.d_o
        elif self.n_a > 0:
            new_d = self.d_a
        else:
            new_d = self.direction

        if self.verbose:
            print("Bird", self.ID)
            print("    direction:", self.direction)
            print("    repulsion:", self.n_r, self.d_r)
            print("    orientation:", self.n_o, self.d_o)
            print("    attraction:", self.n_a, self.d_a)
            print("    new_d:", new_d)

        # 得到方向的球面坐标，并在角度上添加一些噪音
        _theta, _phi = cart2sphere(new_d)
        _theta += sigma * np.random.randn()
        _phi += sigma * np.random.randn()
        self.new_d = sphere2cart(_theta, _phi)
        self.new_d /= np.linalg.norm(self.new_d)

        # 如果新旧方向之间的角度大于每个步长尺寸允许的角度，则将当前方向向新方向旋转每个步长的最大弧度
        angle = np.arccos(np.clip(np.dot(self.new_d, self.direction), -1.0, 1.0))
        if angle > thetatau:
            self.new_d = rotate_towards(self.direction, self.new_d, thetatau)

        if self.verbose:
            print("    after noise and rotation:", new_d)

        self.reset_direction_influences()

        return self.new_d


# note: 空间的维度以扑翼机来衡量

class Swarm:
    """用于Swarm模拟
    
    参数
    ----------
    number_of_bird : int, default : 8
        扑翼机实验数
    bird : list of :mod:`couzinswarm.objects.Bird`
        Contains the `Bird` objects which are simulated in this setup.
    repulsion_radius : float, default : 1.0
        扑翼机的排斥半径
        (单位：一个扑翼机的长度).
    orientation_width : float, default : 10.0
        取向区宽度
        (单位：一个扑翼机的长度).
    attraction_width : float, default : 10.0
        吸引区宽度
        (单位：一个扑翼机的长度).
    angle_of_perception : float, default : 340/360*pi
        扑翼机的观测角度
        (单位: 幅度, with a maximum value of :math:`\pi`.
    turning_rate : float, default : 0.1
        转向角速度
        单位时间的转向角度为 ``turning_rate * dt``
        (单位：幅度每单位时间).
    speed : float, default : 0.1
        扑翼机的速度
        (单位: 单位时间扑翼机长度).
    noise_sigma : float, default : 0.01
        径向噪声的标准偏差。每个方向调整的标准偏差
        (单位: 幅度).
    dt : float, default : 0.1
        时间步长
        (单位: 单位时间).
    box_lengths : list or numpy.ndarray of float, default : [100,100,100]
        仿真实验区域大小
        (单位: 一个扑翼机的长度)
    reflect_at_boundary ：list of bool, default : [True, True, True]
        对于每个空间维度决定边界是否应该反射。
        如果它们不反射，就被认为是周期性的（还没有实现）
    verbose : bool, default : False
        be chatty.
    show_progress : bool, default : False
        显示模拟的进度。

    """

    def __init__(self,
                 number_of_bird=8,
                 repulsion_radius=1,
                 orientation_width=10,
                 attraction_width=10,
                 angle_of_perception=340 / 360 * np.pi,
                 turning_rate=0.1,
                 speed=0.1,
                 noise_sigma=0.01,
                 dt=0.1,
                 box_lengths=[100, 100, 100],
                 reflect_at_boundary=[True, True, True],
                 verbose=False,
                 show_progress=False,
                 ):
        self.number_of_bird = number_of_bird
        self.repulsion_radius = repulsion_radius
        self.orientation_width = orientation_width
        self.attraction_width = attraction_width
        self.angle_of_perception = angle_of_perception
        self.turning_rate = turning_rate
        self.speed = speed
        self.noise_sigma = noise_sigma
        self.dt = dt
        self.box_lengths = np.array(box_lengths, dtype=float)
        self.reflect_at_boundary = reflect_at_boundary
        self.verbose = verbose
        self.show_progress = show_progress
        self.box_copies = [[0.], [0.], [0.]]

        for dim, reflect in enumerate(self.reflect_at_boundary):
            if not reflect:
                self.box_copies[dim].extend([-self.box_lengths[dim], +self.box_lengths[dim]])

        self.bird = []

        self.init_random()

    def init_random(self):
        """
        扑翼机列表
        """

        self.bird = [Bird(position=self.box_lengths * np.random.random((3,)),
                          ID=i,
                          verbose=self.verbose
                          ) for i in range(self.number_of_bird)]

    def simulate(self, N_time_steps):
        """按规则模拟扑翼机集群

        参数
        ----------
        N_time_steps : int
           模拟时间部属

        Returns
        -------
        positions : numpy.ndarray of shape ``(self.number_of_fish, N_time_steps+1, 3_)``
            每个扑翼机在每个时间步长的空间位置
        directions : numpy.ndarray of shape ``(self.number_of_fish, N_time_steps+1, 3_)``
            每个扑翼机在每个时间步长的速度向量
        """

        # 创建结果数组并填入初始位置
        positions = np.empty((self.number_of_bird, N_time_steps + 1, 3))
        directions = np.empty((self.number_of_bird, N_time_steps + 1, 3))
        for i in range(self.number_of_bird):
            positions[i, 0, :] = self.bird[i].position
            directions[i, 0, :] = self.bird[i].direction

        # 进度条
        bar = PB(maxval=N_time_steps)
        # 每个时间步长下
        for t in range(1, N_time_steps + 1):

            # 遍历扑翼机
            for i in range(self.number_of_bird - 1):
                B_i = self.bird[i]
                r_i = B_i.position
                v_i = B_i.direction

                for j in range(i + 1, self.number_of_bird):

                    B_j = self.bird[j]
                    relationship_counted = False

                    for X in self.box_copies[0]:

                        if relationship_counted:
                            break

                        for Y in self.box_copies[1]:
                            for Z in self.box_copies[2]:

                                r_j = B_j.position + np.array([X, Y, Z])
                                v_j = B_j.direction

                                # 得到他们之间的距离以及单位方向向量
                                r_ij = (r_j - r_i)
                                distance = np.linalg.norm(r_ij)
                                r_ij /= distance
                                r_ji = -r_ij

                                # 位于排斥区，添加斥力
                                if distance < self.repulsion_radius:
                                    B_i.zor_update(r_ij)
                                    B_j.zor_update(r_ji)
                                    relationship_counted = True
                                elif distance < self.repulsion_radius + self.orientation_width + self.attraction_width:

                                    # 位于取向区和吸引区，首先判断是否在视野内
                                    angle_i = np.arccos(np.clip(np.dot(r_ij, v_i), -1.0, 1.0))
                                    angle_j = np.arccos(np.clip(np.dot(r_ji, v_j), -1.0, 1.0))

                                    if self.verbose:
                                        print("angle_i", angle_i, self.angle_of_perception)
                                        print("angle_j", angle_j, self.angle_of_perception)

                                    # 如果i能看见j,添加j的影响
                                    if angle_i < self.angle_of_perception:
                                        if distance < self.repulsion_radius + self.orientation_width:
                                            B_i.zoo_update(v_j)
                                        else:
                                            B_i.zoa_update(r_ij)

                                    # 如果j能看见i，添加i的影响
                                    if angle_j < self.angle_of_perception:
                                        if distance < self.repulsion_radius + self.orientation_width:
                                            B_j.zoo_update(v_i)
                                        else:
                                            B_j.zoa_update(r_ji)

                                    relationship_counted = True

            # 对每个扑翼机
            for i in range(self.number_of_bird):

                B_i = self.bird[i]

                # 评估新的需求方向，并重置影响。
                new_v = B_i.evaluate_direction(self.turning_rate * self.dt, self.noise_sigma)

                # 根据方向评估所需的位置变化
                dr = self.speed * new_v * self.dt

                # 检查边界条件
                for dim in range(3):

                    # 如果新的位置超出边界
                    if dr[dim] + B_i.position[dim] > self.box_lengths[dim] or \
                            dr[dim] + B_i.position[dim] < 0.0:

                        # 如果这个边界是周期性的
                        if not self.reflect_at_boundary[dim]:
                            if dr[dim] + B_i.position[dim] > self.box_lengths[dim]:
                                dr[dim] -= self.box_lengths[dim]
                            else:
                                dr[dim] += self.box_lengths[dim]
                        else:
                            # 如果这个边界是反射性的
                            dr[dim] *= -1
                            new_v[dim] *= -1

                # 更新位置和方向
                B_i.position += dr
                B_i.direction = new_v

                # 保存位置和方向
                positions[i, t, :] = B_i.position
                directions[i, t, :] = B_i.direction

            # bar.update(t)

        return positions, directions


swarm = Swarm(
    number_of_bird=8,
    repulsion_radius=1,
    orientation_width=10,
    attraction_width=10,
    # 这个角度是以弧度为单位的，最高为pi（而不是像论文中的360度）。
    angle_of_perception=np.pi,
    # 每单位时间的弧度
    turning_rate=0.1,
    # 单位时间内扑翼机长度
    speed=0.1,
    # 以扑翼机长度为单位
    noise_sigma=0.1,
    dt=0.1,
    # 仿真环境大小
    box_lengths=[100, 100, 100],
    # 边界条件
    reflect_at_boundary=[True, True, True],
    verbose=False,
)

fig = pl.figure()
ax = fig.add_subplot(fc='whitesmoke',
                     projection='3d')

N_t = 100

t = np.arange(N_t + 1)

# Note that r.shape = v.shape = ( N_fish, N_t+1, 3 )
positions, directions = swarm.simulate(N_t)
r, v = positions, directions

for i in range(swarm.number_of_bird):
    ax.plot(r[i, 100, 0], r[i, 100, 1], r[i, 100, 2], 'b.')
    ax.quiver(r[i, 99, 0], r[i, 99, 1], r[i, 99, 2], r[i, 100, 0], r[i, 100, 1], r[i, 100, 2])

pl.show()
