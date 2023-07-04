# Netspresso: a non-invasive power sensor for coffee availability 
by Alfred Langerbeck - al226nm

<p align="center">
<img src="/doc/coffe_beat.jpg"/>
</p>

## Introduction
The netspresso project is built to help satisfy one of the basic human needs, Coffee!! The basic purpose is to measure when a device, in this case a coffee brewer, is powered on. In addition, the power draw of the device is measured. This is a pretty easy problem to solve, and in fact I have already made a simple project to do this before by modifying a standard coffee brewer. The previous solution was shut down quite quickly when a building manager walked in and saw the construction, called it a fire hazard, and kindly told us not to modify devices in this way in the future. So how do you do this without modifying the device and not having to worry about working with the power in the mains directly.

In this project, a split core transformer is used to measure the current that is drawn by the coffee maker with minimal interference with the device itself. The project took about a week of evenings (~20 hours) to complete, and I hope my experience with the project will help anyone who wants to do anything like this. Recreating the project with all components at hand could probably be done in 1–2 days of casual work.


## Objective
As stated earlier, the objective is to create a device that can detect when a coffee maker or another general device without interfering with the device itself, and more importantly without modifying it or directly disturbing power from mains. The measurements are then to be uploaded, so any interested party can check if there is coffee brewing or if there was some coffee made recently. I choose to do this project to create
something that I will actually use.

The project touched many different techniques and was a perfect start for interacting with MQTT, IC2, DACs, Wi-Fi, Sockets and very light data analysis. It gives insight both into details about these subject
but also into what it takes to integrate all these small parts together.

## Material
The materials required for the project are presented here in two parts. The project can easily be constructed on a breadboard. After validating with the breadboard
setup i chose to also solder the components to a PCB, but this is optional.

