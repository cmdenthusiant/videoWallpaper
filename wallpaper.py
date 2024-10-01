import win32api
import win32gui
import cv2
import screeninfo
import math

screen = screeninfo.get_monitors()[0]
screenSize = (screen.width, screen.height)

progman = win32gui.FindWindow("Progman", None)
worker = None
def findWorker(hwnd, extra):
    global worker
    if worker:return
    p = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
    if p:
        worker = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)

win32api.SendMessage(progman, 0x052C,  0x0000000D,  0)
win32api.SendMessage(progman, 0x052C,  0x0000000D,  1)
win32gui.EnumWindows(findWorker, 0x0000000D)

cv2.namedWindow("wallpaperPY", cv2.WINDOW_NORMAL)
wallpaper = win32gui.FindWindow(None, "wallpaperPY")

cv2.setWindowProperty("wallpaperPY", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
win32gui.SetParent(wallpaper, worker)

video = cv2.VideoCapture('video.mp4')
fps = video.get(cv2.CAP_PROP_FPS)
frameDelay = math.ceil(1000/fps)
try:
    while video.isOpened():
        success, frame = video.read()
        if success:
            frame = cv2.resize(frame, screenSize, interpolation=cv2.INTER_LINEAR)
            cv2.imshow("wallpaperPY", frame)
            cv2.waitKey(1)
            
        else: video.set(cv2.CAP_PROP_POS_FRAMES, 0)
except:
        win32api.SendMessage(progman, 0x052C,  0x0000000D,  0)
        win32api.SendMessage(progman, 0x052C,  0x0000000D,  1)
        win32gui.EnumWindows(findWorker, 0x0000000D)