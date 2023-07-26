import cv2
import numpy as np
import pandas as pd

FRAMES = 26


def get_binary_array(np_frames):
    """
    Copied from Bard
    Returns a binary array with shape (26, 32, 32) from a numpy array with shape (26, 32, 32, 3).
    If last dimension numbers are all zeroes then we should get zero, if they are not all zeroes, then we get one.

    Args:
      np_frames: NumPy array with shape (26, 32, 32, 3).

    Returns:
      NumPy array with shape (26, 32, 32) containing ones and zeros.
    """

    binary_array = np.zeros_like(np_frames[:, :, :, 0])
    for i in range(len(np_frames)):
        for j in range(len(np_frames[0])):
            for k in range(len(np_frames[0][0])):
                if np.all(np_frames[i][j][k] == 0):
                    binary_array[i][j][k] = 0
                else:
                    binary_array[i][j][k] = 1

    return binary_array

def generate_pickle(filepath):
    video = cv2.VideoCapture('assets/sample1.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    print('fps:', fps)

    frames = []
    offset = 26

    for frame_id in range(offset, 1000, 12)[:FRAMES]:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        cropped_frame = frame[:, 60:420]
        resized = cv2.resize(cropped_frame, (32, 32))

        u_green = np.array([4, 190, 4])
        l_green = np.array([0, 170, 0])
        mask = cv2.inRange(resized, l_green, u_green)
        and_frame = cv2.bitwise_and(resized, resized, mask=mask)
        subtracted = resized - and_frame

        # cv2.imshow('frame', subtracted)
        # cv2.waitKey(0)

        frames.append(subtracted)

        print('frame.shape:', frame.shape)
        print('cropped_frame.shape:', cropped_frame.shape)
        print('mask.shape:', mask.shape)
        print('resized.shape:', resized.shape)
        print('and_frame.shape:', and_frame.shape)
        print('subtracted.shape:', subtracted.shape)
        print('---------------')

    np_frames = np.asarray(frames)
    print('np_frames.shape:', np_frames.shape)
    # print(np_frames[:, :, 1])
    result = get_binary_array(np_frames)
    print('result.shape:', result.shape)
    print('result:', result)
    result.tofile('assets/sample1.pickle')


if __name__ == '__main__':
    generate_pickle('video/sample1.mp4')
