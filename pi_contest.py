#!/usr/bin/env python3
__version__ = "1.0"

from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.clock import Clock
from kivy.core.window import Window

import pygame

from pi_game import PiGame
from ask import AskLayout
from count import DownClock
from graph import GraphLayout
from circle import CircleLayout
from player import PlayerPopup, TemplatePopup

SLEEP = 1.0
REPEAT = 50

pi_str = chr(0x3c0)
err_str = chr(0x3b5)


class AppScreen(BoxLayout):
    pass


class HomeScreen(Screen):
    pass


class FameScreen(Screen):
    pass


class DemoScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.demo_init()
        Clock.schedule_interval(self.update, 0.5)

    def demo_init(self):
        self.pi_game = PiGame()
        self.ids.ask.update_value_and_error("-", "-")
        self.ids.countdown.reset_clock(True)
        self.ids.circle.clean()
        self.ids.graph.clean()

    def update(self, dt):
        if self.ids.countdown.ids.downclock.running:
            coords = self.pi_game.throw_coords()
            self.ids.ask.ask_coords(coords)
            self.pi_game.add()
            self.ids.ask.update_value_and_error(
                self.pi_game.value(), self.pi_game.error())
            self.ids.graph.add(self.pi_game.value())
            self.ids.circle.add(self.pi_game.coords())


class PlayScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.play_init()
        Clock.schedule_interval(self.update, 0.1)

    def play_init(self):
        print("play init of play")
        self.pi_game = PiGame()
        self.ids.ask.update_value_and_error("-", "-")
        self.ids.ask.reset()
        self.ids.countdown.reset_clock()
        self.ids.circle.clean()
        self.ids.graph.clean()

    def update(self, dt):
        if self.ids.countdown.ids.downclock.running:
            if self.ids.ask.answer and not self.ids.ask.answered:

                coords = self.pi_game.throw_coords()
                is_inside = self.pi_game.inside()

                print(">>> coords", coords)
                print(">>> inside", is_inside)

                self.ids.ask.ask_coords(coords)

            if self.ids.ask.answered:
                self.ids.ask.answer = True
                self.ids.ask.answered = False

                #self.ids.ask.right_answer(self.ids.ask.answer_inside == self.pi_game.inside())

                right_answer = self.ids.ask.answer_inside == self.pi_game.inside()

                print(">>> right?", right_answer)

                if not right_answer:
                    ErrorNumberPopup().open()
                    # time.sleep(SLEEP)

                self.pi_game.add()

                coords = self.pi_game.coords()

                if right_answer:
                    if REPEAT:
                        print("REPEAT")
                    for i in range(REPEAT):
                        self.pi_game.throw_coords()
                        self.pi_game.add()

                print(self.pi_game.value(), self.pi_game.error())

                self.ids.ask.update_value_and_error(
                    self.pi_game.value(), self.pi_game.error())
                self.ids.circle.add(coords)
                self.ids.graph.add(self.pi_game.value())


class Algorithm(BoxLayout):
    pass


class CountDown(AnchorLayout):

    def start_clock(self):
        App.get_running_app().reset()
        self.ids.downclock.start()

    def reset_clock(self, demo=False):
        self.ids.downclock.reset(demo)


class AskCoords(AskLayout):
    pass


class Circle(CircleLayout):
    pass


class Graph(GraphLayout):
    pass


class Result(BoxLayout):
    pass


class ErrorNumberPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.dismiss, 2)


class EndTimePopup(TemplatePopup):

    def __init__(self, msg, title=""):
        super().__init__()
        self.title = title
        self.ids.msg.text = msg


class JoyListener(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_joy_button_up=self.on_joy_button_up)

    def on_joy_button_up(self, win, stickid, buttonid):
        app = App.get_running_app()
        if (buttonid % 2):
            app.play.ids.ask.press_button(False)  # OUT
        else:
            app.play.ids.ask.press_button(True)  # IN


class pi_contest(App):

    icon = "figure/pi_logo.gif"

    pi_str = pi_str

    def build(self):

        pygame.init()
        try:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        except BaseException:
            print("No Joystick found")

        sm = ScreenManager(transition=WipeTransition())

        self.play = PlayScreen()
        self.demo = DemoScreen()
        self.fame = FameScreen()

        sm.add_widget(HomeScreen())
        sm.add_widget(self.demo)
        sm.add_widget(self.play)
        sm.add_widget(self.fame)

        sm.current = 'home'

        return sm

    def reset(self):
        try:
            self.play_init()
        except:
            pass
        try:
            self.demo_init()
        except:
            pass

    def play_init(self):
        self.demo.ids.countdown.reset_clock()
        self.play.play_init()

    def demo_init(self):
        self.play.ids.countdown.reset_clock()
        self.demo.demo_init()

    def update_scores(self):
        self.demo.ids.countdown.reset_clock()
        self.play.ids.countdown.reset_clock()
        self.fame.ids.list_player.text = PlayerPopup().list(True, True)

    def time_end(self):

        value = self.play.pi_game.value()
        error = self.play.pi_game.error()

        p = PlayerPopup(
            error, "{} = {}, {} = {}%".format(
                pi_str, value, err_str, error))

        pop = EndTimePopup(
            "Hai finito!\n{} = {}\n{} = {}%".format(
                pi_str,
                value,
                err_str,
                error),
            "{} Contest terminato".format(pi_str))

        pop.ids.save_button.bind(on_press=p.open)

        pop.open()


if __name__ == '__main__':
    pi_contest().run()
