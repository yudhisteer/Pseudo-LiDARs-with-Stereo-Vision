import numpy as np
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import os


def display_image_pair(index, left_image_folder, right_image_folder, show_picture=True):
    """
    Load and display a pair of left and right images from the specified folders.

    Args:
        index (int): Index of the image pair to display.
        left_image_folder (str): Path to the folder containing the left images.
        right_image_folder (str): Path to the folder containing the right images.
        show_picture (bool): Whether to display the image pair using matplotlib.
    """
    # Load the left image
    left_image_path = os.path.join(left_image_folder, os.listdir(left_image_folder)[index])
    left_image = cv2.cvtColor(cv2.imread(left_image_path), cv2.COLOR_BGR2RGB)

    # Load the right image
    right_image_path = os.path.join(right_image_folder, os.listdir(right_image_folder)[index])
    right_image = cv2.cvtColor(cv2.imread(right_image_path), cv2.COLOR_BGR2RGB)

    if show_picture:
        # Create subplots and display the image pair
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.imshow(left_image)
        ax1.set_title('Image Left', fontsize=15)
        ax2.imshow(right_image)
        ax2.set_title('Image Right', fontsize=15)

        # Show the plot
        plt.show()

    # Return the left and right images
    return left_image, right_image



#--- Function to compute and display disparity
def compute_disparity(left_img, right_img, num_disparities=6 * 16, block_size=11, window_size=6, matcher="stereo_sgbm", show_disparity=True):
    """
    Compute the disparity map for a given stereo image pair.

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

def display_text_file(index, folder_path):
    """
    Display the contents of a text file based on the specified index.

    Args:
        index (int): Index of the text file to display.
        folder_path (str): Path to the folder containing the text files.

    Returns:
        str: Contents of the text file.
    """
    # Get the list of text files in the folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    if index >= 0 and index < len(txt_files):
        # Get the file path of the text file based on the index
        file_path = os.path.join(folder_path, txt_files[index])

        # Open the file and read its contents
        with open(file_path, 'r') as file:
            contents = file.read()

        # Display the contents of the text file
        print(f"Text file at index {index}:\n{contents}")

        # Return the contents of the text file
        return contents
    else:
        print("Invalid index.")
        return None


#--- Function to retrieve callibration parameters
def get_calibration_parameters(file_contents):
    """
    Retrieve calibration parameters from the contents of a calibration file.

    Args:
        file_contents (str): Contents of the calibration file.

    Returns:
        tuple: Tuple containing the calibration parameters:
            - p_left (numpy.ndarray): Projection matrix for the left camera.
            - p_right (numpy.ndarray): Projection matrix for the right camera.
            - p_ro_rect (numpy.ndarray): Rectification matrix.
            - p_velo_to_cam (numpy.ndarray): Transformation matrix from velodyne to camera coordinates.
            - p_imu_to_velo (numpy.ndarray): Transformation matrix from IMU to velodyne coordinates.
    """
    fin = file_contents.split('\n')
    for line in fin:
        if line[:2] == 'P2':
            p_left = np.array(line[4:].strip().split(" ")).astype('float32').reshape(3, -1)
        elif line[:2] == 'P3':
            p_right = np.array(line[4:].strip().split(" ")).astype('float32').reshape(3, -1)
        elif line[:7] == 'R0_rect':
            p_ro_rect = np.array(line[9:].strip().split(" ")).astype('float32').reshape(3, -1)
        elif line[:14] == 'Tr_velo_to_cam':
            p_velo_to_cam = np.array(line[16:].strip().split(" ")).astype('float32').reshape(3, -1)
        elif line[:14] == 'Tr_imu_to_velo':
            p_imu_to_velo = np.array(line[16:].strip().split(" ")).astype('float32').reshape(3, -1)
    return p_left, p_right, p_ro_rect, p_velo_to_cam, p_imu_to_velo

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
        plt.title('Depth map', fontsize=12)
        plt.show()

    return depth_map




def save_disparity_maps(left_image_folder, right_image_folder, output_folder):
    # Get the list of image files in the left image folder
    left_image_files = os.listdir(left_image_folder)

    # Iterate over the image files
    for image_file in left_image_files:
        # Construct the paths for the left and right images
        left_image_path = os.path.join(left_image_folder, image_file)
        right_image_path = os.path.join(right_image_folder, image_file)

        # Read the left and right images
        left_image = cv2.imread(left_image_path)
        right_image = cv2.imread(right_image_path)

        # Calculate the disparity map
        disparity_map = compute_disparity(left_image, right_image, num_disparities=90, block_size=5, window_size=5,
                                          matcher="stereo_sgbm", show_disparity=False)

        # Normalize the disparity map to [0, 255]
        disparity_map_normalized = cv2.normalize(disparity_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        # Apply a colorful colormap to the disparity map
        colormap = cv2.COLORMAP_JET
        disparity_map_colored = cv2.applyColorMap(disparity_map_normalized, colormap)

        # Construct the output file path
        output_file = os.path.join(output_folder, image_file)

        # Save the disparity map as an image
        cv2.imwrite(output_file, disparity_map_colored)

        print(f"Disparity map saved: {output_file}")



def save_depth_maps(left_image_folder, right_image_folder, output_folder, baseline, focal_length):
    # Get the list of image files in the left image folder
    left_image_files = os.listdir(left_image_folder)

    # Iterate over the image files
    for image_file in left_image_files:
        # Construct the paths for the left and right images
        left_image_path = os.path.join(left_image_folder, image_file)
        right_image_path = os.path.join(right_image_folder, image_file)

        # Read the left and right images
        left_image = cv2.imread(left_image_path)
        right_image = cv2.imread(right_image_path)

        # Calculate the disparity map
        disparity_map = compute_disparity(left_image, right_image, num_disparities=90, block_size=5, window_size=5,
                                          matcher="stereo_sgbm", show_disparity=False)

        # Calculate the depth map
        depth_map = calculate_depth_map(disparity_map, baseline, focal_length, show_depth_map=False)

        # # Normalize the depth map to [0, 255]
        # depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        #
        # # Apply a colorful colormap to the depth map
        # colormap = cv2.COLORMAP_BONE
        # depth_map_colored = cv2.applyColorMap(depth_map_normalized, colormap)

        # Construct the output file path
        output_file = os.path.join(output_folder, image_file)

        # Save the depth map as an image
        cv2.imwrite(output_file, depth_map)

        print(f"Depth map saved: {output_file}")




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


def display_ground_truth(frame, bounding_boxes, show_output=True):
    frame_copy = frame.copy()
    for bbox, distance in bounding_boxes:
        # Extract bounding box coordinates
        x1, y1, x2, y2 = map(int, bbox)
        center_x = (x1 + x2) // 2

        # Convert distance to string
        distance_str = f"{distance:.2f} m"

        # Draw bounding box on the frame
        cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

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
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

    if show_output:
        # Convert frame from BGR to RGB
        image_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        # Display the image with bounding boxes
        cv2.imshow("Bounding Boxes", image_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


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


def process_pipeline_images(left_image_folder, right_image_folder, output_folder_distance, object_class=['car', 'bicycle']):
    # Get the list of image files in the left image folder
    left_image_files = os.listdir(left_image_folder)

    # Iterate over the image files
    for image_file in left_image_files:
        # Construct the paths for the left and right images
        left_image_path = os.path.join(left_image_folder, image_file)
        right_image_path = os.path.join(right_image_folder, image_file)

        # Read the left and right images
        left_image = cv2.imread(left_image_path)
        right_image = cv2.imread(right_image_path)

        disparity_map_colored, frame_rgb, depth_map_colored = pipeline(left_image, right_image, object_class)

        # Construct the output file path
        output_file = os.path.join(output_folder_distance, image_file)

        # Save the disparity map as an image
        cv2.imwrite(output_file, disparity_map_colored)

        print(f"Disparity map saved: {output_file}")

def frames_to_video(frame_folder, output_folder, output_filename):
    """
    Converts a sequence of frames in a folder into an MP4 video and saves it in the specified output folder.

    Args:
        frame_folder (str): Path to the folder containing the frames.
        output_folder (str): Path to the output folder where the video will be saved.
        output_filename (str): Name of the output video file (including the .mp4 extension).
    """

    # Get the list of frame filenames in the folder
    frame_filenames = sorted(os.listdir(frame_folder))

    # Read the first frame to get frame size information
    first_frame_path = os.path.join(frame_folder, frame_filenames[0])
    first_frame = cv2.imread(first_frame_path)
    height, width, channels = first_frame.shape

    # Define the video codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_path = os.path.join(output_folder, output_filename)
    video_writer = cv2.VideoWriter(output_path, fourcc, 15, (width, height))

    # Iterate over the frame filenames and write each frame to the video
    for frame_filename in frame_filenames:
        frame_path = os.path.join(frame_folder, frame_filename)
        frame = cv2.imread(frame_path)
        video_writer.write(frame)

    # Release the VideoWriter and print completion message
    video_writer.release()
    print("Video saved successfully at:", output_path)



def concatenate_videos_vertical(video1_path, video2_path, output_path):
    # Read the input videos
    video1 = cv2.VideoCapture(video1_path)
    video2 = cv2.VideoCapture(video2_path)

    # Get video properties
    width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video1.get(cv2.CAP_PROP_FPS)

    # Create a VideoWriter object to save the concatenated video
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height * 2))

    while True:
        # Read frames from both videos
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()

        if not ret1 or not ret2:
            # Either video1 or video2 has ended
            break

        # Resize the frames to match the width of the output video
        frame1_resized = cv2.resize(frame1, (width, height))
        frame2_resized = cv2.resize(frame2, (width, height))

        # Concatenate the frames vertically
        concat_frame = cv2.vconcat([frame1_resized, frame2_resized])

        # Write the concatenated frame to the output video
        output_video.write(concat_frame)

    # Release resources
    video1.release()
    video2.release()
    output_video.release()

    print("Concatenation complete. Output video saved:", output_path)












if __name__ == '__main__':

    # Get the current directory
    current_directory = os.getcwd()

    # Go back to the parent directory
    parent_directory = os.path.dirname(current_directory)

    # Set input directory
    left_image_folder = os.path.join(parent_directory, 'Data', 'Left', 'image_2')
    right_image_folder = os.path.join(parent_directory, 'Data', 'Right', 'image_3')
    labels_folder = os.path.join(parent_directory, 'Data', 'Labels', 'training')
    calibration_folder = os.path.join(parent_directory, 'Data', 'Callibration', 'training', 'calib')
    output_disparity_folder = os.path.join(parent_directory, 'Data', 'Output_Disparity_1')
    output_depth_folder = os.path.join(parent_directory, 'Data', 'Output_Depth_1')


    # Choose index of image
    index = 13

    # Display the image pair and get the left and right images
    left_image, right_image = display_image_pair(index=index, left_image_folder=left_image_folder, right_image_folder=right_image_folder, show_picture=True)
    print("\nImage shape: ", left_image.shape)

    # Compute disparity map
    disparity_map = compute_disparity(left_image, right_image, num_disparities=90, block_size=5, window_size=5, matcher="stereo_sgbm", show_disparity=True) #stereo_bm   #stereo_sgbm
    print(disparity_map)
    print("\nDisparity map shape: ", disparity_map.shape)

    # Display the text file contents
    calibration_file = display_text_file(index, calibration_folder)
    label_file = display_text_file(index, labels_folder)

    # Extract calibration parameters
    p_left, p_right, p_ro_rect, p_velo_to_cam, p_imu_to_velo = get_calibration_parameters(calibration_file)
    print("\nLeft P Matrix")
    print(p_left)
    print("\nRight P Matrix")
    print(p_right)
    print("\nRO to Rect Matrix")
    print(p_ro_rect)
    print("\nVelodyne to Camera Matrix")
    print(p_velo_to_cam)
    print("\nIMU to Velodyne Matrix")
    print(p_imu_to_velo)

    # Decompose the projection matrix
    camera_matrix_left, rotation_matrix_left, translation_vector_left = decompose_projection_matrix(p_left)
    camera_matrix_right, rotation_matrix_right, translation_vector_right = decompose_projection_matrix(p_right)

    # Print the decomposed components
    print("\nCamera Matrix Left:")
    print(camera_matrix_left)
    print("\nRotation Matrix Left:")
    print(rotation_matrix_left)
    print("\nTranslation Vector Left:")
    print(translation_vector_left)

    print("\nCamera Matrix Right:")
    print(camera_matrix_right)
    print("\nRotation Matrix Right:")
    print(rotation_matrix_right)
    print("\nTranslation Vector Right:")
    print(translation_vector_right)

    # Extract the focal length and baseline
    focal_length_x = camera_matrix_right[0, 0]
    focal_length_y = camera_matrix_right[1, 1]
    baseline = abs(translation_vector_left[0] - translation_vector_right[0])

    # Print the extracted values
    print("\nFocal Length (x-direction):", focal_length_x)
    print("\nFocal Length (y-direction):", focal_length_y)
    print("\nBaseline:", baseline, "\n")

    depth_map = calculate_depth_map(disparity=disparity_map, baseline=baseline, focal_length=focal_length_x, show_depth_map=True)
    print("Depth Map: ", depth_map)
    print("\nDepth map shape: ",depth_map.shape)
    print("\nDepth map distance: ", depth_map[200,600], " m")

    #save_disparity_maps(left_image_folder, right_image_folder, output_disparity_folder)

    #save_depth_maps(left_image_folder, right_image_folder, output_depth_folder, baseline, focal_length_x)

    # Instantiate model
    weights_path = os.path.join(parent_directory, 'Weights', 'yolov8m.pt')
    model = YOLO(weights_path)
    names = model.names
    print(names)

    # Process the frame to get bounding box centers
    bbox_coordinates = get_bounding_box_center_frame(left_image, model, names, object_class=['car', 'bicycle'], show_output=True)

    # Calculate distance from camera to objects
    disparity_map_distance, frame_distance, depth_map_distance = calculate_distance(bbox_coordinates, left_image, depth_map, disparity_map,show_output=True)

    ###-------COMPARE WITH GROUND TRUTH

    # Get data from labels.txt
    bounding_boxes_ground_truth = ground_truth_bbox(label_file, object_class=['Car', 'Cyclist', 'Pedestrian'])

    # Display ground truth image with distance
    display_ground_truth(left_image, bounding_boxes_ground_truth, show_output=True)





    ###-------------PIPELINE ON SINGLE IMAGE
    focal_length = focal_length_x
    index = 7

    # Load the left image
    left_image_path = os.path.join(left_image_folder, os.listdir(left_image_folder)[index])
    left_image = cv2.cvtColor(cv2.imread(left_image_path), cv2.COLOR_BGR2RGB)
    print(left_image)

    # Load the right image
    right_image_path = os.path.join(right_image_folder, os.listdir(right_image_folder)[index])
    right_image = cv2.cvtColor(cv2.imread(right_image_path), cv2.COLOR_BGR2RGB)


    disparity_map_colored, frame_rgb, depth_map_colored = pipeline(left_image, right_image, object_class=['car', 'bicycle'])

    # # Show the output frame with bounding boxes
    # frame_rgb = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2RGB)
    # cv2.imshow("Output disparity map", disparity_map_colored)
    # cv2.imshow("Output frame", frame_rgb)
    # cv2.imshow("Output depth map", depth_map_colored)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()





    ### ------------ PIPELINE ON FOLDER ----------------------------- ###
    # Set input and output directory
    left_image_folder = os.path.join(parent_directory, 'Data', 'Left_4')
    right_image_folder = os.path.join(parent_directory, 'Data', 'Right_4')
    output_folder_distance = os.path.join(parent_directory, 'Data', 'Output_Disparity_Distance_4')
    output_video_folder = os.path.join(parent_directory, 'Data', 'Output_Video')

    # ##--- Process all images in folder and save disparity map
    # process_pipeline_images(left_image_folder, right_image_folder, output_folder_distance, object_class=['car', 'bicycle', 'person'])
    #
    # ### ---- Convert frames to video
    # frames_to_video(output_folder_distance, output_video_folder, 'output_disparity_4.mp4')
    # frames_to_video(left_image_folder, output_video_folder, 'output_4.mp4')


    ### - Concat videos
    # video_1 = output_video_folder = os.path.join(parent_directory, 'Data', 'Output_Video', 'output_1.mp4')
    # video_2 = output_video_folder = os.path.join(parent_directory, 'Data', 'Output_Video', 'output_disparity_1.mp4')
    # output_video_folder = os.path.join(parent_directory, 'Data', 'Output_Video', 'concat_1.mp4')
    # concatenate_videos_vertical(video_1, video_2, output_video_folder)
    #
    #








