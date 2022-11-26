# encoding: utf-8
from __future__ import division
import numpy as np
import math
from planning.FreeBot import freebot
from collada import Collada
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import trimesh
from shapely.geometry.point import Point
from shapely.geometry import LineString
from shapely.geometry import LinearRing

from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from anytree import AnyNode, RenderTree, LevelOrderIter
import pickle

RADIUS=0.06
DIAMETER=2*RADIUS
ACCURACY=0.000001#the floating point calculation of python is imprecise
POINT_ACCU=0.4*RADIUS

NUM_MODULES = 25

init_magnet=[0,0,-1]
init_wheels=[0,1,0]
init_rot_axis_W2M=np.cross(init_wheels,init_magnet)
init_rot_axis_M2W=np.cross(init_magnet,init_wheels)

OBSTACLE_POS=np.array([0,0,0])
#OBSTACLE_POS=np.array([0,0,0])
#rosrun gazebo_ros spawn_model -file /home/luo/model_editor_models/terrain2/model.sdf -sdf -model terrain -x 0 -y 0 -z 0
Inch2Meter=0.0254

class configuration():
    def __init__(self):
        self.config=[]
        self.id_list=[]
        self.connect_matrix=np.zeros((NUM_MODULES, NUM_MODULES ))
        self.final_tree=[]

    def current_config(self,model_states):
        str_m='module_'
        for i in range(len(model_states.name)):
            try:
                model_states.name[i].index(str_m)
            except ValueError:
                pass
            else:
                id=int(model_states.name[i].split('_')[1])
                self.id_list.append(id)

                pos=np.array([model_states.pose[i].position.x,model_states.pose[i].position.y,model_states.pose[i].position.z])
                ori=np.array([model_states.pose[i].orientation.x,model_states.pose[i].orientation.y,model_states.pose[i].orientation.z,model_states.pose[i].orientation.w])
                one=freebot(id, pos, ori)
                self.config.append(one)

        self.cal_matrix()


    def cal_matrix(self):
        #initialization
        self.connect_matrix = np.zeros((NUM_MODULES, NUM_MODULES))

        for i in range(NUM_MODULES):
            support_m=self.config[i].path[-1][1] + DIAMETER * Rotation.from_quat(self.config[i].path[-1][2]).apply(init_magnet)
            for j in range(NUM_MODULES):
                if np.linalg.norm(support_m-self.config[j].path[-1][1])<POINT_ACCU:
                    self.connect_matrix[i,j]=1

        return self.connect_matrix

    def save_pos(self, period):
        final=[]
        for i in range(NUM_MODULES):
            final.append(('v'+str(i), globals()['v'+str(i)].pos, globals()['v'+str(i)].parent))

        df = open('final_tree'+str(period)+'.txt', "wb")
        pickle.dump(final, df)
        df.close()

    def reload_nodes(self, period):
        df = open('final_tree'+str(period)+'.txt', "rb")
        final=pickle.load(df)
        df.close()

        for i in range(1, NUM_MODULES):
            globals()['v' + str(i)] = AnyNode(name='v' + str(i), ID=i, parent=globals()['v'+str(final[i][2].ID)], pos=final[i][1], matched=None)



    def save_path(self, moving_path):
        positions=[]
        for i in range(len(moving_path)):
            positions.append(moving_path[i][2])

        df = open('moving_path.txt', "wb")
        pickle.dump(positions, df)
        df.close()


    def draw_convex_hull(self, Points, hull):
        plt.plot(Points[:, 0], Points[:, 1], 'o')
        for simplex in hull.simplices:
            plt.plot(Points[simplex, 0], Points[simplex, 1], 'k-')
        plt.plot(Points[hull.vertices, 0], Points[hull.vertices, 1], 'r--', lw=2)
        plt.plot(Points[hull.vertices[0], 0], Points[hull.vertices[0], 1], 'ro')
        plt.show()

    def draw_clip_points(self, P):
        X=[]
        Y=[]
        Z=[]
        for i in range(len(P)):
            X.append(0)#P[i][0][0]
            Y.append(P[i][0][1])
            Z.append(P[i][0][2])
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(X, Y, Z)

        ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
        ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
        ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})
        plt.show()


    def plot_line(ax, ob):
        plt.figure()
        for part in ob:
            x, y = part.xy
            plt.plot(y, x, linewidth=3, solid_capstyle='round', zorder=1)
        plt.xlim((-3.5, 3.5))
        plt.ylim((-3.5, 3.5))
        plt.show()
