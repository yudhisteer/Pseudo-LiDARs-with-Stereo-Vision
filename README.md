# Pseudo-LiDARs and 3D Computer-Vision

## Problem Statement

## Abstract

## Plan of Action
1. Linear Camera Model
2. Intrinsic and Extrinsic Parameters
3. Simple Stereo
4. Uncalibrated Stereo
5. Epipolar Geometry
6. Fundamental Matrix
7. Correspondences
8. Estimating Depth


------------------

## 1. Linear Camera Model
Before proceeding, we need to develop a method to estimate the camera's internal and external parameters accurately. This requires creating a linear camera model, which simplifies the estimation process compared to nonlinear models.

In the image below, we have a point ```P``` in the world coordinates ```W``` and the camera with its own coordinates ```C```. If we know the relative position and orientation of the camera coordinate frame with respect to the world coordinates frame, then we can write an expression that takes us all the way from the point ```P``` in the world coordinate frame to its projection ```P'``` onto the image plane. That complete mapping is what we refer to as the ```forward imaging model```.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/96c7a839-e841-429a-9192-fabfe656b017" width="700" height="370"/>

</div>


<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/71c1cc4b-08f1-4528-b336-9d24133bda94" width="650" height="250"/>
    <p><b> Fig 1. Forward Imaging Model: 3D to 2D </b></p>
</div>

### 1.1 Mapping of Camera Coordinates to Image Coordinates (3D to 2D)
We assume that the point has been defined in the camera coordinate frame and using ```perspective projection equations```:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/195b17d0-f6a1-4d0b-aec7-457eeec1cbe4)"/>
</div>

![CodeCogsEqn (20)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/2b5022c1-da9c-4d7d-a9fd-5d89a713289b) and ![CodeCogsEqn (21)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/1e908801-21a5-4b72-8150-cdcb2583f51a) are the coordinates of point ```P``` onto the image plane and ```f``` is the focal length which is the distance between the Centre of Projection (COP) and the image plane of the camera.











### 1.2 Mapping of World Coordinates to Camera Coordinates (3D to 3D)












![download](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/ef279136-0334-4240-95e1-01a1e0919b77)

----

## 2. Intrinsic and Extrinsic Parameters












----------

## References
1. https://github.com/mileyan/AnyNet
2. https://github.com/JiaRenChang/PSMNet
3. https://github.com/autonomousvision/unimatch
4. 
