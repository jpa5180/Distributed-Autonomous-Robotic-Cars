import os
import picamera
import picamera.array
from pupil_apriltags import Detector
from PIL import Image

resolution = (400, 300)
if not os.path.exists(os.path.join('images')):
    os.mkdir(os.path.join('images'))
if not os.path.exists(os.path.join('images', 'calibration')):
    os.mkdir(os.path.join('images', 'calibration'))
if not os.path.exists(os.path.join('images', 'captured')):
    os.mkdir(os.path.join('images', 'captured'))

try:
    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        at_detector = Detector(families='tagStandard41h12',
                               nthreads=1,
                               quad_decimate=1.0,
                               quad_sigma=0.0,
                               refine_edges=1,
                               decode_sharpening=0.25,
                               debug=0)

        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            # At this point the image is available as stream.array
            image = stream.array[:,:,0]

            postfix = 1
            while os.path.exists(os.path.join('images', 'captured', 'image' + str(postfix) + '.png')):
                postfix += 1
            Image.fromarray(image).resize(resolution, Image.ANTIALIAS).save(os.path.join('images', 'captured', 'image' + str(postfix) + '.png'))

            stream.truncate(0)
            del image

except KeyboardInterrupt:
    print("\nThe Camera has been killed.\n")
except Exception as e:
    print(e)