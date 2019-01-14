#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <iostream>

using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{

  char *videoPath = argv[1];

  printf("Video Path Is: %s", videoPath);

  // Create a VideoCapture object and open the input file
  // If the input is the web camera, pass 0 instead of the video file name
  VideoCapture cap(videoPath);

  // Check if camera opened successfully
  if (!cap.isOpened())
  {
    cout << "Error opening video stream or file" << endl;
    return -1;
  }

  // get cap property
  double scale = 0.33;
  int start = 0;
  if (argc > 2)
  {
    sscanf(argv[2], "%d", &start);
  }
  cap.set(CAP_PROP_POS_MSEC, start * 1000);
  double width = cap.get(CAP_PROP_FRAME_WIDTH) * scale;
  double height = cap.get(CAP_PROP_FRAME_HEIGHT) * scale;

  namedWindow("fisheye", WINDOW_NORMAL);
  // resize the window
  resizeWindow("fisheye", width, height);

  // K = [fx 0 cx]
  //       [0 fy cy]
  //       [0  0  1]
  Matx33d theK;
  theK(0, 0) = width / 3;
  theK(1, 1) = width / 3;
  theK(0, 2) = width / 2;
  theK(1, 2) = height / 2;
  theK(2, 2) = 1;

  Mat theD = Mat(1, 4, CV_32F, {0., 0., 0., 0.});

  while (1)
  {

    Mat frame, dst_frame, undistorted;
    // Capture frame-by-frame
    cap >> frame;

    // If the frame is empty, break immediately
    if (frame.empty())
      break;
    Matx33d newK = theK;
    resize(frame, dst_frame, Size(), scale, scale);
    fisheye::undistortImage(dst_frame, undistorted, theK, theD, newK);

    // Display the resulting frame
    imshow("fisheye", undistorted);

    // Press  ESC on keyboard to exit
    char c = (char)waitKey(25);
    if (c == 27)
      break;
  }

  // When everything done, release the video capture object
  cap.release();

  // Closes all the frames
  destroyAllWindows();

  return 0;
}
