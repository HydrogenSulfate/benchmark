#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

import datetime
import re
import sys
import json
import os

def analyze(model_item, log_file, res_log_file, device_num, bs, fp_item, time_pat, skip_num=3):
    time_pat = re.compile(time_pat)
    logs = open(log_file).readlines()
    logs = ";".join(logs)
    time_res = time_pat.findall(logs)
    time_res = [tuple(map(int, x)) for x in time_res]

    gpu_num = int(device_num[3:])
    run_mode = "DP"
    bs = int(bs)
    ips = 0

    if len(time_res) > skip_num + 1:
        time_res = time_res[skip_num:]
        curr_year = datetime.datetime.today().year
        st_time = datetime.datetime(curr_year, *time_res[0])
        ed_time = datetime.datetime(curr_year, *time_res[-1])
        if ed_time <= st_time:
            ed_time = datetime.datetime(curr_year + 1, *time_res[-1])
        avg_time = (ed_time - st_time).total_seconds() / (len(time_res) - 1)
        ips = round(bs / avg_time, 3) * gpu_num
    model_name = model_item+"_"+"bs"+str(bs)+"_"+fp_item+"_"+run_mode
    info = {    "model_branch": os.getenv('model_branch'),
                "model_commit": os.getenv('model_commit'),
                "model_name": model_name,
                "batch_size": bs,
                "fp_item": fp_item,
                "run_process_type": "MultiP",
                "run_mode": run_mode,
                "convergence_value": 0,
                "convergence_key": "",
                "ips": ips,
                "speed_unit":"images/s",
                "device_num": device_num,
                "model_run_time": os.getenv('model_run_time'),
                "frame_commit": "",
                "frame_version": os.getenv('frame_version'),
        }
    json_info = json.dumps(info)
    print(json_info)
    with open(res_log_file, "w") as of:
        of.write(json_info)

if __name__ == "__main__":
    if len(sys.argv) != 8:
        sys.exit()

    model_item = sys.argv[1]
    log_file = sys.argv[2]
    res_log_file = sys.argv[3]
    device_num = sys.argv[4]
    bs = sys.argv[5]
    fp_item = sys.argv[6]
    time_pat = sys.argv[7]
    analyze(model_item, log_file, res_log_file, device_num, bs, fp_item, time_pat)