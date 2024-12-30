import csv
import random
import os
from segmentation.segmentation import SegmentationAlgorithm
from paging.paging import PagingAlgorithm 


def generate_processes_to_csv(filename, num_processes, max_memory, max_duration):
    processes = []
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Process ID", "Memory Required", "Duration"])
        for pid in range(1, num_processes + 1):
            memory_required = random.randint(1, max_memory // 4)
            duration = random.randint(1, max_duration)
            writer.writerow([pid, memory_required, duration])
            processes.append({"id": pid, "memory": memory_required, "duration": duration, "status": "Waiting"})
    return processes

def read_processes_from_csv(filename):
    processes = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            pid, memory_required, duration = int(row[0]), int(row[1]), int(row[2])
            processes.append({"id": pid, "memory": memory_required, "duration": duration, "status": "Waiting"})
    return processes

def run_simulation():
    total_memory = int(input("Enter total memory of the system: "))
    num_processes = int(input("Enter the number of processes to generate: "))
    max_duration = int(input("Enter the maximum duration for any process: "))

    process_file = "processes_temp.csv"
    json_output_file_segmentation = "segmentation/segmentation_simulation_log.json"
    json_output_file_paging = "paging/paging_simulation_log.json"

    # if os.path.exists(process_file):
    #     print(f"Found existing process file: {process_file}")
    #     processes = read_processes_from_csv(process_file)

    processes = generate_processes_to_csv(process_file, num_processes, total_memory, max_duration)

    print("Choose memory allocation algorithm:")
    print("1. Segmentation")
    print("2. Paging")
    choice = int(input("Enter your choice: "))

    use_paging = choice == 2
    if choice not in [1, 2]:
        print("Invalid choice!")
        return

    # Initialize the selected memory allocation algorithm
    if use_paging:
        page_size = int(input("Enter page size for paging: "))
        paging_algorithm = PagingAlgorithm(total_memory, page_size)
        paging_algorithm.run_simulation(processes, json_output_file_paging)
        print(f"Paging simulation completed. Results saved to {json_output_file_paging}")
    else:
        segmentation_algorithm = SegmentationAlgorithm(total_memory)
        segmentation_algorithm.run_simulation(processes, json_output_file_segmentation)
        print(f"Segmentation simulation completed. Results saved to {json_output_file_segmentation}")


if __name__ == "__main__":
    run_simulation()
