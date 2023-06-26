import cv2
import numpy as np
import math

def warp_to_birds_eye_view(image, square):
    width, height = 1000, 1000
    dst_points = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
    src_points = np.float32(square.reshape(4, 2))
    transform_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_image = cv2.warpPerspective(image, transform_matrix, (width, height))
    return warped_image

# Function to split an image into a grid of equal cell size
def split_image_into_grid(image, num_rows, num_cols):
    height, width = image.shape[:2]
    cell_height = height // num_rows
    cell_width = width // num_cols

    cells = []
    for r in range(num_rows):
        for c in range(num_cols):
            start_x = c * cell_width
            start_y = r * cell_height
            end_x = start_x + cell_width
            end_y = start_y + cell_height

            cell = image[start_y:end_y, start_x:end_x]
            cells.append(cell)

    return cells


x_samples = [cv2.imread('x.png', 1), cv2.imread('x2.png', 1), cv2.imread('x-sample.png', 1), ]
o_samples = [cv2.imread('o.png', 1), cv2.imread('o-sample.png', 1), cv2.imread('o2.png', 1), cv2.imread('o3.png', 1), ]

# Display the individual cells
def find_x_with_sample(cells, sample, matrica):
    for i, cell in enumerate(cells):
        # Perform template matching
        result = cv2.matchTemplate(cell, sample, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Get the coordinates of the matched region
        top_left = max_loc
        bottom_right = (top_left[0] + sample.shape[1], top_left[1] + sample.shape[0])

        # Draw a rectangle around the matched region
        if min_val < -0.35:
            cv2.rectangle(cell, top_left, bottom_right, (0, 0, 255), 2)
            matrica[math.floor(i/3)][2-(i % 3)] = 'x'

def find_o_with_sample(cells, sample, matrica):
    for i, cell in enumerate(cells):
        # Perform template matching
        result = cv2.matchTemplate(cell, sample, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Get the coordinates of the matched region
        top_left = max_loc
        bottom_right = (top_left[0] + sample.shape[1], top_left[1] + sample.shape[0])

        # Draw a rectangle around the matched region
        if min_val < -0.13:
            cv2.rectangle(cell, top_left, bottom_right, (0, 255, 0), 4)
            matrica[math.floor(i/3)][2-(i % 3)] = 'o'

def find_x(cells, matrica):
    for sample in x_samples:
        find_x_with_sample(cells, sample, matrica)

def find_o(cells, matrica):
    for sample in o_samples:
        find_o_with_sample(cells, sample, matrica)

def get_matrix():
    # Read the input image
    cap = cv2.VideoCapture('http://192.168.8.100:8080/video')
    ret, image = cap.read()

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred, 20, 50)

    # Find contours in the edge image

    kernel = np.ones((11, 11), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_square = None
    largest_area = -1

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_square = approx

    # Warp the image to bird's eye view
    warped_image = warp_to_birds_eye_view(image, largest_square)
    # cv2.imshow('warped', warped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # Split the warped image into a 3x3 grid
    cells = split_image_into_grid(warped_image, 3, 3)

    # Display the original and warped images
    matrica = [['_' for _ in range(0, 3)] for _ in range(3, 0, -1)]
    find_x(cells, matrica)
    find_o(cells, matrica)
    return matrica

def flip(matrica):
    return [[matrica[i][j] for j in range(2,-1,-1)] for i in range(2, -1, -1)]

def procitaj():
    matrica = None
    while True:
        matrica = get_matrix()
        print(matrica)
        user_input = input('Is the matrix okay? yes/no: ')

        if user_input.lower() == 'no':
            user_input2 = input('Is the matrix flipped? yes/no: ')
            if user_input2.lower() == 'yes':
                matrica = flip(matrica)
                print(matrica)
                user_input3 = input('Is the matrix now okay? yes/no: ')
                if user_input3.lower() == 'yes':
                    break
                else:
                    continue
            else:
                continue
        elif user_input.lower() == 'yes':
            break
        else:
            print('Type yes/no')

    return matrica
