import open3d as o3d
import numpy as np
from types import FunctionType
print("Get ready! Tachyon Era coming soon ")
last_scientific_update="27th March 2022"
cmapf={"quark":(.533, .698, 0), "lepton":(0, .58, .941)}
cmapb={"photon":(.565, .004, 1.00), "gluon":(.937, 1., .004), "w":(1., .396, 0), "z":(1., .408, .576), "higgs":(.706, .749, .98)}
cmap=cmapf
cmap.update(cmapb)
class Fermion(object):
    
    def __init__(self, name,start, end):
        _=name.lower()
        if _ not in cmapf:
            if _ in {"up","down","charm","strange","top","bottom"}:
                self.name="quark"
            elif _ in {"electron","electron neutrino","muon","muon neutrino","tau","tau neutrino"}:
                self.name="lepton"
            else:
                raise ValueError(f"{name} is not a known to be included in standard model by the time on {last_scientific_update}")
        else:
            self.name=_
            
        if type(start) not in {list, tuple}:
            raise TypeError("Starting point must be a tuple or list ")
        
        if type(end) not in {list, tuple}:
            raise TypeError("Ending point must be a tuple or list ")
        
        if not len(start)==3:
            raise ValueError("The entity is defined to be had 1 temporal and 2 spatial dimension")
            
        if not len(end)==3:
            raise ValueError("The entity is defined to be had 1 temporal and 2 spatial dimension")
        
        self.delta=np.array((end[0]-start[0], end[1]-start[1], end[2]-start[2]))
        self.io=np.array((start,end))
    
    
    
class Boson(object):
    def __init__(self, name, start, end):
        _=name.lower()
        if _ not in cmapb:
            raise ValueError(f"{name} is not a known to be included in standard model by the time on {last_scientific_update}")
        else:
            self.name=_
            
        if type(start) not in {list, tuple}:
            raise TypeError("Starting point must be a tuple or list ")
        
        if type(end) not in {list, tuple}:
            raise TypeError("Ending point must be a tuple or list ")
        
        if not len(start)==3:
            raise ValueError("The entity is defined to be had 1 temporal and 2 spatial dimension")
            
        if not len(end)==3:
            raise ValueError("The entity is defined to be had 1 temporal and 2 spatial dimension")
        
        self.delta=np.array((end[0]-start[0], end[1]-start[1], end[2]-start[2]))
        self.__normalized=self.delta/np.linalg.norm(self.delta)
        theta=np.arccos(self.__normalized[2])
        phi=np.arctan2(self.__normalized[1], self.__normalized[0])-np.pi
        
        roty=np.array([[np.cos(theta), 0 , -np.sin(theta)], [0,1,0], [np.sin(theta), 0, np.cos(theta)]])
        rotz=np.array([[np.cos(phi), -np.sin(phi), 0],[np.sin(phi), np.cos(phi), 0], [0,0,1]])
        self.translator=np.dot(rotz, roty)
        self.io=np.array((start,end))

