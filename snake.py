import os
import mysql.connector
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import random
from PIL import Image, ImageTk

load_dotenv()


ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS 

mycon = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "snake"),
)
cursor=mycon.cursor()
cursor.execute("create table if not exists stats(id int auto_increment primary key, username varchar(50) not null, score int not null, played_at timestamp default current_timestamp)")
name=''

window=None
canvas=None

#game loop
def change_direction(e):
    global velocityX, velocityY, game_over
    if (game_over):
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
        
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score, name, walls, wall
    if (game_over):
        cursor.fetchall()
        cursor.execute("insert into stats (username, score) values (%s, %s)", (name, score))
        window.after(2000)
        window.destroy()
        mycon.commit()
        npage()
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #hitting a wall
    if wall==True:
        if len(walls)>1:
            for i in walls:
                if i.x==snake.x and i.y==snake.y:
                    game_over = True
                    return
    
    #collision
    if (snake.x == food.x and snake.y == food.y): 
        
        if snake_body != []:
            last_tile = snake_body[-1]
            if velocityX == 1 or velocityY == 1:
                newx = last_tile.x - TILE_SIZE
                newy = last_tile.y - TILE_SIZE
            elif velocityX == -1 or velocityY == -1:
                newx = last_tile.x - TILE_SIZE
                newy = last_tile.y - TILE_SIZE
        else:
            if velocityX == 1 or velocityY == 1:
                newx = snake.x - TILE_SIZE
                newy = snake.y - TILE_SIZE
            elif velocityX == -1 or velocityY == -1:
                newx = snake.x - TILE_SIZE
                newy = snake.y - TILE_SIZE

        snake_body.append(Tile(newx, newy))

        while True:
            food.x = random.randint(0, COLS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE
            if wall:
                if all(i.x!=food.x or i.y!=food.y for i in walls+snake_body):
                    break
                else:
                    pass
            else:
                break
        score += 1

        #creating new walls when a food is eaten

        rate = int(len(snake_body)/2) + 2

        if wall==True:
            for i in range(rate):
                    if walls and len(walls)>1:
                        while True:
                            x=random.randrange(0,25)
                            y=random.randrange(0,25)
                            tile=Tile(x * TILE_SIZE,y * TILE_SIZE)
                            if all(i.x!=tile.x or i.y!=tile.y for i in walls):
                                walls.append(tile)
                                break
                            else:
                                continue

                    else:
                        first_wall = Tile(TILE_SIZE * 12, TILE_SIZE * 12)
                        walls.append(first_wall)

    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score, walls,wall
    move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = 'blue')

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'blue')

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")

    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")
    
    window.after(100, draw)

def draw1():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = 'blue')

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'blue')

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")

    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")
    
    window.after(75, draw1)

def draw2():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = 'blue')

    if wall:
        for i in walls:
            canvas.create_rectangle(i.x, i.y, i.x + TILE_SIZE, i.y + TILE_SIZE, fill = '#67756b')
            
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'blue')

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")

    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")
    
    window.after(100, draw2)

def back():
    global levels,led,bg_image
    bg_image=None
    led.destroy()
    levels()

def leaderboard():
    global levels,led,bg_image
    l.destroy()
    led=ctk.CTk()
    led.title("Leaderboard")
    led.geometry("500x600")
    ctk.set_appearance_mode("Dark")
    led.resizable(False,False)

    bg_image=ctk.CTkImage(dark_image=Image.open("lboardbg.png"),size=(500,600))
    display_bg_image=ctk.CTkLabel(led,image=bg_image,text="")
    display_bg_image.pack()

    cursor.fetchall()
    cursor.execute("select username, max(score) as best from stats group by username order by best desc, username limit 5")
    data=cursor.fetchall()

    name = ctk.CTkLabel(led, text="Name",font=("ARCADECLASSIC",30),padx=20,pady=20,bg_color='#F5F5DC',text_color="black")
    name.place(relx=0.01,rely=0.1)

    score = ctk.CTkLabel(led, text="Score",font=("ARCADECLASSIC",30),padx=20,pady=20,bg_color='#F5F5DC',text_color="black")
    score.place(relx=0.75,rely=0.1)

    t = ctk.CTkLabel(led, text="TOP 5",font=("ARCADECLASSIC",35),padx=20,pady=20,bg_color='#F5F5DC',text_color="black")
    t.place(relx=0.389,rely=0.01)

    b = ctk.CTkButton(led, text="Back", command= lambda: back())
    b.place(relx=0.7,rely=0.9)

    ry=0.18

    for rec in data:
        n = ctk.CTkLabel(led, text=rec[0],font=("ARCADECLASSIC",25),padx=20,pady=20,bg_color='#F5F5DC',text_color="black")
        n.place(relx=0.01,rely=ry+0.03)

        s = ctk.CTkLabel(led, text=rec[1],font=("ARCADECLASSIC",25),padx=20,pady=20,bg_color='#F5F5DC',text_color="black")
        s.place(relx=0.75,rely=ry+0.03)
        
        ry+=0.1
        
    led.mainloop()

