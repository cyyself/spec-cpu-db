#!/usr/bin/env python3

import sys
import re

SHOW_PERF = True
SHOW_TIME = False
SHOW_USER = False
SHOW_SYS = False
SIMPLE_NAME = False

if __name__ == "__main__":
    filename = sys.argv[1]
    buf = []
    cur_cmd = ""
    with open(filename, 'r') as f:
        lines = f.readlines()
        cur_filename = ""
        for line in lines + ['# started on \n']:
            if line.startswith('# started on '):
                if len(buf) > 0:
                    if cur_filename == "":
                        print("Error: cur_filename is empty", file=sys.stderr)
                        sys.exit(1)
                    # write from buf
                    is_counter = False
                    for x in buf:
                        if x.strip().endswith('seconds time elapsed'):
                            is_counter = False
                            if SHOW_TIME:
                                time = x.strip().split()[0]
                                print(f"{cur_filename},time,{time}")
                        if x.strip().endswith('seconds user') and SHOW_USER:
                            time = x.strip().split()[0]
                            print(f"{cur_filename},user,{time}")
                        if x.strip().endswith('seconds sys') and SHOW_SYS:
                            time = x.strip().split()[0]
                            print(f"{cur_filename},sys,{time}")
                        if is_counter:
                            if '#' in x:
                                x = x.strip().split('#')[0].strip()
                            data = x.strip().replace('<not counted>','0').replace(',','').split()
                            if len(data) == 2 and SHOW_PERF:
                                print(f"{cur_filename},{data[1]},{data[0]}")
                        if x.strip().startswith('Performance counter stats for '):
                            is_counter = True
                    buf = []
            else:
                buf.append(line)
                if line.startswith(' Performance counter stats for \''):
                    # find filename
                    split_l = line.find("'")
                    split_r = line.rfind("'")
                    cur_filename = f"\"{line[split_l+1:split_r]}\""
                    if SIMPLE_NAME:
                        r = re.compile("(/[0-9]{3}\\.[A-Za-z0-9_]+/)")
                        m = r.search(cur_filename)
                        if m:
                            cur_filename = m.group(1).strip().replace('/', '')
