#!/usr/bin/env python3

import logging
import threading

from controller.controller import Controller

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    c = Controller()
    c.init_args()

    # Create runner thread
    runner_thread = threading.Thread(target=c.start_runner)
    runner_thread.start()

    # Start ui
    c.start_ui()

    runner_thread.join()
