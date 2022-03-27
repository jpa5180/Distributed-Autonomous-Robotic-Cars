import os

tag_count = 10

directory = 'tags/'
for i in range(tag_count):
    command = 'wget -P ' + directory + ' https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tagStandard41h12/tag41_12_0000' + str(i) + '.png'
    os.system(command)