def setup():
    global window,canvas,snake,food,velocityX,velocityY,snake_body,game_over,score,wall
    #game window
    wall= False
    l.destroy()
    window = tk.Tk()
    window.title("Snake")
    window.geometry("625x625")
    window.resizable(False, False)
    canvas = tk.Canvas(window, bg = "green", width = 625, height = 625, borderwidth = 0, highlightthickness = 0)
    canvas.pack()
    window.update()

    #center the window
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = int((screen_width/2) - (window_width/2))
    window_y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    #initialize game
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) 
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0

    draw()
    
    window.bind("<KeyPress>", change_direction)
    window.mainloop()

def setup1():
    global window,canvas,snake,food,velocityX,velocityY,snake_body,game_over,score,window_x,window_y,wall
    #game window
    wall = False
    l.destroy()
    window = tk.Tk()
    window.title("Snake")
    window.geometry("625x625")
    window.resizable(False, False)
    canvas = tk.Canvas(window, bg = "green", width = 625, height = 625, borderwidth = 0, highlightthickness = 0)
    canvas.pack()
    window.update()

    #center the window
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = int((screen_width/2) - (window_width/2))
    window_y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    #initialize game
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) 
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0

    draw1()
    
    window.bind("<KeyPress>", change_direction)
    window.mainloop() 

def setup2():
    global window,canvas,snake,food,velocityX,velocityY,snake_body,game_over,score
    #game window
    
    window = tk.Tk()
    window.title("Snake")
    window.geometry("625x625")
    window.resizable(False, False)
    canvas = tk.Canvas(window, bg = "green", width = 625, height = 625, borderwidth = 0, highlightthickness = 0)
    canvas.pack()
    window.update()

    #center the window
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = int((screen_width/2) - (window_width/2))
    window_y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    #initialize game
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) 
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0

    draw2()
    
    window.bind("<KeyPress>", change_direction)
    window.mainloop()

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def l3():
    global walls, wall
    walls = []
    wall = True
    l.destroy()
    setup2()

def levels():
    global l,levels
    l=ctk.CTk()
    l.title("Snake Game")
    l.geometry("800x400")
    ctk.set_appearance_mode("Dark")
    l.resizable(False,False)

    bg_image=ctk.CTkImage(dark_image=Image.open("BG.png"),size=(800,400))
    display_bg_image=ctk.CTkLabel(l,image=bg_image,text="")
    display_bg_image.pack()

    Levels = ctk.CTkLabel(l, text="Levels:-", font=("mexcellent 3d",30))
    Levels.place(relx=0.08,rely=0.2)

    lvl1=ctk.CTkButton(l, text="Level 1" , command= lambda: setup())
    lvl1.place(relx=0.08,rely=0.3)

    lvl2=ctk.CTkButton(l, text="Level 2" , command= lambda: setup1())
    lvl2.place(relx=0.4,rely=0.3)

    lvl3=ctk.CTkButton(l, text="Level 3" , command= lambda: l3())
    lvl3.place(relx=0.7,rely=0.3)

    lboard=ctk.CTkLabel(l, text="Leaderboard:-", font=("mexcellent 3d",30))
    lboard.place(relx=0.08,rely=0.5)

    leaderboard_button = ctk.CTkButton(l, text="Leaderboard" , command=lambda: leaderboard())
    leaderboard_button.place(relx=0.08,rely=0.6)

    l.mainloop()

def start_game():
    global entry, name
    name=entry.get().strip()[:50]
    print(name)
    if name=='':
        messagebox.showerror("Error",'Please Enter a name')
        return
    n.destroy()
    levels()


wall = False

app=None
entry=None
game_over=None

#first page
def npage():
    global n,entry
    n=ctk.CTk()
    n.title("Snake Game")
    n.geometry("800x400")
    ctk.set_appearance_mode("Dark")
    n.resizable(False,False)

    bg_image=ctk.CTkImage(dark_image=Image.open("BG.png"),size=(800,400))
    display_bg_image=ctk.CTkLabel(n,image=bg_image,text="")
    display_bg_image.pack()

    s = ctk.CTkLabel(n, text="SNAKE GAME", font=("mexcellent 3d",33))
    s.place(relx=0.375,rely=0.27)

    label = ctk.CTkLabel(n, text="Enter your name:", font=("mexcellent 3d",27))
    label.place(relx=0.35,rely=0.4)

    entry = ctk.CTkEntry(n, width=200)
    entry.place(relx=0.36,rely=0.5)

    play_game_button1 = ctk.CTkButton(n, text="Play Game" , command= lambda: start_game())
    play_game_button1.place(relx=0.4,rely=0.6)

    n.mainloop()

if __name__ == '__main__':
    npage()
