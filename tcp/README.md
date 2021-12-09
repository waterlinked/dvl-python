dvl-python - TCP
================

Code for working with TCP protocol output from the Water Linked DVL.

Contains the following scripts.

| Script             | Description                                                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| dvl_tcp_parser.py  | Parses the TCP output stream from the DVL, extracting velocity or dead reckoning messages, adding a `log_time` parameter whose value is the Unix timestamp in microseconds at the moment the message is parsed, and optionally saving them to a CSV file   |
| plot_dead_reckoning_positions.py | Plots dead reckoning positions from a CSV file. Can be used with a CSV file that is being updated live, e.g. by means of the dvl_tcp_parser.py script, or to playback an existing file |

Pre-requisites
--------------

None for the script `dvl_tcp_parser.py`.

The script `plot_dead_reckoning_positions.py` requires that the Python package `matplotlib` be available, for example in a virtual environment. To set up such a virtual environment, one can run the following.

```
python3 -m venv venv
source venv/bin/activate
pip install matplotlib
deactivate
```

This creates a directory `venv` in the directory in which you ran the above commands.

Therefter, before running the script `plot_dead_reckoning_positions.py`, one needs to activate the virtual environment by running the following from the same directory as contains the directory `venv`.

```
source venv/bin/activate
```

One then runs the script `plot_dead_reckoning_positions.py` as explained below. When done, the virtual environment can be de-activated by running the following from the same directory.

```
deactivate
```

Usage
-----

### dvl_tcp_parser.py

To see all command line options:

```
python dvl_tcp_parser.py --help
```

Typical use:

| Command                                                                         | Description                                                                                                                                       |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python dvl_tcp_parser.py velocity`                                             | Print velocity messages to stdout. Assumes IP address of DVL to be 192.168.2.95 |
| `python dvl_tcp_parser.py velocity -i 10.11.12.100`                             | Same as above with IP address of DVL specified to be 10.11.12.100 |
| `python dvl_tcp_parser.py velocity -c velocities.csv`                           | Print velocity messages to stdout and also save them to a CSV file named 'velocities.csv' (any file path can be used). Assumes IP address of DVL to be 192.168.2.95  |
| `python_dvl_tcp_parser.py velocity -t "%Y-%m-%dT%H-%M-%S.%fZ"`                   | Format all timestamps in velocity messages with the provided time format string: the format string in this example would give the format of the ISO 8601 standard, i.e. Year-Month-DayTHour-Minute-Second.MillisecondZ |
| `python dvl_tcp_parser.py velocity -i 10.11.12.100 -t "%Y-%m-%dT%H-%M-%S.%fZ"`  | Combines the IP address and time format options for velocity messages |
| `python dvl_tcp_parser.py velocity -i 10.11.12.100 -c velocities.csv`           | Combines the IP address and saving to CSV options for velocity messages |
| `python dvl_tcp_parser.py velocity -i 10.11.12.100 -t "%Y-%m-%dT%H-%M-%S.%fZ" -c velocities.csv` | Combines all three options for velocity messages |
| `python dvl_tcp_parser.py dead_reckoning`                                       | Print dead reckoning messages to stdout. Assumes IP address of DVL to be 192.168.2.95  |
| `python dvl_tcp_parser.py dead_reckoning -i 10.11.12.100`                       | Same as above with IP address of DVL specified to be 10.11.12.100 |
| `python_dvl_tcp_parser.py dead_reckoning -t "%Y-%m-%dT%H-%M-%S.%fZ"`                   | Format all timestamps in dead reckoning messagess with the provided time format string: the format string in this example would give the format of the ISO 8601 standard, i.e. Year-Month-DayTHour-Minute-Second.MillisecondZ |
| `python dvl_tcp_parser.py dead_reckoning -c dead_reckoning.csv`                 | Print dead reckoning messages to stdout and also save them to a CSV file named 'dead_reckoning.csv' (any file path can be used). Assumes IP address of DVL to be 192.168.2.95 |
| `python_dvl_tcp_parser.py dead_reckoning -i 10.11.12.100 -t "%Y-%m-%dT%H-%M-%S.%fZ"` | Combines the IP address and time format options for dead reckoning messages |
| `python dvl_tcp_parser.py dead_reckoning -i 10.11.12.100 -c dead_reckoning.csv` | Combines the IP address and saving to CSV options for dead reckoning messages |
| `python_dvl_tcp_parser.py dead_reckoning -i 10.11.12.100 -t "%Y-%m-%dT%H-%M-%S.%fZ" -c dead_reckoning.csv` | Combines all three options for dead reckoning messages  |

The permitted modifiers of the time format string are those documented [here](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior).

To modify which fields are saved into the CSV file, adjust the arrays in the function `_csv_field_names`.

To disable printing to stdout, or handle the velocity or dead reckoning messages in a different way, comment out or replace the line `print(json.dumps(report))` in the function `_handle`.


### plot_dead_reckoning_positions.py

As described in the section 'Pre-requisites' above, first open a virtual environment containing `matplotlib`.

To see all command line options:

```
python plot_dead_reckoning_positions.py --help
```

Typical use in general:

| Command                                                            | Description |
| ------------------------------------------------------------------ | ----------- |
| `python plot_dead_reckoning_positions.py "dvl_data.csv"`           | Plots in 2-D the x and y coordinates of the dead reckoning data in a file named 'dvl_data.csv' (any path can be used). This file can be written to at the same time as the script is run, i.e. the script can be used to plot dead reckoning data 'live', or to playback an existing file. The x and y coordinates must be given in the third and fourth columns from the left respectively (which is the case for CSV files created using the `dvl_tcp_parser.py` script |
| `python plot_dead_reckoning_positions.py "dvl_data.csv" -3`        | Same as above except that the plot is in 3-D of the x, y, and z coordinates of the dead reckoning data, which must be given in the third, fourth, and fifth columns from the left respectively of the CSV file |
| `python plot_dead_reckoning_positions.py "dvl_data.csv" -d 1.5`    | Same as in the first row except that there is a delay in seconds specified by the `-d` parameter (1.5 seconds in this case) between the plotting of points. |
| `python plot_dead_reckoning_positions.py "dvl_data.csv" -3 -d 1.5` | Same as in the second row, except that there is a delay between plotting of points as in the third row |

Typical use when combined with the `dvl_tcp_parser.py` script:

1. Run
    ```
    python plot_dead_reckoning_positions.py "dvl_data.csv"
    ```
    or one of the variations on this command in one terminal

2. Run
    ```
    python dvl_tcp_parser.py dead_reckoning -c "dvl_data.csv"
    ```
    in another terminal


References
==========

[Water Linked DVL TCP protocol](https://waterlinked.github.io/dvl/dvl-protocol/#ethernet-protocol-tcp)
