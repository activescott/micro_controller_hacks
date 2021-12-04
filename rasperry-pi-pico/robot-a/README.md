# Robot Alpha

This is a relatively simple robot to build on. The general goal is to have an autonomous robot that can move around and avoid obstacles using various sensors. We'll see what else we add...

## Notes and learning
### Motors 
- **faster is harder**: I learned that going too fast makes it hard to stop fast enough before hitting the obstacle. I know, "duh", right? This wasn't obvious to me at first though. I tried various things like briefly backing up to stop faster and that sorta helped but introduced new problems. For example, it would move back too far and then not see an obstacle and blast forward again 🤣. For now I was able to just make the robot always go slower and it mitigated this issue.
- **devices act weird when underpowered**: I had an LCD sensor that worked perfectly by itself. Then when I integrated it into the robot it went bockers and I started getting weird IO errors. Turned out it was due to the motors running and take too much power off of the USB bus. The motors worked fine and the LCD kinda did, but would frequently just appear to crash the firmware (or turn off momentarily?) and cause IO exceptions. Hooking up a battery pack to the motors/motor driver and the pico at the same time made a world of difference.

### Pico
Multiple power sources:
- For the Pico I use ita 3V3 (OUT) pin (pin 36) to power devices. I plug this into one power rail on a bread board. For sensors and LCDs it's fine. For motors its not. 
- I use a standard USB battery (i.e. an extra battery pack for a phone) and plug it into one rail on the breadboard using a simple USB breakout board). It is essentially a ~5 volt power rail on one side of the bread board. 
- Connect the grounds of each rail together. 
- Connect the 5V rail to the VSYS pin on the Pico (pin 39). This will power the pico without anything being plugged into USB and allows the robot to be mobile. It's fine to leave both the USB plugged into the Pico and the 5V rail connected to VSYS (I gritted my teeth at one point and checked and its been that way for a while now without any problems).



### Ultrasonic Distance Sensors

- An ultrasonic sensor (HC-SR04) is a cheap way to detect distance. Super easy to use and quite accurate _most of the time_. However, at times it just returns completely nonsensical readings. It is due to the environment. Some specific observations on this:
- **Leave a gap between the front of the bot and the sensor**: If your ultrasonic sensor is in the very front of the robot and it gets close to a wall with <2cm of the sensor (approximate) it will start returning values >200cm. So you mount the sensor.
- **Ultrasonic sucks at angles**: At one point I was super stumped as it sat on my desk and gave intermittency bizarre readings at times and I realized later it was pointing across the room into a window with blinds. If I shut the blinds all the way it was reasonably consistent readings. With the blinds open and the bot pointed that direction it was super wacky returning readings like <1cm.
- **Ultrasonic sucks at angles**: Take your sensor and point it directly at a wall about 10cm away. Good reading right? Now, aim it at a ~45deg angle towards the wall also at about 10cm. I usually see >200cm readings.

## Todo:

- [+] Move forward and stop before hitting an obstacle
- [+] after stopping... avoid an obstacle by turning and finding a direction to go in that doesn't have an obstacle
- [ ] Come up with way to turn a specified number of degrees according to compass (this will be a good test of agent design it requires concurrency)
- [ ] refactor state machine to a series of pub/sub messages consumed and published by **Agents**:
  - **Agents** can publish or consume messages and proffer which ones they are listening for and publishing. Potential agents: FrontDistance, Drive, Compass, Display/LCD, FrontBumper, Speech, Visual, etc.
  - A **broker** handles registration of agents and pub/sub of messages to/from agents
  - **Messages** have a name and a set of well-defined parameters.
  - **Context**: At any given time there is a "system context" of the system overall that is an aggregation of state provided by agents. Each agent provides a `context` and `name` that the broker uses to assemble a system state (`systemState.<agent name>` => `agent.state`). This way agents only modify their own state, but can read state from any agent and have no coupling to any agent beyond the agent's name to access state.
- [ ] when avoiding obstacle instead of choosing the first "free" direction to go in, spin 360 deg and find the direction to go with the greatest distance we can go in a straight line
- [ ] Slow down as an obstacle gets closer
- [ ] make the logger periodically check the size or line count in the log file and delete older lines.
- [ ] LCD sensor that shows the current activity/state of the robot

- [ ] Charge the battery with solor. Have the bot detect teh current charge and automatically find bright spots to charge its own battery

- [ ] detect that we're not driving in a straight line (happens with cheap motors, cheap wheels shrug 🤷‍♂️) and adjust
