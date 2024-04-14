from PIL import Image, ImageDraw

def draw_coordinates(image_path, move):
    # Load the chessboard image
    chessboard = Image.open(image_path)

    # Get the starting and ending coordinates from the move string
    start_square = move[:2]
    end_square = move[2:]

    # Map file letters to numerical values
    file_mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    # Extract the file (column) and rank (row) from the coordinates
    start_file, start_rank = start_square[0], start_square[1]
    end_file, end_rank = end_square[0], end_square[1]

    # Get numerical values from the file mapping
    start_file_num = file_mapping[start_file]
    end_file_num = file_mapping[end_file]

    # Define the coordinate color, font size, and arrow color
    coordinate_color = (255, 0, 0)  # Red color
    arrow_color = (0, 0, 255)  # Blue color for arrow
    font_size = 20

    # Create a drawing object
    draw = ImageDraw.Draw(chessboard)

    # Calculate the center coordinates for start and end
    start_x = (start_file_num + 0.5) * 50
    start_y = (int(start_rank) + 0.5) * 50
    end_x = (end_file_num + 0.5) * 50
    end_y = (int(end_rank) + 0.5) * 50

    # Draw the centered coordinates on the image
    draw.text((start_x, start_y), start_square, fill=coordinate_color, font=None)
    draw.text((end_x, end_y), end_square, fill=coordinate_color, font=None)

    # Draw a line from start to end
    draw.line([(start_x, start_y), (end_x, end_y)], fill=arrow_color, width=2)

    # Draw arrowheads manually
    arrow_size = 10
    draw.line([(end_x, end_y), (end_x - arrow_size, end_y - arrow_size)], fill=arrow_color, width=2)
    draw.line([(end_x, end_y), (end_x - arrow_size, end_y + arrow_size)], fill=arrow_color, width=2)

    # Save the modified image
    chessboard.save('./image.png')

# Example usage
move = 'a1a8'
image_path = './image.png'
draw_coordinates(image_path, move)
