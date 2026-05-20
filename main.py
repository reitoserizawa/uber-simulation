import random

# vars

ACTIVE_DRIVER_COUNT = 10

# time - counting 1 as 1 sec
TOTAL_DURATION = 3600
INTERVAL = 600
WINDOW_START_TIME = 0
WINDOW_END_TIME = 1800
# picking random time duration between 100 and 600 seconds for events
RANDOM_TIME_DURATION = (100, 600)

# driver actions
ACTIONS = ["ride", "offline"]


# classes

class Event:
    def __init__(self, id: int, type: str, time: float):
        self.id = id
        # "is_online" | "picked_up" | "dropped_off" | "is_offline"
        self.type = type
        self.time = time


class Driver:
    def __init__(self, id: int):
        self.id = id
        self.events: list[Event] = []

    def status_at(self, current_time: int) -> str:
        # get events up to current time and return status
        # assume is_online and dropped_off as idle
        status = "offline"
        for e in sorted(self.events, key=lambda e: e.time):
            if e.time > current_time:
                break
            if e.type == "is_online":
                status = "idle"
            elif e.type == "dropped_off":
                status = "idle"
            elif e.type == "picked_up":
                status = "driving"
            elif e.type == "is_offline":
                status = "offline"
        return status


# simulation

def simulate(active_driver_count: int):
    event_id = 0
    drivers = [Driver(id=i) for i in range(active_driver_count)]

    for driver in drivers:
        driver.events.append(Event(event_id, "is_online", 0))
        event_id += 1

        time = 0
        while time < TOTAL_DURATION:
            action = random.choice(ACTIONS)

            if action == "ride":
                pickup_time = time + random.uniform(*RANDOM_TIME_DURATION)
                dropoff_time = pickup_time + \
                    random.uniform(*RANDOM_TIME_DURATION)
                # if dropoff is after duration (time window), skip it
                if dropoff_time > TOTAL_DURATION:
                    break
                driver.events.append(
                    Event(event_id, "picked_up", pickup_time))
                event_id += 1
                driver.events.append(
                    Event(event_id, "dropped_off", dropoff_time))
                event_id += 1
                time = dropoff_time

            elif action == "offline":
                offline_time = time + random.uniform(*RANDOM_TIME_DURATION)
                online_time = offline_time + \
                    random.uniform(*RANDOM_TIME_DURATION)
                # only record offline event if within duration
                if offline_time < TOTAL_DURATION:
                    driver.events.append(
                        Event(event_id, "is_offline", offline_time))
                    event_id += 1
                # only record online event if within duration
                if online_time < TOTAL_DURATION:
                    driver.events.append(
                        Event(event_id, "is_online",  online_time))
                    event_id += 1
                time = online_time

    return drivers


# utilization

def utilization(drivers: list[Driver], start: int, end: int, interval: int):
    steps = int((end - start) / interval)
    print("------------------")
    for i in range(steps + 1):
        t = start + i * interval
        statuses = [driver.status_at(t) for driver in drivers]

        online = sum(s != "offline" for s in statuses)
        driving = sum(s == "driving" for s in statuses)
        idle = sum(s == "idle" for s in statuses)
        util = driving / online if online else 0

        print(f"Snapshot at time -> {t}s")
        print(f"Total online drivers: {online}")
        print(f"Driving: {driving}")
        print(f"Idle: {idle}")
        print(f"Utilization: {util:.1%}")
        print("------------------")

# tests


def test():
    # a driver who is never picked up should be idle
    driver = Driver(id=0)
    driver.events.append(Event(0, "is_online", 0))
    assert driver.status_at(500) == "idle"

    # a driver who is picked up should be driving
    driver = Driver(id=1)
    driver.events.append(Event(0, "is_online", 0))
    driver.events.append(Event(1, "picked_up", 100))
    assert driver.status_at(200) == "driving"

    # a driver who is dropped off should be idle again
    driver = Driver(id=2)
    driver.events.append(Event(0, "is_online", 0))
    driver.events.append(Event(1, "picked_up", 100))
    driver.events.append(Event(2, "dropped_off", 500))
    assert driver.status_at(600) == "idle"

    # a driver who went offline should be offline
    driver = Driver(id=3)
    driver.events.append(Event(0, "is_online", 0))
    driver.events.append(Event(1, "is_offline", 200))
    assert driver.status_at(300) == "offline"

    # querying before an event should not count that event
    driver = Driver(id=4)
    driver.events.append(Event(0, "is_online", 0))
    driver.events.append(Event(1, "picked_up", 500))
    assert driver.status_at(100) == "idle"

    print("All tests passed.")


if __name__ == "__main__":
    test()
    drivers = simulate(active_driver_count=ACTIVE_DRIVER_COUNT)
    # update window accordingly
    utilization(drivers, start=WINDOW_START_TIME,
                end=WINDOW_END_TIME, interval=INTERVAL)
