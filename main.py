import time

import belissiconsole as bc


def main():
    # a = bc.rainbow("🌈 THIS SHOULD BE A RAINBOW 🌈")
    # time.sleep(5)
    # a.stop()

    bc.rainbow_print("WOW SO PRETTY ✨")
    bc.rainbow_print("WOW SO PRETTY 🚀")
    bc.rainbow_print("WOW SO PRETTY 🌈")
    bc.rainbow_print("WOW SO PRETTY 🌟")

    a = bc.rainbow("🌈 THIS SHOULD BE A RAINBOW 🌈")
    time.sleep(3)
    a.stop()

    a = bc.rainbow("🌈 This tests 🌈\n🌈 multiple lines 🌈")
    time.sleep(3)
    a.stop()

    a = bc.rainbow("\n".join("a lot of lines, this might lag" for _ in range(20)))
    time.sleep(5)
    a.stop()

    a = bc.rainbow("this should flash very fast", speed=10)
    time.sleep(5)
    a.stop()


if __name__ == "__main__":
    main()
