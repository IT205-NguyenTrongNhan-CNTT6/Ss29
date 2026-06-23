from abc import ABC, abstractmethod
import logging

# ================== LOGGING ==================
logging.basicConfig(
    filename="iot_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================== BASE DEVICE ==================
class BaseDevice(ABC):
    factory_name = "Rikkei Smart Factory"
    base_maintenance_cost = 1_000_000

    def __init__(self, device_code, name):
        self.device_code = device_code
        self.name = self._format_name(name)
        self.__operating_hours = 0

    # -------- property encapsulation --------
    @property
    def operating_hours(self):
        return self.__operating_hours

    def _add_hours(self, hours):
        self.__operating_hours += hours

    # -------- name normalize --------
    def _format_name(self, name):
        return " ".join(name.strip().upper().split())

    # -------- static method --------
    @staticmethod
    def validate_device_code(code):
        return isinstance(code, str) and len(code) == 10 and code[0].isalpha()

    # -------- class method --------
    @classmethod
    def update_maintenance_cost(cls, new_cost):
        cls.base_maintenance_cost = new_cost

    # -------- operator overloading --------
    def __add__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError("ERR-IOT-04")
        return self.operating_hours + other.operating_hours

    def __lt__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError("ERR-IOT-04")
        return self.operating_hours < other.operating_hours

    # -------- abstract --------
    @abstractmethod
    def track_performance(self):
        pass

    @abstractmethod
    def run_diagnostic(self):
        pass


# ================== PRODUCTION ROBOT ==================
class ProductionRobot(BaseDevice):
    def __init__(self, device_code, name):
        super().__init__(device_code, name)
        self.completed_products = 0

    def track_performance(self, hours, products):
        self._add_hours(hours)
        self.completed_products += products

        oee = (self.completed_products / (self.operating_hours * 100)) * 100
        print(f"Chỉ số hiệu suất thiết bị tổng thể (OEE): {round(oee,2)}%")

    def run_diagnostic(self):
        if self.completed_products > 10000:
            print("[Cảnh báo]: Cần bảo trì robot!")
        else:
            print("Robot hoạt động ổn định")


# ================== THERMAL SENSOR ==================
class ThermalSensor(BaseDevice):
    def __init__(self, device_code, name):
        super().__init__(device_code, name)
        self.current_temperature = 0
        self.safety_threshold = 80

    def track_performance(self, hours, temp):
        self._add_hours(hours)
        self.current_temperature = temp
        print(f"Biên độ nhiệt: {self.current_temperature}°C")

    def run_diagnostic(self):
        if self.current_temperature > self.safety_threshold:
            print(f"Nguy hiểm: Vượt ngưỡng nhiệt! ({self.current_temperature}/{self.safety_threshold})")
            print(f"Chi phí bảo trì: {self.base_maintenance_cost}")
        else:
            print("Nhiệt độ an toàn")


# ================== HYBRID DEVICE (MRO) ==================
class HybridSmartActuator(ProductionRobot, ThermalSensor):
    def __init__(self, device_code, name):
        ProductionRobot.__init__(self, device_code, name)
        ThermalSensor.__init__(self, device_code, name)


# ================== DUCk TYPING GATEWAYS ==================
class MQTTEngineGateway:
    def process_stream(self, device):
        print("[Hệ thống MQTT Engine]: Kết nối Cloud IoT...")
        print(f"Xuất dữ liệu thiết bị {device.device_code} thành công")


class ERPReportGateway:
    def process_stream(self, device):
        print("[ERP System]: Đồng bộ dữ liệu vào ERP...")
        print(f"Thiết bị {device.device_code} đã được ghi nhận")


def export_telemetry_data(gateway, device):
    if not hasattr(gateway, "process_stream"):
        print("[Lỗi] (ERR-IOT-05): Cổng không tương thích")
        return
    gateway.process_stream(device)


# ================== VALIDATION ==================
def input_int(prompt):
    while True:
        try:
            value = input(prompt)
            if value.strip() == "":
                raise ValueError
            value = int(value)
            if value <= 0:
                raise ValueError
            return value
        except:
            print("[Lỗi] (ERR-IOT-03): Giá trị phải là số > 0")


# ================== SYSTEM ==================
devices = []
current_device = None


def create_device():
    global current_device

    print("--- ĐĂNG KÝ THIẾT BỊ ---")
    print("1. Robot")
    print("2. Sensor")
    print("3. Hybrid")

    choice = input("Chọn: ")

    code = input("Nhập mã thiết bị: ")
    if not BaseDevice.validate_device_code(code):
        print("[Lỗi] (ERR-IOT-01): Mã thiết bị không hợp lệ")
        return

    name = input("Nhập tên: ")

    if choice == "1":
        current_device = ProductionRobot(code, name)
    elif choice == "2":
        current_device = ThermalSensor(code, name)
    elif choice == "3":
        current_device = HybridSmartActuator(code, name)
    else:
        print("[Lỗi] (ERR-IOT-06): Lựa chọn không hợp lệ")
        return

    devices.append(current_device)
    print("[Thành công] Đăng ký thiết bị!")


def view_device():
    global current_device
    if not current_device:
        print("[Lỗi] (ERR-IOT-02)")
        return

    print("--- THÔNG TIN ---")
    print("Nhà máy:", current_device.factory_name)
    print("Tên:", current_device.name)
    print("Giờ chạy:", current_device.operating_hours)
    print("MRO:", type(current_device).__mro__)


def update_device():
    global current_device
    if not current_device:
        print("[Lỗi] (ERR-IOT-02)")
        return

    hours = input_int("Nhập giờ chạy: ")

    if isinstance(current_device, ProductionRobot):
        products = input_int("Sản phẩm: ")
        current_device.track_performance(hours, products)
    elif isinstance(current_device, ThermalSensor):
        temp = input_int("Nhiệt độ: ")
        current_device.track_performance(hours, temp)


def diagnostic():
    global current_device
    if not current_device:
        print("[Lỗi] (ERR-IOT-02)")
        return
    current_device.run_diagnostic()


def compare_devices():
    if len(devices) < 2:
        print("Cần ít nhất 2 thiết bị")
        return

    a = devices[0]
    b = devices[1]

    print("A < B:", a < b)
    print("Tổng giờ:", a + b)


def export_data():
    if not current_device:
        print("[Lỗi] (ERR-IOT-02)")
        return

    print("1. MQTT")
    print("2. ERP")
    choice = input("Chọn: ")

    if choice == "1":
        export_telemetry_data(MQTTEngineGateway(), current_device)
    elif choice == "2":
        export_telemetry_data(ERPReportGateway(), current_device)


# ================== MENU ==================
def menu():
    while True:
        print("\n===== SMART FACTORY =====")
        print("1. Tạo thiết bị")
        print("2. Xem thiết bị")
        print("3. Cập nhật vận hành")
        print("4. Chẩn đoán")
        print("5. So sánh")
        print("6. Export")
        print("7. Thoát")

        c = input("Chọn: ")

        if c == "1":
            create_device()
        elif c == "2":
            view_device()
        elif c == "3":
            update_device()
        elif c == "4":
            diagnostic()
        elif c == "5":
            compare_devices()
        elif c == "6":
            export_data()
        elif c == "7":
            print("Thoát hệ thống")
            break
        else:
            print("[Lỗi] (ERR-IOT-06)")


# ================== RUN ==================
if __name__ == "__main__":
    menu()