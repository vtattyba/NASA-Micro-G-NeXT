<img src="https://github.com/vtattyba/University-at-Buffalo-Micro-g-NExT-Team-/blob/master/Logo.png" width="200" height="170">

# UB AIAA Micro-g NExT Research Team
NASA’s Microgravity University proposes a series of design challenges for undergraduate students on an annual basis, which directly relate to space exploration missions. During fall semester, Micro-g Neutral Buoyancy Experiment Design Teams develop and propose a tool or device which meets the requirements of their preferred challenge. NASA officials review submitted proposals and offer the opportunity for selected teams’ lead officials to test their devices in-person at the Johnson Space Center’s Neutral Buoyancy Laboratory. 

Learn More at [**UB MICROG**](https://www.ubaiaa.org/microg.html)

<img src="https://github.com/vtattyba/University-at-Buffalo-Micro-g-NExT-Team-/blob/master/AMSAR%201.0/Media/EDCC062B-61B5-4FDE-B08B-45D953DA8902.JPEG" width="410" height="600">

# AMSAR (Autonomous Maritime Search and Rescue)
Challenge 1: Surface Autonomous Vehicle for Emergency Response (SAVER)

[**Proposal**](https://www.ubaiaa.org/docs/2021.pdf)

###### Background
NASA has been challenged to go forward to the Moon by 2024 with our Artemis Program, using
Orion as the spacecraft. In the event of an unplanned egress (launch abort, contingency landing, etc.), Orion crewmembers will be exiting the crew vehicle and using a life raft. Each astronaut will be equipped with a 406 MHz emergency distress beacon to ensure they can be located should they individually be separated from the life raft and Orion capsule. The SAVER vehicle will assist with long-range Search and Rescue efforts by acting as a force-multiplier, assisting current efforts to tend to survivors on the scene immediately. The current ability to drop a lifeboat from rescue assets allows on-scene rescuers to immediately tend to survivors in the main life raft while SAVER autonomously searches for any isolated victims. Objective Design a surface vehicle capable of assisting astronauts in distress in a maritime environment, through the location and delivery of crew survival aids.

## Software
AMSAR is a fully autonomous system that must undergo multiple mission procedures in order to
attain its goal state. Figure 4 [pp. 3] shows the System Block Diagram which defines the exact actions and states within the AMSAR system. The sensors required for mission success include the accelerometer, Kerberos SDR, motor software, TensorFlow object detection, and ultrasonic proximity detection/object avoidance.

<img src="https://github.com/vtattyba/University-at-Buffalo-Micro-g-NExT-Team-/blob/master/AMSAR%202.0/Software/software.png" width="470" height="500">

##### Plugins

AMSAR is currently extended with the following plugins.

| Plugin | Sensor |
| ------ | ------ |
| Selenium | SDR |
| Adafruit | Accelerometer |
| TensorFlow | Camera |

Install the following dependencies
```sh
sudo apt update
sudo apt full-upgrade
sudo pip3 install adafruit-circuitpython-lis3dh
sudo apt install python3-dev python3-pip python3-venv
sudo apt install libatlas-base-dev 
pip install --upgrade tensorflow
pip install selenium
./run.sh
```
> Note: `Raspberry Pi 4` is required for full system testing.

## Structures
<img src="https://github.com/vtattyba/University-at-Buffalo-Micro-g-NExT-Team-/blob/master/AMSAR%202.0/Structures/Screen%20Shot%202021-05-05%20at%2010.35.53%20PM.png" width="900" height="300">

## Electronics
Main power connections are represented by solid lines, while dashed lines show connections that include data transfer. It can be assumed that all components listed in a specific sub-circuit are connected in series (with the exception of the dependent Pi_1 components).

<img src="https://github.com/vtattyba/University-at-Buffalo-Micro-g-NExT-Team-/blob/master/AMSAR%202.0/Electronics/Circuit.png " width="550" height="350">

# TEAM

<img src="https://github.com/vtattyba/University-at-Buffalo-Micro-g-NExT-Team-/blob/master/2020-2021%20Team.jpg" width="540" height="400">

The Micro-G NEXT challenge team members decorated the UB bull outside the Student Union. From left are Mirka Arevalo, Sean Flynn, Jonah Bannon, Imon Tatar, Mark Ng, Ryan Hughes, Teresa Bompczyk, Tamaghan Maurya, Vladimir Tattybayev, Kevin Zheng, Liam Field and Joshua Duell.
