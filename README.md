
# VDR

VDR is a Python library to simulate a VDR (Voyage Data Recorder).

## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install vdr.

```bash
pip3 install vdr
```

## Usage
You need first to configure your VDR that will receive all the data.
```python
import vdr

VDR = vdr.Vdr('/home/USER')                         # Create the VDR with its storage path
VDR.add_connection("localhost", 12345, 'ecdis')     # Create socket connection called 'ecdis'
VDR.add_connection("localhost", 12346, 'nmea')      # Create socket connection called 'nmea'
VDR.add_connection("localhost", 12347, 'voice')     # Create socket connection called 'voice'

# Initialize threads with each data type that connections will received
ECDIS = vdr.ReceivingFrame(VDR, "ecdis")
NMEA = vdr.ReceivingNmea(VDR, "nmea")
VOICE = vdr.ReceivingVoice(VDR, "voice")

# Start threads, ready to receive and store data
ECDIS.start()
NMEA.start()
VOICE.start()
```

Then, the library proposed different kind of agent to facilitate data emission.
### Frame Agent
```python
import screenagent

agent = screenagent.ScreenAgent("localhost", 12345)
agent.send_screenshot()


```
### Sound Agent
```python
import soundagent

agent = soundagent.SoundAgent("localhost", 12347)
agent.send_sound()


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)