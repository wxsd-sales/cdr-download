from lib.cdr_collector import CDRCollector

if __name__ == "__main__":
    data = CDRCollector()
    data.get_cdrs(write_csv=True, send_missed_sms=False)

