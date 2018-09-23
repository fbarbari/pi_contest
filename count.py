from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.animation import Animation

TIME = 60


class DownClock(Label):
    a = NumericProperty()  # seconds

    running = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_seconds = TIME
        self.demo = False
        self.reset()

    def reset(self, demo=False):
        Animation.cancel_all(self)  # stop any current animations
        self.a = float(self.num_seconds)
        self.demo = demo
        if demo:
            duration = 60 * 60 * 24
        else:
            duration = self.num_seconds
        self.anim = Animation(a=0, duration=duration)
        if not demo:
            self.anim.bind(on_complete=self.finish_callback)
        self.running = False

    def start(self):
        self.reset(self.demo)
        if not self.demo:
            self.anim.start(self)
        self.running = True

    def on_a(self, instance, value):
        self.text = str(round(value, 1))

    def finish_callback(animation, *args):
        animation.running = False
        animation.text = "FINISH"
        App.get_running_app().time_end()
