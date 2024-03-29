# การเรียกใช้เครื่องมือและ Libaries
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from random import uniform
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup


#Menu App
class MenuScreen(BoxLayout):
    def __init__(self, start_callback, show_score_rank_callback, exit_callback, show_about_callback, setting_callback,
                 volume_up_callback, volume_down_callback, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 0
        
        #Start Reaction Test
        self.start_button = Button(text="Start Reaction Test", on_press=start_callback, font_size='70sp')
        self.start_button.background_color = (200/255, 70/255, 90/255, 1)
        self.add_widget(self.start_button)

        #Score Rank
        self.score_rank_button = Button(text="Score Test", on_press=show_score_rank_callback, font_size='30sp')
        self.score_rank_button.background_color = (100/255, 100/255, 255/255, 1)
        self.add_widget(self.score_rank_button)
        
        #About
        self.about_button = Button(text="About", on_press=show_about_callback, font_size='30sp')
        self.about_button.background_color = (100/255, 100/255, 255/255, 1)
        self.add_widget(self.about_button)
        
        #Setting
        self.setting_button = Button(text="Setting", on_press=setting_callback, font_size='30sp')
        self.setting_button.background_color = (100/255, 100/255, 255/255, 1)
        self.add_widget(self.setting_button)

        #Exit
        self.exit_button = Button(text="Exit", on_press=exit_callback, font_size='30sp')
        self.exit_button.background_color = (100/255, 100/255, 5/255, 1)
        self.add_widget(self.exit_button)
        
        

        #vol up down
        self.volume_up_callback = volume_up_callback
        self.volume_down_callback = volume_down_callback
        
        

class ButtonsLayout(BoxLayout): #กล่องเล็กใน หน้า reaction test
    def __init__(self, reset_callback, save_callback, back_to_menu_callback, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = 0
        self.size_hint=(1, 0.3)
        
        #Try again
        self.reset_button = Button(text="Try again", font_size='35sp', on_press=reset_callback)
        self.reset_button.background_color = (100/255, 100/255, 255/255, 1)
        self.reset_button.opacity = 0

        #Save Score
        self.save_button = Button(text="Save Score", font_size='35sp', on_press=save_callback)
        self.save_button.background_color = (100/255, 100/255, 255/255, 1)
        self.save_button.opacity = 0

        #Back to Menu
        self.back_to_menu_button = Button(text="Back to Menu", font_size='35sp', on_press=back_to_menu_callback)
        self.back_to_menu_button.background_color = (100/255, 100/255, 255/255, 1)

        #to_screen
        self.add_widget(self.reset_button)
        self.add_widget(self.save_button)
        self.add_widget(self.back_to_menu_button)
        
# การทำงานขอว Object ที่อยู่ในหน้าเล่น reaction test
class ReactionTimeGame(BoxLayout):
    def __init__(self, reset_callback, save_callback, back_to_menu_callback, **kwargs):
        super(ReactionTimeGame, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 0

        self.reset_callback = reset_callback
        self.save_callback = save_callback
        self.back_to_menu_callback = back_to_menu_callback
        self.reaction_times = []

        self.reaction_box = Button(text="Click me!", font_size='80sp', on_press=self.record_reaction_time, 
                            size_hint=(1, 2 ))
        self.reaction_box.background_color = (1/255, 230/255, 50/255, 1)
        self.reaction_box.opacity = 0

        self.reaction_time_label = Label(text="")
        #เรียกใช้กล่องเล็ก ที่ footer ในเกมเทส
        self.buttons_layout = ButtonsLayout(
            reset_callback=self.reset_test,
            save_callback=self.save_score,
            back_to_menu_callback=self.back_to_menu    
        )

        self.add_widget(self.reaction_box)
        self.add_widget(self.reaction_time_label)
        self.add_widget(self.buttons_layout)

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
            if reaction_time >=  250:
                print('You need more practice.')
            elif 160 < reaction_time < 249 :
                print("It's good time. ")
            elif reaction_time < 160 :
                print('You are real G.O.A.T .')
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
        self.buttons_layout.reset_button.opacity = 1
        self.buttons_layout.save_button.opacity = 1
        self.reaction_times.append(average_reaction_time)

    def reset_test(self, instance):
        self.reaction_box.disabled = False
        self.reaction_time_label.text = ""
        self.num_attempts = 0
        self.total_reaction_time = 0
        self.buttons_layout.reset_button.opacity = 0
        self.buttons_layout.save_button.opacity = 0

        self.clear_widgets()

        self.add_widget(self.reaction_box)
        self.add_widget(self.reaction_time_label)
        self.add_widget(self.buttons_layout)

        Clock.schedule_once(self.start_test)

    def save_score(self, instance):
        if hasattr(App.get_running_app(), 'save_callback'):
            App.get_running_app().save_callback(instance)

    def back_to_menu(self, instance):
        self.back_to_menu_callback()

# setting ต่างของฟังก์ชั่น ใน App
class ReactionTimeTestApp(App):
    def build(self):
        
        self.title = 'God Reaction Test'
        self.icon = 'game/icon_x.png'
        
        self.sound = SoundLoader.load('GODS.mp3')
        if self.sound:
            self.sound.volume = 0.01
            self.sound.loop = True
            self.sound.play()
        else:
            print("Failed to load sound file.")
            
        self.menu_screen = MenuScreen(
            start_callback=self.start_game,
            show_score_rank_callback=self.show_score_rank,
            show_about_callback=self.show_about,
            setting_callback=self.show_setting,
            exit_callback=self.exit_game,
            volume_up_callback=self.volume_up,
            volume_down_callback=self.volume_down
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
        self.menu_screen = MenuScreen(
            start_callback=self.start_game,
            show_score_rank_callback=self.show_score_rank,
            show_about_callback=self.show_about,
            setting_callback=self.show_setting,
            exit_callback=self.exit_game,
            volume_up_callback=self.volume_up,
            volume_down_callback=self.volume_down,
            back_to_menu_callback= self.back_to_menu
        )
        
    def exit_game(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text='You wanan leave me alone T_T ?'))
    
        # pop up exit
        popup = Popup(title='Exit is crying ', content=content, size_hint=(None, None), size=(300, 200))
        popup.background_color = (0, 0.3, 0.3, 1)
        yes_button = Button(text='Yes, i did well .', on_press=lambda x: self.stop())
        yes_button.background_color = (0.8, 0.2, 0.2, 1)
        no_button = Button(text='No, i want more better !', on_press=popup.dismiss)
        no_button.background_color = (0.2, 0.8, 0.2, 1)

        content.add_widget(yes_button)
        content.add_widget(no_button)
        popup.open()

    def save_score(self, instance):
        if hasattr(self, 'game_screen') and isinstance(self.game_screen, ReactionTimeGame):
            self.game_screen.save_score(instance)

    def back_to_menu(self, instance=None):
        self.menu_screen.clear_widgets()
        self.menu_screen.add_widget(MenuScreen(
            start_callback=self.start_game,
            show_score_rank_callback=self.show_score_rank,
            exit_callback=self.exit_game,
            show_about_callback=self.show_about,
            setting_callback = self.show_setting,
            volume_up_callback=self.volume_up,
            volume_down_callback=self.volume_down,
    ))

        
    def show_score_rank(self, instance):
        if hasattr(self, 'game_screen') and isinstance(self.game_screen, ReactionTimeGame):
            reaction_times = self.game_screen.reaction_times
            if reaction_times:
                average_reaction_time = sum(reaction_times) / len(reaction_times)
                self.display_average_score(average_reaction_time)
            else:
                print("No reaction times recorded yet.")

    def display_average_score(self, average_score):
        about_layout = BoxLayout(orientation="vertical", spacing=6)
        score_label = Label(
            text=f"Score Reaction Time: {average_score:.2f} ms",
            font_size='50sp',
            halign='center',
            valign='middle',
            size_hint = (1,4)
        )
        about_layout.add_widget(score_label)

        back_to_menu_button = Button(
            text="Back to Menu",
            font_size='20sp',
            background_color=(0.8, 0.8, 0.8, 1),
            on_press=lambda x: self.back_to_menu(x)
        )
        about_layout.add_widget(back_to_menu_button)

        self.menu_screen.clear_widgets()
        self.menu_screen.add_widget(about_layout)


    def show_about(self, instance):
        about_layout = BoxLayout(orientation="vertical", spacing=0)

        about_label = Label(
            text="My Contact \n"
                "Follow me on social media for CONTENT:",
            font_size='30sp',
            halign='center',
            valign='middle'
        )
        about_layout.add_widget(about_label)

        instagram_button = Button(
            text="Instagram",
            font_size='25sp',
            background_color=(0, 0, 1, 1),
            on_press=lambda x: self.open_link("https://www.instagram.com/tng.aj/")
        )
        about_layout.add_widget(instagram_button)

        twitter_button = Button(
            text="Twitter",
            font_size='25sp',
            background_color=(0, 0.5, 1, 1),
            on_press=lambda x: self.open_link("https://twitter.com/Xhi3r")
        )
        about_layout.add_widget(twitter_button)

        github_button = Button(
            text="GitHub",
            font_size='25sp',
            background_color=(0.5, 0, 0, 1),
            on_press=lambda x: self.open_link("https://github.com/xhier2547/game_benchmark_kivy")
        )
        about_layout.add_widget(github_button)

        back_to_menu_button = Button(
            text="Back to Menu",
            font_size='20sp',
            background_color=(0.8, 0.8, 0.8, 1),
            on_press=lambda x: self.back_to_menu(x)  
        )
        about_layout.add_widget(back_to_menu_button)

        self.menu_screen.clear_widgets()
        self.menu_screen.add_widget(about_layout)


    def show_setting(self, instance):
        setting_layout = BoxLayout(orientation="vertical", spacing=0)

        setting_label = Label(
            text="- Setting -\n"
                "you can up or down of volume music hear",

            font_size='40sp',
            halign='center',
            valign='middle'
        )
        setting_layout.add_widget(setting_label)
        
        self.setting_label = Label(text=f"Volume: {self.sound.volume:.1f}", font_size='35sp', halign='center',
                                valign='middle')
        setting_layout.add_widget(self.setting_label)
        
        vol_up_button = Button(
            text="Volume Up",
            font_size='20sp',
            background_color=(0.2, 1, 0.2, 1),
            on_press=self.volume_up
        )
        setting_layout.add_widget(vol_up_button)

        vol_down_button = Button(
            text="Volume Down",
            font_size='20sp',
            background_color=(1, 0.2, 0.2, 1),
            on_press=self.volume_down
        )
        setting_layout.add_widget(vol_down_button)

        back_to_menu_button = Button(
            text="Back to Menu",
            font_size='20sp',
            background_color=(0.8, 0.8, 0.8, 1),
            on_press=lambda x: self.back_to_menu(x)  
        )
        setting_layout.add_widget(back_to_menu_button)
        
        self.menu_screen.clear_widgets()
        self.menu_screen.add_widget(setting_layout)
        
    def update_volume_label(self):
        if hasattr(self, 'setting_label') and isinstance(self.setting_label, Label) and hasattr(self, 'sound') and self.sound:
            self.setting_label.text = f"Volume: {self.sound.volume:.2f}"

    def volume_up(self, instance):
        if hasattr(self, 'sound') and self.sound:
            self.sound.volume = min(1, self.sound.volume + 0.1)
            self.update_volume_label()

    def volume_down(self, instance):
        if hasattr(self, 'sound') and self.sound:
            self.sound.volume = max(0, self.sound.volume - 0.1)
            self.update_volume_label()
            
    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

# รัน App
if __name__ == '__main__':
    ReactionTimeTestApp().run()