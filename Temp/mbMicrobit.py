import microbit
import array

sourceimageintarray = [9, 0, 9, 9, 9, 0, 0, 9, 9]
sourceimagechararray = array.array('b', sourceimageintarray)
sourceimage = microbit.Image(3, 3, sourceimagechararray)

img1 = microbit.Image("99999:00000:99009:90009:00900")

str(img1)
