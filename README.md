# Installation
Copy img/ + haarcascade + faec.py file somewhere (like /opt/face)

Install with `sudo ln -s <absolute-path-of-face.py> /usr/bin/face` 

# Usage
`face a.jpg b.jpg` -> will create `_a.jpg`, `_b.jpg`

Modify `scaleFactor=1.2` for stronger/weaker face detection

Add/remove images from img folder

# Requirements
* opencv2
* cv2-python bindings
* PIL or Pillow

# Demo
![before](before.jpg) ![after](after1.jpg) ![after](after2.jpg)