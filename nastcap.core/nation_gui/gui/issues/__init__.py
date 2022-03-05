import operator
import PySimpleGUI as psg

from nation_gui.logger import ISL


__MODULE_NAME__ = 'NationGUI.gui.issues'
__MOD_LOG__ = ISL.device.add_child(__MODULE_NAME__)


class ToggleObj(object):
    """

    An object that functions as a toggle switch that keeps track of number of state changes and binary cycles.

    """

    def __init__(self, tg1, tg2, init_state: bool = True):
        self.__toggle_dict = {True: tg1, False: tg2}
        self.__state = init_state
        self.states_held = 1
        self.cycles = 0


    @property
    def state(self):
        """

        Toggle the state and return the new value.

        Returns:
            The value of the state.

        """
        self.__state = not self.__state
        self.states_held += 1
        if self.states_held % 2 == 0:
            self.cycles += 1
        return self.__toggle_dict[self.__state]


class IssueWindow(object):
    """

    The object representing the issue selection window.

    """

    TABLE_HEADINGS = [
            'Title',
            'Author',
            'Editor',
            'ID'
            ]
    """
    The headers for the table we'll create within the window.
    """


    def make_table(self):
        """

        Unpacks issue list into a list lists of issue details for a table.

        Returns:
            table data

        """
        return [[
                issue['title'],
                issue['author'],
                issue['editor'],
                int(issue['id'])
                ] for issue in self.issues]


    def sort_table(self, cols):
        """ sort a table by multiple columns
            table: a list of lists (or tuple of tuples) where each inner list
                   represents a row
            cols:  a list (or tuple) specifying the column numbers to sort by
                   e.g. (1,0) would sort by column 1, then by column 0
        """

        table = self.table_data[1:][:]

        if self.last_sorted_by[0] == cols:
            states = {
                    'ascending' : False,
                    'descending': True
                    }

            state = states[self.last_sorted_by[1].state]
            print(state)

        else:
            self.last_sorted_by = (cols, ToggleObj('ascending', 'descending'))
            state = False

        for col in reversed(cols):
            try:
                table = sorted(table, key=operator.itemgetter(col), reverse=state)
            except Exception as e:
                psg.popup_error('Error in sort_table', 'Exception in sort_table', e)
        self.sorted_data = table
        return table


    def __init__(self, issues):

        self.issues = issues
        self.table_data = [self.TABLE_HEADINGS]
        self.data = self.make_table()
        self.sorted_data = self.data
        self.table_data.extend(
                self.data[issue_num] for issue_num in range(len(self.issues))
                )

        self.layout = [
                [
                        psg.Table(
                                values=self.table_data[1:][:],
                                headings=self.TABLE_HEADINGS,
                                max_col_width=30,
                                auto_size_columns=True,
                                justification='center',
                                num_rows=len(self.table_data),
                                alternating_row_color='darkblue',
                                key='ISSUE_TABLE',
                                enable_events=True,
                                expand_x=True,
                                expand_y=True,
                                enable_click_events=True,
                                tooltip='Issues currently awaiting your attention.'
                                )
                        ],
                [
                        psg.Text(
                                '',
                                key="ISSUE_TEXT",
                                expand_x=True,
                                expand_y=True,
                                visible=False,
                                relief=psg.RELIEF_RAISED
                                )
                        ],
                [
                        psg.Button('Read Issue', key='READ_BUTTON'), psg.Button('Go Back', key='BACK_BUTTON')
                        ]
                ]

        self.window = psg.Window('Issue Window', layout=self.layout, ttk_theme='clam', resizable=True)

        self.running = False
        """
        A flag that controls the running state of the window.
        """

        self.last_sorted_by = (None, None)


    def run(self):
        """

        Run the instance of the issue window we've created.

        """
        self.running = True
        while self.running:
            event, values = self.window.read(timeout=100)

            if isinstance(event, tuple):
                if event[0] == 'ISSUE_TABLE' and event[2][0] == -1:
                    print('Heading clicked!')
                    col_num_clicked = event[2][1]

                    new_table = self.sort_table((col_num_clicked, 0))
                    self.window['ISSUE_TABLE'].update(values=new_table)

            if event == psg.WIN_CLOSED:
                break

            if event == 'BACK_BUTTON':
                break

            if event == 'READ_BUTTON':
                print('Read button received click!')
                print(values)

            if event == 'ISSUE_TABLE':
                print(event[2])
                print(values)
                try:
                    print(self.sorted_data[values['ISSUE_TABLE'][0]])
                except IndexError:
                    pass

        self.running = False

        if not self.running:
            self.window.close()

# from nation_gui.helpers import Nation
#
#


# class IssueWindow(object):
#
#     logger_registered = False
#
#     def __get_issue_title_list(self):
#         log = ISL.device.add_child(str(__MODULE_NAME__) + '.__get_issue_title_list')
#         log.debug('Registered logging device.')
#         finds = []
#         log.debug('Getting issue titles.')
#         for issue in self.nation.issues:
#             finds.append(issue['title'])
#
#         return finds
#
#     def find_issue_by_id(self, id):
#         """
#
#         Find a nationstates issue by its ID.
#
#         Args:
#             id: The ID for the issue you'd like access to.
#
#         Returns:
#             The issue found by the ID passed as the value for 'id'.
#
#         """
#         for issue in self.nation.issues:
#             if issue.id == id:
#                 return issue
#
#
#     def __init__(self, nation_obj):
#         """
#
#         Instantiate the IssueWindow. This will handle window construction and once the object is instantiated you can
#         call the 'run' function.
#
#         Args:
#             nation_obj:
#                 An instantiated instance of 'nation_gui.
#         """
#         self.class_logger_name = str(f'{__MODULE_NAME__}.IssueWindow')
#
#         if not self.logger_registered:
#             self.log = ISL.device.add_child(self.class_logger_name)
#             self.log.debug('Registered Logging Device')
#
#
#         self.issue_select_col = []
#         self.issue_details_col = []
#
#         self.nation = nation_obj
#
#         try:
#             self.nation.issues
#         except AttributeError as e:
#             self.log.error(f"The nation object for {self.nation.full_name} contains no issue object!\n{e}")
#
#         self.layout = [
#             [psg.Text('test window')]
#         ]
#
#
#
#         self.button_keys = []
#
#         self.window = psg.Window(f'{nation_obj.full_name} Issues', layout=self.layout, resizable=True)
#
#         self.running = False
#
#
#     def run(self):
#         if not self.running:
#             self.running = True
#
#         active_issue = None
#
#         while self.running:
#             event, values = self.window(timeout=100)
#
#             if event is None:
#                 self.running = False
#                 self.window.close()
#                 break
#
#             if event.startswith('ISSUE_'):
#                 print('Issue selected!')
#
#             if 'timeout' not in event.lower():
#                 print(event)
