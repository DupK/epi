from tkinter import *
import tkinter.font as TkFont
from collections import Counter
import kociemba
import sys
import time


class Timer:
    def start(self):
        if hasattr(self, 'interval'):
            del self.interval
        self.start_time = time.time()

    def stop(self):
        if hasattr(self, 'start_time'):
            self.interval = time.time() - self.start_time
            del self.start_time


class UserInterface:
    """
    UserInterface initialise l'interface de base,
    affiche les configurations liées au Rubik's Cube
    et bind les méthodes.

    """

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
    res_software_label = None
    res_robot_label = None
    w = None
    h = None
    faces_array = []
    rubiks = None

    def __init__(self, tk_parent):

        """ Initialisation de Tk """

        self.main_parent = tk_parent

        self.main_parent.geometry("1845x950")
        self.main_parent.focus_set()

        self.main_parent.resizable(width=False, height=False)
        self.main_parent.title('Epicube')

        """ Initialisation des Frames """

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

        """ Initialisation des Fonts """

        self.ui_font = TkFont.Font(family='Segoe UI Light', size=12)
        self.mini_ui_font = TkFont.Font(family='Segoe UI Light', size=10)

        """ Initialisation des Labels """

        self.console_label = Label(self.board_parent, text="Rubik's cube configuration", font=self.ui_font,
                                   bg='#1B1B1B', fg='#FFFFFF')
        self.console_label.place(x=18, y=790)

        self.timer_label = Label(self.board_parent, text="Measures of performance", font=self.ui_font,
                                 bg='#1B1B1B', fg='#FFFFFF')
        self.timer_label.place(x=825, y=790)

        """ Initialisation des Frames (webcam) """

        self.camera_parent = Frame(self.board_parent, width=800, height=500, bg='#000', bd=2, relief='sunken')
        self.camera_parent.place(x=370, y=120)

    def draw(self):

        """ Gestion d'erreurs """

        if not self.rubiks.safe():
            self.is_not_safe_label = Label(self.board_parent, text="» Rubik's cube is not solvable",
                                           font=self.mini_ui_font,
                                           bg='#3B3B3B', fg='#FF0000')
            self.is_not_safe_label.place(x=18, y=830)
            return
        else:
            self.is_safe_label = Label(self.board_parent, text="» Rubik's cube is solvable", font=self.mini_ui_font,
                                       bg='#000', fg='#00C000')
            self.is_safe_label.place(x=24, y=850)

            """ Affichage du cube """

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

            """ Affichage du token """

            self.token_label = Label(self.board_parent, text="» " + self.rubiks.__get__(), font=self.mini_ui_font,
                                     bg="#000", fg='#FFF')
            self.token_label.place(x=24, y=830)
            self.rubiks.lock_solving = False

    def update(self, instance):

        """ Clean up """

        if self.faces_array is not None:
            if len(self.faces_array) != 0:
                for n in range(54):
                    self.faces_array[n].destroy()
        if self.is_not_safe_label is not None:
            self.is_not_safe_label.destroy()
        if self.is_safe_label is not None:
            self.is_safe_label.destroy()
        if self.token_label is not None:
            self.token_label.destroy()
        if self.solve_label is not None:
            self.solve_label.destroy()
        if self.res_software_label is not None:
            self.res_software_label.destroy()
        if self.res_robot_label is not None:
            self.res_robot_label.destroy()

        """ Update """

        self.faces_array = []
        self.rubiks = instance
        self.draw()
        self.main_parent.bind("<Return>", lambda event: self.rubiks.solve())


