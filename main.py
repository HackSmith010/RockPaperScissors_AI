import random
import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands...
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(
                imgBG,
                str(int(timer)),
                (605, 445),
                cv2.FONT_HERSHEY_PLAIN,
                6,
                (255, 0, 255),
                4,
            )

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randNum = random.randint(1, 3)

                    imgAI = cv2.imread(f"Resources/{randNum}.png", cv2.IMREAD_UNCHANGED)
                    imgAIScaled = cv2.resize(imgAI, (0, 0), None, 0.6, 0.776)
                    imgBG = cvzone.overlayPNG(imgBG, imgAIScaled, (100, 260))

                    # Player Wins
                    if (
                        (playerMove == 1 and randNum == 3)
                        or (playerMove == 2 and randNum == 1)
                        or (playerMove == 3 and randNum == 2)
                    ):
                        scores[1] += 1

                    # AI Wins
                    if (
                        (playerMove == 3 and randNum == 1)
                        or (playerMove == 1 and randNum == 2)
                        or (playerMove == 2 and randNum == 3)
                    ):
                        scores[0] += 1

                    print(playerMove)

    imgBG[239:659, 835:1235] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAIScaled, (100, 260))

    cv2.putText(
        imgBG, str(scores[0]), (380, 230), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6
    )
    cv2.putText(
        imgBG,
        str(scores[1]),
        (1170, 230),
        cv2.FONT_HERSHEY_PLAIN,
        4,
        (255, 255, 255),
        6,
    )

    # cv2.imshow("Image",img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled",imgScaled)

    key = cv2.waitKey(1)
    if key == ord(" "):
        startGame = True
        initialTime = time.time()
        stateResult = False
