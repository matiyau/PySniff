# ReadMe

PySniff is a set of scripts for logging captured WLAN packets and runnung analysis on the detected MAC addresses.

## Info

### Course
ET4394 - Wireless IoT & Local Area Networks

### Group
8

### OS Compatibility
Ubuntu

## Usage

### Capture

1. In order to start capturing packets, navigate to the *PROJECT_ROOT* directory and run:
```bash
python3 capture.py [options]
```

2. For more info, execute:
```bash
python3 capture.py --help
```

3. In order to setup a capturing service, which starts at boot and runs continuously, navigate to the *PROJECT_ROOT/service* and run:
```bash
./service_setup.sh
```

### Analysis

Not implemented yet

