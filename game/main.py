from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from random import uniform


class MenuScreen(BoxLayout):
    def __init__(self, start_callback, show_score_rank_callback, show_about_callback, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10

        self.start_button = Button(text="Start Reaction Test", on_press=start_callback, font_size='70sp')
        self.start_button.background_color = (200/255, 70/255, 90/255, 1)
        self.add_widget(self.start_button)

        self.score_rank_button = Button(text="Score Rank", on_press=show_score_rank_callback, font_size='20sp')
        self.score_rank_button.background_color = (100/255, 100/255, 255/255, 1)
        self.add_widget(self.score_rank_button)

        self.about_button = Button(text="About", on_press=show_about_callback, font_size='20sp')
        self.about_button.background_color = (100/255, 100/255, 255/255, 1)
        self.add_widget(self.about_button)

class ReactionTimeGame(BoxLayout):
    def __init__(self, reset_callback, save_callback, back_to_menu_callback, **kwargs):
        super(ReactionTimeGame, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 0

        self.reset_callback = reset_callback
        self.save_callback = save_callback
        self.back_to_menu_callback = back_to_menu_callback
        self.reaction_times = []

        self.reaction_box = Button(text="Click me!", font_size='60sp', on_press=self.record_reaction_time)
        self.reaction_box.background_color = (1/255, 230/255, 50/255, 1)
        self.reaction_box.opacity = 0
        self.add_widget(self.reaction_box)

        self.reaction_time_label = Label(text="")
        self.add_widget(self.reaction_time_label)

        self.reset_button = Button(text="Try again", font_size='60sp', on_press=self.reset_test)
        self.reset_button.background_color = (100/255, 100/255, 255/255, 1)
        self.reset_button.opacity = 0
        self.add_widget(self.reset_button)

        self.save_button = Button(text="Save Score", font_size='20sp', on_press=self.save_score)
        self.save_button.background_color = (100/255, 100/255, 255/255, 1)
        self.save_button.opacity = 0
        self.add_widget(self.save_button)

        self.back_to_menu_button = Button(text="Back to Menu", font_size='20sp', on_press=self.back_to_menu)
        self.back_to_menu_button.background_color = (100/255, 100/255, 255/255, 1)
        self.add_widget(self.back_to_menu_button)

        self.num_attempts = 0
        self.total_reaction_time = 0

    def start_test(self, *args):
        self.reaction_box.disabled = True
        self.reaction_box.background_color = (206/255, 38/255, 54/255, 1)
        self.reaction_box.opacity = 1
        Clock.schedule_once(self.change_color, uniform(1.5, 4))

    def change_color(self, dt):
        self.reaction_box.disabled = False
        self.reaction_box.background_color = (0/255, 240/255, 100/255, 1)
        self.start_time = Clock.get_time()

    def record_reaction_time(self, instance):
        if hasattr(self, 'start_time'):
            self.reaction_box.disabled = True
            end_time = Clock.get_time()
            reaction_time = (end_time - self.start_time) * 1000
            self.reaction_time_label.text = f"{reaction_time:.0f} ms \n "
            self.reaction_time_label.font_size = '70sp'
            self.num_attempts += 1
            self.total_reaction_time += reaction_time
            if self.num_attempts < 5:
                Clock.schedule_once(self.start_test)
            else:
                self.display_average_reaction_time()

    def display_average_reaction_time(self):
        average_reaction_time = self.total_reaction_time / self.num_attempts
        self.reaction_time_label.text = f"Average Reaction Time: {average_reaction_time:.0f} ms"
        self.reaction_time_label.font_size = '40sp'
        self.reset_button.opacity = 1
        self.save_button.opacity = 1
        self.reaction_times.append(average_reaction_time)

    def reset_test(self, instance):
        self.reaction_box.disabled = False
        self.reaction_time_label.text = ""
        self.num_attempts = 0
        self.total_reaction_time = 0
        self.reset_button.opacity = 0
        self.save_button.opacity = 0
        self.reset_callback()

    def save_score(self, instance):
        self.save_callback(instance)

    def back_to_menu(self, instance):
        self.back_to_menu_callback()

class ReactionTimeTestApp(App):
    def build(self):
        self.menu_screen = MenuScreen(
            start_callback=self.start_game,
            show_score_rank_callback=self.show_score_rank,
            show_about_callback=self.show_about
        )
        return self.menu_screen

    def start_game(self, instance):
        self.game_screen = ReactionTimeGame(
            reset_callback=self.reset_game,
            save_callback=self.save_score,
            back_to_menu_callback=self.back_to_menu
        )
        self.menu_screen.clear_widgets()
        self.menu_screen.add_widget(self.game_screen)
        self.game_screen.start_test()

    def reset_game(self):
        self.menu_screen.clear_widgets()
        self.menu_screen.add_widget(MenuScreen(
            start_callback=self.start_game,
            show_score_rank_callback=self.show_score_rank,
            show_about_callback=self.show_about
        ))

    def save_score(self, instance):
        if hasattr(self, 'game_screen') and isinstance(self.game_screen, ReactionTimeGame):
            self.game_screen.save_score(instance)

    def back_to_menu(self):
        self.menu_screen.clear_widgets()
        self.menu_screen.add_widget(MenuScreen(
            start_callback=self.start_game,
            show_score_rank_callback=self.show_score_rank,
            show_about_callback=self.show_about
        ))

    def show_score_rank(self, instance):
        # รอใส่ฟังก์ชั่น
        pass

    def show_about(self, instance):
        # รอใส่ฟังก์ชั่น
        pass


if __name__ == '__main__':
    ReactionTimeTestApp().run()
