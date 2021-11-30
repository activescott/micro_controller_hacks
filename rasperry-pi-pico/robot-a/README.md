# Robot Alpha
This is a relatively simple robot to build on. The general goal is to have an autonomous robot that can move around and avoid obstacles using various sensors. We'll see what else we add...

## Notes and learning
- An ultrasonic sensor (HC-SR04) is a cheap way to detect distance. Super easy to use and quite accurate _most of the time_. However, at times it just returns completely nonsensical readings. I presume due to the environment. At one point I was super stumped as it sat on my desk and gave intermittency bizarre readings at times and I realized later it was pointing across the room into a window with blinds. If I shut the blinds all the way it was pretty consistent. With the blinds open and the bot pointed that direction it was super wacky returning readings like <1cm.
- I learned that going too fast makes it hard to stop fast enough before hitting the obstacle. I know, "duh", right? This wasn't obvious to me at first though. I tried various things like briefly backing up to stop faster and that sorta helped but introduced new problems. For example, it would move back too far and then not see an obstacle and blast forward again 🤣. For now I was able to just make the robot always go slower and it mitigated this issue.



## Todo:
- [+] Move forward and stop before hitting an obstacle
- [ ] after stopping... avoid an obstacle by turning and finding a direction to go in that doesn't have an obstacle
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