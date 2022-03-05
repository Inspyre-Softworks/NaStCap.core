import PySimpleGUI as psg
from inspyre_toolbox.humanize import Numerical
from nation_gui.helpers.tools import download_image

from nation_gui.gui.issues import IssueWindow

from box import Box

from time import sleep


class NationWindow(object):
    def __init__(self, nation_obj):
        self.layout = []

        print(nation_obj.shards)

        self.frame_layout = []
        
        self.window_title = f'Nation View | {nation_obj.full_name}'
        #
        # for val in nation_obj.shards.keys():
        #     row = [psg.Text(val), psg.InputText(nation_obj.shards[val], readonly=True, key=f'{val.upper()}_OUTPUT')]
        #     self.frame_layout.append(row)
        #
        # self.layout.append([psg.Frame('Nation Information',layout=self.frame_layout,)])
        
        self.layout = []

        self.nation = nation_obj
        
        self.layout_top_banner = [
                [psg.Text(self.nation.full_name, expand_y=True)],
                [psg.Text(self.nation.motto)]
        ]
        
        self.layout.append([psg.Frame('', self.layout_top_banner, element_justification='center', expand_y=True, expand_x=True,)])
        self.layout.append([psg.Text(self.nation.category), psg.Text(f'Pop: {self.nation.population}')])
        
        self.button_row = [
                [
                        psg.Button('Quit', enable_events=True, key='QUIT_BUTTON'),
                        psg.Button('Find Another Nation', enable_events=True, key='FIND_NEW_BUTTON'),
                        psg.Button('Refresh Info', enable_events=True, key='REFRESH_BUTTON')
                        ]
                ]

        self.nation.shards = Box(self.nation.nation.get_shards(full_response=True))

        if self.nation.nation.is_auth:
            self.button_row[0].append(psg.Button('Issues', enable_events=True, key='ISSUES_BUTTON'))
        
        self.layout.append(self.button_row)
        
        self.window = psg.Window(self.window_title, layout=self.layout, grab_anywhere=True)
        
        self.running = False

        
    def clean_exit(self):
        if self.running:
            self.running = False
            self.window.close()
        
        
    def run(self):
        if not self.running:
            self.running = True
        
        acc = None
        
        while self.running:
            event, vals = self.window.read(timeout=100)
            
            if event is None:
                print('User most likely pressed the "X" button in the corner.')
                self.clean_exit()
                break
                
            if event == 'QUIT_BUTTON':
                print('Quit button pressed!')
                self.clean_exit()
                break
                
            if event == 'ISSUES_BUTTON':
                self.window.hide()
                acc = 0
                iw = IssueWindow(self.nation.issues)
                iw.run()

                
            if event == 'FIND_NEW_BUTTON':
                self.window.close()
                break
                
            
            if acc is not None:
                print(acc)
                if acc >= 100:
                    self.window.un_hide()
                    acc = None
                else:
                    acc += 1
                
            if 'timeout' not in event.lower():
                print(event)
