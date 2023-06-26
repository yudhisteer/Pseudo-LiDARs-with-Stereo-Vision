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

#### 1.1.1 Image Plane to Image Sensor Mapping
We assume that the point has been defined in the camera coordinate frame and using ```perspective projection equations```:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/195b17d0-f6a1-4d0b-aec7-457eeec1cbe4"/>
</div>

![CodeCogsEqn (20)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/2b5022c1-da9c-4d7d-a9fd-5d89a713289b) and ![CodeCogsEqn (21)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/1e908801-21a5-4b72-8150-cdcb2583f51a) are the coordinates of point ```P``` onto the image plane and ```f``` is the focal length which is the distance between the Centre of Projection (COP) and the image plane of the camera.

We have assumed we know the coordinates of the image plane in terms of **millimeters (mm)** which is the same unit in the camera coordinate frame. However, in reality we have an image sensor whose units are **pixels (px)**. Hence, we need to convert our coordinate of ```P``` from mm to pixel coordinates using **pixel densities (pixels/mm)**.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/13dd200d-7179-40f3-bf80-a649ca5b3a03"/>
</div>

![CodeCogsEqn (25)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/60822e05-06af-4160-a1be-3f218e96a368) and ![CodeCogsEqn (26)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/b737884c-7f5e-478e-b37c-73afeb946a44) are the pixel densities (px/mm) in the x and y directions respectively.

Since now we treated the midpoint of the image plane as the origin but generally, we treat the top-left corner as the origin of the image sensor. ![CodeCogsEqn (27)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/41a107b2-ac17-4cf1-8a35-bb51c6fe956a) is the **Principle Point** where the optical axis pierces the sensor.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/47bc0e6e-499e-4944-8376-357fb53e094c"/>
</div>

We re-write the equation above whereby ![CodeCogsEqn (28)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/d117f243-d85a-4c38-9c46-9781769e3440) are the focal lengths in pixels in the x and y directions:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/197455fb-61f5-425f-a621-2264b2fe7d19"/>
</div>


- ![CodeCogsEqn (29)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/0e376ffc-6c75-4d15-98d3-c80b3370f17c): **Intrinsic parameters** of the camera.
- They represent the camera's **internal geometry**.
- The equation tells us that objects **farther** away appear **smaller** in the image.
- ```(u,v)``` are **non-linear models** as we are dividing by ```z```.


#### 1.1.2 Homogeneous Coordinates
We need to go from a ```non-linear``` model to a ```linear``` model and we will use homogeneous coordinates to do so. we will transform ```(u,v)``` from **pixel** coordinates to **homogeneous** coordinates.

The homogeneous representation of a 2D point ![CodeCogsEqn (30)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/bc650530-723c-4079-aa4e-818cf5969bcf)
 is a 3D point ![CodeCogsEqn (42)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/9651d451-3d53-45b8-8ecb-60a980aed781). The third coordinate ![CodeCogsEqn (32)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/99821523-c643-4c47-8fd2-94613d385fa0) is fictitious.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/115f60f7-7241-49a6-8537-639fad347513"/>
</div>

Similarly, we multiply the equation below by ![CodeCogsEqn (35)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/ac370ee0-77e7-4cf5-b535-d62e8d6fdbc9)
: 

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/197455fb-61f5-425f-a621-2264b2fe7d19"/>
</div>

We now have a ```3 x 4``` matrix which contains all the internal parameters of the camera multiplied by the homogeneous coordinates of the 3-dimensional point ```P``` defined in the camera coordinate frame. This gives us a **Linear Model for Perspective Projection**.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/901ba416-c4b5-495b-a89c-989eddb64572"/>
</div>

Note that this ```3 x 4``` matrix is called the **Intrinsic Matrix**:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/1b88da02-8d8e-4551-aebb-684bd690e069"/>
</div>

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/0fa18ea9-e340-4e3d-af4e-8a42f31803e1"/>
</div>

Its structure is an upper-right triangular matrix which we can separate as ```K```:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/2bd8d169-e94e-4e2d-ba2f-45c7bf783d19"/>
</div>

Hence, we have ![CodeCogsEqn (40)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/8ebfebd3-fbd1-4b9f-92d1-30af6daf694d) that takes us from the homogeneous coordinate representation of a point in the camera coordinate frame 3D to its pixel coordinates in the image, ![CodeCogsEqn (41)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/e05c6a7e-5d8c-42d6-a6e3-348da8319c63).


<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/72659965-e977-4ff7-8290-7ecb46eef247"/>
</div>


### 1.2 Mapping of World Coordinates to Camera Coordinates (3D to 3D)
Now we need the mapping of a point from the ```world``` coordinates to the ```camera``` coordinates: 3D to 3D. That can be done by using the **position**, ![CodeCogsEqn (43)](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/6675c7ec-7b20-428e-9ff7-c7379dfe3c79)
 and **orientation**, ```R```,  of the camera coordinate frame. The position and orientation of the camera in the world coordinate frame ```W``` are the camera's **Extrinsic Parameters**.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/562e5971-3a82-4f01-a0fb-9670d6d00b77" width="450" height="300"/>
</div>

Orientation or Rotation matrix R is **orthonormal**: 

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/e4ec7ec5-bd8d-4027-ba64-4a72b36c4e81"/>
</div>


If we now map ```P``` from the word coordinate frame to the camera coordinate frame **rotation** matrix ```R``` and **translation** matrix ```t```:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/c962e766-1733-44d8-91cd-72ca44ef3c75"/>
</div>


We can write the equation above using homogeneous coordinates:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/61909c55-d3f6-4982-abb5-12ef7b72236a"/>
</div>

The **Extrinsic Matrix** is the ```4 x 4``` matrix:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/bb7c227e-5fc3-4cc0-95d2-410099431e2c"/>
</div>

And this is how we transformed a point from the world coordinates frame to the camera coordinates frame:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/54d6c234-cfe4-461a-a135-ba914b2f98af"/>
</div>


<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/c75fb9f1-e23d-4bd1-9c03-e822848dfb8b" width="500" height="350"/>
</div>





























![download](https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/ef279136-0334-4240-95e1-01a1e0919b77)

----

## 2. Intrinsic and Extrinsic Parameters












----------

## References
1. https://github.com/mileyan/AnyNet
2. https://github.com/JiaRenChang/PSMNet
3. https://github.com/autonomousvision/unimatch
4. 
