#include "opencv2/opencv.hpp"
#include <iostream>

using namespace std;
using namespace cv;

int main()
{

  // Create a VideoCapture object and open the input file
  // If the input is the web camera, pass 0 instead of the video file name
  VideoCapture cap("chaplin.mp4");
  // Ptr<BackgroundSubtractor> model = createBackgroundSubtractorKNN();
  // Check if camera opened successfully
  if (!cap.isOpened())
  {
    cout << "Error opening video stream or file" << endl;
    return -1;
  }
  // Mat foregroundMask, foreground;
  while (1)
  {

    Mat frame;
    // Capture frame-by-frame
    cap >> frame;

    // If the frame is empty, break immediately
    if (frame.empty())
      break;

    // model->apply(frame, foregroundMask, 0);

    // foreground = Scalar::all(0);
    // frame.copyTo(foreground, foregroundMask);

    // Display the resulting frame
    imshow("Frame", frame);

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
