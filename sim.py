import sys
import tkinter as tk
import numpy as np
import random
import math
from tkinter import messagebox

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import random
import time
from sys import exit as exit

def create_circle(x, y, r, canvasName, color): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill = color)

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

class Maze:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self):

        self.canvas.create_rectangle(0, 0, 700, 10, fill='black')
        self.canvas.create_rectangle(0, 0, 10, 700, fill='black')
        self.canvas.create_rectangle(0, 690, 700, 700, fill='black')
        self.canvas.create_rectangle(700, 0, 690, 700, fill='black')

        self.pos = self.canvas.create_text(850,50, fill="darkblue", font="Times 15 bold", text="Absolute Position")

        self.pos_out = self.canvas.create_text(850,80, fill="darkblue", font="Times 15 bold", text="Position")

        target = np.load('only_target.npy')

        self.target = create_circle(target[0][0], target[0][1], 25, self.canvas, 'red')

        # print(self.target)

        polygons = np.load('polygons2.npy')

        for i in range(0, len(polygons)):
            if len(polygons[i]) == 2:
                create_circle(polygons[i][0], polygons[i][1], 45, self.canvas, 'red')

            else:
                self.canvas.create_polygon(polygons[i], fill="green", outline="red")

class Robot:
    def __init__(self, canvas, color):
        self.canvas = canvas
        # self.id = self.canvas.create_oval(-10, 10, 10, -10, fill=color)
        self.id = create_circle(0,0, 10, self.canvas, 'black')
        self.canvas.move(self.id, 350, 350)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.x = 350
        self.y = 200

    def draw(self):
        self.canvas.move(self.id,0, 0)
        pos = self.canvas.coords(self.id)


def robomulator():
    track = True
    robot_positions = []
    reached = False
    layout = [[sg.Canvas(size=(1000, 700), background_color='white', key='canvas')],
              [sg.T(''), sg.Button('Quit'), sg.Button('Move-R'), sg.Button('Move-L'), sg.Button('Move-U'), sg.Button('Move-D'), sg.Button('Tracking On/Off')]]

    window = sg.Window('Robot Simulator', return_keyboard_events=True).Layout(layout).Finalize()

    canvas = window.FindElement('canvas').TKCanvas

    # canvas.configure(cursor="crosshair")

    maze = Maze(canvas)

    robot = Robot(canvas, 'black')

    maze.draw()

    i = 0

    while True:

        i += 1

        robot.draw()

        pos_target = canvas.coords(maze.target)

        target_center_pos = [pos_target[0] + 25, pos_target[1] + 25]

        print(pos_target)

        event, values = window.Read(timeout=0)
        # canvas.move(1, 2, -9)

        # x_vel = random.randint(-1,1)
        # y_vel = random.randint(-1,1)

        x_dir = math.cos(math.degrees(45))
        y_dir = math.sin(math.degrees(45))
        # print(x_vel, y_vel)

        if i % 7 == 0 and reached is not True:
            canvas.move(robot.id, -3* x_dir, -3* y_dir)

        if event is None or event == 'Move-R':
            canvas.move(1, 10, 0)

        if event is None or event == 'Move-L':
            canvas.move(1, -10, 0)

        if event is None or event == 'Move-D':
            canvas.move(1, 0, 10)

        if event is None or event == 'Move-U':
            canvas.move(1, 0, -10)

        pos = canvas.coords(robot.id)

        center_pos = [pos[0] + 10, pos[1] + 10]
        center_pos = [round(center_pos[0],2), round(center_pos[1],2)]

        robot_positions.append(center_pos)

        # print(center_pos)

        if event == 'Quit':
            exit(69)

        if event == "Tracking On/Off":
            if track == True:
                track = False
            else:
                track = True

        if track:
            create_circle(center_pos[0], center_pos[1], 1, canvas, 'blue')



        canvas.itemconfig(maze.pos_out, text = str(center_pos))

        dist_to_target = calculateDistance(center_pos[0], center_pos[1], target_center_pos[0], target_center_pos[1])

        # print(dist_to_target)

        if dist_to_target <= 20:
            # exit(69)
            # messagebox.showinfo("Title", "a Tk MessageBox")
            reached = True
            # canvas.after(10)

        canvas.after(10)

if __name__ == '__main__':
    robomulator()
