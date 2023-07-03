# Netspresso: a non-invasive power sensor for coffee availability 
by Alfred Langerbeck - al226nm

## Introduction
The netspresso project is built to help satisfy one of the basic human needs, Coffee!!
The basic purpose is to measure when a device, in this case a coffee brewer, is powered on. In addition, the power draw of the device is measured.
This is a pretty easy problem to solve and in fact i have already made a simple project to do this before by modifying a standard coffee brewer. 
The previous solution was shut down quite quickly when a building manager walked in and saw the construction, called it a fire hazard and kindly told us not
to modify devices in this way in the future. So how do you do this without modifying the device and not having to worry about working with the power in the mains directly.

In this project, a split core transformer is used to measure the current that is drawn by the coffee maker with minimal interference with the device itself.
The project took about a week of evenings (~20 hours) to complete, and I hope my experience with the project will help anyone who wants to do anything like this. 

Give a short and brief overview of what your project is about. What needs to be included:
    Title
    Your name and student credentials (xx666x)
    Short project overview
    How much time it might take to do (approximation)

## Objective
As stated earlier, the objective is to create a device that can detect when a coffee maker or another general device without interfering with the device itself, and more importantly without modifying it or directly disturbing power from mains. The measurements are then to be uploaded, so any interested party can check if there is coffee brewing or if there was some coffee made recently. 

The project touched many different techniques and was a perfect start for interacting with MQTT, IC2, DACs, Wi-Fi, Sockets and very light data analysis.




Describe why you have chosen to build this specific device. What purpose does it serve? What do you want to do with the data, and what new insights do you think it will give?

    Why you chose the project
    What purpose does it serve
    What insights you think it will give

## Material
The materials required for the project are presented here in two parts. The project can easily be constructed on a breadboard. After validating witht the breadboard
setup i chose to also solder the components to a pcb but this is optional.

| ITEM  | Price | Aquisition |
| ------------- | ------------- | ------------- |
| Raspberry pi pico w | 98.00 SEK*|[electrokit](https://www.electrokit.com/en/product/raspberry-pi-pico-w/)|
| SCT-013  | 122,80 SEK | [Amazon](https://www.amazon.se/dp/B07MY361ZW?psc=1&ref=ppx_yo2ov_dt_b_product_details) |
| Audio jack 3.5 mm  | 1.60 $ | [sparkfun](https://www.sparkfun.com/products/8032)|
| ADS1115  | 84,99 SEK for 3  | [Amazon](https://www.amazon.se/dp/B07QHWLTTS?psc=1&ref=ppx_yo2ov_dt_b_product_details) |
| Breadboard | 69.00 SEK* | [electrokit](https://www.electrokit.com/en/product/solderless-breadboard-840-tie-points-2/) |
| Jumper wire | 29.00 SEK*  | [electrokit](https://www.electrokit.com/en/product/jumper-wires-20-pin-30cm-male-male/) |

*Bought as part of a kit and might have been aquired a little cheaper
### optional

| ITEM  | Price | Aquisition |
| ------------- | ------------- | ------------- |
| PCB | 79,19 SEK |[Amazon](https://www.amazon.se/gp/product/B078HV79XX/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)|
| Solder | <100 SEK  | Any technical store |
| Wiring for soldering | <20 SEK  |Any technical store|
| Header Pins | 139,99kr  | [Amazon](https://www.amazon.se/gp/product/B07CC4V9ZY/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)|

#### Raspberry pi pico w
The Raspberry pi picp is a microcontroller with wireless capabilities and is the core of this project. It does the computing and comunication with sensors. 
One great benefit of this board is that it is wifi capable and can easily be programed using Micropython
<img src="/doc/pico.png" width="300"/>

#### SCT-013
This is the main sensor in the project. It is a split core transformer which measures the current through a wire. It works by the phenomenon of induced current from the field 
created from an ac current. The transformer can measure a current up to 30 Amp and will produce an output between 0 and 1 volt relating to this current.

<img src="/doc/sct013.jpg" width="300"/>

#### ADS1115
The ADS1115 is a an external analog to digital converter. It was deemed that the onboard ADC on the raspberry pi was not enought and this was choosen since it was 
easy to do the differnetial input setup needed to calculate the AC voltage from the current transformer. The ADC came without headers soldered on so this needed to be self soldered.

<img src="/doc/ads1115.jpg" width="400"/>

#### Connections
The remaining components were used to connect the the components togheter. Since the SCT-013 connects with a 3.5 mm AUX cable an audio jack was also used to create an easy
connection. The breadboard is a good place to connect components with clear lines and without needing to solder. Finaly there are of course some wires to connect components.
<p float="left">
<img src="/doc/audioJack.jpg" width="200"/>
<img src="/doc/breadboard.jpg" width="200"/>
<img src="/doc/jumper.jpg" width="200"/>
</p>

#### Solder material
<p float="left">
<img src="/doc/pcb.jpg" width="200"/>
<img src="/doc/solder.jpg" width="200"/>
<img src="/doc/headers.jpg" width="200"/>
</p>

Explain all material that is needed. All sensors, where you bought them and their specifications. Please also provide pictures of what you have bought and what you are using.

    List of material
    What the different things (sensors, wires, controllers) do - short specifications
    Where you bought them and how much they cost

Computer setup

How is the device programmed. Which IDE are you using. Describe all steps from flashing the firmware, installing plugins in your favorite editor. How flashing is done on MicroPython. The aim is that a beginner should be able to understand.

    Chosen IDE
    How the code is uploaded
    Steps that you needed to do for your computer. Installation of Node.js, extra drivers, etc.

Putting everything together

How is all the electronics connected? Describe all the wiring, good if you can show a circuit diagram. Be specific on how to connect everything, and what to think of in terms of resistors, current and voltage. Is this only for a development setup or could it be used in production?

    Circuit diagram (can be hand drawn)
    *Electrical calculations

Platform

Describe your choice of platform. If you have tried different platforms it can be good to provide a comparison.

Is your platform based on a local installation or a cloud? Do you plan to use a paid subscription or a free? Describe the different alternatives on going forward if you want to scale your idea.

    Describe platform in terms of functionality
    *Explain and elaborate what made you choose this platform

The code

Import core functions of your code here, and don’t forget to explain what you have done! Do not put too much code here, focus on the core functionalities. Have you done a specific function that does a calculation, or are you using clever function for sending data on two networks? Or, are you checking if the value is reasonable etc. Explain what you have done, including the setup of the network, wireless, libraries and all that is needed to understand.

import this as that

def my_cool_function():
    print('not much here')

s.send(package)

# Explain your code!

Transmitting the data / connectivity

How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.

    How often is the data sent?
    Which wireless protocols did you use (WiFi, LoRa, etc …)?
    Which transport protocols were used (MQTT, webhook, etc …)
    *Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.

Presenting the data

Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?

    Provide visual examples on how the dashboard looks. Pictures needed.
    How often is data saved in the database.
    *Explain your choice of database.
    *Automation/triggers of the data.

Finalizing the design

Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in an other way, or even better? Pictures are nice!

    Show final results of the project
    Pictures
    *Video presentation
