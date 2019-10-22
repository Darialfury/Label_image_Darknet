import cv2
import glob
"""
Python script to label images for darknet with one class
using the yolov3
"""
# convert image path to label path
def convert_path(image_path):
    im_ = image_path.split('.')[0].split('images/')[1]
    lpath = "labels/{0}.txt".format(im_)
    return lpath

# save - xcenter ycenter width height - bounding box label
def save_label(im, im_path, rp):
    h, w, _ = im.shape
    # set class for label
    c = 0
    xl = (rp[0][0] + rp[1][0])/(2*w)
    yl = (rp[0][1] + rp[1][1])/(2*h)
    wl = (abs(rp[1][0] - rp[0][0]))/w
    hl = (abs(rp[1][1] - rp[0][1]))/h
    print(rp)
    print(h, w)
    lpath = convert_path(im_path)
    l = "{} {} {} {} {}".format(c, xl, yl, wl, hl)
    print(l)
    with open(lpath, "w") as f:
        f.write(l)
    print("saved {}".format(lpath))


# now let's initialize the list of reference point
ref_point = [(0,0), (1,1)]
drawing = False


def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, drawing, image, clone_draw

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        if not(drawing):
            drawing = True
            ref_point[0] = (x, y)
        else:
            drawing = False
            clone_draw = image.copy()

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_MOUSEMOVE:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        if drawing:
            ref_point[1] = (x, y)

            # draw a rectangle around the region of interest
            image = clone_draw.copy()
            cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 5)
            cv2.imshow("image", image)

# Read folder with images
list_images_path = sorted(list(glob.glob("images/*.*")))
num_images = len(list_images_path)

# Create window to show image
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
#cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)

sw = True
filw_with_train = "train_list.txt"

# index track images
k = 0

while sw:
    print(" image {0} of {1}".format(k + 1, num_images))
    image = cv2.imread(list_images_path[k])
    clone = image.copy()
    clone_draw = cv2.imread(list_images_path[k])
    cv2.imshow("image", image)
    height, width, _ = image.shape
    key = cv2.waitKey(0) & 0xFF

    # press 'r' to reset the window
    if key == ord("r"):
        image = clone.copy()
    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break
    elif key == ord("s"):
        save_label(image, list_images_path[k], ref_point)
        k += 1
    else:
        k += 1

    if k == num_images:
        sw = False

# close all open windows
cv2.destroyAllWindows()
