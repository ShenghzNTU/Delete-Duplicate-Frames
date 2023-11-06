import cv2
import numpy as np
from tqdm import tqdm
import argparse

# one command can replace all the following program:  ffmpeg -i PATH_OF_SOURCE_FILE.mp4 -vf mpdecimate,setpts=N/FRAME_RATE/TB PATH_OF_OUTPUT_FILE.mp4


# How to use: python main.py --input input.mp4 --output output.mp4 --num_repeats 2


# Set up the argument parser
parser = argparse.ArgumentParser(description='Remove repeated frames from a video.')
parser.add_argument('-i', '--input', help='Input video file path', required=True)
parser.add_argument('-o', '--output', help='Output video file path', required=True)
parser.add_argument('-n', '--num_repeats', help='Number of consecutive frames to keep', type=int, default=3)
args = parser.parse_args()

# Use the arguments to set the video file paths and the number of repeated frames to detect
video_path = args.input
output_path = args.output
n = args.num_repeats  # Number of consecutive frames to check for repeats

# Open the video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Cannot open video file {video_path}.")
    exit()

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Create a VideoWriter object to write the video
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Read the first frame
ret, prev_frame = cap.read()
if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    exit()

# Initialize variables
consecutive_count = 1
prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Process video frames with a progress bar
for _ in tqdm(range(total_frames), desc="Processing video"):
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Check if the current frame is identical to the previous frame
    if np.array_equal(prev_frame_gray, frame_gray):
        consecutive_count += 1
    else:
        consecutive_count = 1

    # Write the first of the repeated frames, or a unique frame, to the output
    if consecutive_count <= n:
        out.write(frame)

    # Update the previous frame
    prev_frame_gray = frame_gray

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()
