from prometheus_client import start_http_server, Counter, Gauge
from datetime import datetime, timedelta
import random
import time

# -------------------------------
# إعداد المتغيرات الثابتة
MAX_SPOTS = 50
CAR_COLORS = ['red', 'blue', 'black', 'white', 'green']
CAR_TYPES = ['sedan', 'suv', 'truck', 'van']
PARKING_SPOTS = [f"spot_{i+1}" for i in range(MAX_SPOTS)]
car_data = {}

# -------------------------------
# إنشاء الميتريكس
total_cars = Counter(
    'garage_total_cars_entered',
    'Total number of cars entered the garage with detailed labels',
    ['color', 'type', 'spot']
)

current_cars = Gauge(
    'garage_current_cars',
    'Current number of cars in the garage with detailed labels',
    ['color', 'type', 'spot']
)

available_spots = Gauge('garage_available_spots', 'Number of available parking spots')

# -------------------------------
def add_car():
    if len(car_data) >= MAX_SPOTS:
        return  # لا توجد أماكن فارغة

    car_id = f"car_{random.randint(1000, 9999)}"
    car_color = random.choice(CAR_COLORS)
    car_type = random.choice(CAR_TYPES)
    available_spots_list = list(set(PARKING_SPOTS) - set(car_data.keys()))
    car_spot = random.choice(available_spots_list)

    # تسجيل السيارة
    car_data[car_spot] = {
        "id": car_id,
        "color": car_color,
        "type": car_type,
        "entry_time": datetime.now()
    }

    # تحديث الميتريكس
    total_cars.labels(color=car_color, type=car_type, spot=car_spot).inc()
    current_cars.labels(color=car_color, type=car_type, spot=car_spot).set(1)
    available_spots.set(MAX_SPOTS - len(car_data))

def remove_old_cars():
    now = datetime.now()
    to_remove = []
    for spot, data in car_data.items():
        if now - data['entry_time'] > timedelta(minutes=3):  # أو 30 يوم لمحاكاة واقعية
            to_remove.append(spot)

    for spot in to_remove:
        color = car_data[spot]['color']
        car_type = car_data[spot]['type']
        
        # تحديث الميتريكس
        current_cars.labels(color=color, type=car_type, spot=spot).set(0)
        del car_data[spot]
        available_spots.set(MAX_SPOTS - len(car_data))

# -------------------------------
if __name__ == '__main__':
    start_http_server(8000)
    print("Garage metrics exporter running at http://localhost:8000")

    while True:
        if random.random() < 0.7:  # 70% احتمال دخول سيارة جديدة
            add_car()
        remove_old_cars()
        time.sleep(5)  # انتظار 5 ثواني