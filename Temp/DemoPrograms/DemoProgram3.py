import microbit

while True:
    if microbit.accelerometer.get_x() == '2':
        microbit.display.show(microbit.Image.HAPPY)
    elif microbit.accelerometer.get_y() == '1':
        microbit.display.show((microbit.Image.SAD))
    elif microbit.accelerometer.get_z() == '3':
        microbit.display.show(microbit.Image.ANGRY)
    else:
        microbit.display.clear()