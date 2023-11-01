from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

root = Tk()
root.title("Title")
root.geometry('1350x900')

coords = []

def resize_image(event):
    global photo, copy_of_image
    new_width = event.width
    new_height = event.height
    copy_of_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(copy_of_image)
    canvas.itemconfig(image_added, image=photo)
    print(new_width, new_height)

def save_coords(event):
    x = event.x
    y = event.y
    print(x, y)
    coords.append((x, y))
    # find closest city
    global first_press, closest_city
    if first_press:
        min_dist = 10
        for i in range(len(data)):
            x_coord = data['X'][i]
            y_coord = data['Y'][i]
            dist = ((x - x_coord)**2 + (y - y_coord)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                closest_city = data['City'][i]
        first_press = False

    else:
        # set new coords to closest city
        index = cities.tolist().index(closest_city)
        data['X'][index] = x
        data['Y'][index] = y
        # save to csv
        data.to_csv('data/map2.csv', index=False)
        # reset
        first_press = True
        closest_city = None
        # draw circles
        draw_circles()

    print(closest_city)

def draw_circles():
    for i in range(len(x)):
        x_coord = x[i]
        y_coord = y[i]
        size = 10
        for j in range(len(connections[i])):
            # find index of connection in cities
            try:
                index = cities.tolist().index(connections[i][j])
            except:
                continue
            # get x and y of connection
            x_coord_c = x[index]
            y_coord_c = y[index]
            # draw line
            if abs(x_coord - x_coord_c) > 300 or abs(y_coord - y_coord_c) > 300:
                continue
            canvas.create_line(x_coord, y_coord, x_coord_c, y_coord_c, fill='white')
    for i in range(len(x)):
        x_coord = x[i]
        y_coord = y[i]
        size = 10
        canvas.create_oval(x_coord - size, y_coord - size, x_coord + size, y_coord + size, fill=colors[i], activeoutline='white', width=2)
        canvas.create_text(x_coord, y_coord - 2*size, text=cities[i], fill='white', activefill='red')

first_press = True
closest_city = None

image = Image.open('data/map.png')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)

canvas = Canvas(root, width=image.width, height=image.height)
canvas.pack()

image_added = canvas.create_image(0, 0, image=photo, anchor=NW)

canvas.bind('<Configure>', resize_image)
canvas.bind('<Button-1>', save_coords)

data = pd.read_csv('data/map.csv')
x = data['X']
y = data['Y']
colors = data['Disease']
cities = data['City']
connections = data['Connections'].tolist()
connections = [connection.split(',') for connection in connections]
connections = [[city.strip() for city in connection] for connection in connections]

draw_circles()

root.mainloop()

print(coords)
