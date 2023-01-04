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
        disk_small_proportion: float,
        disk_small_radius: int,
        disk_large_proportion: float,
        disk_large_radius: int,
        square_size = 20,
    ) -> None:
        self.square_size = square_size
        self.disk_small_radius = disk_small_radius
        self.disk_small_proportion = disk_small_proportion
        self.disk_large_radius = disk_large_radius
        self.disk_large_proportion = disk_large_proportion

        self.disk_num = None
        self.overlap_threshold_proportion = None
        self.sample_num = None
        self.disks : list[Disk] = []
    
    def place_disks(self) -> None:
        self.disks.clear()

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

    def calculate_average(self, times: int) -> float:
        proportions = []

        for _ in range(times):
            self.place_disks()
            proportions.append(self.calculate())
        
        average = sum(proportions) / times

        return average

    def calculate_variance(self, times: int) -> float:
        proportions = []

        for _ in range(times):
            self.place_disks()
            proportions.append(self.calculate())
        
        average = sum(proportions) / times
        variance = sum([(p-average)**2 for p in proportions]) / times

        return variance

    def calculate(self) -> float:
        '''
        Calculate packing fraction.
        '''
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
        PackingProblem(
            disk_small_proportion=0.5,
            disk_small_radius=pi**-0.5,
            disk_large_proportion=0.5,
            disk_large_radius=pi**-0.5,
        ),
        PackingProblem(
            disk_small_proportion=0.5,
            disk_small_radius=(1/(2*pi))**0.5,
            disk_large_proportion=0.5,
            disk_large_radius=(3/(2*pi))**0.5,
        ),
        PackingProblem(
            disk_small_proportion=0.8,
            disk_small_radius=(15/(16*pi))**0.5,
            disk_large_proportion=0.2,
            disk_large_radius=(5/(4*pi))**0.5,
        ),
    ]

    # Generate configurations
    # We choose the third one:
    problem = problems[2]

    problem.sample_num = 200
    for threshold, disk_num in (
        # We choose these 3 pairs:
        (0.18, 100),
        (0.65, 200),
        (0.81, 300),
    ):
        problem.disk_num = disk_num
        problem.overlap_threshold_proportion = threshold
        problem.place_disks()
        with open(f'{threshold} - {disk_num}.txt', 'w') as f:
            f.write(problem.configure_output())

    # Generate plots
    disk_nums = [50, 100, 200, 400]

    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(len(problems), len(disk_nums))
    plt.subplots_adjust(wspace=0.5, hspace=0.8)

    repetition_num = 10
    thresholds = [0.4, 0.6, 0.7, 0.8, 0.9, 1.0]

    for problem_id, problem in enumerate(problems):
        problem.sample_num = 200
        for disk_num_id, disk_num in enumerate(disk_nums):
            problem.disk_num = disk_num
            proportions = []
            for threshold in thresholds:
                problem.overlap_threshold_proportion = threshold
                proportions.append(problem.calculate_average(repetition_num))

            axis_now = axis[problem_id][disk_num_id]
            axis_now.set_ylim(0, 1)
            axis_now.set_xlim(0.4, 1)
            axis_now.plot(thresholds, proportions)
            axis_now.set_title(f'{problem_id+1} - {disk_num}')

    figure.set_size_inches(8, 4)
    figure.savefig('Plots.png', dpi=300)

    # Generate accuracy table
    sample_nums = [100, 200, 400]
    repetition_nums = [10, 20, 40, 80]

    for problem_id, problem in enumerate(problems):
        problem.overlap_threshold_proportion = 0.8
        problem.disk_num = 400

        table = [[''
            for _ in range(len(repetition_nums)+1)]
            for _ in range(len(sample_nums)+1)]

        for sample_num_id, sample_num in enumerate(sample_nums):
            table[sample_num_id+1][0] = str(sample_num)
        for repetition_num_id, repetition_num in enumerate(repetition_nums):
            table[0][repetition_num_id+1] = str(repetition_num)

        for sample_num_id, sample_num in enumerate(sample_nums):
            for repetition_num_id, repetition_num in enumerate(repetition_nums):
                problem.sample_num = sample_num

                table[sample_num_id+1][repetition_num_id+1] = \
                    '%.3f' % problem.calculate_variance(repetition_num)
        
        with open(f'Accuracy - {problem_id+1}.csv', 'w') as f:
            f.write('\n'.join([','.join(line) for line in table]))

if __name__ == '__main__':
    main()
