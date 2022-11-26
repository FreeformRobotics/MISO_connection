#!/usr/bin/env python
from __future__ import division

import os
import pickle
import rospy
from gazebo_msgs.msg import ModelStates
from planning.Robots import robots
import Talker
import numpy as np
from scipy.spatial.transform import Rotation
init_magnet = [0, 0, -1]
T_NUM = 50
NUM_MODULES = 30
from scipy.spatial.transform import Rotation
import math
import time

def save_steps(path_all, period, step):

    df = open(os.getcwd() + '/path/'+str(period)+'/reconfig_' + str(step) + '.txt', "wb")
    pickle.dump(path_all, df)
    df.close()

def listener_replay(period, step):

    rospy.init_node('listener', anonymous=True)

    States=rospy.wait_for_message('/gazebo/model_states', ModelStates)

    df=open(os.getcwd() + '/path/'+str(period)+'/reconfig_'+ str(step) + '.txt', "rb")
    path_all=pickle.load(df)
    df.close()
    for i in range(T_NUM):
        for j in range(NUM_MODULES):
            t.set_pose(j, path_all[i * NUM_MODULES +j, 1:4], path_all[i * NUM_MODULES +j, 4:8])
        time.sleep(0.5)


def listener(period, step):

    rospy.init_node('listener', anonymous=True)

    States = rospy.wait_for_message('/gazebo/model_states', ModelStates)
    rob = robots(States)
    path_all = rob.step()
    for i in range(T_NUM):
        for j in range(NUM_MODULES):
            t.set_pose(j, path_all[i * NUM_MODULES +j, 1:4], path_all[i * NUM_MODULES +j, 4:8])

    print("finished one reconfigration")

    save_steps(path_all, period, step)

def attach(perio, tep):

    rospy.init_node('listener', anonymous=True)

    States = rospy.wait_for_message('/gazebo/model_states', ModelStates)
    rob = robots(States)
    orient_m=29
    attach_m=17
    pos=rob.current_configuration.config[orient_m].position
    pos_attach=rob.current_configuration.config[attach_m].position
    pp=pos_attach-pos
    pp = pp / np.linalg.norm(pp)
    ori=Rotation.from_quat(rob.current_configuration.config[orient_m].orientation)
    axis = np.cross(ori.apply(init_magnet), pp)

    for i in range(0, 650):
        ori1 = Rotation.from_rotvec(math.radians(i*0.1) * axis)
        ori2 = ori1 * ori
        t.set_pose(orient_m, pos, ori2.as_quat())
        time.sleep(0.05)


if __name__ == '__main__':
    t=Talker.talker()
    #t.del_modules()
    #t.spawn_snake()

    t.init_pose()
    #listener_replay(1, 1)

    #t.last_step(1, 1)
    #attach(1, 2)
    #listener_replay(1, 3)

    listener_replay(1, 4)
    listener_replay(1, 5)

    #t.last_step(1, 5)
    attach(1,6)
    listener_replay(1, 6)
    #listener(1, 6)




