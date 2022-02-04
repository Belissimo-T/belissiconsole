import time

import belissiconsole as bc


def main():
    # a = bc.rainbow("🌈 THIS SHOULD BE A RAINBOW 🌈")
    # time.sleep(5)
    # a.stop()

    bc.rainbow_print("WOW SO PRETTY1")
    bc.rainbow_print("WOW SO PRETTY2")
    bc.rainbow_print("WOW SO PRETTY3")
    bc.rainbow_print("WOW SO PRETTY4")

    a = bc.rainbow("🌈 THIS SHOULD BE A RAINBOW 🌈")
    time.sleep(5)
    a.stop()


if __name__ == "__main__":
    main()
