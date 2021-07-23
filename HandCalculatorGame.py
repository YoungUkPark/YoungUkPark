import cv2
from time import time
import random
from handDetector import handDetector
from handDetector import fingerQuantification
from kivy.uix.screenmanager import SlideTransition
from kivy.graphics.texture import Texture
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import sys, os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class HandCalculatorGame:
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
        self.playtime = 0
        self.answer_check = 0
        self.question = False
        self.blank_position = None
        self.gameinfo = screen.ids.handcalculator.ids.gameinfo
        self.mission = screen.ids.handcalculator.ids.mission
        self.gameimage_left = screen.ids.handcalculator.ids.gameimage_left
        self.gameimage_right = screen.ids.handcalculator.ids.gameimage_right
        self.quest_hand = screen.ids.handcalculator.ids.quest_hand
        self.result_image = screen.ids.handcalculator.ids.result_image
        self.result_text = screen.ids.handcalculator.ids.result_text
        self.text_left = screen.ids.handcalculator.ids.text_left
        self.text_right = screen.ids.handcalculator.ids.text_right
        self.detector = handDetector(detectionCon=0.75)
        self.result = True
        self.fingerPoint = {1: [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 1, 0, 0], [1, 1, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
                       2: [[1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [1, 1, 1, 0, 0], [0, 0, 1, 1, 1], [1, 1, 1, 1, 0]],
                       3: [[0, 0, 0, 1, 0], [1, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 0, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1]]}
        self.variables = [
            {'time': 10, 'wating': 4, 'rule': 'plus', 'blank': False, 'myhand': 'one', 'description': '5초 안에 산수 식의 정답을 편한 손으로 나타내주세요!'},  # 1
            {'time': 10, 'wating': 2, 'rule': 'plus', 'blank': False, 'myhand': 'one', 'description': '3초 안에 산수 식의 정답을 편한 손으로 나타내주세요!'},  # 2
            {'time': 10, 'wating': 4, 'rule': 'p_m', 'blank': False, 'myhand': 'one', 'description': '5초 안에 산수 식의 정답을 편한 손으로 나타내주세요!'},  # 3
            {'time': 10, 'wating': 2, 'rule': 'p_m', 'blank': False, 'myhand': 'one', 'description': '3초 안에 산수 식의 정답을 편한 손으로 나타내주세요!'},  # 4
            {'time': 10, 'wating': 4, 'rule': 'plus', 'blank': True, 'myhand': 'one', 'description': '5초 안에 빈칸에 들어갈 답을 편한 손으로 나타내주세요!'},  # 5
            {'time': 10, 'wating': 2, 'rule': 'plus', 'blank': True, 'myhand': 'one', 'description': '3초 안에 빈칸에 들어갈 답을 편한 손으로 나타내주세요!'},  # 6
            {'time': 10, 'wating': 4, 'rule': 'p_m', 'blank': True, 'myhand': 'one', 'description': '5초 안에 빈칸에 들어갈 답을 편한 손으로 나타내주세요!'},  # 7
            {'time': 10, 'wating': 2, 'rule': 'p_m', 'blank': True, 'myhand': 'one', 'description': '3초 안에 빈칸에 들어갈 답을 편한 손으로 나타내주세요!'},  # 8
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': False, 'myhand': 'one', 'description': '5초 안에 산수 식의 정답을 편한 손으로 나타내주세요!'},  # 9
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': False, 'myhand': 'one', 'description': '3초 안에 산수 식의 정답을 편한 손으로 나타내주세요!'},  # 10
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': True, 'myhand': 'one', 'description': '5초 안에 빈칸에 들어갈 답을 편한 손으로 나타내주세요!'},  # 11
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': True, 'myhand': 'one', 'description': '3초 안에 빈칸에 들어갈 답을 편한 손으로 나타내주세요!'},  # 12
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': False, 'myhand': 'or', 'description': '5초 안에 산수 식의 정답을 화면에 나타난 손으로 나타내주세요!'},  # 13
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': False, 'myhand': 'or', 'description': '3초 안에 산수 식의 정답을 화면에 나타난 손으로 나타내주세요!'},  # 14
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': True, 'myhand': 'or', 'description': '5초 안에 빈칸에 들어갈 답을 화면에 나타난 손으로 나타내주세요!'},  # 15
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': True, 'myhand': 'or', 'description': '3초 안에 빈칸에 들어갈 답을 화면에 나타난 손으로 나타내주세요!'},  # 16
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': False, 'myhand': 'both', 'description': '5초 안에 산수 식의 정답을 양손으로 나타내주세요!\n왼손은 십의 자리, 오른손은 일의 자리입니다.'},  # 17
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': False, 'myhand': 'both', 'description': '3초 안에 산수 식의 정답을 양손으로 나타내주세요!\n왼손은 십의 자리, 오른손은 일의 자리입니다.'},  # 18
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': True, 'myhand': 'both', 'description': '5초 안에 빈칸에 들어갈 답을 양손으로 나타내주세요!\n왼손은 십의 자리, 오른손은 일의 자리입니다.'},  # 19
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': True, 'myhand': 'both', 'description': '3초 안에 빈칸에 들어갈 답을 양손으로 나타내주세요!\n왼손은 십의 자리, 오른손은 일의 자리입니다.'},  # 20
            {'time': 10, 'wating': 4, 'rule': 'same', 'blank': False, 'myhand': 'or', 'description': '5초 안에 화면에 나타난 손 모양을 따라해보세요!'},  # 21
            {'time': 10, 'wating': 2, 'rule': 'same', 'blank': False, 'myhand': 'or', 'description': '3초 안에 화면에 나타난 손 모양을 따라해보세요!'},  # 22
            {'time': 10, 'wating': 4, 'rule': 'same', 'blank': False, 'myhand': 'both', 'description': '5초 안에 양손 모두 화면에 나타난 손 모양을 따라해보세요!'},  # 23
            {'time': 10, 'wating': 2, 'rule': 'same', 'blank': False, 'myhand': 'both', 'description': '3초 안에 양손 모두 화면에 나타난 손 모양을 따라해보세요!'},  # 24
            {'time': 10, 'wating': 4, 'rule': 'same', 'blank': True, 'myhand': 'or', 'description': '5초 안에 화면에 나타난 손 모양을 따라해보세요!'},  # 25
            {'time': 10, 'wating': 2, 'rule': 'same', 'blank': True, 'myhand': 'or', 'description': '3초 안에 화면에 나타난 손 모양을 따라해보세요!'},  # 26
            {'time': 10, 'wating': 4, 'rule': 'same', 'blank': True, 'myhand': 'both', 'description': '5초 안에 양손 모두 화면에 나타난 손 모양을 따라해보세요!'},  # 27
            {'time': 10, 'wating': 2, 'rule': 'same', 'blank': True, 'myhand': 'both', 'description': '3초 안에 양손 모두 화면에 나타난 손 모양을 따라해보세요!'},  # 28
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': True, 'myhand': 'one', 'description': '5초 안에 최대한 많은 점수를 내세요!\n손모양이 특이할수록 높은 점수를 받습니다'},  # 29
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': True, 'myhand': 'one', 'description': '3초 안에 최대한 많은 점수를 내세요!\n손모양이 특이할수록 높은 점수를 받습니다'},  # 30
            {'time': 10, 'wating': 4, 'rule': 'cal', 'blank': True, 'myhand': 'or', 'description': '5초 안에 화면에 나타난 손으로 최대한 많은 점수를 내세요!\n손모양이 특이할수록 높은 점수를 받습니다'},  # 31
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': True, 'myhand': 'or', 'description': '3초 안에 화면에 나타난 손으로 최대한 많은 점수를 내세요!\n손모양이 특이할수록 높은 점수를 받습니다'},  # 32
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': True, 'myhand': 'both', 'description': '3초 안에 화면에 양손으로 최대한 많은 점수를 내세요!\n손모양이 특이할수록 높은 점수를 받습니다\n왼손은 십의 자리, 오른손은 일의 자리입니다.'},  # 33
            {'time': 10, 'wating': 2, 'rule': 'cal', 'blank': True, 'myhand': 'both', 'description': '3초 안에 화면에 양손으로 최대한 많은 점수를 내세요!\n손모양이 특이할수록 높은 점수를 받습니다\n왼손은 십의 자리, 오른손은 일의 자리입니다.'}  # 34
        ]
        # rule : 'same'/'match'/'mission'/'point'
        # myhand/opponent : 'one'/'or'/'both'
        if self.lv == 0:
            self.lv = 1
        if self.variables[self.lv - 1]['myhand'] == 'one':
            self.myHand = ['편한손']
        elif self.variables[self.lv - 1]['myhand'] == 'or':
            self.myHand = ['오른손', '왼손']
        elif self.variables[self.lv - 1]['myhand'] == 'both':
            self.myHand = ['양손']
        if self.variables[self.lv - 1]['rule'] == 'cal' or self.variables[self.lv - 1]['rule'] == 'same':
            self.sign = ['+', '-', '/', 'x']
        elif self.variables[self.lv - 1]['rule'] == 'plus':
            self.sign = ['+']
        elif self.variables[self.lv - 1]['rule'] == 'p_m':
            self.sign = ['+', '-']
        self.questionMake()
        self.description_screen(self.variables[self.lv - 1]['description'])
        self.ready = False
        self.screen.ids.handcalculator.ids.gamebar.script = str(self.lv) + '  [font=fonts/NotoSansKR-Regular.otf][size=15sp]' + self.variables[self.lv - 1]['description'] + '[/size][/font]'
        self.nextHand = random.choice(self.myHand)
        self.gameinfo.text = f"점수: {int(self.point)}\n남은 시간: {self.variables[self.lv-1]['time']-int(self.playtime)}/{self.variables[self.lv-1]['time']}"
        self.mission.text = ''
        self.quest_hand.text = ''
        self.gameimage_left.source = ''
        self.gameimage_right.source = ''
        if self.variables[self.lv-1]['myhand'] == 'both' and self.variables[self.lv-1]['rule'] != 'same':
            self.text_left.text = '십의 자리'
            self.text_left.opacity = 1
            self.gameimage_left.opacity = 0
            self.text_right.text = '일의 자리'
            self.text_right.opacity = 1
            self.gameimage_right.opacity = 0
        self.fingers = self.making_fingerlist()
        if self.variables[self.lv - 1]['rule'] == 'same':
            self.finger = random.choice(self.fingers[self.nextQuestion])
            if self.variables[self.lv - 1]['myhand'] == 'both':
                self.finger2 = random.choice(self.fingers[self.nextQuestion2])

    def making_fingerlist(self):
        fingers_str = []
        for i in range(32):
            temp = str(bin(i))[2:]
            zero = ''
            for j in range(5 - len(temp)):
                zero += '0'
            fingers_str.append(zero + temp)
        fingers_list = []
        for finger in fingers_str:
            finger_list = []
            for bi in finger:
                finger_list.append(int(bi))
            fingers_list.append(finger_list)

        fingers = [[] for i in range(6)]
        for finger in fingers_list:
            str_finger = ''
            for bi in finger:
                str_finger += str(bi)
            fingers[sum(finger)].append([str_finger, finger])

        return fingers

    def questionMake(self):
        if self.variables[self.lv-1]['myhand'] == 'both':
            self.nextQuestion = random.randint(0, 5)
            self.nextQuestion2 = random.randint(0, 5)
            correct_answer = self.nextQuestion * 10 + self.nextQuestion2
        else:
            self.nextQuestion = random.randint(0, 5)
            correct_answer = self.nextQuestion
        self.nextNumber = random.randint(0, 10)
        self.nextSign = random.choice(self.sign)
        if self.variables[self.lv-1]['blank']:
            self.blank_position = random.randint(0, 2)
            if self.nextSign == '+':
                if self.blank_position == 2:
                    self.theNumber = correct_answer - self.nextNumber
                else:
                    self.theNumber = self.nextNumber - correct_answer
            elif self.nextSign == '-':
                self.theNumber = self.nextNumber + correct_answer
            elif self.nextSign == '/':
                if self.blank_position == 0:
                    while True:
                        if self.nextNumber == 0:
                            self.nextNumber = random.randint(1, 5)
                        self.theNumber = correct_answer / self.nextNumber
                        if int(self.theNumber) == self.theNumber:
                            self.theNumber = int(self.theNumber)
                            break
                        self.nextNumber = random.randint(0, 5)
                else:
                    self.theNumber = self.nextNumber * correct_answer
            elif self.nextSign == 'x':
                if self.blank_position == 1:
                    self.theNumber = self.nextNumber
                    self.nextNumber = self.theNumber * correct_answer
                elif self.blank_position == 0:
                    self.theNumber = self.nextNumber
                    self.nextNumber = correct_answer * self.theNumber
                elif self.blank_position == 2:
                    while True:
                        if self.nextNumber == 0:
                            self.nextNumber = random.randint(1, 5)
                        self.theNumber = correct_answer / self.nextNumber
                        if int(self.theNumber) == self.theNumber:
                            self.theNumber = int(self.theNumber)
                            break
                        self.nextNumber = random.randint(0, 5)
        else:
            if self.nextSign == '+':
                self.theNumber = correct_answer - self.nextNumber
            elif self.nextSign == '-':
                self.theNumber = correct_answer + self.nextNumber
            elif self.nextSign == '/':
                if self.nextNumber == 0:
                    self.nextNumber = random.randint(1, 10)
                self.theNumber = self.nextNumber * correct_answer
            elif self.nextSign == 'x':
                while True:
                    if self.nextNumber == 0:
                        self.nextNumber = random.randint(1, 5)
                    self.theNumber = correct_answer / self.nextNumber
                    if int(self.theNumber) == self.theNumber:
                        self.theNumber = int(self.theNumber)
                        break
                    self.nextNumber = random.randint(1, 5)

    def description_screen(self, description):
        self.alert = MDDialog(
            buttons=[
                MDFlatButton(
                    text="확인", font_name='fonts/NotoSansKR-Regular.otf', text_color=self.app.theme_cls.primary_color,
                    on_release=self.ready_button
                )
            ],
        )
        self.alert.text = f"[font=fonts/NotoSansKR-Regular.otf]{description}\n\n\n[color=#881111FF]손바닥이 카메라를 향하도록 내야합니다![/color]\n\n[color=#111111FF]준비 되셨으면 확인을 눌러주세요![/color][/font]"
        self.alert.open()

    def ready_button(self, inst):
        self.alert.dismiss()
        self.ready = True

    def close_dialog(self, inst):
        self.alert.dismiss()
        self.app.game_end_screen('handcalculator')
        self.app.user_lv['handcalculator'] = self.lv
        self.screen.ids.home.ids.handcalculator_card.text = 'Level: ' + str(self.lv)

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
                    self.qTime = self.cTime
                else:
                    if self.playtime <= self.variables[self.lv-1]['time'] + 3:
                        self.result_image.source = ''
                        self.result_image.opacity = 0
                        if not self.question:
                            self.answer_check = self.cTime - self.sTime
                            if self.answer_check < 1:
                                if self.answer is not None:
                                    self.result_text.opacity = 0
                                    self.result_text.text = ''
                                    self.result_image.source = resource_path('imgs/' + self.answer)
                                    self.result_image.opacity = 0.7
                            if self.answer_check > 1:
                                self.question = True
                                self.qTime = time()
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
                                if len(RightlmList) == 0 and len(LeftlmList) == 0:
                                    self.answer = 'timeout.png'
                                    self.point -= 1
                                else:
                                    if self.variables[self.lv - 1]['rule'] == 'same':
                                        if (len(RightlmList) > 0) and (self.nextHand == '오른손') and rightFinger == self.finger[1]: # 여기서부터 다시하기
                                            self.answer = 'correct.png'
                                            if rightFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif rightFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif rightFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            else:
                                                self.point += 4
                                        elif (len(LeftlmList) > 0) and (self.nextHand == '왼손') and leftFinger == self.finger[1]:
                                            self.answer = 'correct.png'
                                            if leftFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif leftFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif leftFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            else:
                                                self.point += 4
                                        elif ((len(LeftlmList) > 0) or (len(RightlmList) > 0)) and (self.nextHand == '편한손') and (leftFinger == self.finger[1] or rightFinger == self.finger[1]):
                                            self.answer = 'correct.png'
                                            if leftFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif leftFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif leftFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            elif rightFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif rightFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif rightFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            else:
                                                self.point += 4
                                        elif ((len(LeftlmList) > 0) or (len(RightlmList) > 0)) and (self.nextHand == '양손') and (leftFinger == self.finger[1] or rightFinger == self.finger[1]):
                                            self.answer = 'correct.png'
                                            if (len(LeftlmList) > 0):
                                                if leftFinger in self.fingerPoint[1]:
                                                    self.point += 1
                                                elif leftFinger in self.fingerPoint[2]:
                                                    self.point += 2
                                                elif leftFinger in self.fingerPoint[3]:
                                                    self.point += 3
                                                else:
                                                    self.point += 4
                                            if (len(RightlmList) > 0):
                                                if rightFinger in self.fingerPoint[1]:
                                                    self.point += 1
                                                elif rightFinger in self.fingerPoint[2]:
                                                    self.point += 2
                                                elif rightFinger in self.fingerPoint[3]:
                                                    self.point += 3
                                                else:
                                                    self.point += 4
                                        else:
                                            self.answer = 'wrong.png'
                                            self.point -= 1
                                            if self.variables[self.lv]['myhand'] == 'both':
                                                self.point -= 1
                                    else:
                                        if (len(RightlmList) > 0) and (self.nextHand == '오른손') and self.nextQuestion == sum(rightFinger):
                                            self.answer = 'correct.png'
                                            if rightFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif rightFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif rightFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            else:
                                                self.point += 4
                                        elif (len(LeftlmList) > 0) and (self.nextHand == '왼손') and self.nextQuestion == sum(leftFinger):
                                            self.answer = 'correct.png'
                                            if leftFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif leftFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif leftFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            else:
                                                self.point += 4
                                        elif ((len(LeftlmList) > 0) or (len(RightlmList) > 0)) and (self.nextHand == '편한손') and (self.nextQuestion == sum(leftFinger) or self.nextQuestion == sum(rightFinger)):
                                            self.answer = 'correct.png'
                                            if leftFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif leftFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif leftFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            elif rightFinger in self.fingerPoint[1]:
                                                self.point += 1
                                            elif rightFinger in self.fingerPoint[2]:
                                                self.point += 2
                                            elif rightFinger in self.fingerPoint[3]:
                                                self.point += 3
                                            else:
                                                self.point += 4
                                        elif ((len(LeftlmList) > 0) or (len(RightlmList) > 0)) and (self.nextHand == '양손') and (self.nextQuestion == sum(leftFinger) and self.nextQuestion2 == sum(rightFinger)):
                                            self.answer = 'correct.png'
                                            if (len(LeftlmList) > 0):
                                                if leftFinger in self.fingerPoint[1]:
                                                    self.point += 1
                                                elif leftFinger in self.fingerPoint[2]:
                                                    self.point += 2
                                                elif leftFinger in self.fingerPoint[3]:
                                                    self.point += 3
                                                else:
                                                    self.point += 4
                                            if (len(RightlmList) > 0):
                                                if rightFinger in self.fingerPoint[1]:
                                                    self.point += 1
                                                elif rightFinger in self.fingerPoint[2]:
                                                    self.point += 2
                                                elif rightFinger in self.fingerPoint[3]:
                                                    self.point += 3
                                                else:
                                                    self.point += 4
                                        else:
                                            self.answer = 'wrong.png'
                                            self.point -= 1
                                            if self.variables[self.lv]['myhand'] == 'both':
                                                self.point -= 1

                                self.totalpoint += 1
                                self.question = False
                                self.questionMake()

                                if self.variables[self.lv - 1]['rule'] == 'same':
                                    self.finger = random.choice(self.fingers[self.nextQuestion])
                                    if self.variables[self.lv - 1]['myhand'] == 'both':
                                        self.finger2 = random.choice(self.fingers[self.nextQuestion2])
                                self.nextHand = random.choice(self.myHand)
                                self.qTime = self.cTime
                                self.sTime = self.cTime
                            if self.variables[self.lv - 1]['rule'] == 'same':
                                if self.variables[self.lv-1]['myhand'] == 'both':
                                    self.gameimage_left.source = resource_path('imgs/handcalculator/' + self.finger[0] + '_left.png')
                                    self.gameimage_left.opacity = 1
                                    self.text_left.opacity = 0
                                    self.gameimage_right.source = resource_path('imgs/handcalculator/' + self.finger2[0] + '_right.png')
                                    self.gameimage_right.opacity = 1
                                    self.text_right.opacity = 0
                                else:
                                    if self.nextHand == '왼손':
                                        self.gameimage_left.source = resource_path('imgs/handcalculator/' + self.finger[0] + '_left.png')
                                        self.gameimage_right.source = ''
                                        self.gameimage_left.opacity = 1
                                        self.text_left.opacity = 0
                                    if self.nextHand == '오른손':
                                        self.gameimage_right.source = resource_path('imgs/handcalculator/' + self.finger[0] + '_right.png')
                                        self.gameimage_left.source = ''
                                        self.gameimage_right.opacity = 1
                                        self.text_right.opacity = 0
                            if self.variables[self.lv-1]['blank'] and self.blank_position == 0:
                                self.mission.text = f'□ {self.nextSign} {self.theNumber} = {self.nextNumber}'
                            elif self.variables[self.lv-1]['blank'] and self.blank_position == 1:
                                self.mission.text = f'{self.theNumber} {self.nextSign} □ = {self.nextNumber}'
                            else:
                                self.mission.text = f'{self.theNumber} {self.nextSign} {self.nextNumber} = □'
                            self.quest_hand.text = f'{self.nextHand}'

                        self.gameinfo.text = f"점수: {int(self.point)}\n남은 시간: {self.variables[self.lv-1]['time']+3-int(self.playtime)}/{self.variables[self.lv-1]['time']}"
                        self.gameinfo.font_style = 'H6'
                    else:
                        if self.result:
                            if self.lv > 28:
                                self.totalpoint *= 2
                            if self.variables[self.lv]['myhand'] == 'both':
                                self.totalpoint *= 2
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
                                     f"[/size][size=16sp]목표점수: [color=#440088FF]{self.totalpoint}[/color] 점\n"
                                     f"달성점수: [color=#884400FF]{self.point}점[/color]\n"
                                     f"달성비율: [color=#440088FF]{int(int(self.point)/int(self.totalpoint) * 100)}%[/color]\n\n"
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
                self.screen.ids.handcalculator.ids.video.texture = self.texture
            else:
                self.pTime = time()
                self.qTime = self.pTime
                self.sTime = time()
