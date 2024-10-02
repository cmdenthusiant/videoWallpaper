import win32api
import win32gui
import cv2
import screeninfo
import math
import time
import decord

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

vr = decord.VideoReader('video.mp4',width=screenSize[0], height=screenSize[1])

framesLen = len(vr)
fps = vr.get_avg_fps()
max_FPS = 60
stepframe = max(int(fps/max_FPS),1)
estimFrameDelay = math.ceil(1000/fps)
print(estimFrameDelay,fps)

offsetFrameDelay = 0

while True:
    for i in range(0,framesLen,stepframe):
        s = time.time()
        cv2.imshow("wallpaperPY", cv2.cvtColor(vr[i].asnumpy(), cv2.COLOR_BGR2RGB))
        cv2.waitKey(max(estimFrameDelay + offsetFrameDelay,1))
        e = time.time()
        offsetFrameDelay = estimFrameDelay - math.ceil((e-s)*1000)