
import numpy as np
import pandas as pd
import math
import os
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, AppLayout
import functools
import difflib
from IPython.display import clear_output
from IPython.display import display, HTML
import time

# instantiate all of the necessary preliminaries
managers = ["Me","Jack", "Jordan","Blake","Jason","Mason","Mike","Johnny", "Ben","Noah","Scott", "BZ"]
limit = 200
positions = ["QB","RB1","RB2","WR1","WR2","TE","FLX1","FLX2","HC","$ Left","Max Bid"]
positions2 = ["QB","RB1","RB2","WR1","WR2","TE","FLX1","FLX2","HC"]

# function to refresh the master board to all NAs and $200 for total $
def refresh(b = None):
    master = pd.DataFrame(columns = managers, index = positions)
    for index, row in master.iterrows():
        if index == "$ Left":
            for i in managers:
                master.at[index,i] = limit
        if index == "Max Bid":
            for i in managers:
                 master.at[index,i] = limit - 9
    return master

# Function to view a specific manager's team in a nice format
def view_manager(manager):
    display(HTML(master[manager].to_frame().to_html()))
    
# Function to add a player to the master board once the bidding has stopped and the 
# player has been sold
def player_sold(manager, pos, name, value):
    if not isinstance(master.at[pos,manager], str):
        stack.append(master.copy())
        master.at[pos, manager] = name +" " + "$" + str(value)
        curr = master.at["$ Left", manager] 
        master.at["$ Left", manager] = curr - value
        Nas = master[manager].isna().sum() - 1
        maxVal = master.at["$ Left",manager] - Nas
        master.at["Max Bid", manager] = maxVal
        #stack.append(master.copy())
    else:
        print("ERROR: Position already filled or manager name not correct")



master = refresh()
stack = []

def create_expanded_button(description, button_style):
    return Button(description=description, button_style=button_style, 
                  layout=Layout(height='auto', width='auto'))


pos = widgets.Text()
name = widgets.Text()
val = widgets.Text()
playerName = widgets.Text()

def select_position(position):
    pos.value = str(position)
    
def player_name(player):
    playerName.value = str(player)
    
def select_manager(manager):
    name.value = str(manager)
    
def select_value(value):
    val.value = str(value)
    
def view_master(b):
    display(HTML(master.to_html()))
    

a = widgets.interactive(select_manager, manager = managers)
b = widgets.interactive(select_position,position = positions2)
c = widgets.interactive(player_name, player = "")
d = widgets.interactive(select_value, value = ((0,110)))

#ADD PLAYER BUTTON
addButton = create_expanded_button("Add Player", "success")

def add_player(b):
    player_sold(name.value, pos.value, playerName.value, int(val.value))
    print("SUCCESS!")
    
addButton.on_click(add_player)

# VIEW BOARD BUTTON
btn = create_expanded_button("View Board","info")
out1 = widgets.Output()
display(out1)
def view_master(b):
    with out1:
        clear_output(wait=True)
        display(HTML(master.to_html()))

        
btn.on_click(view_master)


dropDown = widgets.Text()

def select_manager2(view_manager):
    name.value = str(view_manager)
    
# SELECT MANAGER DROPDOWN
#e = widgets.interactive(select_manager2, view_manager = managers, 
#                        layout = Layout(width = "auto", grid_area = 'sidebar'))

#VIEW MANAGER BUTTON
show = create_expanded_button("View Manager","info")

out = widgets.Output()
display(out)
def on_button_clicked(b):
    with out:
        clear_output(wait = True)
        view_manager(name.value)
show.on_click(on_button_clicked)

def undo_add(na):
    global master
    try:
        master = stack.pop()
    except:
        print("NOTHING TO UNDO!")
    
#UNDO BUTTON
undo = create_expanded_button("Undo","danger")
undo.on_click(undo_add)

def refresh_v2(nan):
    global master
    master = refresh()
    global stack
    stack = []
    
#REFRESH BUTTON
refreshButton = create_expanded_button("Refresh Board","Danger")
refreshButton.on_click(refresh_v2)


items = [a,b,c,d]
display(widgets.VBox(items))
AppLayout(header=refreshButton,
          left_sidebar=show,
          center=addButton,
          right_sidebar=btn,
          footer=undo)