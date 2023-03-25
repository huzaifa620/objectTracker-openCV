import argparse
import cv2

def inputROI():
    while True:
        # Define the codec and create VideoCapture object
        cap = cv2.VideoCapture(args.video)

        # Read the first frame from the video
        ret, frame = cap.read()

        # Select ROI for tracking
        region = cv2.selectROI(frame)

        if region != (0,0,0,0):
            # Create a tracker object
            tracker = cv2.TrackerCSRT_create()

            cv2.destroyWindow("ROI selector")
            return cap, frame, region, tracker
        else:
            print('Selct the target object')


def main():
    global cap, frame, region, tracker

    # Initialize the tracker with the ROI
    tracker.init(frame, region)

    while True:
        # Read a new frame from the video
        ret, frame = cap.read()

        # If video has ended, break the loop
        if not ret:
            break

        # Update the tracker with the new frame
        success, reg = tracker.update(frame)

        if success:
            # Convert the coordinates to integers
            (x, y, w, h) = tuple(map(int, reg))

            # Draw a bounding box around the tracked object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            tracker.init(frame, region)
            print('No matches')
            
        # Show the frame
        cv2.imshow('Frame', frame)

        # Exit if the user presses 'q' key
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Object tracking using OpenCV')
    parser.add_argument('video', type=str)
    args = parser.parse_args()

    cap, frame, region, tracker = inputROI()
    if tracker:
        main()
