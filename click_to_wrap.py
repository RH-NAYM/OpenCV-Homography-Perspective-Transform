# Interactive Click-to-Warp Perspective Transform
'''
✅ How it Works

Click 4 points in clockwise order on the image window.

The script calculates a homography matrix from these points to a rectangle.

Applies cv2.warpPerspective to warp the image.

Displays original points and warped result side-by-side.
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Global list to store clicked points
clicked_points = []

def click_event(event, x, y, flags, param):
    """Callback function to record points clicked by the user."""
    global clicked_points, image_copy
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append([x, y])
        # Draw a small circle where clicked
        cv2.circle(image_copy, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Select 4 Points (Clockwise)", image_copy)
        if len(clicked_points) == 4:
            print("4 points selected! Applying perspective transform...")

# Load image
image_copy = image.copy()  # Use original loaded image
cv2.imshow("Select 4 Points (Clockwise)", image_copy)
cv2.setMouseCallback("Select 4 Points (Clockwise)", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()

if len(clicked_points) == 4:
    pts_src = np.float32(clicked_points)

    # Define destination points as a rectangle (width x height based on distances)
    width = int(max(np.linalg.norm(pts_src[0] - pts_src[1]), np.linalg.norm(pts_src[2] - pts_src[3])))
    height = int(max(np.linalg.norm(pts_src[0] - pts_src[3]), np.linalg.norm(pts_src[1] - pts_src[2])))
    pts_dst = np.float32([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]])

    # Compute homography and warp
    H, status = cv2.findHomography(pts_src, pts_dst)
    warped = cv2.warpPerspective(image, H, (width, height))

    # Display results using matplotlib
    plt.figure(figsize=(12,6))
    plt.subplot(1,2,1)
    plt.title("Original Image with Selected Points")
    img_vis = image.copy()
    for pt in pts_src:
        cv2.circle(img_vis, tuple(pt.astype(int)), 5, (0,0,255), -1)
    plt.imshow(cv2.cvtColor(img_vis, cv2.COLOR_BGR2RGB))

    plt.subplot(1,2,2)
    plt.title("Warped Perspective")
    plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    plt.show()
else:
    print("Select exactly 4 points to perform the perspective warp.")
