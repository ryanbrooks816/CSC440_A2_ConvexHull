import time
from random import randint
from typing import List
from typing import Set

import matplotlib.pyplot as plt

from convex_hull import Point
from convex_hull import base_case_hull
from convex_hull import compute_hull
import numpy as np


def generate_points(
        num_points: int,
        min_x: int = 0,
        max_x: int = 1_000,
        min_y: int = 0,
        max_y: int = 1_000,
) -> List[Point]:
    """ Creates a list of random and unique points for benchmarking the convex_hull algorithm.

    :param num_points: number of unique points to generate.
    :param min_x: minimum x-coordinate for points
    :param max_x: maximum x-coordinate for points
    :param min_y: minimum y-coordinate for points
    :param max_y: maximum y-coordinate for points
    """
    points: Set[Point] = set()
    while len(points) < num_points:
        points.add((randint(min_x, max_x), randint(min_y, max_y)))
    return list(points)


def run_benchmarks():
    sizes: List[int] = [0, 10, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 300_000, 600_000, 1_000_000]
    dnc_hull_times: List[float] = list()
    naive_hull_times: List[float] = list()
    num_runs = 3

    for n in sizes:
        print(f'n: {n}')
        dnc_times = []
        naive_times = []

        for _ in range(num_runs):
            points = generate_points(n)
            # start_time = time.time()
            # compute_hull(points)
            # time_taken = time.time() - start_time  # time taken (in seconds) for divide-and-conquer
            # dnc_times.append(time_taken)

            start_time = time.time()
            base_case_hull(points)
            time_taken = time.time() - start_time  # time taken (in seconds) for naive
            naive_times.append(time_taken)

            print(f'time: {time_taken}')

        # avg_dnc_time = sum(dnc_times) / num_runs
        avg_naive_time = sum(naive_times) / num_runs

        # print(f'avg_dnc_time_taken: {avg_dnc_time}')
        # dnc_hull_times.append(avg_dnc_time)

        print(f'avg_naive_time_taken: {avg_naive_time}')
        naive_hull_times.append(avg_naive_time)
    
    n = np.array(sizes)
    t = np.array(naive_hull_times)
    return n, t

    # plt.scatter(sizes, dnc_hull_times, c='blue')
    # plt.plot(sizes, dnc_hull_times, c='blue', label='Divide-and-Conquer')
    # plt.scatter(sizes, naive_hull_times, c='red')
    # plt.plot(sizes, naive_hull_times, c='red', label='Naive')
    # plt.legend()
    # plt.xlabel('Number of Points')
    # plt.ylabel('Time (s)')
    # plt.title('Convex Hull Benchmark')
    # plt.savefig('benchmark_plot.png')


if __name__ == '__main__':
    run_benchmarks()
