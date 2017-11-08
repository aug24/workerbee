# workerbee
An interface to a honeycomb, created by a drone.

## Setup

Pip installs:
 * pandas
 * requests
 * plotly

Set and export PYTHONPATH.

# Usage

## Expose password (required for non-interactive use, optional for interactive)

```
  read -s -p "Hivehome password: " WORKERBEE_PASSWORD; echo
  export WORKERBEE_PASSWORD
```

## Interactive usage

```
  python interactive.py [--username <user name>] [--debug]
```

## Command line usage (so far)

To create a graph of the last 24 hours 'temperature' channel from a specific device:

```
  python graph.py --username <user name> --device <device name> --filename <file name> [--debug]
```
