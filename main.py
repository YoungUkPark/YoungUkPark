from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivy.metrics import dp
from functools import partial
from threading import Thread
import cv2
import requests
import json
import re
import os, sys
from animation import MyAnimation
from RockScissorPaperGame import RockScissorPaperGame
from HandCalculatorGame import HandCalculatorGame
from wids.alert import Alert
from kivy.clock import Clock


os.environ['KIVY_IMAGE'] = 'pil,sdl2'


class Login(MDScreen):
    pass


class Home(MDScreen):
    pass


class NewMember(MDScreen):
    pass


class RockScissorPaper(MDScreen):
    pass


class RockScissorPaper_ending(MDScreen):
    pass


class DanceDance(MDScreen):
    pass


class DanceDance_ending(MDScreen):
    pass


class WordClimbing(MDScreen):
    pass


class WordClimbing_ending(MDScreen):
    pass


class Drawer(MDScreen):
    pass


class Drawer_ending(MDScreen):
    pass


class NewsPaper(MDScreen):
    pass


class NewsPaper_ending(MDScreen):
    pass


class HandCalculator(MDScreen):
    pass


class HandCalculator_ending(MDScreen):
    pass


class ListItem(OneLineListItem):
    icon = StringProperty()


class Loading(MDScreen):
    pass


