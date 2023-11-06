# Delete Duplicate Frames
 This script is initially built for removing repeated frames from a video file. But then I realized that only one command is enough to do the job:

 ~~~
ffmpeg -i PATH_OF_SOURCE_FILE.mp4 -vf mpdecimate,setpts=N/FRAME_RATE/TB PATH_OF_OUTPUT_FILE.mp4
~~~

So now this repository is used for keeping codes for future needs.


## Prerequisites for running the above command:



## Prerequisites for runing the codes:

- Python 3.x
- OpenCV library for Python (`opencv-python`)
- tqdm
- ffmpeg


