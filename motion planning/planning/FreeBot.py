# encoding: utf-8
from __future__ import division
import numpy as np
import math
from scipy.spatial.transform import Rotation
from shapely.geometry.polygon import orient
import trimesh
from shapely.geometry.point import Point
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.geometry import LinearRing

from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from shapely.ops import split
from shapely.ops import linemerge
from shapely.ops import nearest_points
from scipy.spatial import ConvexHull

RADIUS = 0.06
DIAMETER = 2 * RADIUS
ANGLE_ACCURACY=0.0005

POINT_ACCU = 0.25 * RADIUS  # 0.05
MARGIN = 0.975
COLLISION_ACU = 0.99
VIA_DIS=DIAMETER/10

STEP_DEGREE = 1

# basic actions
START=-1
REVOLUTE = -2
ROTATE = -3
WAIT=0

init_magnet = [0, 0, -1]
init_wheels = [0, 1, 0]
init_negetive_wheels = [0, -1, 0]
init_rot_axis_W2M = np.cross(init_wheels, init_magnet)
init_rot_axis_M2W = np.cross(init_magnet, init_wheels)


class freebot:

    def __init__(self, id, pos, ori):
        self.id = id
        self.path = []
        self.module_path = []
        self.position_path = []
        self.init_T(pos, ori)
        self.final_pos = []
        self.bifur_c = []
        self.bifur_f = []
        self.all_priority = []
        self.bypass_id=[]
        self.bypass_pos=[]
        self.finished=False

    def init_T(self, pos, ori):
        self.position = pos
        self.orientation = ori
        self.magnet = Rotation.from_quat(self.orientation).apply(init_magnet)
        self.wheels_1 = Rotation.from_quat(self.orientation).apply(init_wheels)

        self.path.append((START, self.position, self.orientation))
        self.support = np.zeros(3)

    def cal_support(self, adjacent):
        r = Rotation.from_quat(self.path[-1][2])
        for module in adjacent:
            if np.linalg.norm(self.path[-1][1] + r.apply(init_magnet) * DIAMETER - module.path[-1][1]) < POINT_ACCU:
                self.support = module.path[-1][1]
                self.support_ID = module.id

        self.ID_int = []
        for ID in self.module_path:
            if type(ID) is int:
                self.ID_int.append(ID)
            if type(ID) is tuple:
                self.ID_int.append(ID[1])
        # self.ID_int.pop(0)#don't consider the self module
        try:
            self.path_index = self.ID_int.index(self.support_ID)
        except ValueError:
            pass


    def plot_line(ax, ob):
        plt.figure()
        for part in ob:
            x, y = part.xy
            plt.plot(y, x, linewidth=3, solid_capstyle='round', zorder=1)
        plt.xlim((-3.5, 3.5))
        plt.ylim((-3.5, 3.5))
        plt.show()

    def next_position(self, start_to_move_high, start_to_stop, adjacent):
        self.cal_support(adjacent)
        middle_state = self.Next_degree(self.path[-1][1], self.path[-1][2])
        if np.linalg.norm(middle_state[1] - self.final_pos) <= POINT_ACCU:
            self.finished=True
            r = Rotation.from_quat(middle_state[2])
            final_magnet=self.support-self.final_pos
            final_magnet=final_magnet/np.linalg.norm(final_magnet)
            angle = self.Angle_two_vector(np.array(r.apply(init_magnet)), final_magnet)
            if angle != 0:
                r1 = Rotation.from_rotvec(angle * np.cross(np.array(r.apply(init_magnet)), final_magnet) )  # need to be verify
                r2 = r1 * r
            else:
                r2=r
            self.path.append((middle_state[0], self.final_pos, r2.as_quat()))
            return


        collision = self.collision_detect(middle_state, adjacent)
        RETREAT = False
        via_bypass=[]
        if collision != []:
            for col in collision:
                if col[0] in start_to_stop:
                    if col[0] == self.ID_int[self.path_index + 1] or len(self.ID_int)>self.path_index+2 and col[0] == self.ID_int[self.path_index + 2]:
                        middle_state = self.attach(middle_state, col[1][-1][1])
                    else:
                        via_bypass.append((col[0],col[1][-1][1]))
                if col[0] in start_to_move_high:
                    i = 0
                    while np.linalg.norm(col[1][-1][1] - middle_state[1]) < MARGIN * DIAMETER and i < len(self.path):
                        i += 1
                        middle_state = (i, self.path[-i][1], self.path[-i][2])
                    RETREAT=True
                    # for j in range(1, i):
                    #     self.path[-j]=(i, middle_state[1], middle_state[2])

        stat=self.via_assign(via_bypass, adjacent)
        if RETREAT==False and stat==WAIT:
            self.path.append((WAIT, self.path[-1][1], self.path[-1][2]))
            return
        r2 = self.Yaw(middle_state[1], middle_state[2], self.target_point)
        next_state = (middle_state[0], middle_state[1], r2)
        self.path.append(next_state)

    # target_vacancy should be the next next position path
    def Yaw(self, pos, ori, target_point):

        r = Rotation.from_quat(ori)
        angle = self.Angle_line_plane(target_point, pos, r.apply(init_rot_axis_W2M))
        if abs(angle)>ANGLE_ACCURACY:
            r1 = Rotation.from_rotvec(-angle * np.array(r.apply(init_magnet)))  # need to be verify
            r2 = r1 * r
            # left mul: because the rotation is respecting to the world coordinate which is fixed but not rotating.
        else:
            #r2 = r
            target_direction=target_point-pos
            target_direction=target_direction/np.linalg.norm(target_direction)

            if np.array(r.apply(init_wheels)).dot(target_direction) >0:
                r2 = r
            else:
                r3 = Rotation.from_rotvec(np.radians(180) * np.array(r.apply(init_magnet)))
                r2=r3 * r
        return r2.as_quat()

    def collision_detect(self, state, adjacent):
        collision = []
        for module in adjacent:
            if np.linalg.norm(state[1] - module.path[-1][1]) < COLLISION_ACU * DIAMETER:
                if state[0] == REVOLUTE and module.id == state[3]:
                    pass
                    # print('collide with support')
                else:
                    collision.append((module.id, module.path))
        return collision

    def attach(self, middle_state, pos_collided):
        pos = middle_state[1]
        r = Rotation.from_quat(middle_state[2])

        pp = pos_collided - pos
        pp = pp / np.linalg.norm(pp)
        angle = self.Angle_two_vector(r.apply(init_magnet), pp)
        axis = np.cross(r.apply(init_magnet), pp)
        axis = axis / np.linalg.norm(axis)
        ori1 = Rotation.from_rotvec(angle * axis)
        ori2 = ori1 * r

        next_state = (ROTATE, pos, ori2.as_quat())

        return next_state

    def Next_degree(self, pos, ori, BACK=False):
        r = Rotation.from_quat(ori)
        type = REVOLUTE
        if BACK == False:
            pos1 = self.D3_update(pos, self.support, r.apply(init_rot_axis_W2M), np.radians(STEP_DEGREE))
            ori1 = self.R3_update(ori, r.apply(init_rot_axis_W2M), np.radians(STEP_DEGREE))
        else:
            pos1 = self.D3_update(pos, self.support, r.apply(init_rot_axis_M2W), np.radians(STEP_DEGREE))
            ori1 = self.R3_update(ori, r.apply(init_rot_axis_M2W), np.radians(STEP_DEGREE))
        middle_state = (type, pos1, ori1, self.support_ID)
        return middle_state

    def Dis_point_plane(self, point, plane_point, plane_normal):
        D = np.array(point) - np.array(plane_point)
        Dis = abs(np.sum(D * plane_normal)) / np.linalg.norm(plane_normal)
        return Dis

    def Angle_line_plane(self, point, plane_point, plane_normal):
        D = np.array(point) - np.array(plane_point)
        angle = math.asin(np.sum(D * plane_normal) / (np.linalg.norm(plane_normal) * np.linalg.norm(D)))
        return angle

    def Angle_two_vector(self, vector1, vector2):
        angle = math.acos(np.sum(vector1 * vector2) / np.linalg.norm(vector1) * np.linalg.norm(vector2))
        # output radians
        return angle

    def D3_update(self, init_p, rot_center, rot_axis, angle):
        r = Rotation.from_rotvec(angle * np.array(rot_axis))
        p = r.apply(np.array(init_p) - np.array(rot_center)) + np.array(rot_center)
        return p

    def R3_update(self, init_r, rot_axis, angle):
        # angle should be radians
        r = Rotation.from_rotvec(angle * np.array(rot_axis))
        r1 = r * Rotation.from_quat(init_r)

        return r1.as_quat()

    def M_update(self, rot_axis, angle):
        r = Rotation.from_rotvec(angle * np.array(rot_axis))

        self.magnet = r.apply(init_magnet)

        return self.magnet

    def W_update(self, rot_axis, angle):
        r = Rotation.from_rotvec(angle * np.array(rot_axis))

        self.wheels_1 = r.apply(init_wheels)

        return self.wheels_1

    def R3_reverse(self, chain_next_pos):
        v = chain_next_pos - self.path[-1][1]
        v = v / np.linalg.norm(v)

        r = Rotation.from_quat(self.path[-1][2])
        v1 = r.apply(init_magnet)

        angle = self.Angle_two_vector(v1, v)
        axis = np.cross(v1, v)
        axis = axis / np.linalg.norm(axis)
        new_ori = self.R3_update(self.path[-1][2], axis, angle)

        return new_ori