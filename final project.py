import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import Image,ImageTk
import FinalModel as fm
from UserInterface import IPL

# Connect to the SQLite database or create it if it doesn't exist
conn = sqlite3.connect("players.db")
cursor = conn.cursor()

# Create the players table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    batting_style TEXT NOT NULL,
    bowling_style TEXT NOT NULL,
    position TEXT NOT NULL,
    nationality TEXT
)
""")

class Player:
    def _init_(self, name, gender, batting_style, bowling_style, position, nationality):
        name = name
        gender = gender
        batting_style = batting_style
        bowling_style = bowling_style
        position = position
        nationality = nationality

# Create the root window
root = tk.Tk()
root.geometry("800x800")

# Define the players list
players = []

# Define the entry variables
entry_name = tk.StringVar()
entry_gender = tk.StringVar()
entry_batting_style = tk.StringVar()
entry_bowling_style = tk.StringVar()
entry_position = tk.StringVar()
entry_nationality = tk.StringVar()

def add_player():
    name = entry_name.get()
    gender = entry_gender.get()
    batting_style = entry_batting_style.get()
    bowling_style = entry_bowling_style.get()
    position = entry_position.get()
    nationality = entry_nationality.get()

    cursor.execute("""
    INSERT INTO players (name, gender, batting_style, bowling_style, position, nationality)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, gender, batting_style, bowling_style, position, nationality))
    conn.commit()

    new_player = Player(name, gender, batting_style, bowling_style, position, nationality)
    players.append(new_player)

    update_player_grid()

def update_player():
    selected_player_index = grid_players.focus()
    if selected_player_index:
        selected_player_index = int(grid_players.index(selected_player_index))
        selected_player = players[selected_player_index]

        selected_player.name = entry_name.get()
        selected_player.gender = entry_gender.get()
        selected_player.batting_style = entry_batting_style.get()
        selected_player.bowling_style = entry_bowling_style.get()
        selected_player.position = entry_position.get()
        selected_player.nationality = entry_nationality.get()

        # Update the selected player in the database
        cursor.execute("""
        UPDATE players
        SET name=?, gender=?, batting_style=?, bowling_style=?, position=?, nationality=?
        WHERE id=?
        """, (selected_player.name, selected_player.gender, selected_player.batting_style, selected_player.bowling_style, selected_player.position, selected_player.nationality, selected_player.id))
        conn.commit()

        update_player_grid()

def delete_player():
    selected_player_index = grid_players.focus()
    if selected_player_index:
        selected_player_index = int(grid_players.index(selected_player_index))
        selected_player = players[selected_player_index]

        # Delete the selected player from the database
        cursor.execute("""
        DELETE FROM players
        WHERE id=?
        """, (selected_player.id,))
        conn.commit()

        del players[selected_player_index]

        update_player_grid()

def update_player_grid():
    # Clear the grid and the players list
    grid_players.delete(*grid_players.get_children())
    players.clear()

    # Populate the players list and the grid from the database
    cursor.execute("""
    SELECT id, name, gender, batting_style, bowling_style, position, nationality
    FROM players
    ORDER BY name
    """)
    for row in cursor.fetchall():
        id, name, gender, batting_style, bowling_style, position, nationality = row
        new_player = Player(name, gender, batting_style, bowling_style, position, nationality)
        new_player.id = id
        players.append(new_player)
        grid_players.insert("", "end", values=(name, gender, batting_style, bowling_style, position, nationality))

