import multiprocessing

Rtemp = multiprocessing.Value('d', 0.0)
frame = multiprocessing.Value('i', 0)
Ftemp = multiprocessing.Value('d', 0.0)
initComplete = multiprocessing.Value('b', False)
servoX = multiprocessing.Value('d', 0)
servoY = multiprocessing.Value('d', 0)
isHydrated = multiprocessing.Value('b', False)