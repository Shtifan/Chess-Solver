import cv2

img = cv2.imread("./image.png", cv2.IMREAD_UNCHANGED)
rows, cols, _ = img.shape

# Define your PIXELS array
PIXELS = [(), (39, 34, 30, 255)]

# Print the shape of the image for debugging
print(img.shape)

# Comment out the line causing the IndexError
# print(img[300, 1000])

cv2.imshow("image", img)


def check_for_pixels(img, row):
    rows, cols, _ = img.shape
    starts = [0, 0]
    for x in range(rows):  # Corrected loop range to iterate over rows
        try:
            index = PIXELS.index(tuple(img[x, row]))
            print(index)
            starts[index] = x if not starts[index] else 0
        except ValueError:
            pass  # Handle the exception explicitly

    if 0 not in starts:
        gap = starts[1] - starts[0]

        return img[starts[0] : starts[0] + gap * 8, row : row + gap * 8]

    return None


for y in range(cols):  # Corrected loop range to iterate over columns
    c = check_for_pixels(img, y)
    if c is not None:
        print("found it")
        cv2.imshow("cropped", c)
        cv2.waitKey(0)

print("finished")
