import sys
import tkinter as tk
import numpy as np
import random
import math
from tkinter import messagebox
import time
# import pyscreenshot as ImageGrab

# root = Tk()

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import random
import time
from sys import exit as exit

def create_circle(x, y, r, canvasName, color, outline=None): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill = color, outline = outline)

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

def calculate_heading(x1,y1,x2,y2):
    heading = math.atan2(y2-y1, x2-x1)
    return math.degrees(heading)

class Robot:
    def __init__(self, canvas, color):
        self.canvas = canvas
        # self.id = self.canvas.create_oval(-10, 10, 10, -10, fill=color)
        self.id = create_circle(350,350, 10, self.canvas, 'black')
        self.step_size = 20
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.x = 350
        self.y = 200

    def draw(self):
        # self.canvas.move(self.id,0, 0)
        pos = self.canvas.coords(self.id)

    def trace_path(self):
        path = np.load('robot_trace.npy')
        # self.canvas.move(self.id, 350, 350)
        for p in path:
            # print(p)
            create_circle(p[0],p[1], 2, self.canvas, 'black', outline = "blue")
            self.canvas.update()
            time.sleep(0.05)



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

        self.canvas.create_text(850,120, fill="darkblue", font="Times 15 bold", text="Heading/Rotation")

        self.rotation = self.canvas.create_text(850,150, fill="darkblue", font="Times 15 bold", text="Rotation")

        self.canvas.create_text(850,600, fill="darkblue", font="Times 15 bold", text="Tracking")

        self.canvas.create_text(850,200, fill="darkblue", font="Times 15 bold", text="Target Centric Navigation")

        self.target_strategy = self.canvas.create_text(850,230, fill="darkblue", font="Times 15 bold", text="False")

        self.canvas.create_text(850,500, fill="darkblue", font="Times 15 bold", text="Obstacle Avoidance")

        self.sonar_status = self.canvas.create_text(850,530, fill="darkblue", font="Times 15 bold", text="True")

        self.canvas.create_text(850,600, fill="darkblue", font="Times 15 bold", text="Tracking")

        self.tracking_status = self.canvas.create_text(850,630, fill="darkblue", font="Times 15 bold", text="False")

        target = np.load('only_target.npy')

        self.target = create_circle(target[0][0], target[0][1], 25, self.canvas, 'yellow')

        # print("Target is id "+str(self.target))

        polygons = np.load('polygons3.npy')

        for i in range(0, len(polygons)):
            if len(polygons[i]) == 2:
                create_circle(polygons[i][0], polygons[i][1], 45, self.canvas, 'green')

            else:
                self.canvas.create_polygon(polygons[i], fill="green", outline="red")

class Sonar():
    def __init__(self, canvas, center_pos):
        self.position = center_pos
        # self.angles = range(0,360,45)
        self.angles = range(0, 360+45, 45)
        self.canvas = canvas
        self.id = create_circle(self.position[0], self.position[1], 60, self.canvas, "")
        self.prev_id = None
        self.lines_id = []
        self.allowed_dir = []
        self.range = 60

    def sweep(self, original_items, target_id, target_centric = False):
        r = self.range

        # Throwing 8 beams at 45 degree interval
        center_pos = self.position
        x1,y1 = (center_pos[0]), (center_pos[1] - r)
        x2, y2 = (center_pos[0] + r * math.cos(math.radians(45))) , (center_pos[1] - r * math.sin(math.radians(45)))
        x3, y3 = (center_pos[0] + r) , center_pos[1]
        x4, y4 = (center_pos[0] + r * math.cos(math.radians(45))) , (center_pos[1] + r * math.sin(math.radians(45)))
        x5, y5 = (center_pos[0]), (center_pos[1] + r)
        x6, y6 = (center_pos[0] - r * math.cos(math.radians(45))) , (center_pos[1] + r * math.sin(math.radians(45)))
        x7, y7 = (center_pos[0] - r) , center_pos[1]
        x8, y8 = (center_pos[0] - r * math.cos(math.radians(45))) , (center_pos[1] - r * math.sin(math.radians(45)))

        x_list = [x1,x2,x3,x4,x5,x6,x7,x8]
        y_list = [y1,y2,y3,y4,y5,y6,y7,y8]

        for i in range(0,8):

            self.lines_id.append(self.canvas.create_line(self.position[0], self.position[1], x_list[i], y_list[i], fill="blue", dash = 4))

        restricted_directions = []

        for l in self.lines_id:
            cc = self.canvas.coords(l)
            # print(cc)
            obstacles = self.canvas.find_overlapping(cc[0],cc[1],cc[2],cc[3])
            # print('--The obstacles are---')
            # print(obstacles)

            orig_obs = tuple(set(obstacles) & set(original_items))
            # if obstacles in original_items:
            #     print('Obstacle detected')
            orig_obs = list(orig_obs)
            orig_obs.remove(1)

            if target_id in orig_obs:
                orig_obs.remove(target_id)

            if len(orig_obs) > 0:
                restricted_directions.append(1)
            else:
                restricted_directions.append(0)

        for i in range(0,8):
            if restricted_directions[i] == 0:
                self.allowed_dir.append(self.angles[i])

        # print((self.allowed_dir))

        # ------------------------Target centric ---------------
        if target_centric:
            if len(self.allowed_dir) == 8:
                self.canvas.delete(self.id)

                for i in self.lines_id:
                    self.canvas.delete(i)
                self.lines_id = []
                return -1

        if len(self.allowed_dir) > 0:
            allowed_dir = random.choice(self.allowed_dir)
        else:
            allowed_dir = random.choice(self.angles)

        dir_map = [270,315,0,45,90,135,180,225, 360]
        dir_orig  = [0,45,90,135,180,225,270,315, 360]

        index_angle = dir_orig.index(allowed_dir)
        allowed_dir = dir_map[index_angle]

        self.canvas.delete(self.id)

        for i in self.lines_id:
            self.canvas.delete(i)
        self.lines_id = []
        return allowed_dir

