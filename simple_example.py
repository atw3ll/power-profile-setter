#!/usr/bin/env python3 
import gi
import subprocess
import os
gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

switch = {
        1:'power-saver',
        2:'balanced',
        3:'performance'
        }

option = list(switch.values()).index(subprocess.check_output("powerprofilesctl get", shell=True).strip().decode()) + 1
# print(list(switch.values()).index("performance"))
# subprocess.call(["/usr/bin/bash", "-c", "powerprofilesctl get | xargs echo -n"])
'''
print(
        subprocess.check_output("powerprofilesctl get", shell=True).strip().decode()
        )
        '''


def on_activate(app):
    # print("sdadasd")
    global label
    global win
    win = Gtk.ApplicationWindow(application=app, resizable=False)

    eck = Gtk.EventControllerKey()
    eck.connect('key-pressed', getInput)
    win.add_controller(eck)

    slider = Gtk.Scale()
    slider.set_digits(0)
    slider.set_range(1, 3)
    slider.set_draw_value(True)
    slider.set_value(option)
    slider.connect('value-changed', slider_changed)

    label = Gtk.Label(label="Set power profile.")
    # label_2 = Gtk.Label(label=subprocess.check_output("loginctl session-status", shell=True).strip().decode())
    
    box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    win.set_child(box1)

    box1.append(slider)
    box1.append(label)
    # box1.append(label_2)
    win.set_default_size(400, 100)
    win.present()
    win.connect('close-request', custom_quit)

def getInput(event_controller, keyval, keycode, state):
    if keyval == 65307:
        win.emit('close-request')

def slider_changed(slider):
    global option
    global label
    option = int(slider.get_value())
    label.set_text(switch.get(option))

def custom_quit(e):
    subprocess.call(["/usr/bin/powerprofilesctl", "set", switch.get(option)])
    e.close()

app = Gtk.Application()
app.connect('activate', on_activate)
app.run()
