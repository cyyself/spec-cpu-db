#!/usr/bin/env python3

from pathlib import Path
import sys
import csv
import argparse

def read_perf_result(filename: Path):
    result = {}
    with open(filename, 'r') as f:
        for line in f:
            if 'Performance counter stats for' in line:
                continue
            line = line.strip().replace('<not counted>','0').split()
            if len(line) >= 2:
                title = line[1] if line[1] != 'seconds' else " ".join(line[2:])
                value = line[0]
                result[title] = value
    return result

def extract_from_dir(dir: Path):
    result = {}
    with open(dir / 'time.csv', 'r') as f:
        for line in f:
            line = line.strip().split(',')
            result[line[0]] = {'time': line[1]}
    for filename in dir.iterdir():
        if filename.name.startswith('perf_'):
            for file in filename.iterdir():
                if file.name in result:
                    result[file.name].update(read_perf_result(file))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str)
    parser.add_argument('-p', '--prefix-tag', type=str, required=False)
    parser.add_argument('-s', '--suffix-tag', type=str, required=False)
    parser.add_argument('-c', '--col-name', nargs='*', action='extend', required=False)
    args = parser.parse_args()
    dir = args.dir
    prefix_tag = args.prefix_tag
    suffix_tag = args.suffix_tag
    col_name = {}
    if args.col_name is not None:
        for x in args.col_name:
            col_name[x.split('=')[0]] = x.split('=')[1]
    result = extract_from_dir(Path(dir))
    writer = csv.writer(sys.stdout)
    # col_name, prefix, suffix
    keys = list(result[next(iter(result))].keys())
    if col_name != {}:
        keys = col_name.values()
    if prefix_tag is not None:
        keys = [prefix_tag + x for x in keys]
    if suffix_tag is not None:
        keys = [x + suffix_tag for x in keys]
    writer.writerow(['benchmark']+keys)
    # write result
    for benchmark, value in result.items():
        result = {}
        for key, val in value.items():
            if col_name != {}:
                if key in col_name:
                    result[col_name[key]] = val
            else:
                result[key] = val
        result_list = [result[key] for key in col_name.values()]
        writer.writerow([benchmark]+result_list)
