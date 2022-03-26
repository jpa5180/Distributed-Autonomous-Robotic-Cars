import time
import os
import math
import traceback
import sys
import picamera.array
from pupil_apriltags import Detector
from PIL import Image

tag_map = {
    4: (1.5, 100),
    5: (5.0, 100),
    6: (8.5, 100),
    7: (12.0, 100),
    8: (15.5, 100),
    9: (19.0, 100)
}


def hypot(a, b):
    return math.sqrt(a * a + b * b)


def vect(id1, id2, d1, d2):
    # Law of Cosines
    d0 = tag_map[id2][0] - tag_map[id1][0]
    cos_a = ((d1 * d1) + (d0 * d0) - (d2 * d2)) / (2 * d1 * d0)
    a = math.acos(cos_a)
    print('Angle:', math.degrees(a))
    rv = d1 * math.cos(a)
    cv = d1 * math.sin(a)
    return rv, cv


if not os.path.exists('calibration_result.txt'):
    print('calibration_result.txt does NOT exist.')
    sys.exit(1)

keep_alive = True
resolution = (640, 480)
tag_size = 0.041275  # in meters

with open('calibration_result.txt') as f:
    lines = f.readlines()
    lines = map(lambda s: s.strip(), lines)
    fx, fy, cx, cy = map(float, lines)

try:
    with picamera.PiCamera() as camera:
        # camera.resolution = resolution
        at_detector = Detector(families='tagStandard41h12',
                               nthreads=1,
                               quad_decimate=1.0,
                               quad_sigma=0.0,
                               refine_edges=1,
                               decode_sharpening=0.25,
                               debug=0)

        with picamera.array.PiRGBArray(camera) as stream:
            while keep_alive:
                camera.capture(stream, format='bgr')
                image = stream.array[:,:,0]
                tags = at_detector.detect(
                    image,
                    estimate_tag_pose=True,
                    camera_params=[fx, fy, cx, cy],
                    tag_size=tag_size
                )

                if len(tags) == 0:
                    print('\nTag not found.\n')
                else:
                    Image.fromarray(image).save('temp_image.png')

                    if len(tags) >= 2:
                        for i in range(len(tags) - 1):
                            id1 = tags[i].tag_id
                            id2 = tags[i+1].tag_id
                            x1, y1, z1 = tags[i].pose_t[0][0], tags[i].pose_t[2][0], tags[i].pose_t[1][0]
                            x2, y2, z2 = tags[i+1].pose_t[0][0], tags[i+1].pose_t[2][0], tags[i+1].pose_t[1][0]
                            d1 = hypot(hypot(x1, y1), z1) * 39.3701
                            d2 = hypot(hypot(x2, y2), z2) * 39.3701
                            print(id1, x1, y1, z1, d1)
                            print(id2, x2, y2, z2, d2)
                            rv, cv = vect(id1, id2, d1, d2)
                            print('rv:', rv, '      cv:', cv)
                            print('Coords:', tag_map[id1][0] + rv, tag_map[id1][1] - cv)
                            print()
                        print('\n\n')

                    # for tag in tags:
                    #     print(tag.tag_id, end='\t')
                    #     print(round(tag.pose_t[0][0], 3), end='\t')
                    #     print(round(tag.pose_t[1][0], 3), end='\t')
                    #     print(round(tag.pose_t[2][0], 3), end='\t')
                    #     print()
                    # print('\n\n')
                    keep_alive = False

                stream.truncate(0)
                del image
                del tags
                time.sleep(0.2)

except KeyboardInterrupt:
    keep_alive = False
    print("\nThe camera has been killed.\n")
except Exception:
    print(traceback.format_exc())