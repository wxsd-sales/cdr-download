import time
from lib.cdr_collector import CDRCollector

if __name__ == "__main__":
    while True:
        data = CDRCollector()
        data.get_cdrs(write_csv=False, send_missed_sms=True)
        print("Waiting for 60 seconds.")
        time.sleep(60)
