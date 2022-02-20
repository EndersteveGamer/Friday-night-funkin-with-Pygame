from pygame import *
import json
from random import *
import time as Time
import cProfile
import sys

Inst = None
Vocals = None
chart = None
misses = 0
health = 50
BG = None
opponentAnimation = ["Up", -10]
playerAnimation = ["Up", -10]
hasPlayedMicDrop = False


def Main_game(musicName, speed, playAs, noDying, arrowSkinID, keybinds):
    global Inst
    global Vocals
    global chart
    global misses
    global health
    global BG
    global opponentAnimation
    global playerAnimation
    global options
    global hasPlayedMicDrop
    misses = 0
    health = 50

    init()

    K_a = keybinds[0]
    K_s = keybinds[1]
    K_w = keybinds[2]
    K_d = keybinds[3]
    K_LEFT = keybinds[4]
    K_DOWN = keybinds[5]
    K_UP = keybinds[6]
    K_RIGHT = keybinds[7]

    # region loading
    # region screen and loading screen
    screen = display.set_mode((0, 0), FULLSCREEN)
    mouse.set_visible(False)
    middleScreen = (display.Info().current_w // 2, display.Info().current_h // 2)

    def loadingscreen(progress):
        screen.fill((0, 0, 0))
        temp = font.SysFont("Comic Sans MS", 100).render("Loading...", 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1])
        screen.blit(temp, temp1)

        draw.line(screen, (255, 255, 255), (95, display.Info().current_h - 95),
                  (display.Info().current_w - 95, display.Info().current_h - 95), 3)
        draw.line(screen, (255, 255, 255), (95, display.Info().current_h - 155),
                  (display.Info().current_w - 95, display.Info().current_h - 155), 3)
        draw.line(screen, (255, 255, 255), (95, display.Info().current_h - 95), (95, display.Info().current_h - 155), 3)
        draw.line(screen, (255, 255, 255), (display.Info().current_w - 95, display.Info().current_h - 95),
                  (display.Info().current_w - 95, display.Info().current_h - 155), 3)
        if progress > 0:
            temp = (display.Info().current_w - 200) / 3
            draw.rect(screen, (255, 255, 255), Rect(100, display.Info().current_h - 150, temp * progress, 50))

        display.flip()

    loadingscreen(0)
    # endregion

    # region variables
    sys.setrecursionlimit(1000000)
    useMustHitSection = False
    clock = time.Clock()
    if 690 >= display.Info().current_w - 690:
        singlePlayer = True
    else:
        singlePlayer = False

    fpsQuality = 100
    fpsList = []
    fpsTime = Time.time()

    accuracy = 0
    accuracyDisplayTime = 0
    showAccuracy = False
    accuracyIndicator = ""
    accuracyIndicatorTime = Time.time()
    accuracyPercentList = []

    Font40 = font.SysFont("Comic Sans MS", 40)

    longNotesChart = []

    bpm = 240 / 100

    opponentHitTimes = [-10 for k in range(4)]
    opponentAnimation = ["Up", -10]
    playerAnimation = ["Up", -10]

    try:
        modifications = json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["modifications"]
    except:
        modifications = []

    hasPlayedMicDrop = False
    # endregion

    # region images loading
    # region load images
    arrowsSkins = [
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Arrows\left.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(image.load("assets\Images\ArrowStyles\{0}\Arrows\down.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150)),
        transform.scale(image.load("assets\Images\ArrowStyles\{0}\Arrows/up.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Arrows/right.png".format(arrowSkinID)).convert_alpha(),
            (150, 150))]

    pressedArrowsSkins = [
        transform.scale(
            image.load(
                "assets\Images\ArrowStyles\{0}\Strum lines\Pressed\left.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load(
                "assets\Images\ArrowStyles\{0}\Strum lines\Pressed\down.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Strum lines\Pressed/up.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load(
                "assets\Images\ArrowStyles\{0}\Strum lines\Pressed/right.png".format(arrowSkinID)).convert_alpha(),
            (150, 150))]

    accuracyIndicatorImages = [
        transform.scale(image.load("assets\Images\Accuracy indicator\sick.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets\Images\Accuracy indicator\good.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets\Images\Accuracy indicator/bad.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets\Images\Accuracy indicator\shit.png").convert_alpha(), (225, 100))]

    greyArrow = [
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Strum lines\Static\left.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Strum lines\Static\down.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Strum lines\Static/up.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(image.load(
            "assets\Images\ArrowStyles\{0}\Strum lines\Static/right.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150))]

    longNotesImg = [
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\Middle\left.png".format(arrowSkinID)).convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\Middle\down.png".format(arrowSkinID)).convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\Middle/up.png".format(arrowSkinID)).convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\Middle/right.png".format(arrowSkinID)).convert_alpha(),
            (52, 46))]

    longNotesEnd = [
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\End\left.png".format(arrowSkinID)).convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\End\down.png".format(arrowSkinID)).convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\End/up.png".format(arrowSkinID)).convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets\Images\ArrowStyles\{0}\Long notes\End/right.png".format(arrowSkinID)).convert_alpha(),
            (52, 46))]

    try:
        backgroundName = json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["stage"]
    except:
        backgroundName = "None"

    if backgroundName != "None":
        Background = []
        for k in range(
                json.load(open("assets\Images\Backgrounds\{0}\stageData.json".format(backgroundName)))["numFrames"]):
            if not display.Info().current_w / display.Info().current_h == 1920 / 1080:
                Background.append(transform.scale(
                    image.load("assets\Images/Backgrounds\{0}\Background{1}.png".format(backgroundName, k)),
                    (1920, 1080)).convert_alpha())
            else:
                Background.append(transform.scale(
                    image.load("assets\Images\Backgrounds\{0}\Background{1}.png".format(backgroundName, k)),
                    (display.Info().current_w, display.Info().current_h)).convert_alpha())
    else:
        Background = [Font40.render("", 1, (255, 255, 255))]
    BGrect = Background[0].get_rect()
    BGrect.center = (middleScreen[0], middleScreen[1])

    BFdead = image.load("assets\Images\Death screen\BF dead.png").convert_alpha()

    # endregion

    # region create image rect
    accuracyIndicatorRect = accuracyIndicatorImages[0].get_rect()
    accuracyIndicatorRect.center = (middleScreen[0], middleScreen[1] - 75)

    arrowRect = arrowsSkins[0].get_rect()

    deathScreenRect = BFdead.get_rect()
    deathScreenRect.midbottom = (middleScreen[0], display.Info().current_h - 50)
    # endregion

    musicList = json.load(open("assets/MusicList.json"))["musics"]

    loadingscreen(1)

    # endregion

    # region music and chart loading
    deathScreenMusic = mixer.Sound("assets\Images\Death screen\gameOver.ogg")
    deathScreenMusicEnd = mixer.Sound("assets\Images\Death screen\gameOverEnd.ogg")
    deathScreenMusicStart = mixer.Sound("assets\Images\Death screen\micDrop.ogg")

    def open_file(music):
        global Inst
        global Vocals
        global chart
        Inst = mixer.Sound("assets\Musics\{0}\Inst.ogg".format(music))
        Vocals = mixer.Sound("assets\Musics\{0}\Voices.ogg".format(music))
        try:
            chart = json.load(open("assets\Musics\{0}\chart.json".format(music)))["song"]["notes"]
        except:
            chart = {"song": json.load(open("assets\Musics\{0}\chart.json".format(music)))}
            json.dump(chart, open("assets\Musics\{0}\chart.json".format(music), "w"))
            chart = chart["song"]["notes"]
        try:
            bpm = json.load(open("assets\Musics\{0}\chart.json".format(music)))["song"]["bpm"]
            bpm = 240 / bpm
        except:
            bpm = 240 / 100

    def play(music=False):
        if not music:
            open_file(musicList[randint(0, len(musicList) - 1)])
        else:
            open_file(music)

    play(musicName)

    temp1 = Inst.get_length()
    temp2 = Vocals.get_length()
    if temp1 > temp2:
        musicLen = temp1
    else:
        musicLen = temp2

    loadingscreen(2)

    # endregion

    # region chart managment
    class Note:
        def __init__(self, pos, column, side, length):
            self.pos = pos
            self.column = column
            self.side = side
            self.length = length

    class LongNote:
        def __init__(self, pos, column, side, isEnd):
            self.pos = pos
            self.column = column
            self.side = side
            self.isEnd = isEnd

    # region tests if chart uses mustHitSection
    notesChart = []

    for section in chart:
        if not section["mustHitSection"]:
            useMustHitSection = True
    # endregion

    # region create notes
    # Column meaning:
    #   If not useMustHitSection:
    #       0 = player left
    #       1 = player down
    #       2 = player up
    #       3 = player right
    #       4 = opponent down
    #       5 = opponent left
    #       6 = opponent up
    #       7 = opponent right
    #
    #   If useMustHitSection:
    #       If mustHit:
    #           0 = player left
    #           1 = player down
    #           2 = player up
    #           3 = player right
    #           4 = opponent left
    #           5 = opponent down
    #           6 = opponent up
    #           7 = opponent right
    #       If not mustHit:
    #           0 = opponent down
    #           1 = opponent left
    #           2 = opponent up
    #           3 = opponent right
    #           4 = player left
    #           5 = player down
    #           6 = player up
    #           7 = player right

    if playAs == "Player":
        tempPlayAs = ["Player", "Opponent"]
    else:
        tempPlayAs = ["Opponent", "Player"]
    for section in chart:
        if not useMustHitSection:
            tempMustHit = True
        else:
            tempMustHit = section["mustHitSection"]
        for note in section["sectionNotes"]:
            tempUser = ""
            tempDirection = ""
            if type(note[2]) == int or type(note[2]) == float:
                if not useMustHitSection:
                    if 3 >= note[1] >= 0:
                        tempUser = tempPlayAs[0]
                    elif 7 >= note[1] >= 4:
                        tempUser = tempPlayAs[1]
                    if note[1] == 0 or note[1] == 5:
                        tempDirection = "Left"
                    if note[1] == 1 or note[1] == 4:
                        tempDirection = "Down"
                    if note[1] == 2 or note[1] == 6:
                        tempDirection = "Up"
                    if note[1] == 3 or note[1] == 7:
                        tempDirection = "Right"
                if useMustHitSection:
                    if tempMustHit:
                        if 3 >= note[1] >= 0:
                            tempUser = tempPlayAs[0]
                        if 7 >= note[1] >= 4:
                            tempUser = tempPlayAs[1]
                        if note[1] == 0 or note[1] == 4:
                            tempDirection = "Left"
                        if note[1] == 1 or note[1] == 5:
                            tempDirection = "Down"
                        if note[1] == 2 or note[1] == 6:
                            tempDirection = "Up"
                        if note[1] == 3 or note[1] == 7:
                            tempDirection = "Right"
                    if not tempMustHit:
                        if 3 >= note[1] >= 0:
                            tempUser = tempPlayAs[1]
                        if 7 >= note[1] >= 4:
                            tempUser = tempPlayAs[0]
                        if note[1] == 1 or note[1] == 5:
                            tempDirection = "Down"
                        if note[1] == 0 or note[1] == 4:
                            tempDirection = "Left"
                        if note[1] == 2 or note[1] == 6:
                            tempDirection = "Up"
                        if note[1] == 3 or note[1] == 7:
                            tempDirection = "Right"
                notesChart.append(Note(note[0], tempDirection, tempUser, note[2]))
    # endregion

    # region sort notes and create long notes
    notesChart.sort(key=lambda s: s.pos)

    longNotesLen = 42 // speed
    for note in notesChart:
        if note.length >= longNotesLen > 0 and int(round(note.length // longNotesLen)):
            for k in range(1, int(round(note.length // longNotesLen))):
                longNotesChart.append(LongNote(note.pos + k * longNotesLen, note.column, note.side, False))
            longNotesChart.append(
                LongNote(note.pos + (note.length // longNotesLen) * longNotesLen, note.column, note.side, True))

    longNotesChart.sort(key=lambda s: s.pos)

    loadingscreen(3)

    # endregion
    # endregion

    # region characters
    class Character:
        def __init__(self, name, characterNum):
            if name != "None":
                if playAs == "Opponent":
                    if characterNum == 1:
                        temp = 2
                    else:
                        temp = 1
                else:
                    temp = characterNum
                self.size = \
                json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["character{0}".format(temp)][
                    "size"]
                self.texture = [image.load("assets\Images\Characters\{0}\left.png".format(name)).convert_alpha(),
                                image.load("assets\Images\Characters\{0}\down.png".format(name)).convert_alpha(),
                                image.load("assets\Images\Characters\{0}/up.png".format(name)).convert_alpha(),
                                image.load("assets\Images\Characters\{0}/right.png".format(name)).convert_alpha(),
                                image.load("assets\Images\Characters\{0}\static.png".format(name)).convert_alpha()]
                self.pos = \
                json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["character{0}".format(temp)]["pos"]
                for tab in self.pos:
                    for k in range(2):
                        if tab[k] == "centered":
                            tab[k] = middleScreen[k]
                        elif type(tab[k]) == str and len(tab[k]) > 9:
                            temp = ""
                            for i in range(9):
                                temp = "{0}{1}".format(temp, tab[k][i])
                            if temp == "centered+" or temp == "centered-":
                                if temp[8] == "+":
                                    operation = "add"
                                else:
                                    operation = "substract"
                                temp1 = ""
                                for i in range(9, len(tab[k])):
                                    temp1 = "{0}{1}".format(temp1, tab[k][i])
                                temp1 = int(temp1)
                                if operation == "add":
                                    tab[k] = middleScreen[k] + temp1
                                else:
                                    tab[k] = middleScreen[k] - temp1
                for k in range(5):
                    self.texture[k] = transform.scale(self.texture[k], (
                    self.texture[k].get_width() * self.size[k][0], self.texture[k].get_height() * self.size[k][1]))
                if characterNum == 2:
                    for k in range(5):
                        self.texture[k] = transform.flip(self.texture[k], True, False)
                    temp1 = self.texture[0]
                    self.texture[0] = self.texture[3]
                    self.texture[3] = temp1
                if characterNum == 1:
                    temp1 = self.pos[0]
                    self.pos[0] = self.pos[3]
                    self.pos[3] = temp1
            else:
                self.texture = [Font40.render("", 1, (255, 255, 255)) for k in range(5)]
                self.pos = [[0, 0] for k in range(5)]

    if playAs == "Player":
        try:
            character1 = Character(
                json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["character1"]["Name"], 1)
        except:
            character1 = Character("None", 1)
        try:
            character2 = Character(
                json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["character2"]["Name"], 2)
        except:
            character2 = Character("None", 2)
    else:
        try:
            character1 = Character(
                json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["character2"]["Name"], 1)
        except:
            character1 = Character("None", 1)
        try:
            character2 = Character(
                json.load(open("assets\Musics\{0}\songData.json".format(musicName)))["character1"]["Name"], 2)
        except:
            character2 = Character("None", 2)

    # endregion
    # endregion

    # region screen and notes update
    def drawGreyNotes():
        width = display.Info().current_w
        currentTime = Time.time() - startTime
        if "hideNotes2" not in modifications:
            temp = arrowRect
            temp.topright = (width - 540, 50)
            if K_a in keyPressed or K_LEFT in keyPressed:
                screen.blit(pressedArrowsSkins[0], temp)
            else:
                screen.blit(greyArrow[0], temp)
            temp = arrowRect
            temp.topright = (width - 380, 50)
            if K_s in keyPressed or K_DOWN in keyPressed:
                screen.blit(pressedArrowsSkins[1], temp)
            else:
                screen.blit(greyArrow[1], temp)
            temp = arrowRect
            temp.topright = (width - 220, 50)
            if K_w in keyPressed or K_UP in keyPressed:
                screen.blit(pressedArrowsSkins[2], temp)
            else:
                screen.blit(greyArrow[2], temp)
            temp = arrowRect
            temp.topright = (width - 60, 50)
            if K_d in keyPressed or K_RIGHT in keyPressed:
                screen.blit(pressedArrowsSkins[3], temp)
            else:
                screen.blit(greyArrow[3], temp)
        if not singlePlayer and "hideNotes1" not in modifications:
            temp = arrowRect
            temp.topleft = (60, 50)
            if currentTime - opponentHitTimes[0] > 0.15:
                screen.blit(greyArrow[0], temp)
            else:
                screen.blit(pressedArrowsSkins[0], temp)
            temp = arrowRect
            temp.topleft = (220, 50)
            if currentTime - opponentHitTimes[1] > 0.15:
                screen.blit(greyArrow[1], temp)
            else:
                screen.blit(pressedArrowsSkins[1], temp)
            temp = arrowRect
            temp.topleft = (380, 50)
            if currentTime - opponentHitTimes[2] > 0.15:
                screen.blit(greyArrow[2], temp)
            else:
                screen.blit(pressedArrowsSkins[2], temp)
            temp = arrowRect
            temp.topleft = (540, 50)
            if currentTime - opponentHitTimes[3] > 0.15:
                screen.blit(greyArrow[3], temp)
            else:
                screen.blit(pressedArrowsSkins[3], temp)

    def drawNotes():
        global misses
        global health
        global opponentAnimation
        currentTime = Time.time() - startTime
        width = display.Info().current_w
        renderNotes = True
        for note in notesChart:
            if renderNotes:
                if note.side == "Opponent" and currentTime * 1000 >= note.pos:
                    opponentAnimation = [note.column, currentTime]
                    opponentHitTimes[["Left", "Down", "Up", "Right"].index(note.column)] = currentTime
                    notesChart.remove(note)
                if currentTime * 1000 - 133 >= note.pos and note.side == "Player" and note.column in ["Left", "Down",
                                                                                                      "Up",
                                                                                                      "Right"]:
                    notesChart.remove(note)
                    misses += 1
                    health -= 4
                    accuracyPercentList.append(0)
                if 50 + (note.pos - currentTime * 1000) * speed < display.Info().current_h + 100:
                    if not singlePlayer and "hideNotes1" not in modifications:
                        if note.side == "Opponent" and note.column == "Down":
                            temp = arrowRect
                            temp.topleft = (220, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[1], temp)
                        elif note.side == "Opponent" and note.column == "Left":
                            temp = arrowRect
                            temp.topleft = (60, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[0], temp)
                        elif note.side == "Opponent" and note.column == "Up":
                            temp = arrowRect
                            temp.topleft = (380, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[2], temp)
                        elif note.side == "Opponent" and note.column == "Right":
                            temp = arrowRect
                            temp.topleft = (540, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[3], temp)
                    if "hideNotes2" not in modifications:
                        if note.side == "Player" and note.column == "Down":
                            temp = arrowRect
                            temp.topright = (width - 380, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[1], temp)
                        elif note.side == "Player" and note.column == "Left":
                            temp = arrowRect
                            temp.topright = (width - 540, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[0], temp)
                        elif note.side == "Player" and note.column == "Up":
                            temp = arrowRect
                            temp.topright = (width - 220, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[2], temp)
                        elif note.side == "Player" and note.column == "Right":
                            temp = arrowRect
                            temp.topright = (width - 60, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[3], temp)

                else:
                    renderNotes = False

    def drawLongNotes():
        global opponentAnimation
        global playerAnimation
        currentTime = Time.time() - startTime
        width = display.Info().current_w
        run = True
        for longNote in longNotesChart:
            if run:
                if currentTime * 1000 - 133 >= longNote.pos:
                    longNotesChart.remove(longNote)
                else:
                    if longNote.side == "Opponent" and currentTime * 1000 >= longNote.pos:
                        if currentTime - opponentAnimation[1] > 0.7:
                            opponentAnimation = [longNote.column, currentTime]
                        opponentHitTimes[["Left", "Down", "Up", "Right"].index(longNote.column)] = currentTime
                        longNotesChart.remove(longNote)
                    if longNote.side == "Player" and currentTime * 1000 >= longNote.pos and longNote.column in ["Left",
                                                                                                                "Down",
                                                                                                                "Up",
                                                                                                                "Right"]:
                        if ((K_LEFT in keyPressed or K_a in keyPressed) and longNote.column == "Left") or (
                                (K_DOWN in keyPressed or K_s in keyPressed) and longNote.column == "Down") or (
                                (K_UP in keyPressed or K_w in keyPressed) and longNote.column == "Up") or (
                                (K_RIGHT in keyPressed or K_d in keyPressed) and longNote.column == "Right"):
                            if currentTime - playerAnimation[1] > 0.7:
                                playerAnimation = [longNote.column, currentTime]
                            longNotesChart.remove(longNote)
                    if 50 + (longNote.pos - currentTime * 1000) * speed < display.Info().current_h + 100:
                        if not singlePlayer and longNote.side == "Opponent" and "hideNotes1" not in modifications:
                            if longNote.column == "Down":
                                temp = arrowRect
                                temp.center = (220 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[1], temp)
                                else:
                                    screen.blit(longNotesImg[1], temp)
                            if longNote.column == "Left":
                                temp = arrowRect
                                temp.center = (60 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[0], temp)
                                else:
                                    screen.blit(longNotesImg[0], temp)
                            if longNote.column == "Up":
                                temp = arrowRect
                                temp.center = (380 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[2], temp)
                                else:
                                    screen.blit(longNotesImg[2], temp)
                            if longNote.column == "Right":
                                temp = arrowRect
                                temp.center = (540 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[3], temp)
                                else:
                                    screen.blit(longNotesImg[3], temp)
                        if longNote.side == "Player" and "hideNotes2" not in modifications:
                            if longNote.column == "Up":
                                temp = arrowRect
                                temp.center = (width - 220 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[2], temp)
                                else:
                                    screen.blit(longNotesImg[2], temp)
                            if longNote.column == "Down":
                                temp = arrowRect
                                temp.center = (width - 380 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[1], temp)
                                else:
                                    screen.blit(longNotesImg[1], temp)
                            if longNote.column == "Left":
                                temp = arrowRect
                                temp.center = (width - 540 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[0], temp)
                                else:
                                    screen.blit(longNotesImg[0], temp)
                            if longNote.column == "Right":
                                temp = arrowRect
                                temp.center = (width - 60 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                if longNote.isEnd:
                                    screen.blit(longNotesEnd[3], temp)
                                else:
                                    screen.blit(longNotesImg[3], temp)
                    else:
                        run = False

    def drawHealthBar():
        global health
        if health > 100:
            health = 100
        if health < 0:
            health = 0
        width = display.Info().current_w
        height = display.Info().current_h
        draw.rect(screen, (255, 255, 255), Rect(45, height - 115, width - 90, 60))
        if health < 100:
            draw.rect(screen, (255, 0, 0), Rect(50, height - 110, (width - 100) / 100 * (100 - health), 50))
        if health > 0:
            draw.rect(screen, (0, 255, 0),
                      Rect(50 + (width - 100) / 100 * (100 - health), height - 110, (width - 100) / 100 * health, 50))

    def drawCharacters():
        currentTime = Time.time() - startTime
        if currentTime - opponentAnimation[1] > 0.75:
            animationDirection = 4
        else:
            animationDirection = ["Left", "Down", "Up", "Right"].index(opponentAnimation[0])
        temp = character1.texture[animationDirection].get_rect()
        temp.midbottom = [character1.pos[animationDirection][0],
                          display.Info().current_h - character1.pos[animationDirection][1]]
        screen.blit(character1.texture[animationDirection], temp)
        if currentTime - playerAnimation[1] > 0.75:
            animationDirection = 4
        else:
            animationDirection = ["Left", "Down", "Up", "Right"].index(playerAnimation[0])
        temp = character2.texture[animationDirection].get_rect()
        temp.midbottom = [display.Info().current_w - character2.pos[animationDirection][0],
                          display.Info().current_h - character2.pos[animationDirection][1]]
        screen.blit(character2.texture[animationDirection], temp)

    # endregion

    # region death screen
    def death():
        global hasPlayedMicDrop
        startDeathTime = Time.time()
        deathScreenMusicStart.play()
        while True:
            for events in event.get():
                if events.type == QUIT:
                    deathScreenMusic.stop()
                    deathScreenMusicEnd.stop()
                    quit()
                    exit()
                if events.type == KEYDOWN:
                    if events.key == K_ESCAPE or events.key == K_BACKSPACE:
                        deathScreenMusic.stop()
                        return False
                    if events.key == K_SPACE or events.key == K_RETURN:
                        deathScreenMusic.stop()
                        deathScreenMusicEnd.play()
                        Time.sleep(deathScreenMusicEnd.get_length() - 2.5)
                        deathScreenMusicEnd.stop()
                        return True
            screen.fill((0, 0, 0))
            if Time.time() - startDeathTime > deathScreenMusicStart.get_length() - 1.5 and not hasPlayedMicDrop:
                deathScreenMusic.play(-1)
                hasPlayedMicDrop = True
            screen.blit(BFdead, deathScreenRect)
            display.flip()

    # endregion

    keyPressed = []

    Inst.play()
    Vocals.play()

    startTime = Time.time()
    while True:
        notesToClear = [[], [], [], []]
        for events in event.get():
            if events.type == QUIT:
                quit()
                exit()
            if events.type == KEYDOWN and events.key == K_ESCAPE:
                Inst.stop()
                Vocals.stop()
                return False
            if events.type == KEYDOWN:
                keyPressed.append(events.key)
            if events.type == KEYDOWN and events.key == K_SPACE:
                print("Debug: Current song position: {0}".format((Time.time() - startTime) * 1000))
            if events.type == KEYUP and events.key in keyPressed:
                keyPressed.remove(events.key)
            if events.type == KEYDOWN:
                currentTime = Time.time() - startTime
                testNotes = True
                for note in notesChart:
                    if testNotes:
                        if note.pos <= currentTime * 1000 + 133:
                            if note.side == "Player" and currentTime * 1000 - 133 <= note.pos <= currentTime * 1000 + 133 and note.column in [
                                "Left", "Down", "Up", "Right"]:
                                if (events.key == K_a or events.key == K_LEFT) and note.column == "Left":
                                    notesToClear[0].append(note)
                                if (events.key == K_s or events.key == K_DOWN) and note.column == "Down":
                                    notesToClear[1].append(note)
                                if (events.key == K_w or events.key == K_UP) and note.column == "Up":
                                    notesToClear[2].append(note)
                                if (events.key == K_d or events.key == K_RIGHT) and note.column == "Right":
                                    notesToClear[3].append(note)
                        else:
                            testNotes = False
        currentTime = Time.time() - startTime
        for k in range(4):
            if len(notesToClear[k]) > 0:
                min = notesToClear[k][0].pos
                minX = 0
                x = 0
                for element in notesToClear[k]:
                    if element.pos < min:
                        min = element.pos
                        minX = x
                    x += 1
                accuracy = str(round(notesToClear[k][minX].pos - currentTime * 1000, 2))
                showAccuracy = True
                accuracyDisplayTime = Time.time()
                # region Accuracy timings info
                # Sick: <= 47
                # Good: <= 79
                # Bad: <= 109
                # Shit: <= 133
                # endregion
                if currentTime * 1000 + 47 >= notesToClear[k][minX].pos >= currentTime * 1000 - 47:
                    accuracyIndicator = accuracyIndicatorImages[0]
                    accuracyPercentList.append(1)
                    health += 2.3
                elif currentTime * 1000 + 79 >= notesToClear[k][minX].pos >= currentTime * 1000 - 79:
                    accuracyIndicator = accuracyIndicatorImages[1]
                    accuracyPercentList.append(0.75)
                    health += 0.4
                elif currentTime * 1000 + 109 >= notesToClear[k][minX].pos >= currentTime * 1000 - 109:
                    accuracyIndicator = accuracyIndicatorImages[2]
                    accuracyPercentList.append(0.5)
                    health += 0.4
                else:
                    accuracyIndicator = accuracyIndicatorImages[3]
                    accuracyPercentList.append(-1)
                    misses += 1
                    health -= 4
                playerAnimation = [notesToClear[k][minX].column, currentTime]
                notesChart.remove(notesToClear[k][minX])
        screen.fill((0, 0, 0))
        backgroundFrameNum = int(((Time.time() - startTime) / bpm * len(Background)) % len(Background))
        screen.blit(Background[backgroundFrameNum], BGrect)
        drawCharacters()
        drawGreyNotes()
        drawLongNotes()
        drawNotes()
        # region draw bottom info bar
        if len(accuracyPercentList) == 0:
            tempAccuracy = "NA"
        else:
            temp = 0
            for element in accuracyPercentList:
                temp += element
            temp /= len(accuracyPercentList)
            tempAccuracy = "{0}%".format(round(temp * 100, 2))
        temp = Font40.render("Misses: {0} | Accuracy: {1}".format(misses, tempAccuracy), 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.midbottom = (middleScreen[0], display.Info().current_h - 5)
        screen.blit(temp, temp1)
        # endregion
        # region accuracy display
        if Time.time() - accuracyDisplayTime > 0.5:
            showAccuracy = False
        if showAccuracy:
            temp = Font40.render(accuracy, 1, (255, 255, 255))
            temp1 = temp.get_rect()
            temp1.center = (middleScreen[0], middleScreen[1])
            screen.blit(temp, temp1)

            screen.blit(accuracyIndicator, accuracyIndicatorRect)
        # endregion
        # region FPS
        fps = 1 / (Time.time() - fpsTime)
        fpsTime = Time.time()
        fpsList.append(fps)
        temp = 0
        for element in fpsList:
            temp += element
        temp /= len(fpsList)
        while len(fpsList) > fpsQuality:
            fpsList.remove(fpsList[0])
        screen.blit(Font40.render(str(round(temp, 2)), 1, (255, 255, 255)), Rect(5, 0, 0, 0))
        # endregion
        # region health bar
        drawHealthBar()
        # endregion
        display.flip()
        if Time.time() - startTime > musicLen:
            Inst.stop()
            Vocals.stop()
            return False
        if health <= 0 and not noDying:
            Inst.stop()
            Vocals.stop()
            return death()
