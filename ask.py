from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class AskLayout(BoxLayout):

    ask_text = StringProperty()
    string_right_answer = StringProperty()
    pi_and_error = StringProperty()

    answer = True
    answered = False

    right_answer = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reset(self):
        self.answer = True
        self.answered = False
        self.answer_inside = None

    def ask_coords(self, coords, demo=False):
        self.answer = False
        self.answered = False
        self.answer_inside = None
        if demo:
            self.answer = True
        print("ask_coords", coords)
        self.ask_text = "x = {:5.1f}\ny = {:5.1f}".format(
            coords[0] * 100, coords[1] * 100)

    def press_button(self, answer):
        #self.answer = True
        self.answered = True
        self.answer_inside = answer

    def right_answer(self, response):
        if response:
            self.string_right_answer = "YES"
        else:
            self.string_right_answer = "NO"

    def update_value_and_error(self, value, error):
        try:
            self.pi_and_error = "PI = {:10.8f}      ERR = {:10.8f}%".format(
                value, error)
        except BaseException:
            self.pi_and_error = "PI = {:>20s}      ERR = {:>20s}%".format(
                "-", "-")
