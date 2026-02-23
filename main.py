import matplotlib.pyplot as plt
import numpy as np

import fastf1


# helper function
def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)


def main():
    session = fastf1.get_session(2023, 'Silverstone', 'Q')
    session.load()

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    circuit_info = session.get_circuit_info()

    # Get an array of shape [n, 2] where n is the number of points and the second
    # axis is x and y.
    track = pos.loc[:, ('X', 'Y')].to_numpy()

    # Convert the rotation angle from degrees to radian.
    track_angle = circuit_info.rotation / 180 * np.pi

    # Rotate and plot the track map.
    rotated_track = rotate(track, angle=track_angle)
    plt.plot(rotated_track[:, 0], rotated_track[:, 1])

    offset_vector = [500, 0]
    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"

        offset_angle = corner["Angle"] / 180 * np.pi
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)

        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y

        text_x, text_y = rotate([text_x, text_y], angle=track_angle)

        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

        plt.scatter(text_x, text_y, color='grey', s=140)
        plt.plot([track_x, text_x], [track_y, text_y], color='grey')
        plt.text(text_x, text_y, txt, va='center_baseline', ha='center', size='small', color='white')
    
    plt.title(session.event['Location'])
    plt.xticks([])
    plt.yticks([])
    plt.axis('equal')
    plt.show()

if __name__ == '__main__':
    main()