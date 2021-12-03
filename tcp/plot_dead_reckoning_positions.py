#!/usr/bin/python3

import argparse
import os

import matplotlib.pyplot as plot

def plot_2d(csv_file_path, plot_delay):
    figure = plot.figure()
    axes = figure.add_subplot(111)
    x = []
    y = []
    line, = axes.plot(x,y)
    figure.canvas.draw()
    plot.show(block = False)
    with open(csv_file_path, "r") as csv_file:
        while True:
            row = csv_file.readline()
            if row:
                row_values = row.split(',')
                try:
                    x.append(float(row_values[1]))
                    y.append(float(row_values[2]))
                except ValueError:
                    continue
                line.set_xdata(x)
                line.set_ydata(y)
                axes.relim()
                axes.autoscale_view(True, True, True)
                figure.canvas.draw()
                plot.pause(plot_delay)

def plot_3d(csv_file_path, plot_delay):
    figure = plot.figure()
    axes = figure.add_subplot(111, projection="3d")
    x = []
    y = []
    z = []
    line,  = axes.plot(x, y, z)
    figure.canvas.draw()
    plot.show(block = False)
    with open(csv_file_path, "r") as csv_file:
        while True:
            row = csv_file.readline()
            if row:
                row_values = row.split(',')
                try:
                    x.append(float(row_values[1]))
                    y.append(float(row_values[2]))
                    z.append(float(row_values[3]))
                except ValueError:
                    continue
                line.set_xdata(x)
                line.set_ydata(y)
                line.set_3d_properties(z)
                axes.axes.set_xlim3d(left = min(x), right = max(x))
                axes.axes.set_ylim3d(bottom = min(y), top = max(y))
                axes.axes.set_zlim3d(bottom = min(z), top = max(z))
                figure.canvas.draw()
                plot.pause(plot_delay)

def arguments_parser():
    parser = argparse.ArgumentParser(
        description = (
            "Plot positions from DVL dead reckoning. Can be used with a " +
            "CSV file that is being updated live, or to playback an existing " +
            "file"))
    parser.add_argument(
        "csv_file_path",
        help = (
            "Path to a CSV file containing dead reckoning data. It is " +
            "assumed that the x, y, and z are in the second, third, and " +
            "fourth columns respectively from the left. In particular, " +
            "the CSV files created by the script dvl_tcp_parser.py have this " +
            "format"))
    parser.add_argument(
        "-3",
        "--three_dimensional",
        action = "store_true",
        help = (
            "Plot the 3D position, i.e. including the z co-ordinate"))
    parser.add_argument(
        "-d",
        "--delay",
        type = float,
        default = 0.01,
        help = (
            "Delay between plotting of one point and the next. Default: " +
            "10 milliseconds"))
    return parser

def main():
    arguments = arguments_parser().parse_args()
    csv_file_path = arguments.csv_file_path
    while not os.path.isfile(csv_file_path):
        pass
    if arguments.three_dimensional:
        plot_3d(csv_file_path, arguments.delay)
    else:
        plot_2d(csv_file_path, arguments.delay)

if __name__ == "__main__":
    main()
