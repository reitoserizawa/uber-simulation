# Uber Driver Utilization Simulation

Simulates Uber driver activity over a time window and computes utilization.

## How it works

Each driver generates random events (`picked_up`, `dropped_off`, `is_offline`, `is_online`) over a set duration. Utilization is calculated by replaying those events at fixed intervals across the window.

```
utilization = drivers driving / drivers online
```

## Run

```bash
python main.py
# or
python3 main.py
```

## Config

Edit the vars at the top of `main.py`:

```python
ACTIVE_DRIVER_COUNT  = 10
TOTAL_DURATION       = 3600  # total simulation duration in seconds
WINDOW_START_TIME    = 0     # start of utilization window
WINDOW_END_TIME      = 1800  # end of utilization window
INTERVAL             = 600   # snapshot every N seconds
```
