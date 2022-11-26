#!/usr/bin/env python
from __future__ import division

import os
import rospy
import numpy as np
import math
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.srv import DeleteModel
from gazebo_ros import gazebo_interface
from scipy.spatial.transform import Rotation
import pickle

MODULE_NUM=30

RADIUS=0.06
DIAMETER=2*RADIUS

init_magnet=[0,0,-1]

class talker():
    def __init__(self):
        self.set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.del_model=rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

    def spawn_terrain(self):

        f = open('terrain.sdf', 'r')
        sdff = f.read()

        init_states = Pose()
        init_states.position.x = -5
        init_states.position.y = -1.8
        init_states.position.z = 0
        init_states.orientation.x = 0
        init_states.orientation.y = 0
        init_states.orientation.z = 0
        init_states.orientation.w = 1

        gazebo_interface.spawn_sdf_model_client('terrain', sdff, rospy.get_namespace(), init_states, "","/gazebo")

    def spawn_stair(self):

        f = open('stair.sdf', 'r')
        sdff = f.read()

        init_states = Pose()
        init_states.position.x = 0
        init_states.position.y = 1
        init_states.position.z = 0
        init_states.orientation.x = 0
        init_states.orientation.y = 0
        init_states.orientation.z = 0
        init_states.orientation.w = 1

        gazebo_interface.spawn_sdf_model_client('stair', sdff, rospy.get_namespace(), init_states, "","/gazebo")

    def spawn_modules(self):
        poses = np.loadtxt("initial.txt")

        f = open('model_wheel.sdf', 'r')
        sdff = f.read()

        init_states = Pose()
        for i in range(MODULE_NUM):
            init_states.position.x = poses[i, 0]
            init_states.position.y = poses[i, 1]
            init_states.position.z = poses[i, 2]
            init_states.orientation.x = poses[i, 3]
            init_states.orientation.y = poses[i, 4]
            init_states.orientation.z = poses[i, 5]
            init_states.orientation.w = 1
            gazebo_interface.spawn_sdf_model_client('module_'+str(i), sdff, rospy.get_namespace(), init_states, "","/gazebo")

    def spawn_final(self, num):
        f = open('final_tree'+str(num)+'.txt', 'rb')
        final=pickle.load(f)
        f.close()

        f = open('model_final.sdf', 'r')
        sdff = f.read()

        final_states = Pose()
        for i in range(MODULE_NUM):
            final_states.position.x = final[i][1][0]
            final_states.position.y = final[i][1][1]
            final_states.position.z = final[i][1][2]

            final_states.orientation.x = 0
            final_states.orientation.y = 0
            final_states.orientation.z = 0
            final_states.orientation.w = 1
            gazebo_interface.spawn_sdf_model_client(final[i][0], sdff, rospy.get_namespace(), final_states, "","/gazebo")

    def spawn_path(self):
        f = open('moving_path.txt', 'rb')
        final=pickle.load(f)
        f.close()

        f = open('model_final.sdf', 'r')
        sdff = f.read()

        final_states = Pose()
        for i in range(len(final)):
            final_states.position.x = final[i][0]
            final_states.position.y = final[i][1]
            final_states.position.z = final[i][2]

            final_states.orientation.x = 0
            final_states.orientation.y = 0
            final_states.orientation.z = 0
            final_states.orientation.w = 1
            gazebo_interface.spawn_sdf_model_client('p'+ str(i), sdff, rospy.get_namespace(), final_states, "","/gazebo")


    def del_vacancies(self):
        for i in range(MODULE_NUM):
            name='v'+str(i)
            self.del_model(name)

    def del_path(self):
        for i in range(41):
            name='p'+str(i)
            self.del_model(name)

    def del_modules(self):
        for i in range(MODULE_NUM):
            name='module_'+str(i)
            self.del_model(name)


    def spawn_all_models(self,n):
        initial = np.loadtxt("initial.txt")

        f = open('model_wheel.sdf', 'r')
        sdff = f.read()

        init_states = Pose()
        for i in range(n):

            init_states.position.x = initial[i%MODULE_NUM, 0]
            init_states.position.y = initial[i%MODULE_NUM, 1]
            init_states.position.z = initial[i%MODULE_NUM, 2]+DIAMETER*2*(i//MODULE_NUM)
            init_states.orientation.x = 0
            init_states.orientation.y = 0
            init_states.orientation.z = 0
            init_states.orientation.w = 1
            gazebo_interface.spawn_sdf_model_client(self.name[i%MODULE_NUM]+str(i//MODULE_NUM), sdff, rospy.get_namespace(), init_states, "","/gazebo")

    def del_all_models(self, n):
        for i in range(n):
            name=self.name[i%MODULE_NUM]+str(i//MODULE_NUM)
            self.del_model(name)

    def spawn_snake(self):

        f = open('model_wheel.sdf', 'r')
        sdff = f.read()

        init_states = Pose()
        for i in range(MODULE_NUM):
            init_states.position.x = 0
            init_states.position.y = 0
            init_states.position.z = 0.06+17*0.12-i*0.12
            init_states.orientation.x = 1
            init_states.orientation.y = 0
            init_states.orientation.z = 0
            init_states.orientation.w = 1
            gazebo_interface.spawn_sdf_model_client('module_'+str(i), sdff, rospy.get_namespace(), init_states, "","/gazebo")

    def init_pose(self):

        init_states = ModelState()
        for i in range(18):
            init_states.pose.position.x = 0
            init_states.pose.position.y = 0
            init_states.pose.position.z = 0+i*0.12
            init_states.pose.orientation.x = 0
            init_states.pose.orientation.y = 0
            init_states.pose.orientation.z = 0
            init_states.pose.orientation.w = 1
            init_states.model_name='module_'+str(i)
            rospy.wait_for_service('/gazebo/set_model_state')
            try:
                resp = self.set_state(init_states)
            except rospy.ServiceException as e:
                print("Service call failed: %s" % e)

        for i in range(18, 24):
            init_states.pose.position.x = 0
            init_states.pose.position.y = (i-18+1)*0.12
            init_states.pose.position.z = 12*0.12
            init_states.pose.orientation.x = -1
            init_states.pose.orientation.y = 0
            init_states.pose.orientation.z = 0
            init_states.pose.orientation.w = 1
            init_states.model_name='module_'+str(i)
            rospy.wait_for_service('/gazebo/set_model_state')
            try:
                resp = self.set_state(init_states)
            except rospy.ServiceException as e:
                print("Service call failed: %s" % e)

        for i in range(24, 30):
            init_states.pose.position.x = 0
            init_states.pose.position.y = -(i-24+1)*0.12
            init_states.pose.position.z = 12*0.12
            init_states.pose.orientation.x = 1
            init_states.pose.orientation.y = 0
            init_states.pose.orientation.z = 0
            init_states.pose.orientation.w = 1
            init_states.model_name='module_'+str(i)
            rospy.wait_for_service('/gazebo/set_model_state')
            try:
                resp = self.set_state(init_states)
            except rospy.ServiceException as e:
                print("Service call failed: %s" % e)

    def init_period(self, period, step):
        df=open(os.getcwd() + '/path/'+str(period)+'/' + 'reconfig_'+ str(step) + '.txt', "rb")
        path_all=pickle.load(df)
        df.close()
        last_config=path_all[0:MODULE_NUM, :]
        for i in range(MODULE_NUM):
            self.set_pose(i, last_config[i, 1:4], last_config[i, 4:8])

    def last_pose(self, period, step):

        df=open(os.getcwd() + '/path/'+str(period)+'/' + 'reconfig_'+ str(step) + '.txt', "rb")
        path_all=pickle.load(df)
        df.close()
        last_config=path_all[-MODULE_NUM:]
        for i in range(MODULE_NUM):
            self.set_pose(i, last_config[i, 1:4], last_config[i, 4:8])

    def last_step(self, period, step):

        df=open(os.getcwd() + '/path/'+str(period)+'/' + 'reconfig_'+ str(step) + '.txt', "rb")
        path_all=pickle.load(df)
        df.close()
        last_step=path_all[-MODULE_NUM:]
        for i in range(MODULE_NUM):
            self.set_pose(i, last_step[i, 1:4], last_step[i, 4:8])
        return path_all


    def set_pose(self, i, pos, quaternion):

        state_msg = ModelState()
        state_msg.model_name = 'module_'+str(i)
        state_msg.pose.position.x = pos[0]
        state_msg.pose.position.y = pos[1]
        state_msg.pose.position.z = pos[2]

        state_msg.pose.orientation.x = quaternion[0]
        state_msg.pose.orientation.y = quaternion[1]
        state_msg.pose.orientation.z = quaternion[2]
        state_msg.pose.orientation.w = quaternion[3]

        rospy.wait_for_service('/gazebo/set_model_state')
        try:
            resp = self.set_state(state_msg)
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
