import open3d as o3d
import numpy as np
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
        
        self.delta=(end[0]-start[0], end[1]-start[1], end[2]-start[2])
        self.io=(start,end)
    
    
    
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
        
        self.delta=(end[0]-start[0], end[1]-start[1], end[2]-start[2])
        self.io=(start,end)

class Entity(object):
    def __init__(self):
        self.__model=o3d.geometry.PointCloud()
        self.__path=np.array(((0,0,0),))
        self.__path=np.array([(i/250, 0, 0) for i in range(0,1000)]+[(0,i/250, 0) for i in range(0,1000)]+[(0, 0, i/250) for i in range(0,1000)])
        self.__colors=np.array(((0,0,0),))
        self.__colors=np.array(((0,0,0),)*3000)
    def add(self, particle):
        if type(particle) in {Boson,Fermion}:
            self.__colors=np.concatenate((self.__colors,np.array((cmap[particle.name],)*1000)),0)
            ds=tuple([particle.delta[i]/1000 for i in range(3)])
            path=np.zeros((1000,3))
            for i in range(1000):
                for j in range(3):
                    path[i][j]=part.io[0][j]+ds[j]*i
            self.__path=np.concatenate((self.__path, path),0)
            
        elif type(particle) in {list, tuple, set}:
            for part in particle:
                if type(part) in {Boson,Fermion}:
                    self.__colors=np.concatenate((self.__colors,np.array((cmap[part.name],)*1000)),0)
                    ds=tuple([part.delta[i]/1000 for i in range(3)])
                    path=np.zeros((1000,3))
                    for i in range(1000):
                        for j in range(3):
                            path[i][j]=part.io[0][j]+ds[j]*i
                    self.__path=np.concatenate((self.__path, path),0)
                else:
                    raise ValueError("No such Boson exists")
    def render(self):
        self.__model.points=o3d.utility.Vector3dVector(self.__path)
        self.__model.colors=o3d.utility.Vector3dVector(self.__colors)
    
    def view(self):
        self.render()
        o3d.visualization.draw_geometries([self.__model])
    
    def savefile(self,path_to_file):
        o3d.io.write_point_cloud(path_to_file, self.__model)
        
    def entity(self):
        return self.__mode
