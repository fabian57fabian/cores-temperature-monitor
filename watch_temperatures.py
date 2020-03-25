import os
import time
import datetime

"""
Requires lm-sensors installed
"""

sleep_time = 5
folder = "./temperatures/"
starting_line = "Core"


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")


def main():
    if not os.path.exists(folder):
        os.mkdir(folder)
    separator = " "
    newline = "\n"
    out_filename = os.path.join(folder, timestamp() + ".txt")
    try:
        with open(out_filename, 'w') as outfile:
            outfile.write("HEADER: timestamp Core0 Core1 Core2 Core3 Core4 Core5 Core6 Core7\n")
        while True:
            ts = timestamp()
            # os.system("sensors > " + os.path.join(folder, filename))
            stream = os.popen("sensors")  # > " + os.path.join(folder, filename))
            output = stream.read()
            cores_temp = []
            for line in output.split("\n"):
                if line.startswith(starting_line):
                    split_line = line.split(':')
                    core_num = int(split_line[0].split(' ')[1])
                    core_str = split_line[0].replace(" ", "")
                    split_tmp = split_line[1][:split_line[1].find('(')]
                    temper = split_tmp.replace(" ", "").replace("+", "").replace("°C", "")
                    temper = float(temper)
                    cores_temp.append(temper)
            with open(out_filename, 'a') as outfile:
                outfile.write(str(ts) + separator)
                for temp in cores_temp:
                    outfile.write(str(temp) + separator)
                outfile.write(newline)
            avg = sum(cores_temp) / len(cores_temp)
            print("Avg on all cpus: %f" % avg)
            time.sleep(sleep_time)
    except KeyboardInterrupt as e:
        print("Exiting")


if __name__ == '__main__':
    main()
