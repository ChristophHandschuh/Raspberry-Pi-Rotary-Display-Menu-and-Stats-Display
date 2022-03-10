from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
import RPi.GPIO as GPIO
import os
import subprocess

pm2status = False
path = os.environ['HOME']
dir = os.listdir(path)
dir.append("cd ..")
dir.append("EXIT")
count = 0
countold = 0
count1 = 0
lastState = "11"
menu = 0


def enc(no):
    global lastState
    global count
    global count1
    p1 = GPIO.input(23)
    p2 = GPIO.input(24)
    newState = "{}{}".format(p1, p2)

    if newState == "00" and lastState == "10" and count + 1 < len(dir):
        count = count + 1
        if menu == 2:
            if count % 6 == 0:
                count1 = count1 + 6

    elif newState == "00" and lastState == "01" and count > 0:
        count = count - 1
        if menu == 2:
            if count % 6 == 5:
                count1 = count1 - 6

    lastState = newState


def button(no):
    global menu
    global path
    global dir
    global count
    global count1

    if menu == 0:
        menu = 1
    elif menu == 1:
        menu = 2
        path = os.environ['HOME']
        dir = os.listdir(path)
        dir.append("cd ..")
        dir.append("EXIT")
        count = 0
        count1 = 0
    elif menu == 2:
        if dir[count] == "cd ..":
            path = path[:-1]
            while path[-1] != "/":
                path = path[:-1]
        elif dir[count][-2] == "j" and dir[count][-1] == "s":
            #subprocess.call(["pm2","start", path + dir[count]])
            print(subprocess.check_output(["pm2", "start", path + dir[count]]))
        elif dir[count] == "EXIT":
            menu = 0
        else:
            path = path + dir[count] + "/"
        print(path)
        dir = os.listdir(path)
        dir.append("cd ..")
        dir.append("EXIT")
        count = 0
        count1 = 0


GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.BOTH, enc)
GPIO.add_event_detect(24, GPIO.BOTH, enc)
GPIO.add_event_detect(25, GPIO.RISING, button, 250)

laststateA = 1
laststateB = 1

# rev.1 users set port=0 substitute spi(device=0, port=0) below if using that interface substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)
# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)


def display():
    global countold
    global count1

    if menu == 0:
        with canvas(device) as draw:
            draw.rectangle((0, 0, 125, 64), fill="black")
    elif menu == 1:
        if pm2status != False:
            processes = str(subprocess.check_output(
                "pm2 status", shell=True), "utf-8").count("online")
        with canvas(device) as draw:
            draw.text((5, 0), "IP: " + str(subprocess.check_output(
                "hostname -I | cut -d\' \' -f1", shell=True), "utf-8"), fill="white")
            draw.text((5, 10), str(subprocess.check_output(
                "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'", shell=True), "utf-8"), fill="white")
            draw.text((5, 20), str(subprocess.check_output(
                "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'", shell=True), "utf-8"), fill="white")
            draw.text((5, 30), str(subprocess.check_output(
                "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'", shell=True), "utf-8"), fill="white")
            draw.text((5, 40), "Temp: " + str(subprocess.check_output(
                "vcgencmd measure_temp |cut -f 2 -d '='", shell=True), "utf-8"), fill="white")
            if pm2status != False:
                draw.text((5, 50), "Pm2: " + str(processes), fill="white")
    elif menu == 2:
        with canvas(device) as draw:
            for i in range(6):
                if count % 6 == i:
                    draw.rectangle((0, 0 + 10*i, 125, 10 + 10*i), fill="white")
                    draw.text((10, 0 + 10*i), dir[i + count1], fill="black")
                elif i < len(dir) - count1:
                    draw.text((10, 0 + 10*i), dir[i + count1], fill="white")


if __name__ == '__main__':
    display()
