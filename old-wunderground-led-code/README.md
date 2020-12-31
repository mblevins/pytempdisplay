pytempdisplay
=============

Python script to display wunderground temperatures

Runs on a Raspberry PI and drives a [cheeky LED](http://dreamcheeky.com/led-message-board) (also available [here](http://www.thinkgeek.com/product/1690/?srp=8))


Requires [dcled](https://github.com/mblevins/dcled) compiled on the raspberry pi

Set the following environment variables to run:

- DCLED - location of dcled binary
- WUNDERGROUND_API_KEY - API key from [wunderground](http://www.wunderground.com/weather/api)
- WUNDEGROUND_PWS - Personal weatherstation ID at wunderground