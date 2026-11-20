import os, csv, time, pathlib
import datetime as dt
import zoneinfo
import requests

KST = zoneinfo.ZoneInfo("Asia/Seoul")
URL = "https://www.ksponco.or.kr/online/main/parkingorsApi.do"
PATH = pathlib.Path("data/parking_log.csv")


def fetch(retries=3):
    status = "unknown"
    for i in range(retries):
        try:
            r = requests.get(URL, params={"apiKey": os.environ["API_KEY"]}, timeout=15)
            r.raise_for_status()
            return int(r.json()[0]["parking_sum"]), "ok"
        except requests.HTTPError as e:
            status = f"http_{e.response.status_code}"
        except Exception as e:
            status = type(e).__name__
        time.sleep(5 * (i + 1))
    return "", status


value, status = fetch()
PATH.parent.mkdir(exist_ok=True)
is_new = not PATH.exists()
with PATH.open("a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if is_new:
        w.writerow(["collected_at_kst", "parking_sum", "status"])
    w.writerow([dt.datetime.now(KST).isoformat(timespec="seconds"), value, status])
print("done:", status)
