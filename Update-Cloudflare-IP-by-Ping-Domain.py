import requests
from ping3 import ping
import time

# اطلاعات مورد نیاز برای اتصال به Cloudflare
CF_EMAIL = "your_email@example.com"
CF_API_KEY = "your_api_key"
CF_ZONE_ID = "your_zone_id"  # شناسه منطقه کلودفلر
CF_RECORD_ID = "your_record_id"  # شناسه رکورد DNS
DOMAIN_NAME = "example.com"  # نام دامنه‌ای که باید پینگ شود
IP_FILE = "ip.txt"  # نام فایل شامل آی‌پی‌ها

def read_ip_list(file_name):
    with open(file_name, "r") as file:
        ip_list = [line.strip() for line in file.readlines()]
    return ip_list

def ping_domain(domain):
    try:
        response_time = ping(domain, timeout=2)  # پینگ با تایم‌اوت ۲ ثانیه
        return response_time is not None
    except Exception as e:
        print(f"Ping error: {e}")
        return False

def update_dns_record(ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{CF_RECORD_ID}"
    headers = {
        "X-Auth-Email": CF_EMAIL,
        "X-Auth-Key": CF_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": DOMAIN_NAME,
        "content": ip,
        "ttl": 1,
        "proxied": False  # پروکسی غیرفعال
    }
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"DNS updated to {ip} with proxy disabled")
    else:
        print(f"Failed to update DNS: {response.json()}")

def main():
    while True:
        if not ping_domain(DOMAIN_NAME):
            print(f"{DOMAIN_NAME} is down. Trying to update DNS...")
            ip_list = read_ip_list(IP_FILE)  # خواندن آی‌پی‌ها از فایل
            for ip in ip_list:
                if ping(ip):
                    update_dns_record(ip)
                    break
        else:
            print(f"{DOMAIN_NAME} is reachable.")
        time.sleep(60)  # بررسی هر ۶۰ ثانیه یک‌بار

if __name__ == "__main__":
    main()
