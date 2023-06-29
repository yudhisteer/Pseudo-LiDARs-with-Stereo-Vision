# Pseudo-LiDARs and 3D Computer-Vision

## Problem Statement

## Abstract

## Plan of Action
1. Linear Camera Model
2. Intrinsic and Extrinsic Parameters
3. Simple Stereo
4. Application of Simple Stereo


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

#### 1.2.1 Projection Matrix
We now have our mapping from world to camera using the **Extrinsic Matrix**:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/fea92f0b-8ab1-4923-94c5-7c609d59d604"/>
</div>

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/18d8151a-50f1-4e40-9b48-f70e21ee372a"/>
</div>


And the mapping of the camera to the image using the **Intrinsic Matrix**:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/1e1d4331-d24c-4ca3-8153-41960e256970"/>
</div>

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/cb2f8275-4b8c-40a4-bfed-efad3733f419"/>
</div>

Therefore, we can combine these two to get a direct mapping from a point in the world coordinate frame to a pixel location in the image:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/4e2ba08a-70f5-4008-9d14-80190dfef2aa"/>
</div>

We then have a ```3 x 4``` matrix called the **Projection Matrix**:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/989813d9-d3c1-4d90-9bac-2e34ef19ce56"/>
</div>

Hence, if we wish to calibrate the camera, all we need to know is the **projection matrix**.  We can then go from any point in 3D to its projection in pixels in the image.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/6b1b9d46-2714-48c8-8c32-ada400a17f73 width="550" height="400"/>
</div>


----

## 2. Intrinsic and Extrinsic Parameters
By employing our calibration method, we are able to achieve a precise estimation of the projection matrix. we can also go beyond this step by decomposing the projection matrix into its constituent parts: the ```intrinsic matrix```, encompassing all ```internal parameters```, and the ```extrinsic matrix```, which captures the ```external parameters``` of the camera.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/e9586b9d-b047-48ba-83df-7efaebb6e4eb"/>
</div>

Now if we check how we get the first 3 columns of the projection matrix, we get it by multiplying the **calibration matrix, K** with the **rotation matrix, R**. Note that ```K``` is an **upper-right triangular matrix** and ```R``` is an **orthonormal matrix**, hence, it is possible to uniquely "decouple" ```K``` and ```R``` from their product using ```QR factorization method```.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/9341dfd1-78c5-497b-8fc4-ef6349a906f6"/>
</div>

Similarly, to get the last column of the projection matrix, we multiply the **calibration matrix, K** with the **translation vector, t**:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/641e8fd9-1e3c-4413-a882-cb2d9c673eed"/>
</div>

Therefore:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/65b24c60-18cb-4d4b-bbc0-d2190822dfca"/>
</div>


Note that pinholes do not exhibit distortions but lenses do. We may encounter **radial** or **tangential** distortion and these are non-linear effects. And in order to take care of these, we need to incorporate the distortion coefficients in our intrinsic model.

--------------- 

## 3. Simple Stereo
Now we want to recover r3-dimensional structure of a scene from two images. Before we dive into this, let's ask ourselves, given a calibrated camera, can we find the 3D scene point from a sinple 2D image? The answer is **no**. But we do know that the corresponding 3D point must lie on an ```outgoing ray``` shown in green and given that the camera is calibrated, we know the equation of this ray.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/1c804ebb-305a-4b2b-a68a-995f20490f86" width="450" height="300"/>
</div>

So in order to reconstruct a 3D scene, we need two images captured from two different locations. Below is an example of a stereo camera whereby we have a **left camera** and a **right camera**, and the right camera is simply identical to the left camera but displaced along the horizontal direction by a distance ```b``` called the ```baseline```.

In the image below we have the projection of a scene point in the left camera and the projection of the same point in the right camera. We shoot out two rays from the projected points and wherever those two rays intersect is where the physical point lies corresponding to these two image points. This is called **triangulation** problem.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/29bf4c3a-46e7-4c7f-9b50-c7564da24df5" width="600" height="580"/>
</div>

Assuming we know the position of the point in the left and right image plane then we have the 2 equations based on the perspective projection equation:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/6ef5d79a-2083-43f1-b161-48a33e7a62f9"/>
</div>

Notice that the position of the point in the vertical direction of the image plane is the same for both the left and right camera meaning we have **no disparity** in the vertical direction. Hence solving for ```(x,y,z)```:


