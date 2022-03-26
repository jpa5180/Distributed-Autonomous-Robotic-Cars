import os

directory = 'tags/'
for filename in os.listdir(directory):
    orig_path = os.path.join(directory, filename)
    new_path = os.path.join('resized_tags', filename)
    command = 'convert ' + orig_path + ' -scale 2000% ' + new_path
    os.system(command)