class Entity(object):
    def __init__(self):
        self.__model=o3d.geometry.PointCloud()
        self.__metric_model=o3d.geometry.PointCloud()
        self.__path=np.array([(i/250, 0, 0) for i in range(0,1000)]+[(0,i/250, 0) for i in range(0,1000)]+[(0, 0, i/250) for i in range(0,1000)])
        self.__colors=np.array(((0,0,0),)*3000)
    
    def add(self, particle):
    
        if type(particle)==Fermion:
            self.__colors=np.concatenate((self.__colors,np.array((cmap[particle.name],)*1000)),0)
            ds=tuple([particle.delta[i]/1000 for i in range(3)])
            path=np.zeros((1000,3))
            for i in range(1000):
                for j in range(3):
                    path[i][j]=particle.io[0][j]+ds[j]*i
            self.__path=np.concatenate((self.__path, path),0)
        
        elif type(particle)==Boson:
            self.__colors=np.concatenate((self.__colors,np.array((cmap[particle.name],)*1000)),0)
            path=np.zeros((1000,3))
            spiral_scalar=(particle.delta[0]**2+particle.delta[1]**2+particle.delta[2]**2)**.5/20
            longitudinal_scalar=np.linalg.norm(particle.delta)/1000
            
            
            for i in range(1000):
                path[i]=particle.io[0]+np.dot(particle.translator, np.array((np.cos(i*0.03)*spiral_scalar,np.sin(i*0.03)*spiral_scalar,i*longitudinal_scalar)))
                
                
            self.__path=np.concatenate((self.__path, path),0)


        elif type(particle) in {list, tuple, set}:
    
            for part in particle:
                
                if type(part)==Fermion:
                    self.__colors=np.concatenate((self.__colors,np.array((cmap[part.name],)*1000)),0)
                    ds=tuple([part.delta[i]/1000 for i in range(3)])
                    
                    path=np.zeros((1000,3))
                    for i in range(1000):
                        for j in range(3):
                            path[i][j]=part.io[0][j]+ds[j]*i
                    self.__path=np.concatenate((self.__path, path),0)
                
                elif type(part)==Boson:
                    self.__colors=np.concatenate((self.__colors,np.array((cmap[part.name],)*1000)),0)
                    
                    path=np.zeros((1000,3))
                    
                    
                    spiral_scalar=(part.delta[0]**2+part.delta[1]**2+part.delta[2]**2)**.5/20
                    longitudinal_scalar=np.linalg.norm(part.delta)/1000
                    
                    for i in range(1000):
                        path[i]=part.io[0]+np.dot(part.translator, np.array((np.cos(i*0.03)*spiral_scalar,np.sin(i*0.03)*spiral_scalar,i*longitudinal_scalar)))
                    
                    self.__path=np.concatenate((self.__path, path),0)
               
                else:
                    raise ValueError("No such Boson exists")


    def render(self):
        
        self.__model.points=o3d.utility.Vector3dVector(self.__path)
        self.__model.colors=o3d.utility.Vector3dVector(self.__colors)
        
        try:
            self.__metric_model.points=o3d.utility.Vector3dVector(self.__metric_set)
            self.__metric_model.colors=o3d.utility.Vector3dVector(self.__colors)
        except:
            pass
    
    def metric_tensor(self, g_uv=[[-1, 0, 0], [0, 1, 0], [0, 0, 1]], signature=(-1,1,1), params=None):
        
        if not isinstance(g_uv, (np.ndarray,tuple, list)):
            raise TypeError("Metric Tensor must be a np.array, tuple or list")
        
        self.__g_uv=np.array(g_uv)
        
        if self.__g_uv.shape!=(3,3):
            raise ValueError("Metric Tensor is in shape of 3x3")
        
        self.__type_map=np.empty((3,3))
        for u in range(3):
            for v in range(3):
                if isinstance(self.__g_uv[u][v],(np.int64,np.int32,np.int16,np.float128,np.float64,np.float32, np.float16,int, float)):
                    self.__type_map[u][v]=True
                    
                else:
                    self.__type_map[u][v]=False
                    
        
        
        
        if not isinstance(signature, (tuple, list)):
            raise TypeError("Signature must be a np.array, tuple or list")
        
        
        self.signature=tuple(signature)
        
        if not(signature==(1,-1,-1) or signature==(-1,1,1)):
            raise ValueError("Conventional (1 time, 2 spatial) signatures are (-1, 1,1) for (-,+,+) or (1,-1,-1) for (+,-,-) ")
    
        
    
    
    def view(self,render=True, mode="topological"):
        if render and mode=="topological":
            self.render()
            o3d.visualization.draw_geometries([self.__model])
        
        elif render and mode=="metric":
            self.__metric_renderer()
            o3d.visualization.draw_geometries([self.__metric_model])
            
        
    
    def savefile(self,path_to_file, render=True):
        
        if render:
            self.render()
        o3d.io.write_point_cloud(path_to_file, self.__model)
        
    def entity(self, render=True):
        
        if render:
            self.render()
        return self.__model
    
    def __metric_renderer(self):
        
        self.__metric_set=[]
        for point in self.__path:
            _T_g=np.empty((3,3))
            for u in range(3):
                for v in range(3):
                    if self.__type_map[u][v]:
                        _T_g[u][v]=self.__g_uv[u][v]
                    else:
                        _T_g[u][v]=self.__g_uv[u][v](point[0],point[1],point[2])
                    
            self.__metric_set.append(np.dot(_T_g, point))
        self.render()
