import time

import belissiconsole as bc


def main():
    # a = bc.rainbow("🌈 THIS SHOULD BE A RAINBOW 🌈")
    # time.sleep(5)
    # a.stop()

    a = bc.rainbow("🌈 THIS SHOULD BE A RAINBOW 🌈\n"
                   "🌈 WITH MULTIPLE LINES 🌈")
    time.sleep(5)
    a.stop()


if __name__ == "__main__":
    main()