class MyApp(MDApp):
    id_allowed = False
    pw_allowed = False
    pw_check_allowed = False
    name_allowed = False
    frame = None
    origin_id = False
    video_loaded = False
    user_lv = {'rockscissorpaper': 3, 'handcalculator': 24, 'dancedance': 1, 'drawer': 1, 'wordclimbing': 1, 'newspaper': 1}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (360, 640)
        Window.minimum_width, Window.minimum_height = (360, 640)
        self.screen = Builder.load_file(self.resource_path('main.kv'))

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def eduYearSetting(self):
        menu_items = [
            {
                "viewclass": "ListItem",
                "height": dp(56),
                "text": f" {i}",
                "on_release": lambda x=f"{i} 년": self.set_item(x),
            } for i in range(17)]
        self.menu = MDDropdownMenu(caller=self.screen.ids.new.ids.eduyear, items=menu_items, position="auto", width_mult=1)
        self.screen.ids.new.ids.eduyear.disabled = True
        self.menu.open()

    def birth_setting(self):
        self.calender = MDDatePicker(min_year=1900, max_year=2021, year=1950, month=7, day=15, primary_color=(215/255, 198/255, 54/255, 0.53))
        self.calender.bind(on_save=self.on_save)
        self.calender.open()

    def loading_screen(self, dt):
        self.root.ids.screen_manager.current = 'loading'
        Thread(target=self.video_loading).start()

    def video_loading(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1410)
        self.video_loaded = True

    def newsPaperPlay(self):
        Window.size = (640, 360)
        Window.minimum_width, Window.minimum_height = (640, 360)

        def video_checking(dt):
            if self.video_loaded:
                self.root.ids.screen_manager.current = 'newspaper'
                check.cancel()
            else:
                pass

        Clock.schedule_once(self.loading_screen)
        check = Clock.schedule_interval(video_checking, 1.0 / 60.0)

    def wordClimbingPlay(self):
        Window.size = (640, 360)
        Window.minimum_width, Window.minimum_height = (640, 360)

        def video_checking(dt):
            if self.video_loaded:
                self.root.ids.screen_manager.current = 'wordclimbing'
                check.cancel()
            else:
                pass

        Clock.schedule_once(self.loading_screen)
        check = Clock.schedule_interval(video_checking, 1.0 / 60.0)

    def drawerPlay(self):
        Window.size = (640, 360)
        Window.minimum_width, Window.minimum_height = (640, 360)

        def video_checking(dt):
            if self.video_loaded:
                self.root.ids.screen_manager.current = 'drawer'
                check.cancel()
            else:
                pass

        Clock.schedule_once(self.loading_screen)
        check = Clock.schedule_interval(video_checking, 1.0 / 60.0)

    def danceDancePlay(self):
        Window.size = (640, 360)
        Window.minimum_width, Window.minimum_height = (640, 360)

        def video_checking(dt):
            if self.video_loaded:
                self.root.ids.screen_manager.current = 'dancedance'
                check.cancel()
            else:
                pass

        Clock.schedule_once(self.loading_screen)
        check = Clock.schedule_interval(video_checking, 1.0 / 60.0)

    def rockScissorPaperPlay(self):
        Window.size = (640, 360)
        Window.minimum_width, Window.minimum_height = (640, 360)

        def video_checking(dt):
            if self.video_loaded:
                self.root.ids.screen_manager.current = 'rockscissorpaper'
                RSPplay = RockScissorPaperGame(self.screen, Window, self.root, app, self.user_lv['rockscissorpaper'])
                Clock.schedule_interval(partial(RSPplay.play, self.capture), 1.0 / 60.0)
                check.cancel()
            else:
                pass

        Clock.schedule_once(self.loading_screen)
        check = Clock.schedule_interval(video_checking, 1.0 / 60.0)

    def handCalculatorPlay(self):
        Window.size = (640, 360)
        Window.minimum_width, Window.minimum_height = (640, 360)

        def video_checking(dt):
            if self.video_loaded:
                self.root.ids.screen_manager.current = 'handcalculator'
                HCplay = HandCalculatorGame(self.screen, Window, self.root, app, self.user_lv['handcalculator'])
                Clock.schedule_interval(partial(HCplay.play, self.capture), 1.0 / 60.0)
                check.cancel()
            else:
                pass

        Clock.schedule_once(self.loading_screen)
        check = Clock.schedule_interval(video_checking, 1.0 / 60.0)

    def set_item(self, text__item):
        self.screen.ids.new.ids.eduyear.text = text__item
        self.screen.ids.new.ids.eduyear.font_name = self.resource_path('fonts/NotoSansKR-Regular.otf')
        self.screen.ids.new.ids.eduyear.disabled = False
        self.menu.dismiss()

    def auto_login(self, dt):
        if os.path.exists(self.resource_path('access/refresh_token')):
            self.refresh_try()

    def build(self):
        Clock.schedule_once(self.auto_login)
        return self.screen

    def duplication_check(self, value):
        if self.id_allowed:
            url = "https://xr.super-brain.co.kr/user/id/check"
            res = requests.post(url, data=json.dumps({'id': value}), headers={'Content-Type': 'application/json'})
            if res.status_code == 401:
                self.screen.ids.new.ids.id_check.text = '사용가능'
                self.screen.ids.new.ids.id_check.font_name = self.resource_path('fonts/NotoSansKR-Regular.otf')
                self.screen.ids.new.ids.id_check.md_bg_color = [0, 0.5, 0, 1]
                self.origin_id = True
            elif res.status_code == 200:
                self.screen.ids.new.ids.id_check.text = '사용불가'
                self.screen.ids.new.ids.id_check.font_name = self.resource_path('fonts/NotoSansKR-Regular.otf')
                self.screen.ids.new.ids.id_check.md_bg_color = [0.5, 0, 0, 1]
                self.origin_id = False
        elif value == '':
            self.screen.ids.new.ids.id_check.text = '입력필요'
            self.screen.ids.new.ids.id_check.font_name = self.resource_path('fonts/NotoSansKR-Regular.otf')
            self.screen.ids.new.ids.id_check.md_bg_color = [0.6, 0.6, 0, 1]
        else:
            self.screen.ids.new.ids.id_check.text = '사용불가'
            self.screen.ids.new.ids.id_check.font_name = self.resource_path('fonts/NotoSansKR-Regular.otf')
            self.screen.ids.new.ids.id_check.md_bg_color = [0.5, 0, 0, 1]
            self.origin_id = False

    def validation_name(self, name):
        if name != '':
            if len(name) < 2:
                self.screen.ids.new.ids.ur_name.color_mode = 'accent'
                self.screen.ids.new.ids.ur_name.helper_text_mode = "persistent"
                self.screen.ids.new.ids.ur_name.helper_text = 'It should be more than 2 letters'
                self.name_allowed = False
            elif len(name) != len(name.replace(" ", "")):
                self.screen.ids.new.ids.ur_name.color_mode = 'accent'
                self.screen.ids.new.ids.ur_name.helper_text_mode = "persistent"
                self.screen.ids.new.ids.ur_name.helper_text = "It can't contain white space"
                self.name_allowed = False
            elif re.search('[`~!@#$%^&*(),<.>/?]+', name) is not None:
                self.screen.ids.new.ids.ur_name.color_mode = 'accent'
                self.screen.ids.new.ids.ur_name.helper_text_mode = "persistent"
                self.screen.ids.new.ids.ur_name.helper_text = "It can't contain special case"
                self.name_allowed = False
            else:
                self.screen.ids.new.ids.ur_name.error = False
                self.screen.ids.new.ids.ur_name.color_mode = 'custom'
                self.screen.ids.new.ids.ur_name.line_color_focus = 0, 0.5, 0, 1
                self.screen.ids.new.ids.ur_name.helper_text_mode = "persistent"
                self.screen.ids.new.ids.ur_name.helper_text = 'Appropriate!'
                self.name_allowed = True
        else:
            self.screen.ids.new.ids.ur_name.error = False
            self.screen.ids.new.ids.ur_name.color_mode = 'primary'
            self.screen.ids.new.ids.ur_name.helper_text_mode = "on_focus"
            self.screen.ids.new.ids.ur_name.helper_text = ''
            self.name_allowed = False

    def validate_id(self, id): # 여기에서 아이디 중복검사
        if id != '':
            if len(id) < 5:
                self.screen.ids.new.ids.the_ur.color_mode = 'accent'
                self.screen.ids.new.ids.the_ur.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_ur.helper_text = 'More than 5 letters'
                self.id_allowed = False
            elif len(id) > 15:
                self.screen.ids.new.ids.the_ur.helper_text = 'Less than 15 letters'
                self.id_allowed = False
            elif len(id) != len(id.replace(" ", "")):
                self.screen.ids.new.ids.the_ur.color_mode = 'accent'
                self.screen.ids.new.ids.the_ur.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_ur.helper_text = "It can't contain white space"
                self.id_allowed = False
            elif re.search('[`~!@#$%^&*(),<.>/?]+', id) is not None:
                self.screen.ids.new.ids.the_ur.color_mode = 'accent'
                self.screen.ids.new.ids.the_ur.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_ur.helper_text = "It can't contain special case"
                self.id_allowed = False
            else:
                self.screen.ids.new.ids.the_ur.error = False
                self.screen.ids.new.ids.the_ur.color_mode = 'custom'
                self.screen.ids.new.ids.the_ur.line_color_focus = 0, 0.5, 0, 1
                self.screen.ids.new.ids.the_ur.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_ur.helper_text = 'Appropriate!'
                self.id_allowed = True
        else:
            self.screen.ids.new.ids.the_ur.error = False
            self.screen.ids.new.ids.the_ur.color_mode = 'primary'
            self.screen.ids.new.ids.the_ur.helper_text_mode = "on_focus"
            self.screen.ids.new.ids.the_ur.helper_text = '5-20 letters'
            self.id_allowed = False

    def validate_password(self, password):
        if password != '':
            if len(password) < 8:
                self.screen.ids.new.ids.the_pw.color_mode = 'accent'
                self.screen.ids.new.ids.the_pw.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw.helper_text = 'It should be more than 8 letters'
                self.pw_allowed = False
            elif len(password) > 20:
                self.screen.ids.new.ids.the_pw.helper_text = 'It should be up to 20 letters'
                self.pw_allowed = False
            elif len(password) != len(password.replace(" ", "")):
                self.screen.ids.new.ids.the_pw.color_mode = 'accent'
                self.screen.ids.new.ids.the_pw.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw.helper_text = "It can't contain white space"
                self.pw_allowed = False
            elif re.search('[0-9]+', password) is None:
                self.screen.ids.new.ids.the_pw.color_mode = 'accent'
                self.screen.ids.new.ids.the_pw.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw.helper_text = 'It should contain at least 1 number'
                self.pw_allowed = False
            elif re.search('[A-Z]+', password) is None:
                self.screen.ids.new.ids.the_pw.color_mode = 'accent'
                self.screen.ids.new.ids.the_pw.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw.helper_text = 'It should contain at least 1 upper case'
                self.pw_allowed = False
            elif re.search('[`~!@#$%^&*(),<.>/?]+', password) is None:
                self.screen.ids.new.ids.the_pw.color_mode = 'accent'
                self.screen.ids.new.ids.the_pw.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw.helper_text = 'It should contain at least 1 special case'
                self.pw_allowed = False
            else:
                self.screen.ids.new.ids.the_pw.error = False
                self.screen.ids.new.ids.the_pw.color_mode = 'custom'
                self.screen.ids.new.ids.the_pw.line_color_focus = 0, 0.5, 0, 1
                self.screen.ids.new.ids.the_pw.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw.helper_text = 'Appropriate!'
                self.pw_allowed = True
        else:
            self.screen.ids.new.ids.the_pw.error = False
            self.screen.ids.new.ids.the_pw.color_mode = 'primary'
            self.screen.ids.new.ids.the_pw.helper_text_mode = "on_focus"
            self.screen.ids.new.ids.the_pw.helper_text = 'Upper & lower case + digits > 4 letters'
            self.pw_allowed = False

    def move_home(self):
        self.change_screen('home', 'left')
        Window.size = (360, 640)
        Window.minimum_width, Window.minimum_height = (360, 640)
        self.screen.ids.rockscissorpaper.ids.gameimage_left.source = ''
        self.screen.ids.rockscissorpaper.ids.gameimage_right.source = ''
        self.screen.ids.rockscissorpaper.ids.result_text.text = ''
        self.screen.ids.rockscissorpaper.ids.mission.text = ''
        self.screen.ids.rockscissorpaper.ids.quest_hand.text = ''
        self.screen.ids.rockscissorpaper.ids.gameinfo.text = f'점수: 0\n남은 시간: '
        self.screen.ids.rockscissorpaper.ids.result_image.source = ''
        self.screen.ids.rockscissorpaper.ids.result_image.opacity = 0
        if self.capture.isOpened():
            self.capture.release()
            self.video_loaded = False

    def check_password(self, check_pw, password):
        if self.screen.ids.new.ids.the_pw.text != '':
            if check_pw != password[:len(check_pw)]:
                self.screen.ids.new.ids.the_pw_check.error = True
                self.screen.ids.new.ids.the_pw_check.color_mode = 'primary'
                self.screen.ids.new.ids.the_pw_check.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw_check.helper_text = 'Not matched'
                self.pw_check_allowed = False
            else:
                self.screen.ids.new.ids.the_pw_check.error = False
                self.screen.ids.new.ids.the_pw_check.helper_text_mode = "persistent"
                self.screen.ids.new.ids.the_pw_check.color_mode = 'custom'
                self.screen.ids.new.ids.the_pw_check.line_color_focus = 0, 0.5, 0, 1
                self.screen.ids.new.ids.the_pw_check.helper_text = 'Matched'
                self.pw_check_allowed = True
        else:
            self.screen.ids.new.ids.the_pw_check.error = False
            self.screen.ids.new.ids.the_pw_check.color_mode = 'primary'
            self.screen.ids.new.ids.the_pw_check.helper_text_mode = "on_focus"
            self.screen.ids.new.ids.the_pw_check.helper_text = 'Must be same with upper value'
            self.pw_check_allowed = False

    def reg_reset(self):
        self.screen.ids.new.ids.id_check.text = '중복검사'
        self.screen.ids.new.ids.id_check.md_bg_color = self.theme_cls.primary_color
        reg_screen = self.screen.ids.new
        id = reg_screen.ids.the_ur
        pw = reg_screen.ids.the_pw
        pw_check = reg_screen.ids.the_pw_check
        name = reg_screen.ids.ur_name
        birth = reg_screen.ids.birth
        eduyear = reg_screen.ids.eduyear
        id.text = ''
        pw.text = ''
        pw_check.text = ''
        name.text = ''
        birth.text = ''
        eduyear.text = ''
        self.change_screen('login', 'right')

    def change_screen(self, sc, way):
        manager = self.root.ids.screen_manager
        manager.transition = SlideTransition()
        manager.transition.duration = 0.5
        manager.transition.direction = way
        manager.current = sc

    def game_end_screen(self, game):
        manager = self.root.ids.screen_manager
        manager.transition = FadeTransition()
        manager.current = game+'_ending'

    def on_start(self):
        pass

    def errorAlert(self, winner, mode):
        score = Alert(winner, app, mode)
        Clock.schedule_once(lambda x: score.open(), 1)

    def login_id_check(self, the_ur):
        the_ur.color_mode = 'primary'
        the_ur.helper_text_mode = "on_focus"
        the_ur.helper_text = ''
        the_ur.focus = True

    def login_pw_check(self, the_pw):
        the_pw.color_mode = 'primary'
        the_pw.helper_text_mode = "on_focus"
        the_pw.helper_text = ''
        the_pw.focus = True

    def loginFunction(self, the_ur, the_pw):
        if the_ur.text == '' or the_pw.text == '':
            self.alert = MDDialog(
                buttons=[
                    MDFlatButton(
                        text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                    )
                ],
            )
            if the_ur.text == '':
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]아이디를 입력해주세요.[/font]"
                the_ur.helper_text_mode = "persistent"
                the_ur.color_mode = 'accent'
                the_ur.helper_text = 'Fill in'
                the_ur.focus = True
            elif the_pw.text == '':
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]비밀번호를 입력해주세요.[/font]"
                the_pw.helper_text_mode = "persistent"
                the_pw.color_mode = 'accent'
                the_pw.helper_text = 'Fill in'
                the_pw.focus = True
        else:
            self.login_post({'id': the_ur.text, 'password': the_pw.text})

    def reset(self, inst, content):
        inst.error = False
        inst.helper_text_mode = "on_focus"
        inst.helper_text = content
        inst.disabled = False

    def registerFunction(self, the_ur, the_pw, ur_name, birth, male, female, eduyear):
        if the_ur.text == '' or the_pw.text == '' or ur_name.text == '' or birth.text == '' or (not male and not female) or eduyear.text == '':
            self.alert = MDDialog(
                buttons=[
                    MDFlatButton(
                        text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                    )
                ],
            )
            if the_ur.text == '':
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]아이디를 입력해주세요.[/font]"
                the_ur.helper_text_mode = "persistent"
                the_ur.error = True
                the_ur.helper_text = 'Fill in'
                the_ur.focus = True
            elif the_pw.text == '':
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]비밀번호를 입력해주세요.[/font]"
                the_pw.error = True
                the_pw.helper_text_mode = "persistent"
                the_pw.helper_text = 'Fill in'
                the_pw.focus = True
            elif ur_name.text == '':
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]이름을 입력해주세요.[/font]"
                ur_name.error = True
                ur_name.helper_text_mode = "persistent"
                ur_name.helper_text = 'Fill in'
                ur_name.focus = True
            elif birth.text == '':
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]생년월일을 입력해주세요.[/font]"
                birth.error = True
                birth.helper_text_mode = "persistent"
                birth.helper_text = 'Fill in'
            elif not male and not female:
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]성별을 체크해주세요.[/font]"
                self.screen.ids.new.ids.gender.color = (1, 0, 0, 1)
            elif eduyear.text == '':
                self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]교육년수를 입력해주세요.[/font]"
                eduyear.error = True
                eduyear.helper_text_mode = "persistent"
                eduyear.helper_text = 'Fill in'
        else:
            if not self.id_allowed or not self.pw_allowed or not self.pw_check_allowed or not self.origin_id:
                self.alert = MDDialog(
                    buttons=[
                        MDFlatButton(
                            text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                        )
                    ],
                )
                if not self.id_allowed:
                    self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]양식에 맞게 아이디를 만들어주세요.[/font]"
                    the_ur.helper_text_mode = "persistent"
                    the_ur.error = True
                    the_ur.helper_text = 'ID is NOT allowed'
                    the_ur.focus = True
                elif not self.pw_allowed:
                    self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]양식에 맞게 비밀번호를 설정해주세요.[/font]"
                    the_pw.error = True
                    the_pw.helper_text_mode = "persistent"
                    the_pw.helper_text = 'Fill in'
                    the_pw.focus = True
                elif not self.origin_id:
                    self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]해당 ID는 사용하실 수 없습니다.[/font]"
                    the_ur.error = True
                    the_ur.helper_text_mode = "persistent"
                    the_ur.helper_text = 'This ID can not be used'
                    the_ur.focus = True
                elif not self.pw_check_allowed:
                    self.alert.text = f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]비밀번호가 일치하지 않습니다.[/font]"
                    self.screen.ids.new.ids.the_pw_check.error = True
                    self.screen.ids.new.ids.the_pw_check.helper_text_mode = "persistent"
                    self.screen.ids.new.ids.the_pw_check.helper_text = 'Password is NOT matched'
                    self.screen.ids.new.ids.the_pw_check.focus = True
            else:
                if male:
                    gender = 'M'
                elif female:
                    gender = 'F'
                self.alert = MDDialog(
                    text=f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]"
                         f"입력하신 정보가 맞습니까?\n\n아이디: {the_ur.text}\n비밀번호: {the_pw.text}\n이름: {ur_name.text}\n생년월일: {birth.text}\n성별: {gender}\n교육년수: {eduyear.text}[/font]",
                    buttons=[
                        MDFlatButton(
                            text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=lambda x: self.register_post({"id": the_ur.text, "password": the_pw.text, "name": ur_name.text, "year": birth.text.split('/')[0], "month": birth.text.split('/')[1], "date": birth.text.split('/')[2], "gender": gender, "education": eduyear.text.split(' ')[0]})
                        ),
                        MDFlatButton(
                            text="취소", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                        ),
                    ],
                )
        self.alert.open()

    def access_try(self, access_token):
        url = "https://xr.super-brain.co.kr/user/reissue"
        res = requests.post(url, headers={"Authorization": "Bearer " + access_token})
        if res.status_code == 200:
            manager = self.root.ids.screen_manager
            manager.transition = FadeTransition()
            manager.current = 'home'
            self.screen.ids.home.ids.mention.ur_name = '영욱'  # 추후 DB에서 정보 받아서 이름 입력
            toast('Login Success')
        else:
            self.alert = MDDialog(
                text=f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]엑세스가 허용되지 않습니다.[/font]",
                buttons=[
                    MDFlatButton(
                        text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'),
                        text_color=self.theme_cls.primary_color, on_release=lambda x: self.alert.dismiss()
                    ),
                ],
            )
            self.alert.open()

    def refresh_try(self):
        if os.path.exists(self.resource_path('access/refresh_token')):
            with open(os.path.join(self.resource_path('access/refresh_token')), 'rb') as file:
                refresh_token = str(file.read(), 'utf-8')
            url = "https://xr.super-brain.co.kr/user/reissue"
            res = requests.post(url, headers={"Authorization": "Bearer " + refresh_token})
            if res.status_code == 200:
                access_token = res.json()['access']
                self.access_try(access_token)
            else:
                self.alert = MDDialog(
                    text=f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]로그인 기간이 만료되었습니다.\n다시 로그인 해주세요.[/font]",
                    buttons=[
                        MDFlatButton(
                            text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'),
                            text_color=self.theme_cls.primary_color, on_release=lambda x: self.alert.dismiss()
                        ),
                    ],
                )
                self.alert.open()
                # the_pw_check = self.screen.ids.new.ids.the_pw_check
                # the_pw_check.bind(on_text_validate=self.check_password, on_focus=self.check_password)

    def login_post(self, value):
        url = "https://xr.super-brain.co.kr/user/login/check"
        res = requests.post(url, data=json.dumps(value), headers={'Content-Type': 'application/json'})
        if res.status_code == 200:
            refresh_token = res.json()['refresh']
            access_token = res.json()['access']
            with open(os.path.join(self.resource_path('access/refresh_token')), 'w+b') as file:
                file.write(bytes(refresh_token, encoding="UTF-8", errors="ignore"))
            with open(os.path.join(self.resource_path('access/access_token')), 'w+b') as file:
                file.write(bytes(access_token, encoding="UTF-8", errors="ignore"))
            self.refresh_try()
        else:
            self.alert = MDDialog(
                text=f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]아이디 또는 비밀번호가 일치하지 않습니다.[/font]",
                buttons=[
                    MDFlatButton(
                        text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=lambda x: self.alert.dismiss()
                    ),
                ],
            )
            self.alert.open()

    def register_post(self, value):
        self.alert.dismiss()
        url = "https://xr.super-brain.co.kr/user/put"
        res = requests.post(url, data=json.dumps(value), headers={'Content-Type': 'application/json'})
        if res.status_code == 200:
            self.alert = MDDialog(
                text=f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]회원가입에 성공하였습니다.[/font]",
                buttons=[
                    MDFlatButton(
                        text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=lambda x: self.register_success()
                    ),
                ],
            )
            self.change_screen('login', 'right')
        else:
            self.alert = MDDialog(
                text=f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]회원가입에 실패하였습니다.[/font]",
                buttons=[
                    MDFlatButton(
                        text="확인", font_name=self.resource_path('fonts/NotoSansKR-Regular.otf'), text_color=self.theme_cls.primary_color, on_release=lambda x: self.alert.dismiss()
                    ),
                ],
            )
        self.alert.open()

    def register_success(self):
        self.reg_reset()
        self.alert.dismiss()

    def close_dialog(self, inst):
        self.alert.dismiss()

    def on_save(self, instance, value, date_range):
        self.root.ids.new.ids.birth.text = value.strftime("%Y/%m/%d")

    def menu_list(self, button):
        self.main_menu = MDDropdownMenu(items=[{"viewclass": "OneLineListItem", "text": f"[font={self.resource_path('fonts/NotoSansKR-Regular.otf')}]로그아웃[/font]", "height": dp(56), "on_release": lambda *args: self.logout()}], width_mult=4, position="auto")
        self.main_menu.caller = button
        self.main_menu.open()

    def logout(self):
        self.main_menu.dismiss()
        self.change_screen('login', 'left')


app = MyApp()
app.run()