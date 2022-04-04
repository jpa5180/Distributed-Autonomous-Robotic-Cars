import os
import sys
import pathlib
import math
from pupil_apriltags import Detector

calibration_filepath = os.path.join(pathlib.Path(__file__).parent.resolve(), 'calibration_result.txt')
if not os.path.exists(calibration_filepath):
    print('calibration_result.txt does NOT exist.')
    print('calibration_result.txt does NOT exist.')
    print('calibration_result.txt does NOT exist.')
    sys.exit(1)

with open('../Camera/calibration_result.txt') as f:
    lines = f.readlines()
    lines = map(lambda s: s.strip(), lines)
    fx, fy, cx, cy = map(float, lines)


TAG_SIZE = 0.034 # in meters
COLLISION_DIST = 50


class Apriltag:
    def __init__(self):
        self.detector = Detector(
            families='tagStandard41h12',
            nthreads=1,
            quad_decimate=1.0,
            quad_sigma=0.0,
            refine_edges=1,
            decode_sharpening=0.25,
            debug=0
        )

    def detect(self, img):
        tags = self.detector.detect(
            img,
            estimate_tag_pose=True,
            camera_params=[fx, fy, cx, cy],
            tag_size=TAG_SIZE
        )

        if len(tags) == 0:
            print('\nTag not found.\n')
            return []
        else:
            return [(tag.tag_id, self.dist(tag)) for tag in tags if self.dist(tag) <= COLLISION_DIST]

    def dist(self, tag):
        x, y, z = tag.pose_t[0][0], tag.pose_t[1][0], tag.pose_t[2][0]
        dist_m = self.hypot(self.hypot(x, y), z)
        dist_cm = int(dist_m * 100)
        return dist_cm

    def hypot(self, a, b):
        return math.sqrt(a * a + b * b)
