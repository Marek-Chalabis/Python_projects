import cv2
import numpy as np
import os


def _sorted_points(contours, average, top_value):
    """Functions dedicated to sort points into above and under average

    Args:
        contours (matrix): counter points of image
        average (int): average of the line
        top_value (int): edge of the image

    Returns:
        x, y [list]: lists with points under and above average
    """
    # list with points under and above average point
    above_average = []
    under_average = []

    for index, i in enumerate(contours[0]):
        x = i[0][0]
        y = i[0][1]

        # fill list with up and down points depends of avg
        if x > 0 and x < top_value:
            if y > average:
                under_average.append(tuple([x, y]))
            elif y < average:
                above_average.append(tuple([x, y]))

    # sorts list
    above_average.sort(key=lambda x: x[0])
    under_average.sort(key=lambda x: x[0])

    # divide points due to if they are on the same point at x axis
    sorted_up = []
    sorted_down = []

    for i in range(0, len(above_average) - 1):
        if above_average[i][0] != above_average[i + 1][0]:
            sorted_up.append(above_average[i])

    for i in range(0, len(under_average) - 1):
        if under_average[i][0] != under_average[i + 1][0]:
            sorted_down.append(under_average[i])

    return sorted_down, sorted_up


def _longest_line(contours):
    """Function dedicated to find point with the most common point in straight line

    Args:
        contours (matrix): counter points of image

    Returns:
        [int]: point where is the longest straight line
    """
    # dict with given values thats apear many times on the line
    line_indexes = {}

    number_of_elements = len(contours[0])

    for index, i in enumerate(contours[0]):
        x = i[0][0]
        y = i[0][1]

        # saves value when it apears in the same points
        if number_of_elements == index + 1:
            break
        elif y == contours[0][index + 1][0][1]:
            if y not in line_indexes:
                line_indexes[y] = [index]
            else:
                line_indexes[y].append(index)

    # defines in how many points line is straight
    find_longest = {}
    for key, value in line_indexes.items():
        number = 0
        find_longest[key] = {}
        for x in range(len(value) - 1):
            if value[x] + 1 == value[x + 1]:
                if number not in find_longest[key].keys():
                    find_longest[key][number] = 1
                else:
                    find_longest[key][number] += 1
            else:
                number += 1

    # checks if there is any two points on the same value on the line
    if len(find_longest) <= 1:
        return False

    # return the longest line for each Y
    straight_lines = {}
    for key, value in find_longest.items():
        list_with_number_of_apears = []
        for _, value1 in value.items():
            list_with_number_of_apears.append(value1)
        if list_with_number_of_apears:
            straight_lines[key] = max(list_with_number_of_apears)

    # longest line on Y:
    longest_line = max(straight_lines, key=straight_lines.get)
    return longest_line


def show_largest_and_average_line(path_to_file, step=20):
    """[summary]

    Args:
        path_to_file ([str]): path to image
        ste ([int]): step to check for difference in image

    Returns:
        [str]: visual lines and differences
    """
    # load images for average and longest
    img_average = cv2.imread(path_to_file)
    img_longest = cv2.imread(path_to_file)

    # change image to black and white and creates thresholding for counturs
    imgray = cv2.cvtColor(img_average, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgray, 127, 255, 0)

    _, width_picture = img_average.shape[:2]

    # returns counter of "cut" in a form of matrix
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # calculate moments of binary image
    moments = cv2.moments(contours[0])

    if moments["m00"] == 0:
        return print(f"Can't find a center of image for this file {path_to_file}")

    # calculate average y height
    avg_y = int(moments["m01"] / moments["m00"])

    longest_line = _longest_line(contours)
    sorted_up, sorted_down = _sorted_points(contours, avg_y, width_picture)

    avg_points = {}
    point = 1
    for index, i in enumerate(zip(sorted_up, sorted_down)):
        x1 = i[0][0]
        y1 = i[0][1]
        x2 = i[1][0]
        y2 = i[1][1]
        half = (y1 + y2) / 2
        # adds points
        cv2.circle(img_average, (x1, int(half)), 1, (0, 0, 255), 1)
        cv2.circle(img_longest, (x1, int(half)), 1, (0, 0, 255), 1)

        # adds steps on image
        if index % step == 0 or index == 0:
            avg_points[point] = half
            cv2.circle(img_average, (x1, int(half)), 1, (255, 0, 255), 2)
            cv2.circle(img_longest, (x1, int(half)), 1, (255, 0, 255), 2)
            point += 1

    # avg line
    cv2.line(img_average, (0, avg_y), (width_picture, avg_y), (0, 255, 0), 1)
    # checks if there is straight line

    if longest_line:
        # longest straight line
        cv2.line(
            img_longest,
            (0, longest_line),
            (width_picture, longest_line),
            (0, 255, 0),
            1,
        )
        print(
            f"Difference between avg Y({avg_y}) and points\t\t\t"
            f"Difference between longest Y line({longest_line}) and points"
        )
        for key, value in avg_points.items():
            print(
                f"Point{key}, Difference: {avg_y - value}\t\t\t\t\t\t"
                f"Point{key}, Difference: {longest_line - value}"
            )

        cv2.imshow("LONGEST_line", img_longest)

    else:
        print(f"Difference between avg Y({avg_y}) and points")
        for key, value in avg_points.items():
            print(f"Point{key}, Difference: {avg_y - value}")
        print("THERE IS NO STRAIGHT LINE")

    cv2.imshow("AVG_line", img_average)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


