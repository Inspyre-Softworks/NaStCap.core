#!/usr/bin/env python3

from box import Box
import nationstates
from inspyre_toolbox.humanize import Numerical
from inspy_logger import InspyLogger

from nation_gui.config import Config

from nation_gui.gui.launch import LaunchWindow


ISL = InspyLogger('ExcitedQbit', 'debug')

prog_log = ISL.device.start()

prog_log.info('Welcome to nsOracle!')
prog_log.debug('Loggging started!')


def main():
    """
    Main entry-point for the program.
    """
    lw = LaunchWindow()
    lw.run()


if __name__ == '__main__':
    main()
