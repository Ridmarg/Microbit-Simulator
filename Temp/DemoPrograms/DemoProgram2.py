import microbit

while True:
    gesture = microbit.accelerometer.current_gesture()
    if gesture != None:
        microbit.display.scroll(gesture, delay=200)
    microbit.sleep(1000)