import os
import matplotlib.pyplot as plt
import time
import datetime
import argparse
import multiprocessing

delimiter = " "


def read_remperatures(filename):
    data = {}
    for i in range(multiprocessing.cpu_count()):
        data[str(i)] = []
    first_ts = True
    start_ts = ""
    last_ts = ""
    with open(filename, 'r') as in_file:
        try:
            for line in in_file.readlines():
                if not line.startswith("HEADER"):
                    splitted = line.split(delimiter)
                    if first_ts:
                        start_ts = splitted[0]
                        first_ts = False
                    last_ts = splitted[0]
                    for i in range(1, len(splitted) - 1, 1):
                        data[str(i - 1)].append(float(splitted[i]))
                    a = 4
        except Exception as e:
            print("Errors while trying to read %s: %s" % (filename, str(e)))
    return data, start_ts, last_ts


def main(filename, core=-1):
    cores_count = multiprocessing.cpu_count()
    r, c = 1, 1
    if cores_count == 2:
        r, c = 2, 1
    elif cores_count <= 4:
        r, c = 2, 2
    elif cores_count <= 6:
        r, c = 2, 3
    elif cores_count <= 8:
        r, c = 2, 4
    else:
        r, c = 4, 4
    fig = plt.figure()
    while True:
        print("Gathering data...")
        data, start_ts, end_ts = read_remperatures(filename)
        plt.clf()
        if core == -1:
            plt.title("Temperatures from %s to %s" % (start_ts, end_ts))
            for (k, d) in data.items():
                plt.subplot(r, c, int(k) + 1)
                plt.plot(d, label="Core {}".format(int(k) + 1))
                plt.legend()
        else:
            plt.title("Temperatures from %s to %s" % (start_ts, end_ts))
            plt.plot(data[str(core)], label="Core {}".format(core))
            plt.legend()
        plt.show(block=False)
        plt.pause(6)


if __name__ == '__main__':
    cores_count = multiprocessing.cpu_count()
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default="_", help="Path to file watched")
    parser.add_argument('--core', type=int, default=-1, help="Core to show in  [0, {}]. If no core passed, plotting all cores".format(cores_count - 1))
    args = parser.parse_args()
    if args.path == "_":
        folder = "./temperatures/"
        files = os.listdir(folder)
        files.sort()
        args.path = os.path.join(folder, files[-1])
        print("Taking last temperature file: %s" % args.path)
    else:
        print("Using selected temperature file: %s" % args.path)
    main(args.path, args.core)
