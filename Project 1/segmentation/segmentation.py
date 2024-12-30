import time
import json

class SegmentationAlgorithm:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.free_memory = total_memory
        self.memory = [True] * total_memory  # True indicates free memory
        self.allocated = []
        self.waiting = []
        self.finished = []

    def allocate_memory(self, process):
        """Allocate non-contiguous memory blocks to a process."""
        needed_memory = process["needed_memory"]
        if needed_memory > self.free_memory:
            process["status"] = "Waiting"
            self.waiting.append(process)
            return

        allocated_segments = []
        allocated = 0

        for i in range(self.total_memory):
            if self.memory[i]:
                self.memory[i] = False
                allocated_segments.append(i)
                allocated += 1
                if allocated == needed_memory:
                    break

        self.free_memory -= needed_memory
        process["allocated_segments"] = allocated_segments
        process["status"] = "Allocated"
        self.allocated.append(process)

    def release_memory(self, process):
        """Release memory of a process and mark it as finished."""
        for index in process["allocated_segments"]:
            self.memory[index] = True
        self.free_memory += process["needed_memory"]
        process["status"] = "Finished"
        process.pop("allocated_segments", None)
        self.finished.append(process)

    def run_simulation(self, processes, json_output_file):
        """Run the segmentation simulation."""
        simulation_time = 0
        simulation_log = []

        # Initialize processes
        for process in processes:
            process["remaining_time"] = process["duration"]
            process["needed_memory"] = process["memory"]
            process["allocated_segments"] = []
            process["status"] = "Waiting"
            self.allocate_memory(process)

        while self.allocated or self.waiting:
            free_memory_blocks = [i for i, free in enumerate(self.memory) if free]

            # Log the current state
            state = {
                "time": simulation_time,
                "free_memory": self.free_memory,
                "free_memory_blocks": free_memory_blocks,
                "allocated_processes": [
                    {
                        "id": process["id"],
                        "duration": process["duration"],
                        "status": process["status"],
                        "remaining_time": process["remaining_time"],
                        "needed_memory": process["needed_memory"],
                        "allocated_segments": process["allocated_segments"],
                    }
                    for process in self.allocated
                ],
                "waiting_processes": [
                    {
                        "id": process["id"],
                        "duration": process["duration"],
                        "status": process["status"],
                        "remaining_time": process["remaining_time"],
                        "needed_memory": process["needed_memory"],
                    }
                    for process in self.waiting
                ],
                "finished_processes": [
                    {
                        "id": process["id"],
                        "duration": process["duration"],
                        "status": process["status"],
                        "needed_memory": process["needed_memory"],
                    }
                    for process in self.finished
                ],
            }
            simulation_log.append(state)

            # Update allocated processes
            for process in list(self.allocated):
                process["remaining_time"] -= 1
                if process["remaining_time"] <= 0:
                    self.allocated.remove(process)
                    self.release_memory(process)

            # Allocate waiting processes if enough memory is available
            for process in list(self.waiting):
                if process["needed_memory"] <= self.free_memory:
                    self.waiting.remove(process)
                    self.allocate_memory(process)

            simulation_time += 1
            time.sleep(1)  # Simulate real-time execution

        # Log final state
        state = {
            "time": simulation_time,
            "free_memory": self.free_memory,
            "free_memory_blocks": [i for i, free in enumerate(self.memory) if free],
            "allocated_processes": [],
            "waiting_processes": [],
            "finished_processes": [
                {
                    "id": process["id"],
                    "duration": process["duration"],
                    "status": process["status"],
                    "needed_memory": process["needed_memory"],
                }
                for process in self.finished
            ],
        }
        simulation_log.append(state)

        # Write log to file
        with open(json_output_file, mode="w") as file:
            json.dump(simulation_log, file, indent=4)
