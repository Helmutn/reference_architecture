import time


class DeviceService:

    def power_on(self, ip):

        print(f"POWER ON {ip}")

        time.sleep(1)

        return True

    def power_off(self, ip):

        print(f"POWER OFF {ip}")

        time.sleep(1)

        return True