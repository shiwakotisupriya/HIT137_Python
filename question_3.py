import turtle

def pattern_drawing(t, length, depth):
    if depth == 0:
        # Draw straight line
        t.forward(length)
    else:
        # Dividing the line into 3 segments
        length = length / 3
        
        # Draw a first thrird in segment 1
        pattern_drawing(t, length, depth - 1)
        
        # Turns right for inward indentation
        t.right(60)
        
        # Draw a left side of indented triangle in segment 2
        pattern_drawing(t, length, depth - 1)
        
        # Turns left to form the indentation
        t.left(120)
        
        # Draw a right side of indented triangle in segment 3
        pattern_drawing(t, length, depth - 1)
        
        # Right turn to turn in original direction
        t.right(60)
        
        # Draw a final 3rd in segment 4
        pattern_drawing(t, length, depth - 1)


def polygon_drawing(t, sides, length, depth):
    """
    Function to draw a polygon
    """
    # Calculating the exterior angle inorder to turn at each corner
    angle = 360 / sides
    # Draw each side of the polygon
    for _ in range(sides):
        pattern_drawing(t, length, depth)
        t.right(angle)  


# Get valid number of sides, length and depth from user
while True:
    try:
        sides = int(input("Enter the number of sides: "))
        if sides < 3:
            print("Error: Number of sides must be at least 3. Please try again.")
            continue
        break
    except ValueError:
        print("Error: Please enter a valid integer.")

while True:
    try:
        length = int(input("Enter the side length: "))
        if length <= 0:
            print("Error: Side length must be positive. Please try again.")
            continue
        break
    except ValueError:
        print("Error: Please enter a valid integer.")

while True:
    try:
        depth = int(input("Enter the recursion depth: "))
        if depth < 0:
            print("Error: Recursion depth must be non-negative. Please try again.")
            continue
        break
    except ValueError:
        print("Error: Please enter a valid integer.")

print()

# Calculates the size of final segment
final_segment_size = length / (3 ** depth)

# Validates that the pattern will be visible
if final_segment_size < 1:
    print("_" * 50)
    print("Pattern will be too small to see!")
    print("_" * 50)
    print(f"With length={length} and depth={depth}:")
    print(f"Final line segments will be of: {final_segment_size:.4f} pixels")
    print(f"This is too small to be visible on screen!")
    print("Recommendations:")
    print(f"  For depth {depth}: use length ≥ {3**depth} pixels")
    print(f"  For length {length}: use depth ≤ {int(length.bit_length() / 1.6)} ")
    
    choice = input("Do you want to continue anyway? (yes/no): ").lower()
    if choice not in ['yes', 'y']:
        print(" Program cancelled. Please run again with better values.")
        exit()
    print()

# Warning of slow performance for high depths
if depth >= 5:
    print("_" * 50)
    print("High recursion depth detected!")
    print("_" * 50)
    print(f"Depth {depth} will create {4**depth:,} line segments.")
    print("This may take a LONG time to draw!")
    print("Recommendations:")
    print("  Depth 2 to 3: Fast and looks great")
    print("  Depth 4: Detailed but slower")
    print("  Depth 5+: Very slow")
    
    choice = input("Do you want to continue anyway? (yes/no): ").lower()
    if choice not in ['yes', 'y']:
        print(" Program cancelled. Please run again with lower depth.")
        exit()
    print()

print(f"Drawing {sides} sided polygon with depth {depth}")
print("Please wait, this may take a moment for high depths.")


# turtle screen opens
screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.title(f"Fractal Pattern: {sides} sides, Depth {depth}")

t = turtle.Turtle()
t.speed(0)  
t.hideturtle()
t.pencolor("white")
t.pensize(2)
t.penup()
t.goto(-length / 2, length / 2)
t.pendown()
polygon_drawing(t, sides, length, depth)

print("Drawing complete! Window will close automatically in 15 seconds")

# screen closes after 15 seconds
screen.ontimer(screen.bye, 15000)

screen.mainloop()