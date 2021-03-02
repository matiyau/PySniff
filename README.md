# ReadMe

PySniff is a set of scripts for logging captured WLAN packets and runnung analysis on the detected MAC addresses.

## Info

### Course
ET4394 - Wireless IoT & Local Area Networks

### Group
8

### OS Compatibility
Tested on Ubuntu 20.04 and 20.10

## Usage

### Short Version
To generate plots for [already gathered data](./logs), run the following command:
```bash
python3 analyse.py
```

More details on the usage can be found below. 

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

1. The pcap and pickled versions of the captured packets are stored in [logs/pcap_filt](./logs/pcap_filt) and [logs/pickle](./logs/pickle) directories.

2. For generating pickles for files in a custom directory, edit the *IN_DIR* and *OUT_DIR* variables in [generate_pickles.py](./generate_pickles.py) and run
```bash
python3 generate_pickles.py
```

3. In order to plot data for pickled files, edit the *PICKLE_DIR* variable in [analyse.py](./analyse.py) and run
```bash
python3 analyse.py
```

### Report
The LaTeX source and pdf version of the report can be found in the [report](./report) directory.