<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/9eac3a8a-f282-4398-b30c-222c22ae319a"/>
</div>

- **Disparity** is the **difference** in the u-coordinates of the same scene point in the two images.
- Using the disparity we can calculate the **depth** ```z``` of the point in the scene.
- **Depth** ```z``` is **inversely proportional** to the **disparity**. That is, if a point is very close to the camera, it will have a big disparity. On the other hand, if a point is far from the camera, it will have a small disparity.
- The **disparity** is **zero** if a point is at **infinity**, that is, at infinity a point will have the same exact position on the left and right image plane.
- **Disparity** is **proportional** to **baseline**, that is, the further apart are the two cameras, the greater the disparity will be.
- When designing a stereo system, we want to use a stereo configuration where the **baseline is large**, as the larger the baseline, the more precise we can make the disparity measurements.

### 3.1 Stereo Matching

Since now we have assumed we know where a point of the left image lands on the right image. That is, we assumed we knew the **correspondence** between points in the left and right image.
Now we need to find that correspondence and that is called **stereo matching**.

As mentioned before, we do NOT have disparity in the vertical direction, which means that the corresponding points must lie on the same ```horizontal line``` in both images. Hence, our search is ```1D``` and we can use ```template matching``` to find the corresponding point in the right image.


<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/079b502a-8779-46b9-b317-9b34e615393b" width="780" height="480"/>
</div>

- We use the window ```T``` as a template and match it with all the windows along the same scan line ```L``` in the right image using a similarity metric (e.g., ```sum of absolute differences```, ```sum of squared differences```).
- The point where it matches best (where the error is lowest) is the match.
- That point is the correspondence that we use to estimate disparity.

Now we want to know how big the window ```T``` should be:
- If the window is very small, we may get good localization but **high-sensitivity noise**. The smaller the window, the less descriptive the pattern is.
- If we use a large window, we may get more robust matches in terms of depth of values but the disparity map is going to be more blurred: **poor localization**.
- Another method could be to use the **adaptive window method**: For each point, we match points using windows of multiple sizes and use the disparity that is a result of the best similarity measure.

Stereo-matching algorithms can be categorized as either ```local``` or ```global``` methods, depending on how they handle the disparity optimization step. 

- Global methods incorporate a **pairwise smoothness** term in the cost function, which encourages spatial continuity across pixels and consistent assignments along edges. 
- These global methods generally perform better than local methods in handling object boundaries and resolving ambiguous matches.
- Global optimization problems are often computationally challenging and can be classified as NP-hard.
- On the other hand, local methods have simpler computations but may struggle with object boundaries and ambiguous matches.


### 3.2 Issues with Stereo Matching

In order to get a good stereo matching, we want to avoid the following:

1. We expect the surface to have **texture**. If we have the image of a smooth wall, then we do not have much texture and if we take a small window ```T``` then we may get many matches between the left and right image.
2. If we do have texture in our image, then this texture should not be **repetitive**. If we have a repetitive pattern we will get multiple matches in the right image where they are all going to be perfectly good matches.
3. An inherent problem of stereo matching is **foreshortening** whereby the projected area of our window onto the left image is different from the projected area in the right image. Hence, we are not matching the same brightness patterns but a warped or distorted version of it.

------------

## 4. Application of Simple Stereo

<img width="579" alt="image" src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/994541de-0959-4fae-ab33-5de84d2e603e">




  

----------

## References
1. https://github.com/mileyan/AnyNet
2. https://github.com/JiaRenChang/PSMNet
3. https://github.com/autonomousvision/unimatch
4. https://groups.csail.mit.edu/commit/papers/2016/min-zhang-meng-thesis.pdf
5. https://arxiv.org/abs/1510.05970
6. https://arxiv.org/pdf/1803.08669.pdf
7. https://arxiv.org/abs/2203.11483
8. https://www.episci.com/product/swarmsense/
9. https://skybrush.io/
10. https://www.modalai.com/
11. https://github.com/darylclimb/cvml_project/tree/master/projections
12. https://towardsdatascience.com/depth-estimation-1-basics-and-intuition-86f2c9538cd1
13. https://towardsdatascience.com/uncertainty-in-depth-estimation-c3f04f44f9
14. https://medium.com/swlh/camera-lidar-projection-navigating-between-2d-and-3d-911c78167a94
15. https://www.mrt.kit.edu/z/publ/download/2013/GeigerAl2013IJRR.pdf
