# getVaxedCowin

This was written because refreshing the cowin portal was getting too tiring.

## Prerequisites

python3

## Installation

To install, just run

`git clone https://github.com/28hardik/cowin-dooars-notifier`

and then run 

`python3 -m venv env` to setup the python virtual environment.

`source ./env/bin/activate` to activate the virtual env.

Then run `pip install -r requirements.txt` to setup all the necessary requirements.

The telegram details need to updated in the messaging.py file. I referred
 [this](https://xabaras.medium.com/sending-a-message-to-a-telegram-channel-the-easy-way-eb0a0b32968) 
medium document to figure out how to setup my own telegram bot, and channel. (Refer this
if you have issues with
 [channel_id](https://stackoverflow.com/questions/41690726/how-to-get-a-telegram-channel-id-without-sending-a-message-to-it))
 
## Running

The main loop scrubs the API every ten seconds(this could be changed). I am currently running it
on an EC2 instance in ap-south-1 (Mumbai) datacentre. The Cowin APIs seem to throw 403 Forbidden errors
when the APIs are hit from foreign IPs.

Just run the program using `./getVaxedCowin.py` on a tmux terminal so that it can keep running for a long time
without needing to have a persistent ssh connection to your remote host.