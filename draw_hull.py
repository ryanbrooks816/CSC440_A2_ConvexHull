"""
Put this debug function in convex_hull.py for testing:

def compute_hull_debug(points: List[Point]):
# No further work needed, returns points in clockwise order
if len(points) <= 1:
    return points, []
if len(points) <= 3:
    clockwise_sort(points)
    return points, []

# Sort the points by x-coordinate
points.sort()

hulls_and_tangents = []

def divide_hull(points: List[Point]) -> List[Point]:
    if len(points) <= 6:
        return base_case_hull(points)
    
    # Divide the points into two halves
    mid = len(points) // 2
    left_points = points[:mid]
    right_points = points[mid:]

    # Recursively compute the hulls of the two halves
    left_hull = divide_hull(left_points)
    right_hull = divide_hull(right_points)
    
    # Merge the two hulls
    merged_hull = merge_hulls(left_hull, right_hull)
    
    # Store the hulls and their tangents for visualization
    tangents_indices = find_tangents(left_hull, right_hull)
    tangents = (left_hull[tangents_indices[0][0]], right_hull[tangents_indices[0][1]]), (left_hull[tangents_indices[1][0]], right_hull[tangents_indices[1][1]])
    hulls_and_tangents.append((left_hull, right_hull, merged_hull, tangents))
    
    return merged_hull

# Sort the complete hull in clockwise order
complete_hull = divide_hull(points)

clockwise_sort(complete_hull)
return complete_hull, hulls_and_tangents
"""

import copy
from tkinter import Button, Canvas, NORMAL, PhotoImage, Tk, Entry
from convex_hull import compute_hull, compute_hull_debug
import random

def draw_point(canvas, x, y):
    canvas.create_image((x, y), image=ram, state=NORMAL)
    canvas.create_text(x + 25, y + 25, text=f"({x}, {y})", anchor="w", font=("Arial", 10))

def add_point(event):
    draw_point(w, event.x, event.y)
    points.append((event.x, event.y))
    return

def draw_hull_step():
    global step_index, draw_stage
    
    if step_index < len(hulls_and_tangents):
        left_hull, right_hull, merged_hull, tangents = hulls_and_tangents[step_index]
        color = colors[step_index % len(colors)]
        
        if draw_stage == 0:
            # Draw left hull
            for i in range(len(left_hull)):
                x1, y1 = left_hull[i]
                x2, y2 = left_hull[(i + 1) % len(left_hull)]
                w.create_line(x1, y1, x2, y2, width=2, fill=color)
            draw_stage = 1
        
        elif draw_stage == 1:
            # Draw right hull
            for i in range(len(right_hull)):
                x1, y1 = right_hull[i]
                x2, y2 = right_hull[(i + 1) % len(right_hull)]
                w.create_line(x1, y1, x2, y2, width=2, fill=color)
            draw_stage = 2
        
        elif draw_stage == 2:
            # Draw first tangent
            (x1, y1), (x2, y2) = tangents[0]
            print(f"Drawing first tangent: ({x1}, {y1}) -> ({x2}, {y2})")
            w.create_line(x1, y1, x2, y2, width=2, fill="black", dash=(4, 2))
            draw_stage = 3

        elif draw_stage == 3:
            # Draw second tangent
            (x3, y3), (x4, y4) = tangents[1]
            print(f"Drawing second tangent: ({x3}, {y3}) -> ({x4}, {y4})")
            w.create_line(x3, y3, x4, y4, width=2, fill="black", dash=(4, 2))
            draw_stage = 4
        
        elif draw_stage == 4:
            # Draw merged hull
            for i in range(len(merged_hull)):
                x1, y1 = merged_hull[i]
                x2, y2 = merged_hull[(i + 1) % len(merged_hull)]
                w.create_line(x1, y1, x2, y2, width=2, fill=color)
            draw_stage = 5
            
        elif draw_stage == 5:
            # Move to next step if there are more steps
            if step_index < len(hulls_and_tangents) - 1:
                step_index += 1
                draw_stage = 0
            else:
                step_index += 1
                
    elif step_index == len(hulls_and_tangents):
        # Draw final hull in black
        hull.append(hull[0])
        for i in range(len(hull) - 1):
            x1, y1 = hull[i]
            x2, y2 = hull[i + 1]
            w.create_line(x1, y1, x2, y2, width=3, fill="black")
        step_index += 1
    return

def draw_hull_debug():
    global hull, hulls_and_tangents, step_index, draw_stage
    hull, hulls_and_tangents = compute_hull_debug(points)
    print("Hull: ", hull)
    step_index = 0
    draw_stage = 0
    draw_hull_step()
    return

def draw_hull():
    hull = copy.copy(compute_hull(points))
    print("Hull: ", hull)
    hull.append(hull[0])
    for i in range(0, len(hull) - 1):
        x1 = hull[i][0]
        y1 = hull[i][1]
        x2 = hull[i + 1][0]
        y2 = hull[i + 1][1]
        w.create_line(x1, y1, x2, y2, width=3)
    return

def erase_canvas():
    w.delete("all")
    points.clear()
    return

def disperse_points():
    erase_canvas()
    try:
        num_points = int(num_points_entry.get())
    except ValueError:
        num_points = 10  # Default value if input is invalid
    for _ in range(num_points):
        x = random.randint(0, canvas_width)
        y = random.randint(0, canvas_height)
        draw_point(w, x, y)
        points.append((x, y))
    return

if __name__ == '__main__':
    master, points = Tk(), list()
    hull, hulls_and_tangents, step_index, draw_stage = [], [], 0, 0
    colors = ["red", "blue", "green", "orange", "purple", "pink", "cyan", "magenta", "yellow"]
    
    submit_button = Button(master, text="Draw Hull", command=draw_hull)
    submit_button.pack()
    submit_debug_button = Button(master, text="Draw Hull Debug", command=draw_hull_debug)
    submit_debug_button.pack()
    step_button = Button(master, text="Step", command=draw_hull_step)
    step_button.pack()
    erase_button = Button(master, text="Erase", command=erase_canvas)
    erase_button.pack()
    disperse_button = Button(master, text="Disperse Points", command=disperse_points)
    disperse_button.pack()
    quit_button = Button(master, text="Quit", command=master.quit)
    quit_button.pack()

    num_points_entry = Entry(master)
    num_points_entry.pack()
    num_points_entry.insert(0, "10")  # Default value

    canvas_width = 1000
    canvas_height = 800
    w = Canvas(master, width=canvas_width, height=canvas_height)
    ram = PhotoImage(file="ram-sm.gif")
    w.pack()
    w.bind('<Button-1>', add_point)

    w.mainloop()
