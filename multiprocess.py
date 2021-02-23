import multiprocessing
import time


def sleep_for_a_bit(sec):
    print(f"Sleeping...{sec} seconds(sec)")
    time.sleep(sec)
    print("Done Sleeping")


p1 = multiprocessing.Process(target=sleep_for_a_bit, args=[1])
p2 = multiprocessing.Process(target=sleep_for_a_bit, args=[1])

if __name__ == '__main__':
    p1.start()
    p2.start()
    p1.join()
    p2.join()


finish = time.perf_counter()
print("Finish : " + str(finish))
