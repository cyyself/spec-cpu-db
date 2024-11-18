#!/usr/bin/env bash

./scripts/extract_perf_result.py --dir 2006/apple-m1/gcc2272cd2508-o3  -p 'nolto-ccmp-' \
-c 'apple_firestorm_pmu/branch_mispred_nonspec:u/=branch_miss' \
-c 'apple_firestorm_pmu/inst_branch:u/=branches' \
-c 'apple_firestorm_pmu/instructions:u/=instructions' \
-c 'apple_firestorm_pmu/cycles:u/=cycles'

./scripts/extract_perf_result.py --dir 2006/apple-m1/gcc2272cd2508-o3-noccmp  -p 'nolto-noccmp-' \
-c 'apple_firestorm_pmu/branch_mispred_nonspec:u/=branch_miss' \
-c 'apple_firestorm_pmu/inst_branch:u/=branches' \
-c 'apple_firestorm_pmu/instructions:u/=instructions' \
-c 'apple_firestorm_pmu/cycles:u/=cycles'

./scripts/extract_perf_result.py --dir 2006/apple-m1/gcc2272cd2508-o3-lto  -p 'lto-ccmp-' \
-c 'apple_firestorm_pmu/branch_mispred_nonspec:u/=branch_miss' \
-c 'apple_firestorm_pmu/inst_branch:u/=branches' \
-c 'apple_firestorm_pmu/instructions:u/=instructions' \
-c 'apple_firestorm_pmu/cycles:u/=cycles'

./scripts/extract_perf_result.py --dir 2006/apple-m1/gcc2272cd2508-o3-lto-noccmp  -p 'lto-noccmp-' \
-c 'apple_firestorm_pmu/branch_mispred_nonspec:u/=branch_miss' \
-c 'apple_firestorm_pmu/inst_branch:u/=branches' \
-c 'apple_firestorm_pmu/instructions:u/=instructions' \
-c 'apple_firestorm_pmu/cycles:u/=cycles'