class RubiksCube:
    """
    Rubik's Cube gère l'ensemble des fonctionalitées
    propre à la réalisation d'un rubik's cube.
    (vérifier sa solvabilitée et le résoudre).

    """
    correlation_table = None
    instruction_table = None
    token = None
    regex = None
    lock_solving = True
    return_code = None

    def __init__(self, value=None):

        """ Initialisation des variables """

        self.correlation_table = {'U': '#FFF000',
                                  'R': '#008000',
                                  'F': '#FF0000',
                                  'D': '#FFFFFF',
                                  'L': '#0000FF',
                                  'B': '#FFA500'}

        self.instruction_table = {"U": "Turn the face (U) to the right (90°)",
                                  "R": "Turn the face (R) to the right (90°)",
                                  "F": "Turn the face (F) to the right (90°)",
                                  "D": "Turn the face (D) to the right (90°)",
                                  "L": "Turn the face (L) to the right (90°)",
                                  "B": "Turn the face (B) to the right (90°)",
                                  "U'": "Turn the face (U) in the counterclockwise direction (90°)",
                                  "R'": "Turn the face (R) in the counterclockwise direction (90°)",
                                  "F'": "Turn the face (F) in the counterclockwise direction (90°)",
                                  "D'": "Turn the face (D) in the counterclockwise direction (90°)",
                                  "L'": "Turn the face (L) in the counterclockwise direction (90°)",
                                  "B'": "Turn the face (B) in the counterclockwise direction (90°)",
                                  "U2": "Turn the face (U) (180°)",
                                  "R2": "Turn the face (U) (180°)",
                                  "F2": "Turn the face (U) (180°)",
                                  "D2": "Turn the face (U) (180°)",
                                  "L2": "Turn the face (U) (180°)",
                                  "B2": "Turn the face (U) (180°)"}

        self.token = value

        self.regex = 'URFDLB'

    def __get__(self):
        return self.token

    def __del__(self):
        print('\n[!] Object add to garbage collector')

    def solve(self):

        """ Si le cube est affiché """

        if not self.lock_solving:

            """ Et qu'il est solvable """

            if not self.safe():
                return
            else:

                """ Néttoyage d'un potentiel cube """

                if ui.solve_label is not None:
                    ui.solve_label.destroy()
                if ui.res_software_label is not None:
                    ui.res_software_label.destroy()
                if ui.res_robot_label is not None:
                    ui.res_robot_label.destroy()

                """ Résolution software """

                timer.start()
                return_code = kociemba.solve(self.__get__())
                timer.stop()

                len(return_code.split())

                ui.solve_label = Label(ui.board_parent, text="» " + return_code,
                                       font=ui.mini_ui_font,
                                       bg='#000', fg='#00C000')
                ui.solve_label.place(x=24, y=870)
                ui.res_software_label = Label(ui.board_parent,
                                              text="» The algorithm has solved the Rubik's cube in " + str(
                                                  round(timer.interval, 3)) + " seconds with " + str(
                                                  len(return_code.split())) + ' moves',
                                              font=ui.mini_ui_font,
                                              bg='#000',
                                              fg='#FFFFFF')
                ui.res_software_label.place(x=827, y=830)

                """ Résolution hardware """

                timer.start()
                # SEND_TO_ROBOT()
                timer.stop()

                ui.res_robot_label = Label(ui.board_parent, text="» The robot has solved the Rubik's cube in " + str(
                    round(timer.interval, 3)) + " seconds", font=ui.mini_ui_font, bg="#000", fg="#FFFFFF")
                ui.res_robot_label.place(x=827, y=850)

    def safe(self):
        c = Counter(self.token)
        return (set(c.keys()) == set(self.regex)) and (all(f == 9 for f in c.values()))


def NewInstance(token):
    instance = RubiksCube(token)
    ui.update(instance)


def GetReturnCamera():

    return 'FLBUULFFLFDURRDBUBUUDDFFBRDDBLRDRFLLRLRULFUDRRBDBBBUFL'


if __name__ == "__main__":
    root = Tk()
    ui = UserInterface(root)
    timer = Timer()

    root.bind("<Up>", lambda event: NewInstance(GetReturnCamera()))
    root.bind("<Escape>", lambda event: sys.exit())

    root.mainloop()
    sys.exit()
