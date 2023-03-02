import multiprocessing

from tracking_process import Track_Yellow

if __name__ == '__main__':
    track_process = multiprocessing.Process(target=Track_Yellow)
    track_process.start()


