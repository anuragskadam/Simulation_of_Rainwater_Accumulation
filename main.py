import numpy as np

ELEVATION_MAP = None
GRADIENT = None
WATER_DIST = None
WATER = None

TIME = 0

INFILTRATION_RATE_C = 1
DECAY_C = 0.01
RAIN_INTANSITY = 0.01

# (startpoint, endpoint, water intake rate)
WATER_CHANNEL_INFO = [[77, 8, 6]]


def generator():
    global ELEVATION_MAP, GRADIENT, WATER_DIST, PROPERTIES, WATER

    a = 0.4
    ELEVATION_MAP = np.array(
        [[(1/a)*(a*x - ((a*x) ** 3)/6 + ((a*x) ** 5)/120) for x in range(100)] for _ in range(100)])
    GRADIENT = np.gradient(ELEVATION_MAP)
    WATER_DIST = np.zeros_like(ELEVATION_MAP)
    WATER = np.sum(WATER_DIST) - 0.001

generator()


def rain(intensity):
    global WATER_DIST, WATER
    WATER += intensity * ELEVATION_MAP.size


def step():
    global ELEVATION_MAP, GRADIENT, WATER_DIST, PROPERTIES, WATER, INFILTRATION_RATE_C, TIME

    # rain
    rain(RAIN_INTANSITY)

    # flow through pipes
    WATER -= WATER_CHANNEL_INFO[0][2]

    # absorbtion
    WATER -= INFILTRATION_RATE_C*ELEVATION_MAP.size
    INFILTRATION_RATE_C /= np.exp(DECAY_C)

    if WATER < 0:
        WATER = 0

    # time increment
    TIME += 1


def main():
    while (WATER <= 0):
        step()
    print("Rainwater Volume Capacity: ", TIME * 100, 'units')


main()
