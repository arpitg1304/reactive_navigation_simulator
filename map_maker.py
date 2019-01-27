from tkinter import *
import numpy as np
root = Tk()

root.title("Simple Graph")

root.resizable(0,0)

points = []

points_list = []
spline = 0

tag1 = "theline"

def point(event):
    c.create_oval(event.x, event.y, event.x+1, event.y+1, fill="black")
    points.append(event.x)
    points.append(event.y)
    # return points

def canxy(event):
	print(event.x, event.y)

def graph(event):
    global theline
    global points
    c.create_polygon(points, outline='#f11', fill='green', width=2)
    points_list.append(points)
    points = []
    print(points_list)
    # c.create_polygon(points1, outline='#f11', fill='red', width=2)


def save(event):
    global points_list
    np.save('target_n_polygons', points_list)

c = Canvas(root, bg="white", width=700, height= 700)
c.configure(cursor="crosshair")
c.pack()

c.bind("<Button-1>", point)
c.bind("<Button-3>", graph)
c.bind("<Button-2>", save)

root.mainloop()
