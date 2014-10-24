#------------------------------------------------------------------------------ 
# Method 2 from http://lodev.org/cgtutor/randomnoise.html
def value_noise(width, height, frequency=0.4, octaves=10.0):
    """
    Generate dat value noise, boi

    frequency - A smaller number generates a more "zoomed-in" terrain with fewer details
    octaves - Smaller number generates more lakes, 0.4 and 10 gives a good result if 320*240 in 2 seconds
    """
    def smooth_noise(x, y):
        """Returns the average value of the 4 neighbors of (x, y) from the
           noise array."""

        fractX = x - int(x)
        fractY = y - int(y)

        x1 = (int(x) + width) % width
        y1 = (int(y) + height) % height

        x2 = (x1 + width - 1) % width
        y2 = (y1 + height - 1) % height

        #Bilinear interpolation http://en.wikipedia.org/wiki/Bilinear_interpolation
        value = 0.0
        value += fractX       * fractY       * noise[y1][x1]
        value += fractX       * (1 - fractY) * noise[y2][x1]
        value += (1 - fractX) * fractY       * noise[y1][x2]
        value += (1 - fractX) * (1 - fractY) * noise[y2][x2]

        return value


    def turbulence(x, y, size):
        """
        This function controls how far we zoom in/out of the noise array.
        The further zoomed in gives less detail and is more blurry.
        """

        value = 0.0
        initial_size = size

        while size >= 1:
            value += smooth_noise(x / size, y / size) * size
            size /= 2.0 #The zooming factor started at 16 here, and is divided through two each time. Keep doing this until the zooming factor is 1.

        return 128.0 * value / initial_size #The return value is normalized so that it'll be a number between 0 and 255

    frequency = 0.4
    octaves = 10.0

    #Generate a list with random noise between 0 and 1
    noise = []
    for y in range(0, height):
        noise_row = []
        for x in range(0, width):
            noise_row.append(random.randint(0, 1000)/1000.0)
        noise.append(noise_row)


    result = []
    for y in range(0, height):
        row = []
        for x in range(0, width):
            noise_smooth_turbulent = int(turbulence(x*frequency,y*frequency,octaves))
            row.append(noise_smooth_turbulent)
        result.append(row)

    #Standardize the coordinates [x,y,z]
    xy_and_height = []
    for y, row in enumerate(result):
        for x, c in enumerate(row):
            xy_and_height.append((x,y,c))

    return xy_and_height
