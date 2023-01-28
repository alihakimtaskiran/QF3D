# QF3D
3D-Feynman Diagram Visualizer

<pre>
pip install QF3D
</pre>

<img src="https://github.com/alihakimtaskiran/QF3D/raw/main/Annihilation.png" width="400">

## Overview

This code defines two classes, Fermion and Boson, and a class Entity that is used to represent 3D models in the Open3D library. The Fermion and Boson classes are used to represent particle-like entities, and each class instance has a name, a start point, and an end point. The Entity class is used to create 3D models of these entities and store information about the models in the Open3D library.

<pre>
import QF3D
# Create a Fermion particle
particle1 = QF3D.Fermion("electron", [0, 0, 0], [1, 2, 3])

# Create a Boson particle
particle2 = QF3D.Boson("gluon", [0, 0, 0], [3, 4, 5])

# Create an Entity object
entity = QF3D.Entity()

entity.add([particle1, particle2])

# Display the scene
entity.view()
</pre>


## Dependencies
- **open3d** is an open-source library for 3D data processing. It is used to create the 3D models of entities in this code.
- **numpy** is a library for numerical computations in Python. It is used for vector calculations in the Fermion and Boson classes.

## Classes

### Fermion(name, start, end)

The Fermion class represents a fermion particle. An instance of this class has the following attributes:

    name: The name of the fermion particle.
    delta: The difference between the end point and the start point.
    io: A two-element list that contains the start and end points.

### Boson(name, start, end)

The Boson class represents a boson particle. An instance of this class has the following attributes:

    name: The name of the boson particle.
    delta: The difference between the end point and the start point.
    translator: A matrix that is used to translate points in the 3D model.
    io: A two-element list that contains the start and end points.

### Entity()

The Entity class is used to represent 3D models in the Open3D library. An instance of this class has the following attributes:

    model: A PointCloud object from the Open3D library that represents the 3D model.
    metric_model: A PointCloud object from the Open3D library that represents a metric-related model.
    path: A NumPy array that represents a path in 3D space.
    colors: A NumPy array that represents colors used in the 3D model.
