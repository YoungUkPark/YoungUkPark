from time import time
import cv2
from handDetector import handDetector
from handDetector import fingerQuantification
from kivy.uix.screenmanager import SlideTransition
from kivy.graphics.texture import Texture
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import random
import sys, os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class RockScissorPaperGame:
    def __init__(self, screen, Window, root, app, lv):
        self.lv = lv
        self.totalpoint = 0
        self.screen = screen
        self.Window = Window
        self.root = root
        self.app = app
        self.answer = None
        self.result = 0
        self.timeLimit = 0
        self.point = 0
        self.fingerShape = {'rock': [[[1, 1, 1, 1, 1]], [[0, 0, 0, 0, 0]], [[0, 1, 1, 0, 0], [1, 1, 0, 0, 0]]],
                       'scissor': [[[0, 0, 0, 0, 0]], [[0, 1, 1, 0, 0], [1, 1, 0, 0, 0]], [[1, 1, 1, 1, 1]]],
                       'paper': [[[0, 1, 1, 0, 0], [1, 1, 0, 0, 0]], [[1, 1, 1, 1, 1]], [[0, 0, 0, 0, 0]]]}
        self.finger_check = [[1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [1, 1, 0, 0, 0]]
        self.choice = ['rock', 'scissor', 'paper']
        self.nextQuestion = ''
        self.action = {'mission': ['이겨라!', '비겨라!', '져라!'], 'same': ['', '따라하세요!'], 'match': ['가위바위보!'], 'point': [0, 0, 0]}
        self.playtime = 0
        self.thinking = 0
        self.question = False
        self.gameinfo = screen.ids.rockscissorpaper.ids.gameinfo
        self.gameimage_left = screen.ids.rockscissorpaper.ids.gameimage_left
        self.gameimage_right = screen.ids.rockscissorpaper.ids.gameimage_right
        self.mission = screen.ids.rockscissorpaper.ids.mission
        self.quest_hand = screen.ids.rockscissorpaper.ids.quest_hand
        self.result_image = screen.ids.rockscissorpaper.ids.result_image
        self.result_text = screen.ids.rockscissorpaper.ids.result_text
        self.detector = handDetector(detectionCon=0.75)
        self.result = True
        self.variables = [
            {'time': 10, 'wating': 4, 'rule': 'same', 'myhand': 'one', 'opponent': 'one', 'description': '5초 안에 가위바위보 손 모양을 따라하세요!'},  # 1
            {'time': 10, 'wating': 2, 'rule': 'same', 'myhand': 'one', 'opponent': 'one', 'description': '3초 안에 가위바위보 손 모양을 따라하세요!'},  # 2
            {'time': 10, 'wating': 4, 'rule': 'same', 'myhand': 'or', 'opponent': 'or', 'description': '5초 안에 주어진 손으로 가위바위보 손 모양을 따라하세요!'},  # 3
            {'time': 10, 'wating': 2, 'rule': 'same', 'myhand': 'or', 'opponent': 'or', 'description': '3초 안에 주어진 손으로 가위바위보 손 모양을 따라하세요!'},  # 4
            {'time': 10, 'wating': 4, 'rule': 'same', 'myhand': 'both', 'opponent': 'both', 'description': '5초 안에 양손 모두 가위바위보 손 모양을 따라하세요!'},  # 5
            {'time': 10, 'wating': 2, 'rule': 'same', 'myhand': 'both', 'opponent': 'both', 'description': '3초 안에 양손 모두 가위바위보 손 모양을 따라하세요!'},  # 6
            {'time': 10, 'wating': 4, 'rule': 'match', 'myhand': 'one', 'opponent': 'one', 'description': '5초 안에 가위 바뷔 보!'},  # 7
            {'time': 10, 'wating': 2, 'rule': 'match', 'myhand': 'one', 'opponent': 'one', 'description': '3초 안에 가위 바뷔 보!'},  # 8
            {'time': 10, 'wating': 4, 'rule': 'match', 'myhand': 'or', 'opponent': 'or', 'description': '5초 안에 주어진 손으로 가위 바뷔 보!'},  # 9
            {'time': 10, 'wating': 2, 'rule': 'match', 'myhand': 'or', 'opponent': 'or', 'description': '3초 안에 주어진 손으로 가위 바뷔 보!'},  # 10
            {'time': 10, 'wating': 4, 'rule': 'match', 'myhand': 'both', 'opponent': 'both', 'description': '5초 안에 양손 모두 이기세요!'},  # 11
            {'time': 10, 'wating': 2, 'rule': 'match', 'myhand': 'both', 'opponent': 'both', 'description': '3초 안에 양손 모두 이기세요!'},  # 12
            {'time': 10, 'wating': 4, 'rule': 'mission', 'myhand': 'one', 'opponent': 'one', 'description': '5초 안에 문제 설명을 잘 읽고 설명에 나온대로 가위바위보를 내세요!'},  # 13
            {'time': 10, 'wating': 2, 'rule': 'mission', 'myhand': 'one', 'opponent': 'one', 'description': '3초 안에 문제 설명을 잘 읽고 설명에 나온대로 가위바위보를 내세요!'},  # 14
            {'time': 10, 'wating': 4, 'rule': 'point', 'myhand': 'one', 'opponent': 'one', 'description': '5초 안에 가위바위보로 가장 많은 점수를 내세요!'},  # 15
            {'time': 10, 'wating': 2, 'rule': 'point', 'myhand': 'one', 'opponent': 'one', 'description': '3초 안에 가위바위보로 가장 많은 점수를 내세요!'},  # 16
            {'time': 10, 'wating': 4, 'rule': 'mission', 'myhand': 'or', 'opponent': 'or', 'description': '5초 안에 문제 설명을 잘 읽고 설명에 나온대로 가위바위보를 내세요!'},  # 17
            {'time': 10, 'wating': 2, 'rule': 'mission', 'myhand': 'or', 'opponent': 'or', 'description': '3초 안에 문제 설명을 잘 읽고 설명에 나온대로 가위바위보를 내세요!'},  # 18
            {'time': 10, 'wating': 4, 'rule': 'mission', 'myhand': 'both', 'opponent': 'both', 'description': '5초 안에 양손 모두 설명에 나온대로 하세요!'},  # 19
            {'time': 10, 'wating': 2, 'rule': 'mission', 'myhand': 'both', 'opponent': 'both', 'description': '3초 안에 양손 모두 설명에 나온대로 하세요!'},  # 20
            {'time': 10, 'wating': 4, 'rule': 'point', 'myhand': 'or', 'opponent': 'or', 'description': '5초 안에 화면에 나타난 손으로 가장 많은 점수를 내세요!'},  # 21
            {'time': 10, 'wating': 2, 'rule': 'point', 'myhand': 'or', 'opponent': 'or', 'description': '3초 안에 화면에 나타난 손으로 가장 많은 점수를 내세요!'},  # 22
            {'time': 10, 'wating': 4, 'rule': 'point', 'myhand': 'both', 'opponent': 'both', 'description': '5초 안에 양손으로 가장 많은 점수를 내세요!'},  # 23
            {'time': 10, 'wating': 2, 'rule': 'point', 'myhand': 'both', 'opponent': 'both', 'description': '3초 안에 양손으로 가장 많은 점수를 내세요!'},  # 24
            {'time': 10, 'wating': 4, 'rule': 'point', 'myhand': 'one', 'opponent': 'both', 'description': '5초 안에 한 손으로 가장 많은 점수를 내세요!'},  # 25
            {'time': 10, 'wating': 2, 'rule': 'point', 'myhand': 'one', 'opponent': 'both', 'description': '3초 안에 한 손으로 가장 많은 점수를 내세요!'},  # 26
            {'time': 10, 'wating': 4, 'rule': 'point', 'myhand': 'or', 'opponent': 'both', 'description': '5초 안에 화면에 나타난 손으로 가장 많은 점수를 내세요!'},  # 27
            {'time': 10, 'wating': 2, 'rule': 'point', 'myhand': 'or', 'opponent': 'both', 'description': '3초 안에 화면에 나타난 손으로 가장 많은 점수를 내세요!'},  # 28
        ]
        #rule : 'same'/'match'/'mission'/'point'
        #myhand/opponent : 'one'/'or'/'both'
        if self.lv == 0:
            self.lv = 1
        self.oppenent_hand = ['right', 'left']
        if self.variables[self.lv-1]['myhand'] == 'one':
            self.myHand = ['편한손으로']
        elif self.variables[self.lv-1]['myhand'] == 'or':
            self.myHand = ['오른손으로', '왼손으로']
        elif self.variables[self.lv-1]['myhand'] == 'both':
            self.myHand = ['양손 모두']
        self.len_nextAction = len(self.action[self.variables[self.lv-1]['rule']])
        self.description_screen(self.variables[self.lv - 1]['description'])
        self.ready = False
        self.screen.ids.rockscissorpaper.ids.gamebar.script = str(self.lv) + '  [font=fonts/NotoSansKR-Regular.otf][size=15sp]' + self.variables[self.lv - 1]['description'] + '[/size][/font]'
        self.gameinfo.text = f"점수: {int(self.point)}\n남은 시간: {self.variables[self.lv-1]['time']-int(self.playtime)}/{self.variables[self.lv-1]['time']}"
        self.mission.text = ''
        self.quest_hand.text = ''
        self.gameimage_left.source = ''
        self.gameimage_right.source = ''

    def description_screen(self, description):
        self.alert = MDDialog(
            buttons=[
                MDFlatButton(
                    text="확인", font_name='fonts/NotoSansKR-Regular.otf', text_color=self.app.theme_cls.primary_color,
                    on_release=self.ready_button
                )
            ],
        )
        self.alert.text = f"[font=fonts/NotoSansKR-Regular.otf]{description}\n[color=#881111FF]손바닥이 카메라를 향하도록 내야합니다![/color]\n\n[color=#111111FF]준비 되셨으면 확인을 눌러주세요![/color][/font]"
        self.alert.open()

    def ready_button(self, inst):
        self.alert.dismiss()
        self.ready = True

    def close_dialog(self, inst):
        self.alert.dismiss()
        self.app.game_end_screen('rockscissorpaper')
        self.app.user_lv['rockscissorpaper'] = self.lv
        self.screen.ids.home.ids.rockscissorpaper_card.text = 'Level: ' + str(self.lv)

    def change_screen(self, sc, way):
        manager = self.root.ids.screen_manager
        manager.transition = SlideTransition()
        manager.transition.duration = 0.5
        manager.transition.direction = way
        manager.current = sc

    def play(self, capture, *largs):
        self.capture = capture
        if self.capture is not None and self.capture.isOpened():
            if self.ready:
                # display image from cam in opencv window
                ret, frame = self.capture.read()
                # convert it to texture
                self.cTime = time()
                self.playtime = self.cTime - self.pTime
                if self.playtime < 3:
                    self.result_image.opacity = 1
                    self.result_image.source = resource_path('imgs/ready.png')
                    self.result_text.opacity = 1
                    self.result_text.text = f'\n\n{3-int(self.playtime)}'
                elif self.playtime < 4:
                    self.result_image.opacity = 0.7
                    self.result_image.source = resource_path('imgs/start.png')
                    self.result_text.opacity = 0
                    self.result_text.text = ''
                    self.sTime = time()
                else:
                    if self.playtime <= self.variables[self.lv-1]['time'] + 3:
                        if not self.question:
                            self.thinking = self.cTime - self.sTime
                            if self.thinking < 1:
                                self.nextQuestion = random.choice(self.choice)
                                if self.variables[self.lv - 1]['opponent'] == 'both':
                                    self.nextQuestion2 = random.choice(self.choice)
                                self.result_image.source = ''
                                self.result_image.opacity = 0
                                if self.variables[self.lv-1]['rule'] == 'mission':
                                    self.nextAction = random.randint(0, self.len_nextAction-1)
                                if self.variables[self.lv - 1]['rule'] == 'point':
                                    if self.variables[self.lv - 1]['opponent'] == 'both':
                                        for point_index in range(len(self.action['point'])):
                                            self.action['point'][point_index] = random.randint(0, 4)
                                    else:
                                        for point_index in range(len(self.action['point'])):
                                            self.action['point'][point_index] = random.randint(0, 9)
                                    # 여기에서 point5 개 중 3개를 뽑아서 {'승': , '무': , '패':}로 넣고 나중에 point에 해당하는 점수를 +시킨다
                                elif self.variables[self.lv-1]['rule'] == 'match':
                                    self.nextAction = 0
                                elif self.variables[self.lv-1]['rule'] == 'same':
                                    self.nextAction = 1
                                self.nextHand = random.choice(self.myHand)
                                self.nextOpponentHand = random.choice(self.oppenent_hand)
                            if self.thinking > 1:
                                self.question = True
                                self.qTime = time()
                            if self.answer is not None:
                                self.result_text.opacity = 0
                                self.result_text.text = ''
                                self.result_image.source = resource_path('imgs/'+self.answer)
                                self.result_image.opacity = 0.7
                        if self.question:
                            self.result_image.source = ''
                            self.result_image.opacity = 0
                            self.timeLimit = self.cTime - self.qTime
                            frame = self.detector.findHands(frame, draw=False)
                            RightlmList = self.detector.rightFindPosition(frame, draw=False)
                            LeftlmList = self.detector.leftFindPosition(frame, draw=False)
                            self.result_text.opacity = 1
                            self.result_text.font_style = 'H2'
                            self.result_text.text = f"{self.variables[self.lv-1]['wating']-int(self.timeLimit)}"

                            leftFinger, rightFinger = fingerQuantification(LeftlmList, RightlmList)

                            if self.timeLimit > self.variables[self.lv-1]['wating']:
                                if self.variables[self.lv-1]['rule'] == 'point':
                                    self.point_check = False
                                    if self.variables[self.lv-1]['myhand'] == 'or':
                                        if self.variables[self.lv - 1]['opponent'] == 'both':
                                            answer1, answer2 = 0, 0
                                            for i, nextact in enumerate(self.fingerShape[self.nextQuestion]):
                                                if ((len(RightlmList) > 0) and (rightFinger in nextact) and (self.nextHand == '오른손으로')) or ((len(LeftlmList) > 0) and (leftFinger in nextact) and (self.nextHand == '왼손으로')):
                                                    answer1 = self.action['point'][i]
                                                    self.point += self.action['point'][i]
                                                    self.point_check = True
                                            for i, nextact in enumerate(self.fingerShape[self.nextQuestion2]):
                                                if ((len(RightlmList) > 0) and (rightFinger in nextact) and (self.nextHand == '오른손으로')) or ((len(LeftlmList) > 0) and (leftFinger in nextact) and (self.nextHand == '왼손으로')):
                                                    answer2 = self.action['point'][i]
                                                    self.point += self.action['point'][i]
                                                    self.point_check = True
                                            self.answer = str(answer1 + answer2) + '.png'
                                        else:
                                            for i, nextact in enumerate(self.fingerShape[self.nextQuestion]):
                                                if (len(RightlmList) > 0) and (self.nextHand == '오른손으로') and (rightFinger in nextact):
                                                    self.answer = str(self.action['point'][i])+'.png'
                                                    self.point += self.action['point'][i]
                                                    self.point_check = True
                                                elif (len(LeftlmList) > 0) and (self.nextHand == '왼손으로') and (leftFinger in nextact):
                                                    self.answer = str(self.action['point'][i])+'.png'
                                                    self.point += self.action['point'][i]
                                                    self.point_check = True
                                    elif self.variables[self.lv-1]['myhand'] == 'one':
                                        if self.variables[self.lv - 1]['opponent'] == 'both':
                                            answer1, answer2 = 0, 0
                                            for i, nextact in enumerate(self.fingerShape[self.nextQuestion]):
                                                if ((len(RightlmList) > 0) and (rightFinger in nextact)) or ((len(LeftlmList) > 0) and (leftFinger in nextact)):
                                                    answer1 = self.action['point'][i]
                                                    self.point += self.action['point'][i]
                                                    self.point_check = True
                                            for i, nextact in enumerate(self.fingerShape[self.nextQuestion2]):
                                                if ((len(RightlmList) > 0) and (rightFinger in nextact)) or ((len(LeftlmList) > 0) and (leftFinger in nextact)):
                                                    answer2 = self.action['point'][i]
                                                    self.point += self.action['point'][i]
                                                    self.point_check = True
                                            self.answer = str(answer1 + answer2) + '.png'
                                        else:
                                            for i, nextact in enumerate(self.fingerShape[self.nextQuestion]):
                                                if ((len(RightlmList) > 0) and (rightFinger in nextact)) or ((len(LeftlmList) > 0) and (leftFinger in nextact)):
                                                    self.answer = str(self.action['point'][i]) + '.png'
                                                    self.point += self.action['point'][i]
                                                    self.point_check = True
                                    # 여기는 finger가 self.fingerShape[self.nextQuestion]의 몇번째 인덱스에 포함되어 있느냐에 따라 승, 무, 패를 판단하고
                                    # 해당 인덱스의 point를 self.point에 더한다.
                                    elif self.variables[self.lv-1]['myhand'] == 'both':
                                        answer1, answer2 = 0, 0
                                        for i, nextact in enumerate(self.fingerShape[self.nextQuestion2]):
                                            if (len(RightlmList) > 0) and (rightFinger in nextact):
                                                answer1 = self.action['point'][i]
                                                self.point += self.action['point'][i]
                                                self.point_check = True
                                        for i, nextact in enumerate(self.fingerShape[self.nextQuestion]):
                                            if (len(LeftlmList) > 0) and (leftFinger in nextact):
                                                answer2 = self.action['point'][i]
                                                self.point += self.action['point'][i]
                                                self.point_check = True
                                        self.answer = str(answer1 + answer2) + '.png'
                                    if not self.point_check:
                                        self.answer = 'timeout.png'
                                        self.point -= 5
                                    # 여기는 finger가 self.fingerShape[self.nextQuestion]의 몇번째 인덱스에 포함되어 있느냐에 따라 승, 무, 패를 판단하고
                                    # 해당 인덱스의 point를 self.point에 더한다.
                                else:
                                    if len(RightlmList) == 0 and len(LeftlmList) == 0:
                                        self.answer = 'timeout.png'
                                        self.point -= 1
                                    else:
                                        if self.variables[self.lv-1]['myhand'] == 'or':
                                            if (len(RightlmList) > 0) and (self.nextHand == '오른손으로') and (rightFinger in self.fingerShape[self.nextQuestion][self.nextAction]):
                                                self.answer = 'correct.png'
                                                self.point += 1
                                            elif (len(LeftlmList) > 0) and (self.nextHand == '왼손으로') and (leftFinger in self.fingerShape[self.nextQuestion][self.nextAction]):
                                                self.answer = 'correct.png'
                                                self.point += 1
                                            else:
                                                self.answer = 'wrong.png'
                                                self.point -= 1
                                        elif self.variables[self.lv-1]['myhand'] == 'one':
                                            if ((len(RightlmList) > 0) and (rightFinger in self.fingerShape[self.nextQuestion][self.nextAction])) or ((len(LeftlmList) > 0) and (leftFinger in self.fingerShape[self.nextQuestion][self.nextAction])):
                                                self.answer = 'correct.png'
                                                self.point += 1
                                            else:
                                                self.answer = 'wrong.png'
                                                self.point -= 1
                                        elif self.variables[self.lv-1]['myhand'] == 'both':
                                            if ((len(RightlmList) > 0) and (rightFinger in self.fingerShape[self.nextQuestion2][self.nextAction])) and ((len(LeftlmList) > 0) and (leftFinger in self.fingerShape[self.nextQuestion][self.nextAction])):
                                                self.answer = 'correct.png'
                                                self.point += 1
                                            else:
                                                self.answer = 'wrong.png'
                                                self.point -= 1
                                if self.variables[self.lv-1]['rule'] == 'point':
                                    if self.variables[self.lv - 1]['opponent'] == 'both' and self.variables[self.lv - 1]['myhand'] == 'both':
                                        self.totalpoint += max(self.action['point']) * 2
                                    if self.variables[self.lv - 1]['opponent'] == 'both' and (self.variables[self.lv - 1]['myhand'] == 'one' or self.variables[self.lv - 1]['myhand'] == 'or'):
                                        if self.nextQuestion == self.nextQuestion2:
                                            self.totalpoint += max(self.action['point']) * 2
                                        else:
                                            self.totalpoint += max(self.action['point']) + sorted(self.action['point'], reverse=True)[1]
                                    # 여기서 self.totalpoint에 가장 높은 point를 꾸준히 더한다.
                                else:
                                    self.totalpoint += 1
                                self.qTime = self.cTime
                                self.question = False
                                self.sTime = self.cTime
                        if self.variables[self.lv-1]['opponent'] == 'both':
                            self.gameimage_left.source = resource_path('imgs/rockscissorpaper/' + str(self.nextQuestion) + '_left.png')
                            self.gameimage_right.source = resource_path('imgs/rockscissorpaper/' + str(self.nextQuestion2) + '_right.png')
                        else:
                            if self.nextOpponentHand == 'left':
                                self.gameimage_left.source = resource_path('imgs/rockscissorpaper/' + str(self.nextQuestion) + '_left.png')
                                self.gameimage_right.source = ''
                            if self.nextOpponentHand == 'right':
                                self.gameimage_right.source = resource_path('imgs/rockscissorpaper/' + str(self.nextQuestion) + '_right.png')
                                self.gameimage_left.source = ''
                        self.quest_hand.text = f'{self.nextHand}'
                        if self.variables[self.lv-1]['rule'] == 'point':
                            mission_text = ''
                            for text, point in zip(['승: ', '무: ', '패: '], self.action['point']):
                                mission_text += text + str(point) + ' | '
                            mission_text = mission_text[:-3]
                        else:
                            mission_text = self.action[self.variables[self.lv-1]['rule']][self.nextAction]
                        self.mission.text = str(mission_text)
                        self.gameinfo.text = f"점수: {int(self.point)}\n남은 시간: {self.variables[self.lv-1]['time']+3-int(self.playtime)}/{self.variables[self.lv-1]['time']}"
                        self.gameinfo.font_style = 'H6'
                    else:
                        if self.result:
                            if int(self.point) / int(self.totalpoint) > 0.9:
                                if self.lv == len(self.variables):
                                    result_description = '이미 최고 레벨에 도달하셨습니다! 대단하시군요!'
                                else:
                                    self.lv += 1
                                    result_description = '축하드립니다! 승급하셨습니다!'
                            elif int(self.point) / int(self.totalpoint) > 0.5:
                                result_description = '잘하셨습니다! 다음엔 더 잘해서 꼭 승급해보세요!'
                            else:
                                if self.lv == 1:
                                    result_description = '더 쉬운 레벨이 없네요...열심히 연습해서 레벨을 올려보아요!'
                                else:
                                    result_description = '아쉽네요! 강등되셨습니다...다음번엔 잘해서 다시 승급해보자구요!'
                                    self.lv -= 1
                            self.alert = MDDialog(
                                text=f"[font=fonts/NotoSansKR-Regular.otf][size=18sp]결과\n\n"
                                     f"[/size][size=16sp]점수: [color=#440088FF]{int(self.point)}점[/color]\n"
                                     f"정확도: [color=#440088FF]{int(int(self.point)/int(self.totalpoint) * 100)}%[/color]\n\n"
                                     f"[color=#123456FF]{result_description}[/color][/size][/font]",
                                buttons=[
                                    MDFlatButton(
                                        text="확인", font_name='fonts/NotoSansKR-Regular.otf', on_release=self.close_dialog,
                                        opacity=0.5
                                    )
                                ],
                            )
                            self.alert.open()
                            self.result = False
                buf1 = cv2.flip(frame, -1)
                buf = buf1.tostring()
                self.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                self.texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.screen.ids.rockscissorpaper.ids.video.texture = self.texture
            else:
                self.pTime = time()
                self.qTime = self.pTime
                self.sTime = time()
