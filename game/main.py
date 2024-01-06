from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from random import uniform


class ReactionTimeTest(App):
    def build(self):
        self.start_button = Button(text="Start Test", on_press=self.start_test)
        self.reaction_box = Button(text="Click me!", on_press=self.record_reaction_time)
        self.reaction_box.background_color = (43/255, 135/255, 209/255, 1)  # Set initial color to blue
        self.reaction_box.opacity = 0 

        self.layout = BoxLayout(orientation="vertical", spacing=50)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.reaction_box)

        self.reaction_time_label = Label(text="")
        self.layout.add_widget(self.reaction_time_label)

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
        self.reaction_box.background_color = (75/255, 119/255, 209/255, 1)
        self.start_time = Clock.get_time()

    def record_reaction_time(self, instance):
        if hasattr(self, 'start_time'):
            self.reaction_box.disabled = True 
            end_time = Clock.get_time()
            reaction_time = (end_time - self.start_time) * 1000
            self.reaction_time_label.text = f"{reaction_time:.2f} ms \n "
            self.num_attempts += 1
            self.total_reaction_time += reaction_time
            if self.num_attempts < 5:
                Clock.schedule_once(self.start_test, 0)
            else:
                self.display_average_reaction_time()

    def reset_test(self):
        self.start_button.disabled = False
        self.reaction_box.opacity = 0
        self.reaction_time_label.text = ""
        self.num_attempts = 0
        self.total_reaction_time = 0

    def display_average_reaction_time(self):
        average_reaction_time = self.total_reaction_time / self.num_attempts
        self.reaction_time_label.text = f"Average Reaction Time: {average_reaction_time:.2f} ms"


if __name__ == '__main__':
    ReactionTimeTest().run()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from random import uniform


class ReactionTimeTest(App):
    def build(self):
        self.start_button = Button(text="Start Test", on_press=self.start_test)
        self.reaction_box = Button(text="Click me!", on_press=self.record_reaction_time)
        self.reaction_box.background_color = (43/255, 135/255, 209/255, 1)  # Set initial color to blue
        self.reaction_box.opacity = 0  # Make it invisible initially

        self.layout = BoxLayout(orientation="vertical", spacing=50)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.reaction_box)

        self.reaction_time_label = Label(text="")
        self.layout.add_widget(self.reaction_time_label)

        self.num_attempts = 0
        self.total_reaction_time = 0

        return self.layout

    def start_test(self, instance):
        self.start_button.disabled = True
        self.reaction_box.disabled = True  # Disable the box during the waiting period
        self.reaction_box.background_color = (206/255, 38/255, 54/255, 1)  # Change color to red
        self.reaction_box.opacity = 1  # Make it visible
        Clock.schedule_once(self.change_color, uniform(1.5, 4))  # Random delay between 1 and 3 seconds

    def change_color(self, dt):
        self.reaction_box.disabled = False  # Enable the box
        self.reaction_box.background_color = (75/255, 119/255, 209/255, 1)  # Change