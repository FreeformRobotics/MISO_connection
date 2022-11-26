# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np
from planning import Configuration

import roboticstoolbox as rtb
from spatialmath import SE3
from roboticstoolbox import ETS as E

from scipy.spatial.transform import Rotation
from planning.Matrix2tree import Matrix2tree
from anytree import PostOrderIter
from anytree.walker import Walker

RADIUS = 0.06
DIAMETER = 2 * RADIUS
POINT_ACCU=0.05*RADIUS
T_NUM = 50

NUM_MODULES=30


# This class represents the robot system, not the configuration
class robots():

    def __init__(self,model_states):
        self.finished = False
        self.set_current_configuration(model_states)

    def set_current_configuration(self, model_states):
        self.current_configuration = Configuration.configuration()
        self.current_configuration.current_config(model_states)


    def quad_I(self, dim):
        I = np.identity(dim)
        for i in range(1, dim):
            I[-i, :] = I[-(i + 1)]
        I[0, :] = 0

        return I

    def three(self, dim):
        I = np.identity(dim)
        for i in range(1, dim):
            I[-i, :] = I[-(i + 1)]
        I[0, :] = 0
        I[20, :] = 0
        I[20, 10] = 1

        return I

    def four(self, dim):
        I = np.identity(dim)
        for i in range(1, dim):
            I[-i, :] = I[-(i + 1)]
        I[0, :] = 0
        I[18, :] = 0
        I[18, 12] = 1
        I[24, :] = 0
        I[24, 12] = 1
        return I

    def four1(self, dim):
        I = np.identity(dim)
        for i in range(1, dim):
            I[-i, :] = I[-(i + 1)]
        I[0, :] = 0
        I[0, 6]=1
        I[3,:]=0

        I[18, :] = 0
        I[18, 12] = 1
        I[24, :] = 0
        I[24, 12] = 1
        return I

    def four2(self, dim):
        I = np.identity(dim)
        for i in range(1, dim):
            I[-i, :] = I[-(i + 1)]
        I[0, :] = 0
        I[0, 6]=1
        I[3,:]=0

        I[18, :] = 0
        I[18, 12] = 1
        I[24, :] = 0
        I[24, 12] = 1
        I[29, :] = 0
        I[29, 17] = 1
        return I

    def generate_T(self,dim):
        C = self.four2(dim)
        # C=Matrix_gen_tree(dim, 3)
        T = Matrix2tree(C, 'current')
        T.matrix2tree(printer=False)
        T.CNL_cal()
        T.Pointer()
        T.tree_render(printer=True, draw=False)
        return T

    def initial_cons(self, T):
        T.nodes[T.roots[0]].pose.append(np.array([0, 0, 0]))
        T.nodes[T.roots[0]].pose.append(np.array([0, 0, 0, 1]))

        for node in PostOrderIter(T.nodes[T.roots[0]]):
            if node.ID==T.roots[0]:
                continue
            node.pose.append(np.array([0, 0, 2*RADIUS]))
            node.pose.append(np.array([0, 0, 0, 1]))
        return T


    def step(self):

        T = self.generate_T(NUM_MODULES)

        T = self.initial_cons(T)

        for i in range(NUM_MODULES):
            T.nodes[i].pose[0]=self.current_configuration.config[i].position
            T.nodes[i].pose[1]=self.current_configuration.config[i].orientation

        for node in PostOrderIter(T.nodes[T.roots[0]]):
            if node.ID==T.roots[0]:
                continue
            child_r=Rotation.from_quat(node.pose[1])
            child_T=SE3.Rt(child_r.as_matrix(), node.pose[0])
            parent_r = Rotation.from_quat(node.parent.pose[1])
            parent_T = SE3.Rt(parent_r.as_matrix(), node.parent.pose[0])
            relative_T=parent_T.inv()*child_T

            node.pose[0]=relative_T.t
            relative_r=Rotation.from_matrix(relative_T.R)
            node.pose[1]=relative_r.as_quat()

        # w=Walker()
        # for node in PostOrderIter(T.nodes[T.roots[0]]):
        #     if node.ID==T.roots[0]:
        #         continue
        #     e = E()
        #     path=w.walk(T.nodes[0],node)
        #     for node_p in path[2]:
        #         e_r = Rotation.from_quat(node_p.pose[1])
        #         e_T = SE3.Rt(e_r.as_matrix(), node_p.pose[0])
        #         e = e * E.SE3(e_T) * E.rz() * E.rx()
        #     node.robot=rtb.ERobot(e)

        start_end=[13, 14, 15, 16, 17, 29]
        T_end = SE3(0, -0.3, 1.9) * SE3.Rx(97, unit='deg') * SE3.Ry(0, unit='deg') * SE3.Rz(0, unit='deg')# SE3.OA([0,0,1], [0,1,0])
        #T_end for start_end

        e_r = Rotation.from_quat(self.current_configuration.config[12].orientation)
        e_T = SE3.Rt(e_r.as_matrix(), self.current_configuration.config[12].position)
        mid_chain=E.SE3(e_T)
        chains=[]
        for i in start_end:
            e_r = Rotation.from_quat(T.nodes[i].pose[1])
            e_T=SE3.Rt(e_r.as_matrix(), T.nodes[i].pose[0])
            mid_chain = mid_chain * E.SE3(e_T) * E.rz() * E.rx()
            chains.append(rtb.ERobot(mid_chain))

        q_start = [0]*len(start_end)*2
        sol=chains[-1].ikine_LM(T_end)
        qt = rtb.tools.trajectory.jtraj(q_start, sol.q, T_NUM)
        #result_q = np.hstack((qt.q, np.zeros((T_NUM, (NUM_MODULES-start_end[1]) * 2))))


        step_result=np.zeros([T_NUM*NUM_MODULES,8])
        for i in range(T_NUM):
            for j in range(NUM_MODULES):
                if j in set(list(range(NUM_MODULES)))-set(start_end):
                    step_result[i * NUM_MODULES + j, 0] = j
                    step_result[i * NUM_MODULES + j, 1:4] =self.current_configuration.config[j].position
                    step_result[i * NUM_MODULES + j, 4:8] = self.current_configuration.config[j].orientation
                    continue


                T1 = chains[start_end.index(j)].fkine(qt.q[i, 0:(start_end.index(j)+1)*2])
                r1 = Rotation.from_matrix(T1.R)

                step_result[i * NUM_MODULES + j,0]=j
                step_result[i * NUM_MODULES + j,1:4]=T1.t
                step_result[i * NUM_MODULES + j,4:8]=r1.as_quat()

        return step_result