| ITEM  | Price | Aquisition |
| ------------- | ------------- | ------------- |
| Raspberry pi pico w | 98.00 SEK*|[electrokit](https://www.electrokit.com/en/product/raspberry-pi-pico-w/)|
| SCT-013  | 122,80 SEK | [Amazon](https://www.amazon.se/dp/B07MY361ZW?psc=1&ref=ppx_yo2ov_dt_b_product_details) |
| Audio jack 3.5 mm  | 1.60 $ | [sparkfun](https://www.sparkfun.com/products/8032)|
| ADS1115  | 84,99 SEK for 3  | [Amazon](https://www.amazon.se/dp/B07QHWLTTS?psc=1&ref=ppx_yo2ov_dt_b_product_details) |
| Breadboard | 69.00 SEK* | [electrokit](https://www.electrokit.com/en/product/solderless-breadboard-840-tie-points-2/) |
| Jumper wire | 29.00 SEK*  | [electrokit](https://www.electrokit.com/en/product/jumper-wires-20-pin-30cm-male-male/) |

*Bought as part of a kit and might have been acquired a little cheaper
### optional

| ITEM  | Price | Aquisition |
| ------------- | ------------- | ------------- |
| PCB | 79,19 SEK |[Amazon](https://www.amazon.se/gp/product/B078HV79XX/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)|
| Solder | <100 SEK  | Any technical store |
| Wiring for soldering | <20 SEK  |Any technical store|
| Header Pins | 139,99kr  | [Amazon](https://www.amazon.se/gp/product/B07CC4V9ZY/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)|

#### Raspberry pi pico w
The Raspberry pi pico is a microcontroller with wireless capabilities and is the core of this project. It does the computing and communication with sensors. 
One great benefit of this board is that it is Wi-Fi capable and can easily be programmed using Micropython

<p align="center">
<img src="/doc/pico.png" width="300"/>
</p>

#### SCT-013
This is the main sensor in the project. It is a split core transformer which measures the current through a wire. It works by the phenomenon of induced current from the field 
created from an ac current. The transformer can measure a current up to 30 Amp and will produce an output between 0 and 1 volt relating to this current.

<p align="center">
<img src="/doc/sct013.jpg" width="300"/>
</p>

#### ADS1115
The ADS1115 is an external analog to digital converter. It was deemed that the onboard ADC on the Raspberry Pi was not enough and this was chosen since it was 
easy to do the differential input setup needed to calculate the AC voltage from the current transformer. The ADC came without headers soldered on, so this needed to be self soldered.

<p align="center">
<img src="/doc/ads1115.jpg" width="400"/>
</p>

#### Connections
The remaining components were used to connect the components together. Since the SCT-013 connects with a 3.5 mm AUX cable, an audio jack was also used to create an easy
connection. The breadboard is a good place to connect components with clear lines and without needing to solder. Finally, there are of course some wires to connect components together.

<p float="left">
<img src="/doc/audioJack.jpg" width="200"/>
<img src="/doc/breadboard.jpg" width="200"/>
<img src="/doc/jumper.jpg" width="200"/>
</p>

#### Solder material
If you have soldering materials and tools lying around, which I had, soldering is a good way to make your device more permanent.
I used and empty PCB, wire, solder and a soldering iron for the process. I also used female headers to make the ADC and Microcontroller easily removable.

<p float="left">
<img src="/doc/pcb.jpg" width="200"/>
<img src="/doc/solder.jpg" width="200"/>
<img src="/doc/headers.jpg" width="200"/>
<img src="/doc/solderIron.jpg" width="200"/>
</p>


## Computer setup
After collecting all materials needed, you should start thinking about your developing environment and how you want to interact with the Raspberry Pi pico w.
All the programmatic and setup parts of this project were done using a pc running Windows 10, but there should be no problems doing the same project using any other
computer. You could even use a regular Raspberry Pi!

### Firmware
<img align="right" src="/doc/micropython.png" width="200"/>

To begin using the Raspberry Pi pico w microcontroller, you first need to install a firmware. For this project, [Micropython](https://micropython.org/) was chosen. The firmware contains a low lever python operating system for the microcontroller,  which allows its many properties to be controlled with python code. Micropython contains a subset of the python standard library. After installing the firmware, the microcontroller can both be uploaded with files to run when not connected with a computer and controlled via an interactive prompt over USB.



1. The firmware can be downloaded [here](https://micropython.org/download/rp2-pico-w/) under the "Firmware" heading. In this project, version 1.20.0 was used.

2. After downloading the firmware, it needs to be uploaded to the microcontroller. This is done by holding done the "BOOTSEL" button indicated in black below and plug in the microcontroller
into your computer using a USB micro cable.
<p align="center">
    <img src="/doc/bootsel.png" alt>
    <em>https://projects.raspberrypi.org/en/projects/get-started-pico-w/1</em>
</p>

3. A file explorer will pop up which looks something like below. Drag and drop the file you downloaded into the file manager. It should close, and the microcontroller should restart, ready to be
   interacted with.
<p align="center">
    <img src="/doc/file_manager.png" alt>
    <em>https://projects.raspberrypi.org/en/projects/get-started-pico-w/1</em>
</p>


### Programing the microcontroller
<img align="right" src="/doc/vs_code_logo.png" width="200"/>

Writing the code for the project I used [Visual Studio Code](https://code.visualstudio.com/) which is an IDE which a large amount of user created modules which helps you with a variety of tasks.
I especially found the [pico-w-go extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) useful since it provides autocompletion for the version of Micropython used in the project. Instruction on how to install the extension can be found by following the provided link.

There is an extension for transferring files to the microcontroller called [pymkr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr), but I  found it very buggy and prone to stop working completely. I instead recommend using [rshell](https://github.com/dhylands/rshell) which is a remote shell terminal tool for interacting with Micropython.

To interact with the Raspberry Pi pico using rshell you should do the following:
1. Make sure you have python3 and pip installed. If you do not, the installation files can be found [here](https://www.python.org/downloads/)
   if python and pip are installed, the following command should provide a version number when run in the Windows terminal.
   
   ```
   python --verion
   pip --version
   ```
3. With pip and python3 installed, run the following command to install rshell
   ```
   pip3 install rshell pyreadline3
   ```
4. Run `rshell` and you should see something like this
    ```
    C:\Users\user>rshell
    Connecting to COM4 (buffer-size 128)...
    Trying to connect to REPL  connected
   ```
5. After the device is connected, files can be moved to the device using the following command:
   ```
   cp localfile.py /pyboard/localfile.py
   ```
   and should give something like this:
   ```
   Copying 'C:\Users\user/localfile.py' to '/pyboard/localfile.py' ...
   ```
   Files can also be removed from the board using
   ```
   rm /pyboard/file.py
   ```
6. After uploading the interactive python prompt can be started using the `repl` command. From the interactive prompt, you can write python commands just like you would on a regular computer.
   While using the interactive prompt via rshell the following control commands can be used:
   ```
   Useful control commands:
      CTRL-C -- interrupt a running program
      CTRL-D -- on a blank line, do a soft reset of the board
      CTRL-E -- on a blank line, enter paste mode
   ```
7. After restarting the board for example via one of the commands above, the board will automatically run boot.py and then main.py files uploaded to the microcontroller while posting prints and error
   codes in the REPL terminal 


## Putting everything together
In terms of hardware, the three main components, current transformer, Analog-to-digital converter and microcontroller, are wired together according to the schema below.

<p align="center">
<img src="/doc/netspresso_sketch_bb.png"/>
</p>

The ADS1115 will connect to the microcontroller the following way:

 - GND -> GND (I've chosen pin 38)
 - VDD -> 3V3 (pin 36) This is powering the ADC
 - SCL -> I2C SCL (I've chosen pin 20)
 - SDA -> I2C SDA (I've chosen pin 19)

The SCT013 is then connected to the ADC using a 3.5 mm audio jack. Where:

- The left channel is connected to A1 on the ADC
- The Ground Channel is connected to A0
- The right channel is left unconnected

Two analog pins are used on the ADC since we get an AC output from the sensor, and we need to read a differential between the signals. 
Since the device is meant to be used in proximity to a coffee maker, the Raspberry Pi  pico w is powered over USB.

One important thing to note is that some current transformers lacks an internal burden resistor. If the output is specified in terms of current and an external burden resistor between the left
channel and ground should be added. If you got the current transformer specified above, this is not a problem.

I chose to solder the components together, which resulted in the following PCB
<p float="left">
<img src="/doc/front_pcb.jpg" width="400" />
<img src="/doc/back_pcb.jpg" width="400"/>
</p>

After connecting all the components, you need to hook up the current transformer around a wire. The transformer needs to be placed around **one** of the phase wires in a normal mains cable. If it encloses
all phase cables, the total current running through the transformer loop will be zero and no result can be attained. I'm doing measurements on a Swedish 2 phase cable without grounding.

<p align="center">
    <img src="/doc/hooked_up_transformer.jpg"  width="600">
</p>

In this prototype, I have opened up a cable. **I do not recommend doing this.** You should try to find an already split cable. If you decide to split your cable despite this, be very careful not to cut the 
inner cable housing. 


## Platform
To present and store the result, two main routes are implemented. The way to interact with the device is through the [Adafruit IO](https://io.adafruit.com/) platform. The adafruit platform provides
an easy way for IoT devices to send and receive data via MQTT, RestAPIs etc. It also provides data visualization and storage. I choose to use it because it seemed a pretty straight forward and easy to use
platform that for my purposes was "good enough". The free adafruit plan was more than enough for this project. Depending on how often you want to send data though, you might need to go for the paid version. 

### Setup AdaFruit IO
To use adafruit in this project, a little setup is needed.

1. Create a free adafruit account [here](https://accounts.adafruit.com/users/sign_up)
2. sign in to your account and go to IO -> Feeds, here you can create feeds for your device to interact with.
3. Two Feeds are required for this project. One to signal when the coffee maker was last turned on and one for signaling measured power draw of the coffee maker.
   Click on the new feed button to create the feeds and name them something relevant. I named them "Power measurement" and "Last turned on"
4. After creating the feed, you need to save the "MQTT by key"  to use the feed later in the code. This is done by clicking on the feed. Going to feed info to the right and copying the string from the
   popup it should be in the format `Adafruit_username/feeds/feed_name`
5. You also need to click on the key symbol in the upper right and copy your "Active Key" for later in the code
   

### Web server
Separate from Adafruit I also chose to display data using a very lite web server running on the microcontroller using sockets. This approach is not scalable, since the pi cannot handle many connections,
but it is a quick and easy way to access when the coffee machine last turned on. It also works without connection to the internet (you still have to be connected to a network, though). To work outside a specific network you would need to use something like [port forwarding](https://en.wikipedia.org/wiki/Port_forwarding), and you would probably need to consider security implications.


## The code
All the code that is included in the project can be found in the src directory, but I will go through some of it here.

One thing that is crucial to know when working with micropython on the pico, is that there are two files which have special meaning. The `boot.py` and `main.py` are automatically executed when the pico is started.

### config.py
In this project there is also another file which the user needs to be aware about. The `config.py` file contains constants used throughout the code, If you live in Sweden and don't care that much about the intricacies of the measurements you only need to worry about the following section of the file. Where you need to input your Wi-Fi credentials to connect to a network and the Adafruit information that was saved during the adafruit setup + your adafruit username.
```
#Connectivity settings
WIFI_SSID = "SSID"
WIFI_PASSWORD = "PASSWORD"

#MQTT Setup
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "Adafruit username"
AIO_KEY = "Adafrutuit Password"

MQTT_LAST_TURN_ON = "Path to last turn on feed"
MQTT_POWER_MEASURMENTS = "Path to power measurment feed"

```
The rest of the constants are related to measurements taken. If you live in Sweden (timezone and mains voltage) and don't care that much about the specifics of the measurement you don't need to worry about these constants.

### boot.py
The boot scripts contain functions for setting up the pi. It contains a function for connecting to a Wi-Fi network using the `network.WLAN` library and a function to set the picos internal Real Time Clock
using values obtained from a [NTP](https://en.wikipedia.org/wiki/Network_Time_Protocol) server. This is needed since one of the core functions of the device is to keep track of when an event (i.e. coffee time) happens in real time. If you want to work with NTP and setting local time, don't forget timezones and don't forget daylight saving (I did, and it was very frustrating). 

The set_time function works by sending creating a socket and sending a request to a NTP server, then using the Micropython machine library to set the RTC.

The connect script is as straightforward as activating the network interface, configuring credentials, starting a connection and waiting for
a connection to be made.


### main.py
The bulk of the code is contained in the main file and if you want any specifics I recommend checking out the file itself in the GitHub.
The is "divided" into two different parts, run by two different thread using the `_threading` library contained in micropython. 
One thread does measurements and handles uploading of data to adafruit IO. The other handles the small web server.

The measure thread interacts with the ads1115 through an imported library found [here](https://github.com/robert-hh/ads1x15) and an ADC class, both located in `src\libs` the library handles the reading of the power
values. The reading is done by calling the `read` function, which takes 120 quick readings and averaging the values. Afterward, the current is calculated from the voltage output using the known relationship between voltage and current from the current transformer. The power is then calculated using the current times the voltage of the mains. The power value is uploaded to adafruit using pycoms MQTT library contained in `src\libs\mqtt.py`.


After measuring power, we want to see if the reading means that the coffee maker has been powered on. This is done by the `find_platue` function. The function checks if the power drain has changed outside a
threshold specified by `config.py` (default 1 Watt), If such a change is positive we begin a scan scanning. In subsequent calls of the find_platue were looking if the value is still outside the threshold and is positive in relation to the first value. If there has been a number of reading specified by `config.py´ (default 5) that is still out of the threshold,  this is read as a plateau which means a turn on off the coffee maker and the function returns true. If this is the case, the timestamp of the power on is both posted to adafruit and updated for the web server to display.


The other part of the code is the web server , while the measurements are handled by a started thread the main thread handles the web server. All the code pertaining to the web server is located in `src\libs\webserver.py` and makes up a very rudamentary web server using sockets which serves the following HTML "site":
```
<!DOCTYPE html>
<html>
<p>{phrase}</p>
</body>
</html>
```
Where phrase is replaced by the timestamp value from the measuring thread.

## Transmitting the data / connectivity
The data is transmitted using the MQTT to adafruit io using pycoms mqtt library. Readings are taken about every 7 seconds, not including the minute time the readings take. The power readings are sent every time one
is taken. The timestamp is only updated when the device is turned on which could be very seldom, though it is limited to 7 seconds as well since it is using the power reading.

Timestamps are also served using the HTTP protocol to any client who sends a get request to the device. This is limited to one device, which could cause problems and would have to be changed before deploying in
frequent use cases.

The device is connected to the internet using Wi-Fi, since it is designed to be used in an indoor workspace this is considered to be no problem at all. Also, it runs of the mains power supply. I kinda wanted to try using LoRa in this course but, for the use case and positioning of the device made Wi-Fi the easier method. 


## Presenting the data
The data is presented in a adafruit dashboard, which looks like this:

<p align="center">
    <img src="/doc/dashboard.png" alt>
    <em>adafruit dashboard</em>
</p> 

The period being shown in the dashboard for the power reading can be changed, but the data is only being stored for 30 days. When the device is running, you should see new values pop up every 7–10 seconds

The website that is being served by the pico is very simple and only serves a string with the timestamp of the last turn on. It can for example look like this:

<p align="center">
    <img src="/doc/socket_website-png.png" alt>
    <em>Simple HTML site</em>
</p> 

## Finalizing the design
The project resulted in a project that does what it says. It gives you the ability to see when the last time the coffee machine was started, both on a dashboard in adafruit and
by accessing a "website". In addition, you can measure the power draw of your coffee maker. The project can of course be used on any device you can plug into the wall and there a power measurement
scenario might be the more probable use case. 

If I had more time I would probably extend the project with an LCD that can show when the device was last turned on locally, and create a chassis, maybe by designing and 3d printing one.
Another thing I would want to do is make the HTTP "site" a prettier pretier and investigate common problems with using sockets the way they are used in the project
 
<p align="center">
    <img src="/doc/complete_setup.jpg" alt>
    <em>The final Setup</em>
</p>
