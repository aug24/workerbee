# workerbee
An interface to a honeycomb, created by a drone.

# Setup

Pip installs:
 * pandas
 * requests
 * plotly

# Basic usage (so far):

To create a graph of the last 24 hours 'temperature' channel from a specific device:

```
  read -s -p "Hivehome password: " WORKERBEE_PASSWORD; echo
  export WORKERBEE_PASSWORD
  python graph.py --username <user name> --device <device name> --filename <file name>
```
