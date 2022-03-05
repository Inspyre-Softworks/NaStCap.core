from configparser import ConfigParser
import os
from pathlib import Path

DEFAULT_APP_DATA_DIR = Path('~/Inspyre-Softworks/NatStaG').expanduser()
"""
The default location recommended by the developer for
application data files.
"""

DEFAULT_CONF_PATH = DEFAULT_APP_DATA_DIR.joinpath('/config/config.ini')
"""
The default location recommended by the developer for application
configuration files.
"""


class DefaultConfig(object):
    def __init__(self):
        """
        
        Contains the default configuration and it's default option values
        'for new  installations of NatStaG.
        
        """
        self.parser = ConfigParser()
        dparser = self.parser['DEFAULT']
        dparser.setdefault('theme', 'DarkAmber')
        dparser.setdefault('master-password', '')
        dparser.setdefault('remember-me', 'false')
        dparser.setdefault('remember-nation-names', 'false')
        dparser.setdefault('watching', '[]')
        dparser.setdefault('app-data-dir', str(DEFAULT_APP_DATA_DIR))
        dparser.setdefault('save-issue-info', 'false')


class Config(object):
    
    def construct(self):
        """
        
        Calling this function shouldn't be necessary as another function
        internal to the class calls this function on instantiation.
        
        Returns:
            None

        """
        
        if not self.config_fp.exists():
            if str(self.config_fp).endswith('.ini'):
                config_fp = self.config_fp.parent
                os.makedirs(config_fp)
            else:
                os.makedirs(self.config_fp)
                self.config_fp = self.config_fp.joinpath('config.ini')
                default_config = DefaultConfig()
                self.parser = default_config.parser
                self.should_save = True
                return
        elif self.config_fp.is_dir():
            self.config_fp = self.config_fp.joinpath('config.ini')
            self.construct()
        else:
            self.parser.read(self.config_fp)
            return
    
    def save(self):
        """
        Saves the current contents of 'self.parser' and saves it to a '.ini'
        file at the location specified on instantiation.
        
        Returns:
            The path at which the configuration file was saved.

        """
        with open(self.config_fp, 'w') as fp:
            self.parser.write(fp)
            
        return self.config_fp
    
    def __init__(self, config_file_path: Path = DEFAULT_CONF_PATH):
        """
        
        Instantiate the 'Config' class for NatStaG.
        
        Args:
            config_file_path (pathlib.Path,  Optional):
                A filepath  indicating where you'd like your configuration
                file to be.
                
        Note:
            The default value for 'config_file_path' is
            <USER HOME DIR>/Inspyre-Softworks/NatStaG/config/config.ini
       
        """
        self.parser = ConfigParser()
        self.config_fp = Path(config_file_path)
        self.should_save = False
        self.construct()
        if self.should_save:
            self.save()
            self.should_save = False
