import matplotlib.pyplot
import numpy as np

import fastf1;


# helper function
def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(rot_mat, xy)


def main():
    session = fastf1.get_session(2023, 'Silverstone', 'Q')
    session.load()

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    circuit_info = session.get_circuit_info()

    # Get an array of shape [n, 2] where n is the number of points and the second
    # axis is x and y.
    print(pos)
    track = pos.loc[:, ('X', 'Y')].to_numpy()


if __name__ == '__main__':
    main()