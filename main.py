import matplotlib.pyplot as plt
import numpy as np

import fastf1


# helper function
def rotate(xy, *, angle) -> np.ndarray:
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

    # Convert the rotation angle of the circuit from degrees to radian.
    track_angle = circuit_info.rotation / 180 * np.pi

    # Rotate and plot the track map.
    rotated_track = rotate(track, angle=track_angle)
    plt.plot(rotated_track[:, 0], rotated_track[:, 1])

    # ----------- Plot the corner names ------------

    # 將文字放在賽道外側，距離賽道 500 單位
    offset_vector = [500, 0]    

    # Iterate over all corners
    for _, corner in circuit_info.corners.iterrows():
        # Create a string from corner number and Letter
        txt = f"{corner['Number']}{corner['Letter']}"

        # convert the corner angle from degrees to radians
        offset_angle = corner["Angle"] / 180 * np.pi

        # Rotate the offset vector so that it is aligned with the corner's angle
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)

        # Add the offset to the position of the corner
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y

        # Rotate the text position so that it is aligned with the corner's angle
        text_x, text_y = rotate([text_x, text_y], angle=track_angle)

        # Rotate the corner position so that it is aligned with the track's angle
        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

        plt.scatter(text_x, text_y, color='grey', s=140)                # Draw a circle next to the track.
        plt.plot([track_x, text_x], [track_y, text_y], color='grey')    # Draw a line from the track to this circle.
        
        # Print the corner number inside the circle.
        plt.text(text_x, text_y, txt, va='center_baseline', ha='center', size='small', color='white')
    
    # Add a title, remove tick labels to clean up the plot, set equal axis ratio, 
    # so that the track is not distorted and show the plot.
    plt.title(session.event['Location'])
    plt.xticks([])
    plt.yticks([])
    plt.axis('equal')
    plt.show()

if __name__ == '__main__':
    main()