def open_new_gui():
    # Create a new window for the new GUI
    new_window = tk.Toplevel(root)
    new_window.title("CricketersRecommendationSystem")
    new_window.geometry("1550x800+0+0")
        
    lbl_title=Label(new_window,text="Cricketers Recommendation System",font=("times new roman",40,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
    lbl_title.place(x=0,y=0,width=1550,height=70)
        
    labelframe=LabelFrame(new_window,bd=2,relief=RIDGE,text="Players Information",font=("times new roman",20,"bold"),padx=3)
    labelframe.place(x=9,y=70,width=550,height=720)

    img3=Image.open("CricketLogo.jpg")
    img3=img3.resize((100,60),Image.BICUBIC)
    photoimg3=ImageTk.PhotoImage(img3)

    lblimg1=Label(new_window,image=photoimg3,bd=0,relief=RIDGE)
    lblimg1.place(x=0,y=3,width=100,height=60)

    img2=Image.open("cricketicon.jpg")
    img2=img2.resize((550,710),Image.BICUBIC)
    photoimg2=ImageTk.PhotoImage(img2)

    lblimg1=Label(new_window,image=photoimg2,bd=0,relief=RIDGE)
    lblimg1.place(x=10,y=105,width=550,height=685)

    cursor.execute("SELECT name FROM players")
    name_data = cursor.fetchall()
        
    label_Player_Name=Label(lblimg1,font=("arial",18,"bold"),text="Player Name:",padx=2,pady=200)
    label_Player_Name.place(x=5,y=250,width=200,height=45)
    combo_player=ttk.Combobox(lblimg1,font=("arial",18,"bold"),width=27)
    combo_player['values']=name_data
    combo_player.place(x=220,y=250,width=300,height=45)

    btnSEARCH=Button(lblimg1,text="Search",font=("arial",12,"bold"),bg="black",fg="gold",width=10,padx=2,pady=6)
    btnSEARCH.place(x=200,y=600,width=100,height=45)

    graph_variable = StringVar()
    graph_variable.set("Select Graph")
    dropdown = OptionMenu(new_window, graph_variable, "Gender Distribution", "Player Type Distribution", "Player vs Batsmen Accuracy", "Player vs Bowler Accuracy", "Player vs All Rounder Accuracy")
    dropdown.config(font=("Arial", 12, "bold"), bg="white", fg="black", width=20)
    dropdown.place(x=170, y=530)

    btnGO=Button(lblimg1,text="Go",font=("arial",12,"bold"),bg="black",fg="gold",width=10,padx=2,pady=6,command=lambda:fm.plotGraph(graph_variable.get()))
    btnGO.place(x=280,y=480,width=100,height=45)

    img=Image.open("cricketicon2.jpg")
    img=img.resize((950,360),Image.BICUBIC)
    photoimg=ImageTk.PhotoImage(img)

    lblimg=Label(new_window,image=photoimg,bd=0,relief=RIDGE)
    lblimg.place(x=565,y=430,width=950,height=360)

    Table_Frame=LabelFrame(new_window,bd=2,relief=RIDGE,text="View Details",font=("arial",20,"bold"),padx=2)
    Table_Frame.place(x=560,y=70,width=960,height=420)

    details_table=Frame(Table_Frame,bd=2,relief=RIDGE)
    details_table.place(x=0,y=30,width=950,height=350)

    scroll_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(details_table,orient=VERTICAL)
    Player_Details_Table=ttk.Treeview(details_table,column=("Player_Name","Player_Status"),xscrollcommand=scroll_x.set)

    scroll_x.pack(side=BOTTOM,fill=X)
    scroll_y.pack(side=RIGHT,fill=Y)

    scroll_x.config(command=Player_Details_Table.xview)
    scroll_y.config(command=Player_Details_Table.yview)

    Player_Details_Table.heading("Player_Name",text="Player Name")
    Player_Details_Table.heading("Player_Status",text="Player Status")
    Player_Details_Table["show"]="headings"

    Player_Details_Table.column("Player_Name",width=100)
    Player_Details_Table.column("Player_Status",width=100)
    Player_Details_Table.pack(fill=BOTH,expand=1)


# Create a heading label
heading_label = ttk.Label( text="Cricketer Recommendation System", background="black", foreground="yellow", font=("Arial", 18))
heading_label.grid(column=1, row=0, padx=5, pady=5, sticky="w")

# Create a frame for the player data entry widgets
player_frame = ttk.LabelFrame(root, text="Player Data")
player_frame.grid(column=0, row=1, padx=10, pady=10, sticky="w")

# Create the player data entry widgets
name_label = ttk.Label(player_frame, text="Name:")
name_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(player_frame, textvariable=entry_name)
name_entry.grid(column=1, row=0, padx=5, pady=5, sticky="w")

gender_label = ttk.Label(player_frame, text="Gender:")
gender_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")
gender_combo = ttk.Combobox(player_frame, textvariable=entry_gender, values=["Male", "Female"])
gender_combo.grid(column=1, row=1, padx=5, pady=5, sticky="w")

batting_style_label = ttk.Label(player_frame, text="Batting Style:")
batting_style_label.grid(column=0, row=2, padx=5, pady=5, sticky="w")
batting_style_combo = ttk.Combobox(player_frame, textvariable=entry_batting_style, values=['Batsman','Middle Order Batter','Top Order Batter','Batting Allrounder'])
batting_style_combo.grid(column=1, row=2, padx=5, pady=5, sticky="w")

bowling_style_label = ttk.Label(player_frame, text="Bowling Style:")
bowling_style_label.grid(column=0, row=3, padx=5, pady=5, sticky="w")
bowling_style_combo = ttk.Combobox(player_frame, textvariable=entry_bowling_style, values=['Bowler','Bowling Allrounder'])
bowling_style_combo.grid(column=1, row=3, padx=5, pady=5, sticky="w")

position_label = ttk.Label(player_frame, text="Position:")
position_label.grid(column=0, row=4, padx=5, pady=5, sticky="w")
position_combo = ttk.Combobox(player_frame, textvariable=entry_position, values=["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
position_combo.grid(column=1, row=4, padx=5, pady=5, sticky="w")

nationality_label = ttk.Label(player_frame, text="Nationality:")
nationality_label.grid(column=0, row=5, padx=5, pady=5, sticky="w")
nationality_combo = ttk.Combobox(player_frame, textvariable=entry_nationality, values=fm.player_country['country_name'].unique())
nationality_combo.grid(column=1, row=5, padx=5, pady=5, sticky="w")

# Create a frame for the buttons
button_frame = ttk.LabelFrame(root, text="Buttons")
button_frame.grid(column=0, row=5, padx=10, pady=10, sticky="w")

# Create the buttons
add_button = ttk.Button(button_frame, text="Add Player", command=add_player)
add_button.grid(column=0, row=0, padx=5, pady=5, sticky="w")

update_button = ttk.Button(button_frame, text="Update Player", command=update_player)
update_button.grid(column=1, row=0, padx=5, pady=5, sticky="w")

delete_button = ttk.Button(button_frame, text="Delete Player", command=delete_player)
delete_button.grid(column=2, row=0, padx=5, pady=5, sticky="w")

goto_search = ttk.Button(button_frame, text="Go to Search", command=open_new_gui)
goto_search.grid(column=3, row=0, padx=5, pady=5, sticky="w")

# Create a frame for the grid
grid_frame = ttk.LabelFrame(root, text="Players")
grid_frame.grid(column=1, row=1, rowspan=5, padx=10, pady=10, sticky="nsew")

# Create a frame for the image
image_frame = ttk.Frame(grid_frame)
image_frame.grid(column=0, row=1, sticky="s")

# Load the image
image = tk.PhotoImage(r"background_image.png")

# Create a label with the image
image_label = ttk.Label(image_frame, image=image)
image_label.image = image
image_label.grid(column=0, row=0, sticky="nsew")

# Create the grid
grid_players = ttk.Treeview(grid_frame, columns=("Name", "Gender", "Batting Style","Bowling Style", "Position", "Nationality"), show="headings")
grid_players.grid(column=0, row=0, sticky="nsew")

grid_players.heading("Name", text="Name")
grid_players.heading("Gender", text="Gender")
grid_players.heading("Batting Style", text="Batting Style")
grid_players.heading("Bowling Style", text="Bowling Style")
grid_players.heading("Position", text="Position")
grid_players.heading("Nationality", text="Nationality")

# Create a scrollbar for the grid
scrollbar_players = ttk.Scrollbar(grid_frame, orient="vertical", command=grid_players.yview)
scrollbar_players.grid(column=1, row=0, sticky="ns")

grid_players.config(yscrollcommand=scrollbar_players.set)

# Populate the grid with the players from the database
update_player_grid()

root.mainloop()

# Close the database connection
conn.close()
