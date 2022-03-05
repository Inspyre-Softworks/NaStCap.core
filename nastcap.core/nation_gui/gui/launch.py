#!/usr/bin/env python3

import PySimpleGUI as psg
from nation_gui.gui import nation_lookup_failed_popup
from nation_gui.helpers import Nation, Region
from nation_gui.gui.nation import NationWindow

from nation_gui.logger import ISL

LOG_DEV = ISL.device
LOG_NAME = 'gui.launch'

ROOT_LOG = LOG_DEV.add_child(LOG_NAME)

ROOT_LOG.debug('Imported!')


def not_empty(*args):
    if not 'window_obj' in args:
        raise


class LaunchWindow(object) :
    
    def hide_button(self, key_prefix):
        key_prefix = key_prefix.upper()
        btn_suffix = '_BUTTON'
        if not key_prefix.endswith(btn_suffix):
            key = key_prefix + btn_suffix
        else:
            key = key_prefix
            
        self.window[key].update(visible=False)
        
        
    def show_button(self, key_prefix):
        key_prefix = key_prefix.upper()
        btn_suffix = '_BUTTON'
        if not key_prefix.endswith(btn_suffix):
            key = key_prefix + btn_suffix
        else:
            key = key_prefix
            
        self.window[key].update(visible=True)


    def disable_button(self, key_prefix) :
        key_prefix = key_prefix.upper()
        btn_suffix = '_BUTTON'
        if not key_prefix.endswith(btn_suffix) :
            key = key_prefix + btn_suffix
        else :
            key = key_prefix
    
        self.window[key].update(disabled=True)


    def enable_button(self, key_prefix) :
        key_prefix = key_prefix.upper()
        btn_suffix = '_BUTTON'
        if not key_prefix.endswith(btn_suffix) :
            key = key_prefix + btn_suffix
        else :
            key = key_prefix
    
        self.window[key].update(disabled=False)
    
    
    def __init__(self) :
        
        ## Do logger stuff
        self.log_name = LOG_NAME + '.LaunchWindow'
        
        self.log = LOG_DEV.add_child(self.log_name)
        
        self.log.debug(f'Logger started for {self.log_name}')
        ## End initial logging stuff
        
        # Assemble some layout structures
        self.layout1 = [
                [
                        psg.Button('Login', key='LOGIN_BUTTON', enable_events=True),
                        psg.Button('Browse Unprivileged', key='CONTINUE_BUTTON', enable_events=True)
                        ]
                ]
        
        self.layout2 = [
                [
                        psg.Text('Nation Name:'),
                        psg.InputText(
                            '',
                            key='NATION_NAME_INPUT',
                            tooltip='The name of the nation you would like to log-in as',
                            enable_events=True
                            )
                        ],
                [
                        psg.Text('Password:'),
                        psg.InputText(
                            '',
                            key='NATION_PASSWORD_INPUT',
                            password_char='*',
                            tooltip='The password for the account you are trying to access',
                            enable_events=True
                            )
                        ],
                [
                        psg.Button('Log In', key='NATION_LOGIN_BUTTON', enable_events=True, disabled=True)
                        ]
                ]
        
        self.layout3 = [
                               [
                                       psg.Text('Nation Name:'),
                                       psg.InputText(
                                               '',
                                               key='BROWSE_NAME_INPUT',
                                               tooltip='The name of the nation you would like to lookup',
                                               enable_events=True
                                               )
                                       ],
                               [
                                       psg.Button(
                                               'Lookup',
                                               key='LOOKUP_BUTTON',
                                               disabled=True,
                                               enable_events=True
                                               )
                                       ]
                               ]
        self.layout4 = [
                [psg.VerticalSeparator(),
                 psg.Text('Please wait.'),
                 psg.VerticalSeparator()]
                ]
        
        
        self.running = False
        self.log.debug("Set window running flag to False.")
        
        
        self.layout = [
                [
                        psg.Column(self.layout1, key='COL1'),
                        psg.Column(self.layout2, visible=False, key='COL2'),
                        psg.Column(self.layout3, visible=False, key='COL3'),
                        psg.Column(self.layout4, visible=False, key='COL4')
                        ],
                [
                        psg.Button('Go Back', key='GO_BACK_BUTTON', visible=False),
                        psg.Button('Quit', key='QUIT_BUTTON')
        
                        ]
                ]
        self.window = psg.Window('nsOracle', layout=self.layout, no_titlebar=True, grab_anywhere=True,
                                 return_keyboard_events=True,
                                 force_toplevel=True)
        self.active_layout = 1
        self.log.debug(f"Set current active layout to: {self.active_layout}")
    
    
    def run(self) :
        self.running = True
        self.log.debug("Running!")
        self.hidden = False
        while self.running :
            event, vals = self.window.read(timeout=100)
            
            if event is None :
                self.window.close()
                self.running = False
                break
                
            if event == 'QUIT_BUTTON':
                self.running = False
                self.window.close()
                break
                
            if event == 'CONTINUE_BUTTON':
                self.active_layout = 3
                self.window.bind('<Return>', 'LOOKUP_BUTTON')
                
                
            if event == 'LOGIN_BUTTON':
                self.active_layout = 2
                
                
            if event == 'GO_BACK_BUTTON':
                self.active_layout = 1
                
            if self.active_layout >= 2:
                self.window['GO_BACK_BUTTON'].update(visible=True)
                self.show_button('LOGIN')
            else:
                self.window['GO_BACK_BUTTON'].update(visible=False)
            
            if event == 'LOOKUP_BUTTON':
                self.active_layout = 4
                self.window.hide()
                nation = Nation(vals['BROWSE_NAME_INPUT'])
                nw = NationWindow(nation)
                nw.run()
                self.active_layout = 3
                self.window['BROWSE_NAME_INPUT'].update('')
                self.window.un_hide()
                
                
                
            if event == 'BROWSE_NAME_INPUT':
                if not vals['BROWSE_NAME_INPUT'].replace(' ', '') == '':
                    self.window['LOOKUP_BUTTON'].update(disabled=False)
                else:
                    self.window['LOOKUP_BUTTON'].update(disabled=True)
            
            login_fields = ['NATION_NAME_INPUT', 'NATION_PASSWORD_INPUT']
            
            
            if event in login_fields:
                has_value = []
                print(dir(self.window['NATION_NAME_INPUT']))
                for field in login_fields:
                    if vals[field] != '':
                        has_value.append(field)
                if len(has_value) >= 2:
                    self.enable_button('NATION_LOGIN')
                    self.window.bind('<Return>', 'NATION_LOGIN_BUTTON')
                else:
                    self.disable_button('NATION_LOGIN')
                    
            nation = None
            if event == 'NATION_LOGIN_BUTTON':
                self.active_layout = 4
                try:
                    self.window.hide()
                    nation = Nation(vals['NATION_NAME_INPUT'], vals['NATION_PASSWORD_INPUT'])
                    
                except:
                    self.log.error('Failed to login!')
                    nation_lookup_failed_popup(vals['NATION_NAME_INPUT'], message='Access denied!')
                    self.active_layout = 2
                    self.window.bring_to_front()

                nw = NationWindow(nation)
                nw.run()
                self.active_layout = 1
                self.window.un_hide()
                
            
            if 'timeout' not in event.lower():
                print(event)
            
            layout_num = 4
            
            for num in range(4):
                key = str(f'COL{num + 1}')
    
                if self.active_layout == num + 1:
                    self.window[key].update(visible=True)
                else:
                    self.window[key].update(visible=False)
                    
            #
            # if self.active_layout == 1:
            #     self.window['COL1'].update(visible=True)
            #     self.window['COL2'].update(visible=False)
            #     self.window['COL3'].update(visible=False)
            #     self.window['COL4'].update(visible=False)
            #
            # elif self.active_layout == 2:
            #     self.window['COL1'].update(visible=False)
            #     self.window['COL2'].update(visible=True)
            #     self.window['COL3'].update(visible=False)
            #     self.window['COL4'].update(visible=False)
            #
            # elif self.active_layout == 3:
            #     self.window['COL1'].update(visible=False)
            #     self.window['COL2'].update(visible=False)
            #     self.window['COL3'].update(visible=True)
            #     self.window['COL4'].update(visible=False)
            #
            # elif self.activ_layout == 4:
            #     self.window['COL1'].update(visible=False)
            #     self.window['COL2'].update(visible=False)
            #     self.window['COL3'].update(visible=False)
            #     self.window['COL4'].update(visible=True)
