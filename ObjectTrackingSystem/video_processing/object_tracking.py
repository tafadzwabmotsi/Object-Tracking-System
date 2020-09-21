__author__ = "Tafadzwa Brian Motsi"

import cv2
import numpy as np
from . display_video import DisplayVideo


class ObjectTracking:
    def __init__(self, camera_source):
        self.camera_source = camera_source

        self.capture = cv2.VideoCapture(self.camera_source)

    # object tracking using meanshift
    def meanshift_track_objects(self):
        # read the video
        cap = self.capture

        # get the first frame
        ret, frame = cap.read()

        # set the initial location of the window
        r, h, c, w = 250, 90, 400, 125

        # set up the tracking window
        tracking_window = (c, r, w, h)

        # set up the region of interest for tracking
        region_of_interest = frame[r:r+h, c:c+w]

        # set up the HSV region of interest
        hsv_region_of_interest = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # set up the mask
        mask = cv2.inRange(hsv_region_of_interest, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

        # calculate the histogram of the region of interest and norminalize
        region_of_interest_histogram = cv2.calcHist([hsv_region_of_interest], [0], mask, [180], [0, 180])
        cv2.normalize(region_of_interest, region_of_interest_histogram, 0, 255, cv2.NORM_MINMAX)

        # set up the termination criteria
        termination_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        while 1:
            ret, frame = cap.read()

            if ret is True:
                hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv_image], [0], region_of_interest_histogram, [0, 180], 1)

                # get the new location by applying meanshift
                ret, tracking_window = cv2.meanShift(dst, tracking_window, termination_criteria)

                # draw the image
                x, y, w, h = tracking_window
                image = cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 2)

                # display the image
                DisplayVideo('image', image)
                if cv2.waitKey(60) & 0xff == 27:
                    break
                else:
                    continue
            else:
                break

        cv2.destroyAllWindows()
        cap.release()

    # object tracking using meanshift
    def camshift_track_objects(self):
        # read the video
        cap = self.capture

        # get the first frame
        ret, frame = cap.read()

        # set the initial location of the window
        r, h, c, w = 250, 90, 400, 125

        # set up the tracking window
        tracking_window = (c, r, w, h)

        # set up the region of interest for tracking
        region_of_interest = frame[r:r+h, c:c+w]

        # set up the HSV region of interest
        hsv_region_of_interest = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # set up the mask
        mask = cv2.inRange(hsv_region_of_interest, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

        # calculate the histogram of the region of interest and norminalize
        region_of_interest_histogram = cv2.calcHist([hsv_region_of_interest], [0], mask, [180], [0, 180])
        cv2.normalize(region_of_interest_histogram, region_of_interest_histogram, 0, 255, cv2.NORM_MINMAX)

        # set up the termination criteria
        termination_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        while 1:
            ret, frame = cap.read()

            if ret is True:
                hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv_image], [0], region_of_interest_histogram, [0, 180], 1)

                # get the new location by applying meanshift
                ret, tracking_window = cv2.CamShift(dst, tracking_window, termination_criteria)

                # draw the image
                points = cv2.boxPoints(ret)
                points = np.int0(points)
                image = cv2.polylines(frame, [points], True, 255, 2)

                # display the image
                DisplayVideo('image', image)
                if cv2.waitKey(60) & 0xff == 27:
                    break
                else:
                    continue
            else:
                break
        cv2.destroyAllWindows()
        cap.release()

    def lucas_kanade_optical_flow_object_tracking(self):
        cap = self.capture

        # parameters from ShiTomasi corner detection
        feature_params = dict(
            maxCorners=100,
            qualityLevel=0.3,
            minDistance=7,
            blockSize=7
        )

        # parameters for lucas kanade optical flow
        lk_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )

        # set up some random colors
        colors = np.random.randint(0, 255, (100, 3))

        # get the first frame and find corners in it
        ret, old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

        # set up a mask image for drawing purposes
        mask = np.zeros_like(old_frame)

        while 1:
            ret, frame = cap.read()
            if ret is True:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Calculate optical flow
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

                # select good points
                good_new = p1[st == 1]
                good_old = p0[st == 1]

                # draw the tracks
                for i, (new, old) in enumerate(zip(good_new, good_old)):
                    a, b = new.ravel()
                    c, d = old.ravel()

                    mask = cv2.line(mask, (a, b), (c, d), colors[i].tolist(), 2)
                    frame = cv2.circle(frame, (a, b), 5, colors[i].tolist(), -1)

                image = cv2.add(frame, mask)

                DisplayVideo('window', image)
                if cv2.waitKey(30) & 0xff == 27:
                    break
                else:

                    # Now update the previous frame and previous points
                    old_gray = frame_gray.copy()
                    p0 = good_new.reshape(-1, 1, 2)
        cv2.destroyAllWindows()
        cap.release()

    def gunner_farneback_object_tracking(self):
        cap = self.capture

        ret, frame1 = cap.read()
        previous_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        hsv = np.zeros_like(frame1)
        hsv[..., 1] = 255

        while 1:
            ret, frame2 = cap.read()
            next_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            flow = cv2.calcOpticalFlowFarneback(previous_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

            hsv[..., 0] = ang*180/np.pi/2
            hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            DisplayVideo('frame2', rgb)

            if cv2.waitKey(30) & 0xff == 27:
                break

            previous_gray = next_gray

        cap.release()
        cv2.destroyAllWindows()

    def background_subtractor_mog2_object_tracking(self):

        cap = self.capture
        foreground_background = cv2.createBackgroundSubtractorMOG2()

        while 1:
            ret, frame = cap.read()
            foreground_mask = foreground_background.apply(frame)

            DisplayVideo('frame', foreground_mask)

            if cv2.waitKey(30) & 0xff == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def background_subtractor_gmg_object_tracking(self):

        video_capture = self.capture
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        foreground_background = cv2.createBackgroundSubtractorMOG2()

        while 1:
            ret, frame = video_capture.read()
            foreground_mask = foreground_background.apply(frame)
            foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel=kernel)

            DisplayVideo('frame', foreground_mask)
            if cv2.waitKey(30) & 0xff == 27:
                break

        video_capture.release()
        cv2.destroyAllWindows()
