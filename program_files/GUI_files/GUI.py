# -*- coding: utf-8 -*-
from datetime import datetime
from tkinter import *
from tkinter import ttk
import subprocess
import os
import csv
from program_files.preprocessing.Spreadsheet_Energy_System_Model_Generator \
    import \
    sesmg_main
from program_files.GUI_files.urban_district_upscaling_GUI \
    import UpscalingFrameClass
from program_files.GUI_files.MethodsGUI import MethodsGUI
import \
    program_files.postprocessing.merge_partial_results as merge_partial_results
import program_files.postprocessing.plotting as plotting
from program_files.preprocessing.create_energy_system import import_scenario
from program_files.Demo_Tool import demo_tool


def save_settings(gui_variables: dict):
    """
        Method that stores the settings entered in the GUI in a csv file
        in program_files/technical_data.

        :param gui_variables: dictionary holding the settings chosen in
            GUI
        :type gui_variables: dict

    """
    dict_to_save = {}
    # remove variable handling from tkinter
    for key, value in gui_variables.items():
        dict_to_save.update({key: value.get()})
    # store extracted variables to csv file
    with open('program_files/technical_data/gui_settings.csv', 'w',
              newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dict_to_save.items():
            writer.writerow([key, value])


def reload_settings(gui_variables: dict):
    """
        Method that loads the settings saved in the csv file and then
        embeds them in the GUI.

        :param gui_variables: dictionary holding the GUI settings
        :type gui_variables: dict
        :return: **gui_variables** (dict) - updated dictionary holding \
            GUI settings
    """
    
    with open(os.path.dirname(os.path.dirname(os.path.join(__file__)))
              + "/technical_data/" + 'gui_settings.csv') \
            as csv_file:
        reader = csv.reader(csv_file)
        dict_to_reload = dict(reader)
    for key, value in dict_to_reload.items():
        gui_variables[key].set(value)
    return gui_variables


class GUI(MethodsGUI):
    """
        This class is used to create the Graphical User Interface
        (GUI). In this context, it uses the methods of the
        superclass MethodsGUI.
    """
    frames = []
    gui_variables = {}
    
    def __init__(self):
        # initialize super class to create an empty tk frame
        super().__init__(
                "SESMG - Spreadsheet Energy System Model Generator",
                "0.x",
                "1200x1050")
        global tab_control
        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill='both')
        tab_control.pressed_index = None
        self.frames.append(ttk.Frame(self))
        tab_control.add(self.frames[-1], text="Demo Tool")

        # ##############
        # # DEMO Frame #
        # ##############
        demo_tool.demo_frame_class(self.frames[0], self)
        # add picture
        if sys.platform.startswith("win"):
            img = PhotoImage(
                file='program_files/Demo_Tool/v0.0.6_demo_scenario/DEMO_System.png')
        else:
            img = PhotoImage(file=os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
                                  + '/Demo_Tool/v0.0.6_demo_scenario/DEMO_System.png')
        img = img.subsample(2, 2)
        lab = Label(master=self.frames[2], image=img) \
            .grid(column=0, columnspan=4, row=22, rowspan=40)

        self.mainloop()
