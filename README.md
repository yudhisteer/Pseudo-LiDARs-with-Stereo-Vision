# Pseudo-LiDARs with Stereo Vision





## Problem Statement
In the context of drone deliveries, it is crucial not only to detect obstacles in ```real-time``` but also to accurately determine their ```distances```. However, the implementation of traditional ```LiDAR``` sensors on drones poses a significant challenge due to their ```high cost``` and ```weight```. The expense and heaviness of LiDAR systems hinder their practicality for integration onto drones for ```obstacle detection``` and ```distance estimation``` purposes. Consequently, an alternative solution is needed to overcome these limitations and enable drones to ```avoid obstacles```, ```plan optimal paths```, and gain a comprehensive understanding of the surrounding environment. Addressing the problem of acquiring accurate obstacle distance measurements becomes essential in providing a cost-effective and lightweight alternative to LiDAR sensors, ensuring the safe and efficient implementation of drone deliveries.

## Abstract
This project presents an economical alternative to LiDAR sensors for ```per-pixel depth estimation``` in drone applications. By utilizing ```block matching``` and ```Semi-Global Block Matching (SGBM)``` algorithms, we showcase how stereo computer vision techniques can accurately determine depth information. The block matching algorithm efficiently establishes ```correspondences``` between stereo camera images, while the SGBM algorithm optimizes the ```disparity map``` estimation process. Extensive experimentation validates the efficacy of this approach, demonstrating its capacity to provide per-pixel depth estimation at a significantly reduced ```cost``` compared to traditional LiDAR systems. Our findings indicate that the integration of ```pseudo-LiDAR``` systems presents a promising and cost-effective solution for replacing LiDAR sensors in drone applications, facilitating affordable depth perception and expanding the possibilities for aerial data collection and analysis.

