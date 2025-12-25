import socket

def check_local_ports():
    # لیست پورت‌هایی که معمولاً فیلترشکن‌ها استفاده می‌کنند
    ports_to_check = [1080, 4000, 10808, 2080, 8080, 7890]
    found_any = False
    
    print("🔍 در حال جستجوی تونل‌های فعال روی سیستم شما...")
    print("-" * 40)
    
    for port in ports_to_check:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1) # زمان انتظار کوتاه
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                print(f"✅ پورت فعال پیدا شد: {port}")
                found_any = True
            else:
                print(f"❌ پورت {port} بسته است.")
                
    print("-" * 40)
    if not found_any:
        print("😞 متأسفانه هیچ پورت فعالی پیدا نشد.")
        print("این یعنی وارپ یا v2ray شما عملاً هیچ راه خروجی باز نکرده‌اند.")
    else:
        print("💡 عددی که جلوی 'پورت فعال' نوشته شده را در کد ربات وارد کنید.")

if __name__ == "__main__":
    check_local_ports()