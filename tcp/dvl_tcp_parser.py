#!/usr/bin/python3

import argparse
import csv
import datetime
import json
import socket

class _CSVWriter:
    def __init__(self, csv_file, message_type):
        self.csv_file = csv_file
        self.csv_writer = self._csv_writer(csv_file, message_type)

    @classmethod
    def _csv_field_names(cls, message_type):
        if message_type == "velocity":
            return [
                "log_time",
                "time_of_validity",
                "time_of_transmission",
                "time",
                "vx",
                "vy",
                "vz",
                "fom",
                "altitude",
                "velocity_valid",
                "status" ]
        return [
            "log_time",
            "ts",
            "x",
            "y",
            "z",
            "std",
            "status" ]

    @classmethod
    def _csv_writer(cls, csv_file, message_type):
        csv_writer = csv.DictWriter(
            csv_file,
            fieldnames = cls._csv_field_names(message_type),
            extrasaction = "ignore",
            delimiter = ',')
        csv_writer.writeheader()
        return csv_writer

    def writerow(self, row):
        self.csv_writer.writerow(row)

    def flush(self):
        self.csv_file.flush()

def _start_dvl_socket(dvl_ip):
    dvl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dvl_socket.connect((dvl_ip, 16171))
    return dvl_socket

def _type(message_type):
    if message_type == "velocity":
        return "velocity"
    return "position_local"

def _format_timestamp(timestamp, time_format):
    return datetime.datetime.strftime(
        datetime.datetime.fromtimestamp(timestamp),
        time_format)

def _format_timestamps(message_type, message, time_format):
    message["log_time"] = _format_timestamp(
        message["log_time"] / 1e6,
        time_format)
    if message_type == "velocity":
        try:
            message["time_of_validity"] = _format_timestamp(
                message["time_of_validity"] / 1e6,
                time_format)
            message["time_of_transmission"] = _format_timestamp(
                message["time_of_transmission"] / 1e6,
                time_format)
        except KeyError:
            pass
    else:
        message["ts"] = _format_timestamp(message["ts"], time_format)

def _handle(message_type, message, time_format, csv_writer):
    if not message:
        return
    try:
        report = json.loads(message)
    except json.decoder.JSONDecodeError:
        print("Could not parse to JSON: " + message)
        return
    if report["type"] != message_type:
        return
    report["log_time"] = int(datetime.datetime.utcnow().timestamp() * 1e6)
    if time_format:
        _format_timestamps(message_type, report, time_format)
    print(json.dumps(report))
    if csv_writer is not None:
        csv_writer.writerow(report)
        csv_writer.flush()

def _process_messages(dvl_socket, message_type, time_format, csv_writer = None):
    buffer_size = 4096
    message = ""
    while True:
        buffer = dvl_socket.recv(buffer_size).decode()
        if not buffer:
            continue
        message_parts = buffer.split("\r\n")
        if len(message_parts) == 1:
            message += message_parts[0]
            continue
        for message_part in message_parts[:-1]:
            message = message + message_part
            _handle(message_type, message, time_format, csv_writer)
            message = ""
        if message_parts[-1]:
            message = message_parts[-1]

def arguments_parser():
    parser = argparse.ArgumentParser(
        description = "Extract data from DVL TCP stream")
    parser.add_argument(
        "message_type",
        choices = [ "velocity", "dead_reckoning" ],
        help = "Type of DVL message to handle")
    parser.add_argument(
        "-i",
        "--ip",
        default = "192.168.2.95",
        help = "IP address of DVL")
    parser.add_argument(
        "-t",
        "--time_format",
        help = (
            "A string describing a date and time format using the directives " +
            "in the table at the following link.\n\n " +
            "https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior" +
            "\nFor example, %%Y-%%m-%%dT%%H-%%M-%%S.%%fZ would be the string " +
            "for obtaining the format of the ISO 8601 standard. If provided, " +
            "the format string will be applied to all timestamps in the " +
            "message"))
    parser.add_argument(
        "-c",
        "--csv",
        default = "",
        help = (
            "Path to CSV file. If a non-empty path is provided, the " +
            "extracted positions will be saved to a CSV file at that path"))
    return parser

def main():
    arguments = arguments_parser().parse_args()
    csv_file_path = arguments.csv
    message_type = _type(arguments.message_type)
    time_format = arguments.time_format
    if csv_file_path:
        with open(csv_file_path, "w") as csv_file:
            _process_messages(
                _start_dvl_socket(arguments.ip),
                message_type,
                time_format,
                _CSVWriter(csv_file, arguments.message_type))
    else:
        _process_messages(
            _start_dvl_socket(arguments.ip),
            message_type,
            time_format)

if __name__ == "__main__":
    main()
