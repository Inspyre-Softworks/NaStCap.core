import PySimpleGUI as psg


class ResolveIssueWindow(object):
    
    
    def __init__(self, issue_obj):
        """
        
        Instantiate a window with an issue, and it's text and options with buttons to select the resolution.
        
        Args:
            issue_obj (dict): The 'nation.issues' object.
        """
        self.issue = issue_obj
        
        issue_frame = [[psg.Text(self.issue.text, size=(30, 5))]]
        opts_layout = []
        
        for option in self.issue['option']:
            row1 = [
                    psg.Text(
                            option['text'],
                            key=f'{option.id}_OPT_TXT',
                            justification=psg.TEXT_LOCATION_CENTER,
                            size=(30, 15)
                            )
                    ]
            
            row2 = [
                    psg.Button(
                            'Select',
                            enable_events=True,
                            key=f'{option.id}_OPT_SEL',
                            size=(5, 5)
                            )
                    ]
            
            opts_layout.append(row1)
            opts_layout.append(row2)
        
        self.layout = [
                [
                        psg.Frame(
                                title=self.issue.title,
                                layout=issue_frame
                                )
                        ],
                [
                        psg.Frame(
                                title='',
                                layout=opts_layout,
                                )
                        ]
                ]
        
        self.window = psg.Window(
                self.issue['title'],
                layout=self.layout,
                grab_anywhere=True,
                auto_size_buttons=True
                )
        
        self.running = False
    
    
    def run(self):
        self.running = True
        
        while self.running:
            
            event, values = self.window.read(timeout=100)
            
            if event is None:
                self.running = False
                self.window.close()
                break
            
            if 'timeout' not in event.lower():
                print(event)
