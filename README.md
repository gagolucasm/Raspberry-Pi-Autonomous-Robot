# Raspberry Pi Autonomous Robot

Autonomous Robot with simple behaviour. Analyzes the environment, finds the correct shape, moves near to it and uploads a picture of it to twitter. Works fluently with a Raspberry Pi 2, used an H-Bridge (L298N) to change polarity.

## Installation

Clone the repository in your computer:

`git clone https://github.com/gagolucasm/Raspberry-Pi-Autonomous-Robot.git`

## Dependencies

You will need:

* [Python 3.5](https://www.python.org/)
* [Opencv](http://opencv.org/)
* [Numpy](http://www.numpy.org/)
* [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)
* [Picamera](https://picamera.readthedocs.io/en/release-1.12/)
* [Tweepy](https://github.com/tweepy/tweepy)


## How to use

If you want to use tweeter features, you have to get everything ready for using Twitter API ([here](https://dev.twitter.com/oauth/overview)). 

Replace your consumer_key, consumer_secret, access_token and access_token_secret into libs.py.

Run:

`python colourRec.py -r 1 -f sq -tw Y`

If you need help with the configuration parameters, run:

`python colourRec.py --help`
