import logging
from locust import HttpUser, task, between, events

logging.basicConfig(level=logging.INFO)

class ASGLoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def access_homepage(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 502:
                response.failure("502 Bad Gateway")
            elif response.status_code == 504:
                response.failure("504 Gateway Timeout")
            else:
                response.failure(f"Error: {response.status_code}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n" + "=" * 30)
    print("      PENGUJIAN SELESAI")
    print("=" * 30)

    if environment.stats.total.num_failures > 0:
        print(f"Total Kegagalan: {environment.stats.total.num_failures}")
    else:
        print("Status: Semua request berhasil.")

    print("=" * 30 + "\n")

    print("="*30 + "\n")
