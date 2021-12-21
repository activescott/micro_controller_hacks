# Robot Alpha

This is a relatively simple robot to build on. The general goal is to have an autonomous robot that can move around and avoid obstacles using various sensors. We'll see what else we add...

## Notes and learning

### Code
NOTE: So this was a simple robot that involved writing multiple drivers for sensors and devices (`micropython-hcsr04` for ultrasonic distance, `micropython-motor-driver-dual-tb6612fng`, `micropython-open-lcd-driver`, `micropython-qmc5883l-magnetic-compass-sensor-driver`, `micropython-wheel-encoder-hall-effect-sensor`). I decided to just hack my way through the main code of the robot to keep the simplest thing working. It started with literally "go forward and stop", next was "go forward and stop before you hit something", and these gradually got more sophisticated as I learned the nuances of things like ultrasonic, the challenges of carpet, why practical robots are round (because their wheels don't stick out and they can always turn/spin safely). It was called robot-a because I kinda figured I'd get to a point where I'd start a new and I here we are... So onto robot-b

### Motors

- **faster is harder**: I learned that going too fast makes it hard to stop fast enough before hitting the obstacle. I know, "duh", right? This wasn't obvious to me at first though. I tried various things like briefly backing up to stop faster and that sorta helped but introduced new problems. For example, it would move back too far and then not see an obstacle and blast forward again 🤣. For now I was able to just make the robot always go slower and it mitigated this issue.
- **devices act weird when underpowered**: I had an LCD sensor that worked perfectly by itself. Then when I integrated it into the robot it went bockers and I started getting weird IO errors. Turned out it was due to the motors running and take too much power off of the USB bus. The motors worked fine and the LCD kinda did, but would frequently just appear to crash the firmware (or turn off momentarily?) and cause IO exceptions. Hooking up a battery pack to the motors/motor driver and the pico at the same time made a world of difference.

### Hall Effect Sensors for Motor/Wheel Speed Tracking

So I worked with so-called "wheel encoder" kit which is really just a hall effect sensor and an 8-pole circular magnet on the wheel. You detect the magnet poles changing, count the poles and then you can reasonably accurately detect how fast a wheel is spinning.

There are two basic approaches here, IRQ or rapid reading in a loop. I first started by using an IRQ. However, IRQs are extremely sensitive to voltage changes (they will fire multiple times within a handful of *micro*seconds due to slight variations in voltage) while the underlying digital signal either hasn't changed or has changed back and forth so quickly that my IRQ handler (aka "ISR") can't read the pin fast enough to tell. IRQs are also hard to work with since [IRQs have a ton of constraints](https://docs.micropython.org/en/latest/reference/isr_rules.html): They must run and exit super fast and generally cannot allocate heap memory (which in MicroPython happens in subtle ways such as creating floating point values).
So this means you have to de-noise and debounce IRQ interrupt readings and due to the constraints of ISRs you have to do it in rather inconvenient ways.

**Using a Loop**: I tried to use a loop reading the pin in a loop using [asynchio](https://docs.micropython.org/en/latest/library/uasyncio.html) (i.e. green threads) to just very frequently read that sensor and this worked in simple applications. It was simple, straightforward code and gave near perfect results. I could very accurately rotate a wheel multiple rotations. However, as soon as I incorporated it into a robot with much more activity happening the results were wildly inconsistent. The wheels would be spinning at the same sped but I'd see one second ~41 RPM and in another 0.1 RPM and I decided that asyncio loop was just being time-sliced at very inconsistent intervals. So back to IRQs...

**IRQs** My next go around with IRQs was much cleaner. I simplified things to their essence and I think I understood the test scenarios much better and pretty quickly got things working well. The biggest challenge here is that the IRQ handling has to be simple and you just have to be aware that it will be called very frequently with the same value regardless of the configuration of the pin/IRQ trigger (I'm ont sure if this is the RP2 processor or the sensor or both).

### Pico

Multiple power sources:

- For the Pico I use ita 3V3 (OUT) pin (pin 36) to power devices. I plug this into one power rail on a bread board. For sensors and LCDs it's fine. For motors its not.
- I use a standard USB battery (i.e. an extra battery pack for a phone) and plug it into one rail on the breadboard using a simple USB breakout board). It is essentially a ~5 volt power rail on one side of the bread board.
- Connect the grounds of each rail together.
- Connect the 5V rail to the VSYS pin on the Pico (pin 39). This will power the pico without anything being plugged into USB and allows the robot to be mobile. It's fine to leave both the USB plugged into the Pico and the 5V rail connected to VSYS (I gritted my teeth at one point and checked and its been that way for a while now without any problems). I later found that the [Pico Datasheet](https://datasheets.raspberrypi.com/) explained in detail how this all works.

### Ultrasonic Distance Sensors

- An ultrasonic sensor (HC-SR04) is a cheap way to detect distance. Super easy to use and quite accurate _most of the time_. However, at times it just returns completely nonsensical readings. It is due to the environment. Some specific observations on this:
- **Leave a gap between the front of the bot and the sensor**: If your ultrasonic sensor is in the very front of the robot and it gets close to a wall with <2cm of the sensor (approximate) it will start returning values >200cm. So you mount the sensor.
- **Ultrasonic sucks at angles**: At one point I was super stumped as it sat on my desk and gave intermittency bizarre readings at times and I realized later it was pointing across the room into a window with blinds. If I shut the blinds all the way it was reasonably consistent readings. With the blinds open and the bot pointed that direction it was super wacky returning readings like <1cm.
- **Ultrasonic sucks at angles**: Take your sensor and point it directly at a wall about 10cm away. Good reading right? Now, aim it at a ~45deg angle towards the wall also at about 10cm. I usually see >200cm readings.

## Todo:

- [+] Move forward and stop before hitting an obstacle
- [+] after stopping... avoid an obstacle by turning and finding a direction to go in that doesn't have an obstacle
- [ ] Come up with way to turn a specified number of degrees according to compass (this will be a good test of agent design it requires concurrency)
- [ ] Backup a recorded *distance* rather than for a given time: Sometimes surface impacts distance traveled during a given time. For example when on a rug he'll go only a fraction of the distance that he'll go on a hard surface.
- [ ] refactor state machine to a series of pub/sub messages consumed and published by **Agents**:
  - **Agents** can publish or consume messages and proffer which ones they are listening for and publishing. Potential agents: Distance, Drive, Compass, Display/LCD, Bumpers, Speech, Visual, etc.
  - A **broker** handles registration of agents and pub/sub of messages to/from agents
  - **Messages** have a name and a set of well-defined parameters.
  - **Context**: At any given time there is a "system context" of the system overall that is an aggregation of state provided by agents. Each agent provides a `context` and `name` that the broker uses to assemble a system state (`systemState.<agent name>` => `agent.state`). This way agents only modify their own state, but can read state from any agent and have no coupling to any agent beyond the agent's name to access state.
  - **Intents, Actions & States**: In the simplest state machine it was even clear that "actions" needed separated from states. So an action had to be specified based on state (e.g. wheel stuck) and another handler would change state to handle that action. Furthermore, as things get more complex it is obvious that intent needs to be separated from action because one Agent's intent to move forward (e.g. go there!) might need overriden by another agent (e.g. Obstacle detected! or wheel is stuck so don't bother!).
- [ ] when avoiding obstacle instead of choosing the first "free" direction to go in, spin 360 deg and find the direction to go with the greatest distance we can go in a straight line
- [ ] Slow down as an obstacle gets closer
- [ ] make the logger periodically check the size or line count in the log file and delete older lines.
- [ ] LCD sensor that shows the current activity/state of the robot

- [ ] Charge the battery with solor. Have the bot detect teh current charge and automatically find bright spots to charge its own battery

- [ ] detect that we're not driving in a straight line (happens with cheap motors, cheap wheels shrug 🤷‍♂️) and adjust
