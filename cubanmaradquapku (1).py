import sys
import time
import multiprocessing
import threading
import os
import signal
def start_ctrl_o_watcher(stop_event):
    if os.name == "nt":
        import msvcrt
        def watcher():
            print("Press Ctrl+O to stop.")
            while not stop_event.is_set():
                if msvcrt.kbhit():
                    ch = msvcrt.getch()
                    # Ctrl+O is 0x0f
                    if ch == b'\x0f':
                        print("\nCtrl+O detected — stopping...")
                        stop_event.set()
                        return
                time.sleep(0.05)
    else:
        import tty, termios
        def watcher():
            print("Press Ctrl+O to stop.")
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while not stop_event.is_set():
                    ch = sys.stdin.read(1)
                    if not ch:
                        continue
                    if ch == '\x0f':  # Ctrl+O
                        print("\nCtrl+O detected — stopping...")
                        stop_event.set()
                        return
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

    t = threading.Thread(target=watcher, daemon=True)
    t.start()
    return t

def cpu_worker(stop_event):
    x = 0
    while not stop_event.is_set():
        # some trivial work to keep CPU busy
        x ^= 0xFFFFFFFF
    # exit when stop_event set

def run_cpu_ramp(stop_event,
                 interval_sec=2.0,
                 initial_workers=1,

    if max_workers is None:
        max_workers = multiprocessing.cpu_count() * 4  # default cap

    created = []
    current = initial_workers

    print(f"Starting CPU ramp: initial={initial_workers}, interval={interval_sec}s, max={max_workers}")
    try:
        # start initial workers
        for _ in range(current):
            p = multiprocessing.Process(target=cpu_worker, args=(stop_event,))
            p.start()
            created.append(p)

        while not stop_event.is_set():
            time.sleep(interval_sec)
            if stop_event.is_set():
                break
            next_count = min(max_workers, current * 2)
            if next_count <= current:
                break
            add = next_count - current
            print(f"Scaling workers: {current} -> {next_count} (+{add})")
            for _ in range(add):
                p = multiprocessing.Process(target=cpu_worker, args=(stop_event,))
                p.start()
                created.append(p)
            current = next_count

    finally:
        print("Stopping CPU workers...")
        for p in created:
            if p.is_alive():
                p.terminate()
        for p in created:
            p.join(timeout=1.0)
        print("All CPU workers stopped.")


def run_cpu_fixed(stop_event, workers=None):
    if workers is None:
        workers = multiprocessing.cpu_count()
    created = []
    print(f"Starting fixed CPU load with {workers} workers.")
    try:
        for _ in range(workers):
            p = multiprocessing.Process(target=cpu_worker, args=(stop_event,))
            p.start()
            created.append(p)
        while not stop_event.is_set():
            time.sleep(0.5)
    finally:
        print("Stopping CPU workers...")
        for p in created:
            if p.is_alive():
                p.terminate()
        for p in created:
            p.join(timeout=1.0)
        print("All CPU workers stopped.")


def main():
    print("Experimental Hacking Tool")
    print("1) Scan Area for PCs to Access")
    print("2) Check PC For Free Spots")
    choice = input("Choose mode (1/2): ").strip()

    stop_event = multiprocessing.Event()
    start_ctrl_o_watcher(stop_event)

    if choice == "1":
        try:
            print("Starting.")
            wait(0.1)
            print("Starting..")
            wait(0.1)
            print("Starting...")
            wait(0.1)
            print("Starting..")
            wait(0.1)
            print("Starting.")
            wait(0.1)
            interval, initial, maxw = 2.0, 1, None
        run_cpu_ramp(stop_event, interval_sec=interval, initial_workers=initial, max_workers=maxw)
     
         if choice == "2":
        try:
            print("Starting.")
            wait(0.1)
            print("Starting..")
            wait(0.1)
            print("Starting...")
            wait(0.1)
            print("Starting..")
            wait(0.1)
            print("Starting.")
            wait(0.1)
            interval, initial, maxw = 2.0, 1, None
        run_cpu_ramp(stop_event, interval_sec=interval, initial_workers=initial, max_workers=maxw)

if __name__ == "__main__":
    try:
        main()
