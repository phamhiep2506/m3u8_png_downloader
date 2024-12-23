#!/usr/bin/env python

import requests
import os
import argparse
import re
import shutil


def download_ts(url: str, referer: str, index: int):
    if os.path.exists(f"{os.getcwd()}/ts/{index}.ts") is True:
        return

    res = requests.get(url, headers={"Referer": referer})

    ts = open(f"{os.getcwd()}/ts/{index}.ts", "wb")
    # png_1x1_1bit
    png_1x1 = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00\x25\xdb\x56\xca\x00\x00\x00\x03\x50\x4c\x54\x45\x00\x00\x00\xa7\x7a\x3d\xda\x00\x00\x00\x01\x74\x52\x4e\x53\x00\x40\xe6\xd8\x66\x00\x00\x00\x0a\x49\x44\x41\x54\x08\xd7\x63\x60\x00\x00\x00\x02\x00\x01\xe2\x21\xbc\x33\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60"
    # png_1x1_8bit = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x77\x53\xde\x00\x00\x00\x10\x49\x44\x41\x54\x78\x9c\x62\xfa\xff\xff\x3f\x20\x00\x00\xff\xff\x06\x06\x03\x00\xb7\x66\x11\x21\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60"
    ts.write(res.content.replace(png_1x1, b""))
    ts.close()


def download_m3u8(url: str, referer: str):
    count = 0
    total_line = 0
    res = requests.get(url, headers={"Referer": referer})
    for line in res.iter_lines():
        if re.search("https", line.decode("utf-8")):
            total_line = total_line + 1

    merge = open(f"{os.getcwd()}/merge.txt", "w")

    for line in res.iter_lines():
        if re.search("https", line.decode("utf-8")):
            count = count + 1
            print(f"Downloading {count}/{total_line}")
            merge.write(f"file 'ts/{count}.ts'")
            merge.write("\n")
            download_ts(line.decode("utf-8"), referer, count)

    merge.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input url m3u8")
    parser.add_argument("-r", "--referer", help="Referer url")
    parser.add_argument("-c", "--continued", action="store_true", help="Continue downloading")
    args = parser.parse_args()

    path_ts = os.path.join(os.getcwd(), "ts")

    if args.continued is False:
        if os.path.exists(path_ts):
            shutil.rmtree(path_ts)
        if not os.path.exists(path_ts):
            os.mkdir(path_ts)

    download_m3u8(args.input, args.referer)
