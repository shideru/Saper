#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import tkinter

window = tkinter.Tk()
window.title("Main Saper")


#def button_one():
#    os.system('/home/lea/PSWMI/PriSap.py')
def button_two():
    os.system('/home/lea/PSWMI/vw_saper.py')
def button_three():
    os.system('/home/lea/PSWMI/vw_saper_zb.py')
#def button_four():
#   os.system('/home/lea/PSWMI/Subproject_BSF.py')


#Button_1 = tkinter.Button(window, text="Find path to bombs by AStar", command=button_one, font=('Verdana', 24, 'bold'))
#Button_1.pack()
Button_2 = tkinter.Button(window, text="Find bomb with Wabbit", command=button_two, font=('Verdana', 24, 'bold'))
Button_2.pack()
Button_3 = tkinter.Button(window, text="Defuse by cutting the right cables", command=button_three, font=('Verdana', 24, 'bold'))
Button_3.pack()
#Button_4 = tkinter.Button(window, text="Defuse by reading the code", command=button_four, font=('Verdana', 24, 'bold'))
#Button_4.pack()

window.mainloop()