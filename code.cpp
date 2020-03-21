#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;
int main(int argc, char** argv )
{
    int lh=80;
    int ls=100;
    int lv=20;

    int uh=100;
    int us=255;
    int uv=255;

    VideoCapture cap(0);
    if(cap.isOpened()==false){
        cout<<"cannot connect to camera"<<endl;
        cin.get();
        return -1;
    }

    double sum_time_count=0;
    int n=0;


    bool grabbed=1;
    while(grabbed){

        int64 e1 = getTickCount();

        Mat frame;
        Mat mask;
        grabbed = cap.read(frame);

        cvtColor(frame,mask,COLOR_BGR2HSV);
        inRange(mask,Scalar(lh,ls,lv),Scalar(uh,us,uv),mask);
        erode(mask, mask, Mat(), Point(), 3);
        dilate(mask, mask, Mat(), Point(), 3);


        vector<vector<Point> > cnts;

        findContours( mask, cnts, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE );

        Point2f center;
        float radius;
        if(cnts.size() > 0){
            double max=0;
            int max_index=0;
            int i=0;
            for (int i = 0; i < cnts.size(); i++) {
                double newArea = contourArea(cnts.at(i));
                if (newArea > max) {
                    max = newArea;
                    max_index = i;
                } 
            }

            minEnclosingCircle(cnts[i],center,radius);

            if(radius > 10)
                circle( frame, center, radius, (255,255,0), 2 );
        }


        imshow("Mask",mask);
        imshow("Frame", frame);


        int64 e2 = getTickCount();
        double t = (e2-e1)/getTickFrequency();
        sum_time_count+=t;n++;
        cout<<"frame time: "<<t<<" avg time: "<<sum_time_count/n<<" total frames: "<<n<<" cpp "<<endl;

        if(waitKey(10) == 'q'){
            grabbed = false;
        }
    }

    return 0;
}