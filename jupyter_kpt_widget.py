

## just quickly adding this here 230709 
## todo: tidy and incorporate into notebooks later

from google.colab import output
output.enable_custom_widget_manager()

%matplotlib widget
import matplotlib.pyplot as plt
import cv2
from ipywidgets import Button, Output, VBox
from IPython.display import display

# Open the video
video = cv2.VideoCapture("/content/tapnet/examplar_videos/horsejump-high.mp4")

# Read the first frame
ret, frame = video.read()

# Check if frame is read correctly
if not ret:
    print("Can't receive frame. Exiting ...")

# OpenCV reads images in BGR format, we need to convert it to RGB
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Create button and output widgets
button = Button(description="Done")
out = Output()

# Display button and output
display(VBox([button, out]))

# Initialize keypoints list
keypoints = []

# Plot image
fig, ax = plt.subplots()
ax.imshow(frame)

# Function to record mouse clicks
def onclick(event):
    global keypoints
    if event.button == 1:  # If left mouse button is clicked
        keypoints.append([event.xdata, event.ydata])
        ax.plot(event.xdata, event.ydata, marker='x', color='red')
        fig.canvas.draw()

# Connect the function to the figure
fig.canvas.mpl_connect('button_press_event', onclick)

# Function to handle button click
def on_button_clicked(b):
    global keypoints
    with out:
        print("Keypoints:")
        print(keypoints)

        # Convert to numpy array and add a time dimension
        keypoints_array = np.array(keypoints, dtype=np.int32)  # Convert to numpy array
        time_array = np.zeros((keypoints_array.shape[0], 1), dtype=np.int32)  # Create a time array with the same number of rows
        keypoints_3d = np.hstack([time_array, keypoints_array])  # Add the time dimension to the keypoints array

        # Save the keypoints to a file
        np.save("keypoints.npy", keypoints_3d)  # Save to a .npy file

# Connect the function to the button
button.on_click(on_button_clicked)
