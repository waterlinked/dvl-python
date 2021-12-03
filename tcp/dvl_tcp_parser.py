#!/usr/bin/python3

import argparse
import csv
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
                "time",
                "vx",
                "vy",
                "vz",
                "fom",
                "altitude",
                "velocity_valid",
                "status" ]
        return [
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

def _handle(message_type, message, csv_writer):
    if not message:
        return
    try:
        report = json.loads(message)
    except json.decoder.JSONDecodeError:
        print("Could not parse to JSON: " + message)
        return
    if report["type"] != message_type:
        return
    print(json.dumps(report))
    if csv_writer is not None:
        csv_writer.writerow(report)
        csv_writer.flush()

def _process_messages(dvl_socket, message_type, csv_writer = None):
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
            _handle(message_type, message, csv_writer)
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
    report_type = _type(arguments.message_type)
    if csv_file_path:
        with open(csv_file_path, "w") as csv_file:
            _process_messages(
                _start_dvl_socket(arguments.ip),
                report_type,
                _CSVWriter(csv_file, arguments.message_type))
    else:
        _process_messages(
            _start_dvl_socket(arguments.ip),
            report_type)

if __name__ == "__main__":
    main()
