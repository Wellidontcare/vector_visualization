import numpy as np
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt

"""
@brief np ndarray with x, y access
"""
class vec2d(np.ndarray):
    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, val):
        self[0] = val

    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, val):
        self[1] = val

"""
@brief np ndarray with x, y, z access
"""        
class vec3d(vec2d):
    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, val):
        self[2] = val

"""
@brief np ndarray with x, y, z, w access
"""
class vec4d(vec3d):
    @property
    def w(self):
        return self[3]
    @w.setter
    def w(self, val):
        self[3] = val
    
    def as_vec3(self):
        return np.array([self.x, self.y, self.z])




"""
@brief create vec3 from python or np array
"""
def vec3(vec):
    vec = np.array([vec[0], vec[1], vec[2]]).view(vec3d)
    return vec

"""
@brief create vec4 from vec3 or np.array by appending 1
"""
def vec4(vec):
    vec = np.append(vec3(vec), 1)
    vec = np.array(vec).view(vec4d)
    return vec
"""
@brief convert from radians to degrees
"""   
def degrees(val):
    return np.deg2rad(val)

"""
@brief convert from degrees to radians
"""
def radians(val):
    return np.rad2deg(val)

"""
@brief create translation matrix
"""
def translate(mat4x4, vec3):
    mat4x4c = np.identity(4)
    vec3 = np.array(vec3).view(vec3d)
    mat4x4c[3, 0] = vec3.x
    mat4x4c[3, 1] = vec3.y
    mat4x4c[3, 2] = vec3.z
    return mat4x4c@mat4x4

"""
@brief rotate point around pivot angles in euler angles (rad)
"""
def rotate_around_pivot(point, pivot, angles):
    T = rotate(np.identity(4), angles)
    return vec3(T@vec4(point - pivot)) + pivot

"""
@brief create rotation matrix from euler angles (rad)
"""
def rotate(mat4x4, vec3):
    rotation = R.from_euler('XYZ', vec3)
    rotation = rotation.as_matrix().copy()
    row = np.zeros((1, 3))
    column = np.zeros((4, 1))
    column[-1] = 1
    rotation = np.append(rotation, row, axis=0)
    rotation = np.append(rotation, column, axis=1)
    return mat4x4@rotation

def normalize(vec3):
    return vec3/np.linalg.norm(vec3)
    
"""
@brief draw a point at [x, y, z]
"""
def draw_point(vec3, axes, style='o'):
    x1, y1, z1 = vec3
    axes.plot([x1], [y1], [z1], style)

"""
@brief create 3d plot with figure figure and xyz-size
"""
def create_3d_plot(figure=1, xsize=20, ysize=20, zsize=20):
    fig = plt.figure(figure)
    ax = fig.gca(projection='3d')
    draw_point([xsize/2, ysize/2, zsize/2], ax, 'w.')
    draw_point([-xsize/2, -ysize/2, -zsize/2], ax, 'w.')
    draw_point([-xsize/2, ysize/2, -zsize/2], ax, 'w.')
    draw_point([-xsize/2, -ysize/2, zsize/2], ax, 'w.')
    draw_point([-xsize/2, ysize/2, zsize/2], ax, 'w.')
    draw_point([xsize/2, -ysize/2, -zsize/2], ax, 'w.')
    draw_point([xsize/2, ysize/2, -zsize/2], ax, 'w.')
    draw_point([xsize/2, -ysize/2, zsize/2], ax, 'w.')
    
    
    return ax

"""
@brief draw a line from point_a to point_b
"""
def draw_line(point_a, point_b, axes, style='-'):
    x1, y1, z1 = point_a
    x2, y2, z2 = point_b
    axes.plot([x2, x1], [y2, y1], [z2, z1], style)

"""
@brief draw line from origin to [x, y, z]
"""
def draw_vec(vec3, axes, style='-'):
    draw_line([0, 0, 0], vec3, axes)
    draw_point(vec3, axes, 'k>')

"""
@brief draw a line with angles (theta_x, theta_z) starting at origin
"""
def draw_ray(origin, theta_xz, length,  axes, style='-'):
    r = length
    theta_x, theta_z = theta_xz
    b = vec3([r*np.sin(theta_z)*np.cos(theta_x), r*np.sin(theta_z)*np.sin(theta_x), r*np.cos(theta_z)]) + origin
    draw_line(origin, b, axes, style)

"""
@brief draw a marker at origin with orientation as [yaw, pitch, roll] in radians
"""    
def draw_orientation(origin, orientation, axes, style='colored'):
    origin = np.array(origin).view(vec4d)
    plus1 = rotate_around_pivot(origin+[1, 0, 0], origin, orientation)  
    plus2 = rotate_around_pivot(origin+[-1, 0, 0], origin, orientation)  
    plus3 = rotate_around_pivot(origin+[0, 1, 0], origin, orientation)  
    plus4 = rotate_around_pivot(origin+[0, -1, 0], origin, orientation)  
    plus5 = rotate_around_pivot(origin+[0, 0, 1], origin, orientation)  
    plus6 = rotate_around_pivot(origin+[0, 0, -1], origin, orientation)
    if style == 'colored':
        draw_line(origin, vec3(plus1), axes, 'b-')
        draw_line(origin, vec3(plus2), axes, 'b-')
        draw_line(origin, vec3(plus3), axes, 'r-')
        draw_line(origin, vec3(plus4), axes, 'r-')
        draw_line(origin, vec3(plus5), axes, 'g-')  
        draw_line(origin, vec3(plus6), axes, 'g-')
        return
    if style == 'object':
        draw_line(origin, vec3(plus1), axes, 'b-')
        draw_line(origin, vec3(plus2), axes, 'b-')
        draw_line(origin, vec3(plus3), axes, 'r-')
        draw_line(origin, vec3(plus4), axes, 'r-')
        draw_line(origin, vec3(plus5), axes, 'g-')
        draw_line(origin, vec3(plus6), axes, 'g-')
        draw_point(vec3(plus1), axes, 'k.')
        return
    else:
        draw_line(origin, vec3(plus1), axes, style)
        draw_line(origin, vec3(plus2), axes, style)
        draw_line(origin, vec3(plus3), axes, style)
        draw_line(origin, vec3(plus4), axes, style)
        draw_line(origin, vec3(plus5), axes, style)  
        draw_line(origin, vec3(plus6), axes, style)

"""
@brief Calculate spherical coordinates from carthesian
return r, theta_x, theta_z
"""
def to_spherical(vec3):
    x, y, z = vec3
    r = np.sqrt(x**2 + y**2 + z**2)
    theta_x = np.arctan2(y, x)
    theta_z = np.arctan2(np.sqrt(x**2 + y**2), z)
    return (r, theta_x, theta_z)
