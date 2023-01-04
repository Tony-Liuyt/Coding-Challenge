from random import random
from math import pi


class Disk:
    class Small: pass
    class Large: pass
    def __init__(self, position: complex, size: Small | Large) -> None:
        self.size = size
        self.position = position


class PackingProblem:
    def __init__(self,
        square_size: int,
        disk_num: int,
        disk_small_proportion: float,
        disk_small_radius: int,
        disk_large_proportion: float,
        disk_large_radius: int,
        overlap_threshold_proportion: float,
        sample_num: int,
    ) -> None:
        self.square_size = square_size
        self.disk_num = disk_num
        self.disk_small_radius = disk_small_radius
        self.disk_small_proportion = disk_small_proportion
        self.disk_large_radius = disk_large_radius
        self.disk_large_proportion = disk_large_proportion
        self.overlap_threshold_proportion = overlap_threshold_proportion
        self.sample_num = sample_num
        self.disks : list[Disk] = []
    
    def calculate(self) -> float:
        '''
        Calculate packing fraction.
        '''
        disk_small_num = 0
        disk_large_num = 0
        for _ in range(self.disk_num):
            new_disk_size = \
                Disk.Small if random() < self.disk_small_proportion else \
                Disk.Large

            new_disk_radius = \
                self.disk_small_radius if new_disk_size == Disk.Small else \
                self.disk_large_radius

            # Prevent the disk outside the square.
            random_fixer = lambda x: \
                x * (self.square_size - 2 * new_disk_radius) + new_disk_radius

            new_disk = Disk(complex(
                    random_fixer(random()),
                    random_fixer(random())),
                    new_disk_size)

            # Prevent the disk that overlaps too much.
            can_be_added = True
            for existing_disk in self.disks:
                existing_disk_radius = \
                    self.disk_small_radius if existing_disk.size == Disk.Small else \
                    self.disk_large_radius
                    
                distance_between = abs(new_disk.position - existing_disk.position)
                distance_maximum = new_disk_radius + existing_disk_radius
                if distance_between < self.overlap_threshold_proportion * distance_maximum:
                    can_be_added = False
                    break
            
            if can_be_added:    
                if new_disk_size == Disk.Small:
                    disk_small_num += 1
                else:
                    disk_large_num += 1
                
                self.disks.append(new_disk)

        sample_inside_disks_num = 0

        for _ in range(self.sample_num):
            sample = complex(random(), random())
            inside = False
            for disk in self.disks:
                disk_radius = \
                    self.disk_small_radius if disk.size == Disk.Small else \
                    self.disk_large_radius
                if abs(sample - disk.position) < disk_radius:
                    inside = True
                    break
            if inside:
                sample_inside_disks_num += 1

        return sample_inside_disks_num / self.sample_num

    def configure_output(self) -> str:
        output = ''

        for disk in self.disks:
            disk_radius = \
                self.disk_small_radius if disk.size == Disk.Small else \
                self.disk_large_radius
            output += '%.3f\t%.3f\t%.3f\n' % (
                disk_radius,
                disk.position.real,
                disk.position.imag)

        return output

def main() -> None:
    problems = [
        # 1
        PackingProblem(
            square_size=20,
            disk_num=1000,
            disk_small_proportion=0.5,
            disk_small_radius=pi**-0.5,
            disk_large_proportion=0.5,
            disk_large_radius=pi**-0.5,
            overlap_threshold_proportion=0.9,
            sample_num=10000,
        ),
        # 2

        # 3
    ]
    for problem_i, problem in enumerate(problems):
        # Output configure

        problem.calculate()
        configure = problem.configure_output()
        configure_a = '%.3f' % problem.overlap_threshold_proportion
        configure_n = '%i' % problem.disk_num
        configure_file_name = f'{configure_a}-{configure_n}.txt'
        with open(configure_file_name, 'w') as f:
            f.write(configure)

        # Plot relation bewteen
        # overlap threshold and inside proportion
        disk_nums = [50, 100, 200, 400]
        thresholds = [0.4, 0.6, 0.7, 0.8, 0.9, 1]
        for disk_num in disk_nums:
            problem.disk_num = disk_num
            proportions = []
            for threshold in thresholds:
                problem.overlap_threshold_proportion = threshold
                proportions.append(problem.calculate())

            # Plot


        


if __name__ == '__main__':
    main()
