#!/usr/bin/env python3

import sys
import re

if __name__ == "__main__":
    filename = sys.argv[1]
    prefix = sys.argv[2]
    buf = []
    cur_filename = ""
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines + ['# started on \n']:
            if line.startswith('# started on '):
                if len(buf) > 0:
                    if cur_filename == "":
                        print("Error: cur_filename is empty")
                        sys.exit(1)
                    print(f"write {cur_filename}")
                    with open(prefix + cur_filename, 'w+') as f:
                        f.writelines(buf)
                    buf = []
                cur_filename = line.split(' ')[3].strip()
            else:
                buf.append(line)
                if line.startswith(' Performance counter stats for '):
                    # Assume the filename is in the format /000.<filename>/
                    # For example, "/400.perlbench/"
                    r = re.compile("(/[0-9]{3}.[A-Za-z0-9]+/)")
                    m = r.search(line)
                    if m:
                        cur_filename = m.group(1).strip().replace('/', '')
