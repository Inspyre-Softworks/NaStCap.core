import PySimpleGUI as psg

from nation_gui.gui.icons import ALERT_ICON, ALERT_ICON_24

def nation_not_found_popup(nation_name:str):
    """
    
    Produce a pop-up warning the end-user that the lookup was unable to find a nation with a matching name.
    
    Args:
        nation_name (str): The string

    Returns:

    """
    pu_title = f'Nation Not Found | "{nation_name}"'
    
    alerting = False
    
    layout = [
            [
                    psg.Image(data=ALERT_ICON),
                    psg.VerticalSeparator(),
                    psg.Text(f'Could not find a nation with the name: "{nation_name}" ')
                    
                    ],
            
            [
                    psg.VerticalSeparator(),
                    psg.Button('OK', key='OK_BUTTON', enable_events=True, bind_return_key=True, expand_x=True),
                    psg.VerticalSeparator()
                    ]
            
            ]
    
    window = psg.Window(title=pu_title, layout=layout, icon=ALERT_ICON_24,)
    
    alerting = True
    
    while alerting:
        
        event, values = window.read(timeout=100)
        
        if event is None:
            alerting = False
            
        
        if event == 'OK_BUTTON':
            alerting = False
            
            
    window.close()
    
    

def nation_lookup_failed_popup(attempted_query:str, message:str=None) -> None:
    """
    
    Produce a pop-up warning the end-user that the lookup they just attempted has failed.
    
    Args:
        attempted_query: The name of the nation you attempted to lookup.
        
        message:
            A custom message to deliver with the pop-up.
            
            Note:
                The default message that will display is; 'Lookup for <attempted_query> failed. Please try your query again.'
                

    Returns:

    """
    pu_title = f'Nation Lookup Failed | "{attempted_query}"'
    default_msg = f'Lookup for "{attempted_query}" failed. Please try your query again.'
    pu_message = (default_msg if message is None else message)
    
    psg.PopupError('Nation Lookup Failed.', image=ALERT_ICON, line_width=200)
    
