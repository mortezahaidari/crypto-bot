# src/monitoring/health_check.py
import psutil
from src.monitoring.logger import logger

class SystemMonitor:
    def __init__(self, thresholds: dict):
        self.thresholds = thresholds  # e.g., {"cpu": 80, "memory": 90}

    def check_cpu_usage(self) -> bool:
        usage = psutil.cpu_percent()
        if usage > self.thresholds["cpu"]:
            logger.warning(f"High CPU usage: {usage}%")
            return False
        return True

    def check_memory_usage(self) -> bool:
        usage = psutil.virtual_memory().percent
        if usage > self.thresholds["memory"]:
            logger.warning(f"High memory usage: {usage}%")
            return False
        return True