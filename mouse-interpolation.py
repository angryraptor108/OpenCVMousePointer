import time
from pynput.mouse import Controller

def move_mouse(x: float, y: float):
    mouse_controller = Controller()
    mouse_controller.position = (x, y)

def cubic_interpolation(start_pos: float, end_post: float, t: float) -> float:
    distance: float = end_post - start_pos # distance remaining
    linear_t: float = t**3 # between 0 and 1
    position: float = start_pos + (distance * linear_t)

    return position

if __name__ == "__main__":
    start_x: float = 500
    end_x: float = 900
    start_y: float = 200
    end_y: float = 600

    duration: float = 2


    start_time: float = time.monotonic() # more reliable than time.time() as it is not affected by system clock changes

    while time.monotonic() - start_time < duration:
        # current time in loop
        elapsed_time: float = time.monotonic() - start_time

        # get time (progress) 0 to 1 (elapsed time / duration)
        progress: float = elapsed_time / duration

        # current position of the object
        current_position_x: float = cubic_interpolation(start_x, end_x, progress)
        current_position_y: float = cubic_interpolation(start_y, end_y, progress)


        # move the mouse
        move_mouse(current_position_x, current_position_y)
    
    move_mouse(end_x, end_y)