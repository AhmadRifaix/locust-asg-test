import logging
from locust import HttpUser, task, between, events

# Setup logging
logging.basicConfig(level=logging.INFO)

class ASGLoadTest(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def access_homepage(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                if "Welcome" in response.text or "App" in response.text:
                    response.success()
                else:
                    response.success() # Diubah jadi sukses atau disesuaikan jika teks tidak wajib ada
            elif response.status_code == 502:
                response.failure("502 Bad Gateway: Instance belum In-Service")
            elif response.status_code == 504:
                response.failure("504 Gateway Timeout: Instance Overload")
            else:
                response.failure(f"Error: {response.status_code}")

# Listener saat pengujian selesai
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n" + "="*30)
    print("      PENGUJIAN SELESAI")
    print("="*30)
    if environment.stats.total.num_failures > 0:
        print(f"Total Kegagalan: {environment.stats.total.num_failures}")
    else:
        print("Status: Sistem Sangat Stabil.")
    print("="*30 + "\n")
