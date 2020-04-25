# opencv

### This repo contains some useful opencp code
### Files and their description are as follows:
* distance.py           : Finds the distance of a blue ball from the camera using the focal length of the camera(webcam)
* code.cpp              : (Blue) Ball detection in c++
* configure_color.py    : uses webcam to show your video with a bunch of sliders, so it's easy to find the HSV values to select.
* configure_distance.py : Useful for finding the apparent focal length of your webcam
* HSV_plot.png          : Plot to decide HSV Values
* objectdetect.py       : (Blue) Ball detection in python
* clean                 : script to clean up the CMake files

### C++ code is build by cmake
command to build and run it
```
cmake .
make
./code
```
