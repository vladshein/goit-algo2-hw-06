import json
from datasketch import HyperLogLog
from datetime import datetime

# Ініціалізація HyperLogLog
hll = HyperLogLog(p=14)


def read_file(file_name):
    ip_list = []
    with open(file_name, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                remote_addr = data.get("remote_addr")
                ip_list.append(remote_addr)
                # print(remote_addr)
            except json.JSONDecodeError:
                print("Invalid JSON:", line)
    return ip_list


def compare_set_with_hll():
    ip_list = read_file("lms-stage-access.log")

    start = datetime.now()
    ip_set = set(ip_list)
    end = datetime.now()
    print("Set time consumption:", end - start)

    unique_from_set = len(ip_set)
    print(f"Unique from set - {unique_from_set}")

    start_one = datetime.now()
    for ip in ip_list:
        hll.update(ip.encode("utf-8"))

    start_two = datetime.now()
    unique_from_hll = hll.count()
    end = datetime.now()
    print("Hll time consumption with adding:", end - start_one)
    print("Hll time consumption only search:", end - start_two)

    print(f"Unique from hll - {unique_from_hll}")


compare_set_with_hll()
