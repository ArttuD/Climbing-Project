
#include <iostream>
#include <sstream>
#include <string>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>

using namespace cv;
using namespace std;

const char* params
    = "{ help h         |           | Print usage }"
      "{ input          | vtest.avi | Path to a video or a sequence of image }"
      "{ algo           | KNN      | Background subtraction method (KNN, MOG2) }";

string video_path = "C:/Users/lehtona6/Dropbox (Aalto)/climbing_project_data_share/online_videos/boulder_example_2.mp4";

Mat src_gray;
int thresh = 100;
RNG rng(12345);
void thresh_callback(int, void* );

int getMaxAreaContourId(vector <vector<cv::Point>> contours) {
    double maxArea = 0;
    int maxAreaContourId = -1;
    std::cout << "running here"<< "\n";
    for (int j = 0; j < contours.size(); j++) {
        double newArea = cv::contourArea(contours.at(j));
        if (newArea > maxArea) {
            maxArea = newArea;
            maxAreaContourId = j;
        } // End if
    } // End for
    return maxAreaContourId;
} // End function

int main(int argc, char* argv[])
{
    CommandLineParser parser(argc, argv, params);
    parser.about( "This program shows how to use background subtraction methods provided by "
                  " OpenCV. You can process both videos and images.\n" );
    if (parser.has("help"))
    {
        //print help information
        parser.printMessage();
    }
    //create Background Subtractor objects
    Ptr<BackgroundSubtractor> pBackSub;
    if (parser.get<String>("algo") == "MOG2")
        pBackSub = createBackgroundSubtractorMOG2();
    else
        pBackSub = createBackgroundSubtractorKNN();
    //VideoCapture capture( samples::findFile( parser.get<String>("input") ) );
    VideoCapture capture(video_path);
    if (!capture.isOpened()){
        //error in opening the video input
        cerr << "Unable to open: " << parser.get<String>("input") << endl;
        return 0;
    }
    int morph_size = 1;
    Mat element = getStructuringElement(
        MORPH_RECT,
        Size(2 * morph_size + 1,
             2 * morph_size + 1),
        Point(morph_size,
              morph_size));
    Mat output;

    Mat frame, fgMask;
    while (true) {
        capture >> frame;
        if (frame.empty())
            break;
        //update the background model
        pBackSub->apply(frame, fgMask);
        cv::threshold(fgMask,fgMask,254,255,cv::THRESH_BINARY); 
        morphologyEx(fgMask, fgMask, MORPH_OPEN, element, Point(-1, -1), 1);
        morphologyEx(fgMask, fgMask, MORPH_CLOSE, element, Point(-1,-1), 2);

        //Draw contours
        vector<vector<Point>> contours;
        vector<Vec4i> hierarchy;
        int max_index;
        findContours(fgMask,contours,hierarchy,RETR_TREE, CHAIN_APPROX_NONE);
        max_index = getMaxAreaContourId(contours);

        if (contours.size() > 0){
            cout<<"Index is "<< max_index <<"\n";
        drawContours(frame, contours[max_index], -1,Scalar(0,255,0)); }
        else{cout<<"no contour_boys found"<<"\n"; }
        //Trial shit
        //cv::erode(fgMask,fgMask,cv::Mat());
        //cv::dilate(fgMask,fgMask,cv::Mat());
        //cv::findContours(fgMask,contours,CV_RETR_EXTERNAL,CV_CHAIN_APPROX_NONE);
        //cv::cvtColor(fgMask,fgMask,CV_GRAY2RGB);
        //cv::drawContours(fgMask,contours,-1,cv::Scalar(255,255,255),CV_FILLED,8);
        //get the frame number and write it on the current frame
        const char* source_window = "Source";
        namedWindow( source_window );
        imshow( source_window, fgMask );
        
        const char* org_window = "org";
        namedWindow( org_window );
        imshow( org_window, frame );
        const int max_thresh = 255;
        // createTrackbar( "Canny thresh:", source_window, &thresh, max_thresh, thresh_callback );
        // thresh_callback( 0, 0 );
        // waitKey();
        stringstream ss;
        ss << capture.get(CAP_PROP_POS_FRAMES);
        string frameNumberString = ss.str();
        putText(fgMask, frameNumberString.c_str(), cv::Point(15, 15),
                FONT_HERSHEY_SIMPLEX, 0.5 , cv::Scalar(0,0,0));
        //show the current frame and the fg masks
        //get the input from the keyboard
        int keyboard = waitKey(1);
        if (keyboard == 'q' || keyboard == 27)
            break;
    }
    return 0;
}
