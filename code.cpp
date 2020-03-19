#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <vector>

#include <iostream>

using namespace std;
using namespace cv;


int maxContourId(vector <vector<Point>> contours) {
    double maxArea = 0;
    int maxAreaContourId = -1;
    for (int j = 0; j < contours.size(); j++) {
        double newArea = contourArea(contours.at(j));
        if (newArea > maxArea) {
            maxArea = newArea;
            maxAreaContourId = j;
        }
    }
    return maxAreaContourId;
}

int main() {

    VideoCapture capWebcam(0);  

    if (capWebcam.isOpened() == false) {    
    cout << "error: Webcam connect unsuccessful\n"; 
    return(0);      
    }

    Mat frame;
    Mat hsv;    
    Mat mask; 

    char charCheckForEscKey = 0;

    int lowH = 80;
    int highH = 100;

    int lowS = 100;
    int highS = 255;

    int lowV = 20;
    int highV = 225;
 
    while (charCheckForEscKey != 27 && capWebcam.isOpened()) {  
        bool blnFrameReadSuccessfully = capWebcam.read(frame); 

        if (!blnFrameReadSuccessfully || frame.empty()) {    
             cout << "error: frame can't read \n"; 
        break;      
        }

        cvtColor(frame, hsv, COLOR_BGR2HSV);    

        inRange(hsv, Scalar(lowH, lowS, lowV), Scalar(highH, highS, highV), mask);    
        erode(mask, mask, 0);
        dilate(mask, mask, 0); 

        vector<vector<Point> > contours;
        findContours( mask, contours, RETR_TREE, CHAIN_APPROX_SIMPLE );
        int i = maxContourId(contours);
        Point2f center;
        float radius;
        minEnclosingCircle(contours[i], center, radius);
        if(radius>10){
            circle( frame, center, 1, Scalar(0,0,255), 3, LINE_AA);
        }

        namedWindow("frame");
        namedWindow("mask"); 

        imshow("frame", frame);    
        imshow("mask", mask);

        charCheckForEscKey = waitKey(1);     
    }
 
 return(0);           
}