# Raspberrypi Rotary Menu and Stats Display<img align="center" width="50px" height="50px" src="images/Raspberry_Pi_Logo.png">

Firstly, you have to download the [`luma oled`](https://luma-oled.readthedocs.io/en/latest/) and select the right display in your code (the one you are using)***Mine was the SH1106***.

The next step is to wire up the rotary encoder to the right pins. The default pin's are `23 24 & 25` for the buttons.

If you run the script and press on the button the stats display should appear. If you click another time you will come to the menu display. When you click `EXIT` you will come back to the black screen saver. If you click on a `.js` script, it will run with `pm2`.

Now you have a Raspberry Pi with a Rotary Display Menu and a Stats Display.

***Feel free to make Pull requests.***
