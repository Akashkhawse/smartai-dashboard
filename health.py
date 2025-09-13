import psutil
import platform
import datetime

def health_check():
    return {
        "time": str(datetime.datetime.now()),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "os": platform.platform()
    }

if __name__ == "__main__":
    status = health_check()
    print("System Health Report:")
    for key, value in status.items():
        print(f"{key}: {value}")
