dvl-python - TCP
----------------

Code for working with TCP protocol output from the Water Linked DVL.

Usage
=====

To see all command line options:

```
python dvl_tcp_parser.py --help
```

Typical use:

| Command                                                                         | Description                                                                                                                                       |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python dvl_tcp_parser.py velocity`                                             | Print velocity messages to stdout. Assumes IP address of DVL to be 192.168.2.95                                                                   |
| `python dvl_tcp_parser.py velocity -i 10.11.12.100`                             | Same as above with IP address of DVL specified to be 10.11.12.100                                                                                 |
| `python dvl_tcp_parser.py velocity -c velocities.csv`                           | Print velocity messages to stdout and also save them to a CSV file named 'velocities.csv'. Assumes IP address of DVL to be 192.168.2.95           |
| `python dvl_tcp_parser.py velocity -i 10.11.12.100 -c velocities.csv`           | Same as above with IP address of DVL specified to be 10.11.12.100                                                                                 |
| `python dvl_tcp_parser.py dead_reckoning`                                       | Print dead reckoning messages to stdout. Assumes IP address of DVL to be 192.168.2.95                                                             |
| `python dvl_tcp_parser.py dead_reckoning -i 10.11.12.100`                       | Same as above with IP address of DVL specified to be 10.11.12.100                                                                                 |
| `python dvl_tcp_parser.py dead_reckoning -c dead_reckoning.csv`                 | Print dead reckoning messages to stdout and also save them to a CSV file named 'dead_reckoning.csv'. Assumes IP address of DVL to be 192.168.2.95 |
| `python dvl_tcp_parser.py dead_reckoning -i 10.11.12.100 -c dead_reckoning.csv` | Same as above with IP address of DVL specified to be 10.11.12.100                                                                                 |


To modify which fields are saved into the CSV file, adjust the arrays in the function `_csv_field_names`.

To disable printing to stdout, or handle the velocity or dead reckoning ways in a different way, comment out or replace the line `print(json.dumps(report))` in the function `_handle`.


References
==========

[Water Linked DVL TCP protocol](https://waterlinked.github.io/dvl/dvl-protocol/#ethernet-protocol-tcp)
