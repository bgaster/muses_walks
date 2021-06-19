
# Author: Benedict R. Gaster


# GPS and OLED imports

import board
import busio
import time
import adafruit_gps
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import serial

# TODO: At the moment the mapping between Geo fence regions and the story is simply
#       handled by searching the story each time a region is entered. This is slow
#       and could be a real issue if we want low-latency real time performance. This can
#       be easily solved by simply generating indexes into the story from the geo fences
#       on loading the story, but only worth doing if it becomes an issue.
#
#       Additionally, regions are represented as strings at the moment and so testing equality
#       is also expensive, we could map to ints, and so on to speed things up, if necessary.

from story import Story
from fence import GeoFences

def main():
     # Setup story
    story = Story("/home/pi/muses_walks/ex1/story.twison")
    # gfs = GeoFences("/home/pi/muses_walks/ex1/muses.geoJSON")
    gfs = GeoFences("/home/pi/muses_walks/ex1/campus_walk.geoJSON")
    
    # Setup GPS and OLED
    uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)

    # Create a GPS module instance.
    gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the SSD1306 OLED class.
    disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

   

    # Clear display.
    disp.fill(0)
    disp.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    height = 12
    font = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Semibold.ttf', height)

    y = 0

    # Main loop runs forever printing the location, etc. every second.
    last_print = time.monotonic()
    last_state = "none"
    while True:
        #
        # Make sure to call gps.update() every loop iteration and at least twice
        # as fast as data comes from the GPS unit (usually every second).
        # This returns a bool that's true if it parsed new data (you can ignore it
        # though if you don't care and instead look at the has_fix property).

        gps.update()

        sentence = gps.readline()
        # print(str(sentence, "ascii").strip())

        # Every second we check to see if region(s) have changed.
        current = time.monotonic()

        if current - last_print >= 1.0:
            draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
            last_print = current

            draw.text((x, top+y*height), "Muses talk", font=font, fill=255)
            if not gps.has_fix:

                # Try again if we don't have a fix yet.
                draw.text((x, top+(y+1)*height), "waiting", font=font, fill=255)
            else:
                lat = gps.latitude
                lon = gps.longitude
                # check to see if we have moved in or out of region(s)
                move = gfs.move((gps.latitude, gps.longitude))

                left = move[0]
                entered = move[1]
                remained = move[2]

                # print("Long: {0:.6f} degrees".format(gps.longitude))
                # print("Lat: {0:.6f} degrees".format(gps.latitude))
                # print(move)

                if len(entered) > 0:
                    # print("entered")
                    for r in entered:
                        draw.text((x, top+(y+1)*height), "Entered: " + r, font=font, fill=255)
                elif len(left) > 0:
                    for r in left:
                        draw.text((x, top+(y+1)*height), "Left: " + r, font=font, fill=255)
                        last_state = r
                elif len(remained):
                    # print("remained")
                    for r in remained:
                        draw.text((x, top+(y+1)*height), "Still: " + r, font=font, fill=255)
                else:
                    draw.text((x, top+(y+1)*height), "Out " + last_state, font=font, fill=255)


        disp.image(image)
        disp.show()
    # move = gfs.move((-2.5334985098113356, 51.4722326416855))

    # # process entered regions
    # entered = move[1]
    # for r in entered:
    #     p = story.find_passage(r)
    #     if p != None:
    #         print(p.split("[[")[0])


if __name__ == "__main__":
    main()


# print(gfs.move((-2.5334985098113356, 51.4722326416855)))
# print(gfs.move((-2.5304521008325733, 51.47166980571885)))
# print(gfs.move((-2.5304521008325733, 51.47166980571885)))


# geo = load_JSON("./ex1/muses.geoJSON")
# print(geo["features"][0])
# print(story.passages[0])

# story.get_region(geo["features"][0]["properties"]["name"])

# loc_one = (-2.5304521008325733, 51.47166980571885)

# loc_two = (-2.5334985098113356, 51.4722326416855)

# print(distance.distance(loc_one, loc_two).km * 1000.0)
