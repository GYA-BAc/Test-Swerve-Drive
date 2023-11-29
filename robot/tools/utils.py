import math


#NOTE: leave these as individual functions, as putting them in a class just makes them harder to access



def limit(number: float, limits: list = (-1, 1)) -> float:
    """Return a number between both limits"""
    return min(max(number, limits[0]), limits[1])



""" angle system
         0 (360)
            ^ y-axis
            |
            |
270 <–––––––+––––––––> 90
            |        x-axis
            |
            v
           180
"""
def vector_to_degrees(vector: list[float, float]) -> float:
    """
    Convert a Xbox controller's joystick output to degrees;\n
    0 degrees is North, and degrees increase clockwise
    """
    # since 0 degrees is north, pass in x first, 
    return math.degrees(math.atan2(vector[0], vector[1]))


def add_vectors(vec1: list[float, float], vec2: list[float, float]) -> list[float, float]:
    return [vec1[0]+vec2[0], vec1[1]+vec2[1]]


def get_vector_length(vector: list[float, float]) -> float:
    return math.sqrt(vector[0]**2 + vector[1]**2)
