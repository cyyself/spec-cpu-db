#!/usr/bin/env python3

from pathlib import Path
import sys
import csv

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
    dir = sys.argv[1]
    result = extract_from_dir(Path(dir))
    writer = csv.writer(sys.stdout)
    writer.writerow(['benchmark']+list(result[next(iter(result))].keys()))
    for key, value in result.items():
        writer.writerow([key]+list(value.values()))
