from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from random import uniform


class ReactionTimeTest(App):
    def build(self):
        self.start_button = Button(text="Start Test", on_press=self.start_test)
        self.start_button.background_color = (20/255, 180/255, 60/255, 1)
        self.reaction_box = Button(text="Click me!", on_press=self.record_reaction_time)
        self.reaction_box.background_color = (1/255, 150/255, 230/255, 1) 
        self.reaction_box.opacity = 0

        self.layout = BoxLayout(orientation="vertical", spacing=10)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.reaction_box)

        self.reaction_time_label = Label(text="")
        self.layout.add_widget(self.reaction_time_label)
        
        self.reset_button = Button(text = "Try again", on_press = self.reset_test)
        self.reset_button.background_color = (150/255, 100/255, 70/255, 1)
        self.reset_button.opacity = 0
        self.layout.add_widget(self.reset_button)

        self.num_attempts = 0
        self.total_reaction_time = 0

        return self.layout

    def start_test(self, instance):
        self.start_button.disabled = True
        self.reaction_box.disabled = True
        self.reaction_box.background_color = (206/255, 38/255, 54/255, 1) 
        self.reaction_box.opacity = 1 
        Clock.schedule_once(self.change_color, uniform(1.5, 4))

    def change_color(self, dt):
        self.reaction_box.disabled = False
        self.reaction_box.background_color = (1/255, 150/255, 230/255, 1) 
        self.start_time = Clock.get_time()

    def record_reaction_time(self, instance):
        if hasattr(self, 'start_time'):
            self.reaction_box.disabled = True 
            end_time = Clock.get_time()
            reaction_time = (end_time - self.start_time) * 1000
            self.reaction_time_label.text = f"{reaction_time:.0f} ms \n "
            self.num_attempts += 1
            self.total_reaction_time += reaction_time
            if self.num_attempts < 5:
                Clock.schedule_once(self.start_test, 0)
            else:
                self.display_average_reaction_time()

    def reset_test(self, *args):
        self.test_started = False
        self.time_elasped = 0
        self.reaction_box.disabled =False
        self.reaction_time_label.text = ""
        self.num_attempts = 0
        self.total_reaction_time = 0
        self.reset_button.opacity = 0

    def display_average_reaction_time(self):
        average_reaction_time = self.total_reaction_time / self.num_attempts
        self.reaction_time_label.text = f"Average Reaction Time: {average_reaction_time:.0f} ms"
        self.reset_button.opacity = 1

if __name__ == '__main__':
    ReactionTimeTest().run()