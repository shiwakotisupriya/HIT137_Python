
import turtle

def draw_pattern(length, depth):
    if depth == 0:
        turtle.forward(length)
    else:
        length = length / 3

        draw_pattern(length, depth - 1)
        turtle.right(60)
        draw_pattern(length, depth - 1)
        turtle.left(120)
        draw_pattern(length, depth - 1)
        turtle.right(60)
        draw_pattern(length, depth - 1)



def draw_polygon(sides, length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_pattern(length, depth)
        turtle.left(angle)



turtle.speed(10)
turtle.hideturtle()
turtle.bgcolor("red")


sides = int(input("Enter the number of sides: "))
length = int(input("Enter the side length: "))
depth = int(input("Enter the recursion depth: "))


turtle.penup()
turtle.goto(-length / 2, length / 2)
turtle.pendown()


draw_polygon(sides, length, depth)

turtle.done()
