import microbit
import array

DemoImage1 = microbit.Image("09990:90009:09090:90009:09990")
DemoImage2List = [0, 1, 2, 3, 4, 5, 6, 7]
DemoImage2Array = array.array('b', DemoImage2List)
DemoImage2 = microbit.Image(4, 2, DemoImage2Array)
DemoImage3 = microbit.Image(5, 5)
DemoImage3.set_pixel(2, 2, 9)
DemoImage3 = DemoImage3.invert()

while True:
    if microbit.button_a.is_pressed() and microbit.button_b.is_pressed():
        microbit.display.show(DemoImage3)
    elif microbit.button_a.is_pressed():
        microbit.display.show(DemoImage1)
    elif microbit.button_b.is_pressed():
        microbit.display.show(DemoImage2)
    else:
        microbit.display.clear()