def robomulator():
    track = False
    robot_positions = []
    reached = False
    move = False
    last_sonar = None
    sweeping = True
    target_centric = False
    layout = [[sg.Canvas(size=(1000, 700), background_color='white', key='canvas')],
              [sg.T(''), sg.Button('Quit'), sg.Button('Sonar_Sweep'),  sg.Button('Start/Stop'), sg.Button('Move-R'), sg.Button('Move-L'), sg.Button('Move-U'), sg.Button('Move-D'), sg.Button('Tracking On/Off'), sg.Button('Trace'), sg.Button('Save-Path'), sg.Button('Target_centric')]]

    window = sg.Window('Robot Simulator', return_keyboard_events=True).Layout(layout).Finalize()

    canvas = window.FindElement('canvas').TKCanvas

    maze = Maze(canvas)

    robot = Robot(canvas, 'black')

    maze.draw()

    original_items = canvas.find_all()

    print('----The original objects are----')
    print(original_items)

    i = 0

    while True:

        i += 1

        robot.draw()

        pos_target = canvas.coords(maze.target)

        target_center_pos = [pos_target[0] + 25, pos_target[1] + 25]

        pos = canvas.coords(robot.id)

        center_pos = [pos[0] + 10, pos[1] + 10]
        center_pos = [round(center_pos[0],2), round(center_pos[1],2)]

        event, values = window.Read(timeout=0)

        x_vel = random.randint(-1,1)
        y_vel = random.randint(-1,1)

        target_heading = calculate_heading(target_center_pos[0], target_center_pos[1] , center_pos[0], center_pos[1])

        angles = range(0,360,45)
        rand_angle = random.choice(angles)
        heading = math.radians(rand_angle)

        allowed_dir = math.degrees(heading)

        x_dir = math.cos(heading)
        y_dir = math.sin(heading)

        # Events binding started

        if event is None or event == 'Move-R':
            canvas.move(1, 10, 0)

        if event is None or event == 'Move-L':
            canvas.move(1, -10, 0)

        if event is None or event == 'Move-D':
            canvas.move(1, 0, 10)

        if event is None or event == 'Move-U':
            canvas.move(1, 0, -10)



        # robot_positions.append(center_pos)

        if event == 'Quit':
            exit(69)

        if event == 'Target_centric':
            target_centric = not target_centric
            canvas.itemconfig(maze.target_strategy, text = str(target_centric))

        if event == "Save-Path":
            np.save('robot_trace.npy', robot_positions)


        if event == "Tracking On/Off":
            track = not track
            canvas.itemconfig(maze.tracking_status, text = str(track))


        if event == "Start/Stop":
            move = not move

        if event == "Sonar_Sweep":
            sweeping = not sweeping
            canvas.itemconfig(maze.sonar_status, text = str(sweeping))

        if event == "Trace":
            robot.trace_path()

        # Events binding end

        if sweeping and move and reached is not True:
            sonar = Sonar(canvas, center_pos)



            # ------------------------Target centric ---------------
            if target_centric:

                allowed_dir = sonar.sweep(original_items, maze.target, True)
                if allowed_dir == -1:
                    allowed_dir = 180+target_heading

            else:
                allowed_dir = sonar.sweep(original_items, maze.target, False)

            x_dir = math.cos(math.radians(allowed_dir))
            y_dir = math.sin(math.radians(allowed_dir))

        if i % 5 == 0 and reached is not True and move:
            canvas.move(robot.id, robot.step_size* x_dir, robot.step_size* y_dir)
            robot_positions.append(center_pos)
            canvas.itemconfig(maze.rotation, text = str(round(allowed_dir,2))+" degrees")

        canvas.itemconfig(maze.pos_out, text = str(center_pos))

        if track:
            create_circle(center_pos[0], center_pos[1], 2, canvas, 'black', outline = "blue")
            if len(robot_positions) > 2:
                l = len(robot_positions)
                p_x1, p_y1 = robot_positions[l-1][0], robot_positions[l-1][1]
                p_x2, p_y2 = robot_positions[l-2][0], robot_positions[l-2][1]
                canvas.create_line(p_x1, p_y1, p_x2, p_y2, fill="blue")

        dist_to_target = calculateDistance(center_pos[0], center_pos[1], target_center_pos[0], target_center_pos[1])

        if dist_to_target <= 20:
            # exit(69)
            # messagebox.showinfo("Title", "a Tk MessageBox")
            reached = True

        canvas.after(10)

if __name__ == '__main__':
    robomulator()
