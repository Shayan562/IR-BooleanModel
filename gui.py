"""
This has nothing of value(perspective of IR)
It only contains the layout setting for the gui
Too messy to keep in main.py
"""
import PySimpleGUI as sg
sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.

layout = [  [sg.Text("Search Engine",expand_x=True, justification=("center"))],  

            [sg.Text("Boolean Query", expand_x=True, justification=("center"), pad=((2,2),(10,0)))],  #debit section
            [sg.InputText(expand_x=True, key="-query_boolean-", do_not_clear=False , justification=("center"),  pad=((20,20),(10,10)), tooltip="In the format t1 and not t2")

                ],
            [sg.Button('Execute Boolean Query', key="-run_boolean-" , size=(26,1),pad=((50,50),(0,20)) )] ,

            [sg.Text("Proximity Query", expand_x=True, justification=("center"), pad=((2,2),(10,0)), )],
            [sg.InputText(expand_x=True, key="-query_proximity-", justification=("center"),do_not_clear=False ,  pad=((20,20),(10,10)),tooltip='In the format t1 t2 /k' )

                ],
            [sg.Button('Execute Proximity Query', key="-run_proximity-" ,size=(26,1),pad=((0,0),(0,20)) )] ,

            ]
