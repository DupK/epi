import tkinter.font as TkFont
import kociemba
from collections import Counter
from tkinter import *
from modules import timer, camera, clean

class Interface:

    main_parent = None
    second_parent = None
    board_parent = None
    info_parent = None
    cube_parent = None
    separator_parent = None
    link_parent = None
    link2_parent = None
    link3_parent = None
    camera_parent = None
    ui_font = None
    console_label = None
    token_label = None
    is_safe_label = None
    is_not_safe_label = None
    solve_label = None
    timer_label = None
    chrono_software = None
    chrono_robot = None
    w = None
    h = None
    faces_array = []
    rubiks = None

    def __init__(self, tk_parent):

        self.main_parent = tk_parent
        self.main_parent.geometry("1845x950")
        self.main_parent.focus_set()
        self.main_parent.resizable(width=False, height=False)
        self.main_parent.title('Epicube')
        self.second_parent = Frame(tk_parent, bg='#1B1B1B')
        self.second_parent.pack(expand=YES, fill=BOTH)
        self.cube_parent = Frame(self.second_parent, width=140, height=750, bg='#000', bd=2, relief='sunken')
        self.cube_parent.place(x=22, y=22)
        self.link_parent = Frame(self.main_parent, width=2, height=108, bg='#5B5B5B')
        self.link_parent.place(x=92, y=771)
        self.board_parent = Frame(tk_parent, width=1670, height=930, bg='#1B1B1B')
        self.board_parent.place(x=170, y=10)
        self.link2_parent = Frame(tk_parent, width=96, height=2, bg='#5B5B5B')
        self.link2_parent.place(x=92, y=879)
        self.link3_parent = Frame(tk_parent, width=379, height=2, bg='#5B5B5B')
        self.link3_parent.place(x=161, y=360)
        self.info_parent = Frame(self.board_parent, width=1635, height=100, bg='#000', bd=2, relief='sunken')
        self.info_parent.place(x=18, y=820)
        self.separator_parent = Frame(self.board_parent, width=2, height=98, bg='#2B2B2B')
        self.separator_parent.place(x=820, y=820)
        self.ui_font = TkFont.Font(family='Segoe UI Light', size=12)
        self.mini_ui_font = TkFont.Font(family='Segoe UI Light', size=10)
        self.console_label = Label(self.board_parent, text="Rubik's cube configuration", font=self.ui_font,
                                   bg='#1B1B1B', fg='#FFFFFF')
        self.console_label.place(x=18, y=790)
        self.timer_label = Label(self.board_parent, text="Measures of performance", font=self.ui_font,
                                 bg='#1B1B1B', fg='#FFFFFF')
        self.timer_label.place(x=825, y=790)
        self.camera_parent = Frame(self.board_parent, width=800, height=500, bg='#000', bd=2, relief='sunken')
        self.camera_parent.place(x=370, y=120)

    def display_cube_info(self):

        if not self.rubiks.safe():
            self.is_not_safe_label = Label(self.board_parent, text="» Rubik's cube is not solvable", font=self.mini_ui_font, bg='#3B3B3B', fg='#FF0000')
            self.is_not_safe_label.place(x=18, y=830)
            return
        else:
            self.is_safe_label = Label(self.board_parent, text="» Rubik's cube is solvable", font=self.mini_ui_font, bg='#000', fg='#00C000')
            self.is_safe_label.place(x=24, y=850)

            self.display_pattern()

            self.token_label = Label(self.board_parent, text="» " + self.rubiks.__get__(), font=self.mini_ui_font, bg="#000", fg='#FFF')
            self.token_label.place(x=24, y=830)
            self.rubiks.lock = False

    def display_pattern(self):
        i = 0
        x = 43
        y = 46
        for raw in self.rubiks.__get__():
            self.faces_array.append(
                Frame(self.second_parent, width=27, height=27, bg=(self.rubiks.correlation_table.get(raw))))
        for n in range(6):
            for a in range(9):
                self.faces_array[i].place(x=x, y=y)
                i += 1
                x += 35
                if a == 2:
                    y += 35
                    x = 43
                if a == 5:
                    y += 35
                    x = 43
            x = 43
            y += 50

    def refresh_the_display(self, instance):

        clean.destroy(True,
                      [self.faces_array,
                       self.is_not_safe_label,
                       self.is_safe_label,
                       self.token_label,
                       self.solve_label,
                       self.chrono_software,
                       self.chrono_robot])

        self.faces_array = []
        self.rubiks = instance
        self.display_cube_info()
        self.main_parent.bind("<Return>", lambda event: self.rubiks.solve())


class Cube:

    correlation_table = None
    token = None
    regex = None
    lock = True
    code = None

    def __init__(self, value=None):

        self.token = value
        self.regex = 'URFDLB'
        self.correlation_table = {'U': '#FFF000',
                                  'R': '#008000',
                                  'F': '#FF0000',
                                  'D': '#FFFFFF',
                                  'L': '#0000FF',
                                  'B': '#FFA500'}

    def __get__(self):
        return self.token

    def solve(self):

        if not self.lock:
            if not self.safe():
                return
            else:
                clean.destroy(False,
                             [ui.solve_label,
                              ui.chrono_software,
                              ui.chrono_robot])

                timer.start()
                return_code = kociemba.solve(self.__get__())
                timer.stop()

                ui.solve_label = Label(ui.board_parent, text="» " + return_code, font=ui.mini_ui_font, bg='#000', fg='#00C000')
                ui.solve_label.place(x=24, y=870)

                text = "» The algorithm has solved the Rubik's cube in " + str(round(timer.interval, 3)) + " seconds with " + str(len(return_code.split())) + ' moves'

                ui.chrono_software = Label(ui.board_parent, text=text, font=ui.mini_ui_font, bg='#000', fg='#FFFFFF')
                ui.chrono_software.place(x=827, y=830)

                timer.start()
                # SEND_TO_ROBOT()
                timer.stop()

                ui.chrono_robot = Label(ui.board_parent, text="» The robot has solved the Rubik's cube in " + str(round(timer.interval, 3)) + " seconds", font=ui.mini_ui_font, bg="#000", fg="#FFFFFF")
                ui.chrono_robot.place(x=827, y=850)

    def safe(self):
        c = Counter(self.token)
        return (set(c.keys()) == set(self.regex)) and (all(f == 9 for f in c.values()))


def instantiate(token):
    instance = Cube(token)
    ui.refresh_the_display(instance)


if __name__ == "__main__":
    root = Tk()
    ui = Interface(root)
    timer = timer.Timer()

    root.bind("<Up>", lambda event: instantiate(camera.get_token()))
    root.bind("<Escape>", lambda event: sys.exit())

    root.mainloop()
    sys.exit()
