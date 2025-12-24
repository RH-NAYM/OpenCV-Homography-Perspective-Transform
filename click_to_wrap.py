# Interactive Click-to-Warp Perspective Transform
"""
✅ How it Works
Click 4 points in clockwise order on the image window.
The script calculates a homography matrix from these points to a rectangle.
Applies cv2.warpPerspective to warp the image.
Displays original points and warped result side-by-side.
"""

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from tools.tools import LearnTools

learn_tools = LearnTools()

# Global list to store clicked points
clicked_points = []

# Load image (async-compatible for LearnTools)
# img_url = "https://i.ibb.co/5x276TvQ/1.jpg"
# img_url = "https://i.ibb.co/QjkCQ6Vm/2.jpg"
img_url = "https://i.ibb.co/NyT8LB5/test.jpg"




if os.path.exists("testImage.jpg"):
    image = cv2.imread("testImage.jpg")
else:
    import asyncio
    pil_image = asyncio.run(learn_tools.get_image(img_url=img_url, padding=0))
    pil_image.save("testImage.jpg", "JPEG")
    image = learn_tools.pil_to_cv2(pil_image)

# Show initial image
learn_tools.show_multiple_images([{'title': 'Original Image', 'image': image}])

def click_event(event, x, y, flags, param):
    """Record points clicked by the user."""
    global clicked_points, image_copy
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append([x, y])
        cv2.circle(image_copy, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Select 4 Points (Clockwise)", image_copy)
        if len(clicked_points) == 4:
            print("✅ 4 points selected! Applying perspective transform...")

# Display image for user clicks
image_copy = image.copy()
cv2.imshow("Select 4 Points (Clockwise)", image_copy)
cv2.setMouseCallback("Select 4 Points (Clockwise)", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Perform perspective warp if 4 points selected
if len(clicked_points) == 4:
    pts_src = np.float32(clicked_points)

    # Compute destination rectangle size
    width = int(max(np.linalg.norm(pts_src[0] - pts_src[1]),
                    np.linalg.norm(pts_src[2] - pts_src[3])))
    height = int(max(np.linalg.norm(pts_src[0] - pts_src[3]),
                     np.linalg.norm(pts_src[1] - pts_src[2])))
    pts_dst = np.float32([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]])

    # Compute homography and warp image
    H, status = cv2.findHomography(pts_src, pts_dst)
    warped = cv2.warpPerspective(image, H, (width, height))

    # Visualize original points and warped image side by side
    plt.figure(figsize=(12, 6))

    # Original with selected points
    plt.subplot(1, 2, 1)
    plt.title("Original Image with Selected Points")
    img_vis = image.copy()
    for pt in pts_src:
        cv2.circle(img_vis, tuple(pt.astype(int)), 5, (0, 0, 255), -1)
    plt.imshow(cv2.cvtColor(img_vis, cv2.COLOR_BGR2RGB))

    # Warped perspective
    plt.subplot(1, 2, 2)
    plt.title("Warped Perspective")
    plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))

    plt.show()

else:
    print("❌ Select exactly 4 points to perform the perspective warp.")
