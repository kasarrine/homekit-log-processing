# Kirk Sarrine
# kasarrine@gmail.com

from datetime import datetime
import os
import pathlib
import re


class Solutions:

    def find_log_files(self, directory, log_array):
        # Find all log files in the given directory, add the absolute path of each log file to
        # log_array
        for file_path in pathlib.Path(directory).glob('**/*'):
            extension = os.path.splitext(file_path)[1]
            if extension == '.log' and file_path.as_posix() not in log_array:
                log_array.append(file_path.as_posix())

    def unify_logs(self, log_array, output):
        dic = dict()
        # Iterate through log_array, which contains the absolute paths
        for log in log_array:
            log = open(log, 'r')
            # Loop through each line of file
            while True:
                line = log.readline()
                if not line:
                    log.close()
                    break
                else:
                    # The '-' will occur at least 3 times in a line with a timestamp
                    if line.count("-") >= 3:
                        # Finding the index of the 3rd occurrence of '-'
                        # Ex: 2020-03-11 14:17:55.755113-0700
                        pos = [c.start() for c in re.finditer(r'-', line)][2]
                        # Create a substring to leave out -7000
                        key = line[0:pos]
                        # Convert to date_string/float
                        date_string = datetime.fromisoformat(key).timestamp()

                    if date_string not in dic:
                        # Insert the date_string in the dic as a key in the dic if it's not in there
                        # Set the entire line (string) as the value. Need to convert from string in order
                        # to sort the lines later.
                        dic[date_string] = line
                    else:
                        # Any subsequent lines with no timestamp after the first line with a timestamp
                        # are still part of it, append the string.
                        dic[date_string] += line

        for key in sorted(dic.keys()):
            # Sort the keys(timestamps) then write the value (line) to the file
            output.write(dic[key])
        output.close()

    def unique_senders(self, log):
        dic = dict()
        # Find the index of the last '/' in absolute path
        index = [c.start() for c in re.finditer(r'/', log)]
        index = index[len(index) - 1]
        # Used for Outputting current log file name
        log_print = log[index + 1:]
        log = open(log, 'r')
        while True:
            line = log.readline()
            if not line:
                print("{}:".format(log_print))
                for key in sorted(dic.keys()):
                    print(key, "->", dic[key])
                print("\n")
                log.close()
                break
            else:
                # The '-' will occur at least 3 times in a line with a timestamp
                if line.count("-") >= 3:
                    # Find the indexes of the 2nd occurrence of '[' and ']'
                    # This is the unique sender
                    pos = [c.start() for c in re.finditer(r'\[', line)][1]
                    pos2 = [c.start() for c in re.finditer(r'\]', line)][1]
                    # Create substring and remove '[' and ']'
                    key = line[pos:pos2 + 1].replace('[', '').replace(']', '')
                    if key not in dic:
                        dic[key] = 1
                    else:
                        dic[key] += 1

    def calculate_ping(self, combined_logs):
        # Store found pings in dic
        pings = dict()
        print("Pings:")
        while True:
            line = combined_logs.readline()
            if not line:
                if pings:
                    # If the dic is not empty, there are pings that were not received.
                    # Iterate through keys and print ERROR
                    for key in pings.keys():
                        print("{} ->".format(key), "ERROR")
                combined_logs.close()
                break
            else:
                if 'Sending ping' in line:
                    # Check for Sending ping in line, then split the line
                    split_line = line.split(' ')
                    # Ping ID in split line is 1 index after ping
                    index = split_line.index('ping')
                    ping_id = split_line[index + 1].strip()
                    # Remove round brackets
                    ping_id = ping_id[1:len(ping_id) - 1]
                    # Create a timestamp substring
                    date = split_line[0] + " " + split_line[1][0:split_line[1].index('-')].strip()
                    # Convert to float
                    date_float = datetime.fromisoformat(date).timestamp()
                    if ping_id not in pings:
                        # Add the ping to the dic if not in
                        pings[ping_id] = date_float

                if 'Received ping' in line:
                    # Check for Received ping in line, then split the line
                    split_line = line.split(' ')
                    # Ping ID in split line is 1 index after ping
                    index = split_line.index('ping')
                    ping_id = split_line[index + 1].strip()
                    # Remove round brackets
                    ping_id = ping_id[1:len(ping_id)-1]
                    # Create a timestamp substring
                    date = split_line[0] + " " + split_line[1][0:split_line[1].index('-')].strip()
                    # Convert to float
                    date_float = datetime.fromisoformat(date).timestamp()
                    if ping_id in pings:
                        # If the Ping ID is in the dict at this point, the
                        # ping time is calculated then the Ping ID deleted from the dic
                        print("{} ->".format(ping_id), date_float - pings[ping_id])
                        del pings[ping_id]


a1 = Solutions()
# Used to store the location of all logs in the folder
all_logs = list()

# Exercise 1
# Search for all log file paths in the given folder and add to all_logs
a1.find_log_files(os.getcwd(), all_logs)

# Create UnifiedLogs file
unified_logs = open('UnifiedLogs.log', 'w')
a1.unify_logs(all_logs, unified_logs)

# Exercise 2
# Search for all log files, which adds the UnifiedLogs.log created in Exercise 1 to all_logs
a1.find_log_files(os.getcwd(), all_logs)
# Iterate through all logs to find unique senders
for log in sorted(all_logs):
    a1.unique_senders(log)

# Exercise 3
unified_logs = open('UnifiedLogs.log', 'r')
a1.calculate_ping(unified_logs)