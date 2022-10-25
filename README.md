# epaper-github-stats

built for the raspberry pi zero 2w with a waveshare 2.13" V3 e-paper display

## Installation

Open the terminal of Raspberry Pi and run the following commands to install corresponding libraries: 

- Install BCM2835 libraries:

```
#Open the Raspberry Pi terminal and run the following command
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install
# For more information, please refer to the official website: http://www.airspayce.com/mikem/bcm2835/
```

- Install WiringPi libraries:

```
#Open the Raspberry Pi terminal and run the following command
sudo apt-get install wiringpi
#For Raspberry Pi systems after May 2019 (earlier than before, you may not need to execute), you may need to upgrade:
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v
# Run gpio -v and version 2.52 will appear. If it does not appear, the installation is wrong
#Bullseye branch system use the following command:
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build
gpio -v
# Run gpio -v and version 2.60 will appear. If it does not appear, it means that there is an installation error
```

- Install Python3 libraries:

```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
sudo pip3 install flask
sudo pip3 install requests
sudo pip3 install python-dotenv
```

## Download Code

```
# if you don't already have git installed
sudo apt-get install git
#

git clone https://github.com/birbexe/epaper-github-stats.git
cd epaper-github-stats
```

### Change .env file

To run the code, you will need to add your own github username into the `GH_USER` section of .env.

You will also have to generate a Github Personal Access Token to access the API

[Here's more info on creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-fine-grained-personal-access-token)

## Run program

```
cd src
python main.py
```

## Troubleshooting

- text left on screen

```
# cd into the 'src' folder
python clear.py
```