## Dataset
For this project, the [KITTI dataset](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d) will be utilized, specifically the stereo camera images. The dataset includes a comprehensive [3D object detection benchmark](https://www.cvlibs.net/datasets/kitti/raw_data.php), comprising ```7,481``` training images and ```7,518``` test images. These images are accompanied by corresponding point clouds, providing a total of ```80,256``` labeled objects for analysis. Additionally, the ```synchronized and rectified raw data``` from the KITTI dataset will be employed during the **inference** stage of the project, further enhancing the accuracy and reliability of the results. The availability of this rich dataset enables thorough exploration and evaluation of the proposed methods and ensures robustness in the project's findings.

## Plan of Action
1. [Linear Camera Model](#lcm)
2. [Intrinsic and Extrinsic Parameters](#ie)
3. [Simple Stereo](#ss)
4. [Application of Simple Stereo](#ass)



------------------

<a name="lcm"></a>
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

<a name="ie"></a>
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

<a name="ss"></a>
## 3. Simple Stereo
Now we want to recover a 3-Dimensional structure of a scene from two images. Before we dive into this, let's ask ourselves, given a calibrated camera, can we find the 3D scene point from a sinple 2D image? The answer is **no**. But we do know that the corresponding 3D point must lie on an ```outgoing ray``` shown in green and given that the camera is calibrated, we know the equation of this ray.

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

<a name="ass"></a>
## 4. Application of Simple Stereo
Now we will try to find the distances of objects using the KITTI Dataset. For that, we first need to know the configuration of the cameras on the autonomous car. Thankfully, we have a  very detailed explanation describing the position and the baseline between the cameras as shown below.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/994541de-0959-4fae-ab33-5de84d2e603e" width="600" height="280"/>
</div>

When downloading the dataset for 3D Object Detection, we have the following files:

- **Left Images**
- **Right Images**
- **Calibration Data**
- **Labels**

### 4.1 Extract Projection Matrix
Below is an example of how the calibration data is. Since we are using left and right color images, we need to extract ```P2``` and ```P3``` to get the projection matrices.

```python
P0: 7.215377000000e+02 0.000000000000e+00 6.095593000000e+02 0.000000000000e+00 0.000000000000e+00 7.215377000000e+02 1.728540000000e+02 0.000000000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 0.000000000000e+00
P1: 7.215377000000e+02 0.000000000000e+00 6.095593000000e+02 -3.875744000000e+02 0.000000000000e+00 7.215377000000e+02 1.728540000000e+02 0.000000000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 0.000000000000e+00
P2: 7.215377000000e+02 0.000000000000e+00 6.095593000000e+02 4.485728000000e+01 0.000000000000e+00 7.215377000000e+02 1.728540000000e+02 2.163791000000e-01 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 2.745884000000e-03
P3: 7.215377000000e+02 0.000000000000e+00 6.095593000000e+02 -3.395242000000e+02 0.000000000000e+00 7.215377000000e+02 1.728540000000e+02 2.199936000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 2.729905000000e-03
R0_rect: 9.999239000000e-01 9.837760000000e-03 -7.445048000000e-03 -9.869795000000e-03 9.999421000000e-01 -4.278459000000e-03 7.402527000000e-03 4.351614000000e-03 9.999631000000e-01
Tr_velo_to_cam: 7.533745000000e-03 -9.999714000000e-01 -6.166020000000e-04 -4.069766000000e-03 1.480249000000e-02 7.280733000000e-04 -9.998902000000e-01 -7.631618000000e-02 9.998621000000e-01 7.523790000000e-03 1.480755000000e-02 -2.717806000000e-01
Tr_imu_to_velo: 9.999976000000e-01 7.553071000000e-04 -2.035826000000e-03 -8.086759000000e-01 -7.854027000000e-04 9.998898000000e-01 -1.482298000000e-02 3.195559000000e-01 2.024406000000e-03 1.482454000000e-02 9.998881000000e-01 -7.997231000000e-01
```
Note that we get a left and right projection matrix:

```python
Left P Matrix
[[     721.54           0      609.56      44.857]
 [          0      721.54      172.85     0.21638]
 [          0           0           1   0.0027459]]

Right P Matrix
[[     721.54           0      609.56     -339.52]
 [          0      721.54      172.85      2.1999]
 [          0           0           1   0.0027299]]

RO to Rect Matrix
[[    0.99992   0.0098378   -0.007445]
 [ -0.0098698     0.99994  -0.0042785]
 [  0.0074025   0.0043516     0.99996]]

Velodyne to Camera Matrix
[[  0.0075337    -0.99997  -0.0006166  -0.0040698]
 [   0.014802  0.00072807    -0.99989   -0.076316]
 [    0.99986   0.0075238    0.014808    -0.27178]]

IMU to Velodyne Matrix
[[          1  0.00075531  -0.0020358    -0.80868]
 [ -0.0007854     0.99989   -0.014823     0.31956]
 [  0.0020244    0.014825     0.99989    -0.79972]]
```
Next, we need to extract the **Intrinsic Matrix** and the **Extrinsic Matrix** from our **Projection Matrix**. Recall from the equation below:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/e9586b9d-b047-48ba-83df-7efaebb6e4eb"/>
</div>

We will use OpenCV's ```decomposeProjectionMatrix``` function for that:

```python
def decompose_projection_matrix(projection_matrix):
    """
    Decompose a projection matrix into camera matrix, rotation matrix, and translation vector.

    Args:
        projection_matrix (numpy.ndarray): 3x4 projection matrix.

    Returns:
        tuple: Tuple containing the decomposed components:
            - camera_matrix (numpy.ndarray): Camera matrix. [ fx   0   cx ]
                                                            [  0  fy   cy ]
                                                            [  0   0    1 ]
            - rotation_matrix (numpy.ndarray): Rotation matrix.
            - translation_vector (numpy.ndarray): Translation vector.
    """

    # Decompose the projection matrix
    camera_matrix, rotation_matrix, translation_vector, _, _, _, _ = cv2.decomposeProjectionMatrix(projection_matrix)
    translation_vector = translation_vector/translation_vector[3]
    # Return the decomposed components
    return camera_matrix, rotation_matrix, translation_vector
```

Below is what we get:

```python
Camera Matrix Left:
[[     721.54           0      609.56]
 [          0      721.54      172.85]
 [          0           0           1]]

Rotation Matrix Left:
[[          1           0           0]
 [          0           1           0]
 [          0           0           1]]

Translation Vector Left:
[[  -0.059849]
 [ 0.00035793]
 [ -0.0027459]
 [          1]]

Camera Matrix Right:
[[     721.54           0      609.56]
 [          0      721.54      172.85]
 [          0           0           1]]

Rotation Matrix Right:
[[          1           0           0]
 [          0           1           0]
 [          0           0           1]]

Translation Vector Right:
[[    0.47286]
 [  -0.002395]
 [ -0.0027299]
 [          1]]
```
Observe how the Rotation Matrix is just an **Identity Matrix**. We need to extract the **Focal Length** from the **Intrinsic Matrix** and calculate the **baseline** from the **translation vectors** as such:

```python
    # Extract the focal length and baseline
    focal_length_x = camera_matrix_right[0, 0]
    focal_length_y = camera_matrix_right[1, 1]
    baseline = abs(translation_vector_left[0] - translation_vector_right[0])
```

Output:

```python
Focal Length (x-direction): 721.5377

Focal Length (y-direction): 721.5377

Baseline: [    0.53271] 
```

Observe the baseline is ```0.53271``` m same as on the configuration on the autonomous car.


### 4.2 Extract Labels

We get a label file for each pair of images. Below is our label.txt file with each object having 15 values. 
```python
Car 0.00 0 -1.56 564.62 174.59 616.43 224.74 1.61 1.66 3.20 -0.69 1.69 25.01 -1.59
Car 0.00 0 1.71 481.59 180.09 512.55 202.42 1.40 1.51 3.70 -7.43 1.88 47.55 1.55
Car 0.00 0 1.64 542.05 175.55 565.27 193.79 1.46 1.66 4.05 -4.71 1.71 60.52 1.56
Cyclist 0.00 0 1.89 330.60 176.09 355.61 213.60 1.72 0.50 1.95 -12.63 1.88 34.09 1.54
DontCare -1 -1 -10 753.33 164.32 798.00 186.74 -1 -1 -1 -1000 -1000 -1000 -10
DontCare -1 -1 -10 738.50 171.32 753.27 184.42 -1 -1 -1 -1000 -1000 -1000 -10
```

```python
#Values    Name      Description
----------------------------------------------------------------------------
   1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                     truncated refers to the object leaving image boundaries
   1    occluded     Integer (0,1,2,3) indicating occlusion state:
                     0 = fully visible, 1 = partly occluded
                     2 = largely occluded, 3 = unknown
   1    alpha        Observation angle of object, ranging [-pi..pi]
   4    bbox         2D bounding box of object in the image (0-based index):
                     contains left, top, right, bottom pixel coordinates
   3    dimensions   3D object dimensions: height, width, length (in meters)
   3    location     3D object location x,y,z in camera coordinates (in meters)
   1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
   1    score        Only for results: Float, indicating confidence in
                     detection, needed for p/r curves, higher is better.
```
Credit to [DarylClimb](https://github.com/darylclimb/cvml_project/tree/master/projections/lidar_camera_projection/data) for this explanation.

Note that ```DontCare``` labels denote regions in which objects have not been labeled, for example, because they have been too far away from the laser scanner. We need to extract the bounding box coordinates and the distance of each object from the labels. We will compare them with the ground truth.

```python
def ground_truth_bbox(labels_file, object_class):
    lines = labels_file.split('\n')  # Split the input string into lines
    bounding_boxes = []

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace

        if line:
            data = line.split()

            # Extract relevant values for each object
            obj_type = data[0]
            #print(obj_type)
            truncated = float(data[1])
            occluded = int(data[2])
            alpha = float(data[3])
            bbox = [float(val) for val in data[4:8]]
            dimensions = [float(val) for val in data[8:11]]
            location = [float(val) for val in data[11:14]]
            distance = float(data[13])
            rotation_y = float(data[14])

            if obj_type in object_class:  # Check if obj_type is in the desired classes
                # Append bounding box dimensions and distance to the list
                bounding_boxes.append((bbox, distance))

                # Print the 3D bounding box information
                print("Object Type:", obj_type)
                print("Truncated:", truncated)
                print("Occluded:", occluded)
                print("Alpha:", alpha)
                print("Bounding Box:", bbox)
                print("Dimensions:", dimensions)
                print("Location:", location)
                print("True Distance:", distance)
                print("Rotation Y:", rotation_y)
                print("------------------------")
    return bounding_boxes
```

Output:

```python
Object Type: Car
Truncated: 0.0
Occluded: 0
Alpha: 1.71
Bounding Box: [481.59, 180.09, 512.55, 202.42]
Dimensions: [1.4, 1.51, 3.7]
Location: [-7.43, 1.88, 47.55]
True Distance: 47.55 
Rotation Y: 1.55
```

### 4.3 Display Left and Right Images

We start by displaying the right and left images of the KITTI dataset. Note that since the baseline is ```54 cm``` which is quite large compared to the OAK-D stereo cameras, we will have a greater disparity hence, it will be more accurate to calculate the depth map.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/296e30d9-bca9-4190-8376-e7690b69bb8f"/>
</div>



### 4.4 Compute Disparity Map

Next, we will use OpenCV's **Block Matching** function (```StereoBM_create```) and **Semi-Global Block Matching** function (```StereoSGBM_create```) to calculate the **disparity**. We will need to fine-tune some parameters: ```num_disparities```, ```block_size```, and ```window_size```.

```python
def compute_disparity(left_img, right_img, num_disparities=6 * 16, block_size=11, window_size=6, matcher="stereo_sgbm", show_disparity=True):
    """
    Compute the disparity map for a given stereo-image pair.

    Args:
        image (numpy.ndarray): Left image of the stereo pair.
        img_pair (numpy.ndarray): Right image of the stereo pair.
        num_disparities (int): Maximum disparity minus minimum disparity.
        block_size (int): Size of the block window. It must be an odd number.
        window_size (int): Size of the disparity smoothness window.
        matcher (str): Matcher algorithm to use ("stereo_bm" or "stereo_sgbm").
        show_disparity (bool): Whether to display the disparity map using matplotlib.

    Returns:
        numpy.ndarray: The computed disparity map.
    """
    if matcher == "stereo_bm":
        # Create a Stereo BM matcher
        matcher = cv2.StereoBM_create(numDisparities=num_disparities, blockSize=block_size)
    elif matcher == "stereo_sgbm":
        # Create a Stereo SGBM matcher
        matcher = cv2.StereoSGBM_create(
            minDisparity=0, numDisparities=num_disparities, blockSize=block_size,
            P1=8 * 3 * window_size ** 2, P2=32 * 3 * window_size ** 2,
            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
        )

    # Convert the images to grayscale
    left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

    # Compute the disparity map
    disparity = matcher.compute(left_gray, right_gray).astype(np.float32) / 16


    if show_disparity:
        # Display the disparity map using matplotlib
        plt.imshow(disparity, cmap="CMRmap_r") #CMRmap_r # cividis
        plt.title('Disparity map with SGBM', fontsize=12)
        plt.show()

    return disparity
```
Observe how the disparity using Block Matching is noisier than SGBM. We will use the SGBM algorithm from now on.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/bb3a6e01-b584-4c8b-b62c-fb3c09877c51" width="400" height="250"/> 
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/27d0eb33-9c5c-42b5-bbf4-ac9efdbe0da1" width="400" height="250"/>
</div>

Note that we have a white strip on the left of the images as there are no features to match from the left image to the right image. This depends on the ```block_size``` parameter.

### 4.5 Compute Depth Map
Next, we will use the **disparity map** to output a **depth map**. We will use the equation below:

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/751c24e2-6e8b-46af-9672-ec0fcbcd31da"/>
</div>

We take in the **baseline**, **focal length**, and the **disparity map** in order to calculate the depth of each pixel:

```python
def calculate_depth_map(disparity, baseline, focal_length, show_depth_map=True):
    """
    Calculates the depth map from a given disparity map, baseline, and focal length.

    Args:
        disparity (numpy.ndarray): Disparity map.
        baseline (float): Baseline between the cameras.
        focal_length (float): Focal length of the camera.

    Returns:
        numpy.ndarray: Depth map.
    """

    # Replace all instances of 0 and -1 disparity with a small minimum value (to avoid div by 0 or negatives)
    disparity[disparity == 0] = 0.1
    disparity[disparity == -1] = 0.1

    # Initialize the depth map to match the size of the disparity map
    depth_map = np.ones(disparity.shape, np.single)

    # Calculate the depths
    depth_map[:] = focal_length * baseline / disparity[:]

    if show_depth_map:
        # Display the disparity map using matplotlib
        plt.imshow(depth_map, cmap="cividis") #CMRmap_r # cividis
        plt.show()

    return depth_map
```

Our output is a depth map that outputs the depth of each pixel. 


<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/08cfd21b-68ee-4d1e-9f03-8ab48074a052" width=550" height="300"/>
</div>

The depth map represents ```per-pixel depth estimation```. However, we are interested in getting the depth or distances of some specific obstacles such as cars or pedestrians. Hence, we will use an object detection algorithm in order to segment our depth map and get the distances of these objects only.

https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/1f402ee7-fa2c-45ba-90d7-4be6de7ca684

### 4.6 Object Detection
The next step is to use ```YOLOv8``` to detect objects in our frames. We want to get the **coordinates** of the **bounding boxes**.

```python
def get_bounding_box_center_frame(frame, model, names, object_class, show_output=True):

    bbox_coordinates = []
    frame_copy = frame.copy()

    # Perform object detection on the input frame using the specified model
    results = model(frame)

    # Iterate over the results of object detection
    for result in results:

        # Iterate over each bounding box detected in the result
        for r in result.boxes.data.tolist():
            # Extract the coordinates, score, and class ID from the bounding box
            x1, y1, x2, y2, score, class_id = r
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)

            # Get the class name based on the class ID
            class_name = names.get(class_id)


            # Check if the class name matches the specified object_class and the detection score is above a threshold
            if class_name in object_class  and score > 0.5:
                bbox_coordinates.append([x1, y1, x2, y2])

                # Draw bounding box on the frame
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)


    if show_output:
        # Convert frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        # Show the output frame with bounding boxes
        cv2.imshow("Output", frame_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # Return the list of center coordinates
    return bbox_coordinates
```

We decide to detect ```cars```, ```persons```, and ```bicycles``` only.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/8b41ee45-40fc-4bc7-a0e7-1b7c83854080" width=750" height="250"/>
</div>



### 4.7 Distances with Object Detection
Since now we have the **bounding box coordinates** and the **depth map** for each frame, we can use two pieces of data and extract the depth of each obstacle. 

    We get the distance of an obstacle by indexing the depth map using the center of the bounding boxes.

```python
def calculate_distance(bbox_coordinates, frame, depth_map, disparity_map, show_output=True):
    frame_copy = frame.copy()

    # Normalize the disparity map to [0, 255]
    disparity_map_normalized = cv2.normalize(disparity_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Apply a colorful colormap to the disparity map
    colormap = cv2.COLORMAP_JET
    disparity_map_colored = cv2.applyColorMap(disparity_map_normalized, colormap)

    # Normalize the depth map to [0, 255]
    depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Apply a colorful colormap to the depth map
    colormap = cv2.COLORMAP_BONE
    depth_map_colored = cv2.applyColorMap(depth_map_normalized, colormap)

    for bbox_coor in bbox_coordinates:
        x1, y1, x2, y2 = bbox_coor
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        distance = depth_map[center_y][center_x]
        print("Calculated distance:", distance)

        # Convert distance to string
        distance_str = f"{distance:.2f} m"

        # Draw bounding box on the frame
        cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw bounding box on the frame
        cv2.rectangle(disparity_map_colored, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw bounding box on the frame
        cv2.rectangle(depth_map_colored, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate the text size
        text_size, _ = cv2.getTextSize(distance_str, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

        # Calculate the position for placing the text
        text_x = center_x - text_size[0] // 2
        text_y = y1 - 10  # Place the text slightly above the bounding box

        # Calculate the rectangle coordinates
        rect_x1 = text_x - 5
        rect_y1 = text_y - text_size[1] - 5
        rect_x2 = text_x + text_size[0] + 5
        rect_y2 = text_y + 5

        # Draw white rectangle behind the text
        cv2.rectangle(frame_copy, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), cv2.FILLED)

        # Put text at the center of the bounding box
        cv2.putText(frame_copy, distance_str, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # Draw white rectangle behind the text
        cv2.rectangle(disparity_map_colored, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), cv2.FILLED)

        # Put text at the center of the bounding box
        cv2.putText(disparity_map_colored, distance_str, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # Draw white rectangle behind the text
        cv2.rectangle(depth_map_colored, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), cv2.FILLED)

        # Put text at the center of the bounding box
        cv2.putText(depth_map_colored, distance_str, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)



    if show_output:
        # Convert frame from BGR to RGB
        #frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)

        # Show the output frame with bounding boxes
        cv2.imshow("Output disparity map", disparity_map_colored)
        cv2.imshow("Output frame", frame_copy)
        cv2.imshow("Output depth map", depth_map_colored)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return disparity_map_colored, frame_copy, depth_map_colored
```
We draw the bounding boxes and the distance of the objects from the camera is displayed on top in meters.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/d5443417-552d-46cd-8fe4-2ea55146507b" width=750" height="550"/>
</div>

### 4.8 Compare with Ground Truth
We can also compare our prediction of distances with the ```ground truth```. The image on the left(red) is the ground truth whereas the image on the right is our **prediction** using SGBM. We still have a discrepancy of ```0.41 m``` which is still a huge number when it comes to self-driving cars.


<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/583c0a6c-0267-4b9a-9056-1159dd8ebe6f" width="400" height="180"/> 
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/341622d5-ce3d-4bb6-83b1-1a735729837e" width="400" height="180"/>
</div>

In this example, we have a difference of ```0.61 m```.

<div align="center">
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/a62203a0-e214-477f-b163-4c16a69680a2" width="400" height="180"/>
  <img src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/cfbff31d-d8cf-44d7-8036-da7f20c474e0" width="400" height="180"/> 
</div>


### 4.9 Pipeline

Finally, we want to create a ```pipeline``` function whereby:

1. We take in all **left** and **right** images
2. Calculate the **disparity**
3. Create a **depth map**
4. Run an **object detection**
5. Display the **distances** with their **bounding boxes**.

```python
def pipeline(left_image, right_image, object_class):
    """
    Performs a pipeline of operations on stereo images to obtain a colored disparity map, RGB frame, and colored depth map.

    Input:
    - left_image: Left stereo image (RGB format)
    - right_image: Right stereo image (RGB format)
    - object_class: List of object classes of interest for bounding box retrieval

    Output:
    - disparity_map_colored: Colored disparity map (RGB format)
    - frame_rgb: RGB frame
    - depth_map_colored: Colored depth map (RGB format)
    """
    global focal_length

    # Calculate the disparity map
    disparity_map = compute_disparity(left_image, right_image, num_disparities=90, block_size=5, window_size=5,
                                      matcher="stereo_sgbm", show_disparity=False)

    # Calculate the depth map
    depth_map = calculate_depth_map(disparity_map, baseline, focal_length, show_depth_map=False)

    # Get bounding box coordinates for specified object classes
    bbox_coordinates = get_bounding_box_center_frame(left_image, model, names, object_class, show_output=False)

    # Calculate colored disparity map, RGB frame, and colored depth map
    disparity_map_colored, frame_rgb, depth_map_colored = calculate_distance(bbox_coordinates, left_image, depth_map, disparity_map, show_output=False)

    return disparity_map_colored, frame_rgb, depth_map_colored

```

Below are the results:


<video src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/f10614c9-8441-4789-b6dd-87c9be27d74c" controls="controls" style="max-width: 730px;">
</video>


<video src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/5ae69b2a-a98e-4a7d-81dd-07c184ad6fd6" controls="controls" style="max-width: 730px;">
</video>

  
<video src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/d5ec731e-192b-4594-80b0-4ec5080de8ee" controls="controls" style="max-width: 730px;">
</video>


<video src="https://github.com/yudhisteer/Pseudo-LiDARs-and-3D-Computer-Vision/assets/59663734/654c0d91-e491-4daa-aa58-b57f3f16833b" controls="controls" style="max-width: 730px;">
</video>


## Conclusion
In conclusion, while traditional techniques such as ```Local```, ```Global```, and ```Semi-Global Matching``` algorithms have been employed in this project, the utilization of Deep Learning provides alternative approaches to determining disparity. For example:

- **MC-CNN**: an algorithm that uses Siamese Networks logic to find disparity

- **PSM-Net**: an algorithm that uses Pyramids architectures

- **AnyNet**: an algorithm optimized for mobile

- **RAFT-Stereo**: an optical flow algorithm adapted to Stereo Vision

- **CreStereo** which is compatible with the OAK-D camera

By employing advanced neural networks architectures like MC-CNN, PSM-Net, AnyNet, RAFT-Stereo, and CreStereo, we can achieve more accurate and reliable depth maps, enabling UAVs to better perceive their surroundings. This improved distance estimation is crucial for obstacle detection during UAV package delivery operations. With precise depth perception, UAVs can effectively identify and locate obstacles such as buildings, trees, or other objects that may obstruct their flight path. By leveraging deep learning, UAVs can analyze real-time scenes, enabling them to make informed decisions and adjust their trajectory to avoid potential collisions or navigate complex environments safely.




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
16. https://www.youtube.com/watch?v=AYjgeaQR8uQ&ab_channel=SevensenseRobotics
17. https://arxiv.org/pdf/2007.10743.pdf
