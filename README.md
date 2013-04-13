# A RasPi Temp Server

Setup your RaspberryPi to give you stats about your household's temp.

![raspi interface](/images/server_screenshot.jpg "Screenshot")
![raspi hardware](/images/raspi.jpg "Hardware")

## Setup
First you need to [setup your raspi](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing). Adafruit's tutorial is fantastic.

Next, run the setup script to build the database:

```
python timeseries_db.py
```

You can edit some things in the `config.py` file too, such as your name and your "get out of bed temperature".

Now just setup the server. I have the logger run in one screen session and the server in another (`sudo apt-get install screen` if you don't have that).

```
# Start the logger
screen -S temp-logger
python temp_logger.py
Ctrl-A d

# Start the server
screen -S temp-server
sudo python temp_server.py
Ctrl-A d
```

That should do it. You can now open a browser on some other box and enter the raspi's ip address. To make it easier, you can [setup zeroconf](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=66&t=18207). This allows you to just type "raspberrypi.local" into your browser.

## License
I took some code from Adafruit for the temp sensor in `temp_lib.py`. They use the CC Share-alike attribute license. I guess That means this code is that too? So ya, that.