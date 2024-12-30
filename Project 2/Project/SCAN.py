import random
import matplotlib.pyplot as plt

# SCAN algorithm implementation
def scan_disk_scheduling(requests, head, direction, disk_size):

    requests.sort()  
    seek_sequence = []
    total_seek_count = 0
    response_times = []
    
    # Separate requests into those less than and greater than the initial head position
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    # Serve requests based on direction
    if direction == "left":
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            head = r
        # Once we reach the beginning of the disk, move to the other end
        if right:
            total_seek_count += head  # Seek to the beginning (0)
            head = 0
        for r in right:
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            response_times.append(total_seek_count)
            head = r

    elif direction == "right":
        for r in right:
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            response_times.append(total_seek_count)
            head = r

        if left:
            total_seek_count += abs(head - (disk_size - 1)) 
            head = disk_size - 1
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            response_times.append(total_seek_count)
            head = r
    
    avg_response_time = sum(response_times) / len(requests)

    return seek_sequence, total_seek_count, avg_response_time



def plot_disk_scheduling(requests, seek_sequence, initial_head, total_seek_count, avg_response_time, direction):

    plot_sequence = [initial_head] + seek_sequence

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(plot_sequence)), plot_sequence, marker='o', linestyle='-', color='blue')


    plt.title("Disk Scheduling: SCAN Algorithm")
    plt.xlabel("Sequence Index")
    plt.ylabel("Cylinder Number")
    plt.grid(True)
    plt.xticks([])

    metrics_text = (f"Requests: {requests}\n"
                    f"Direction: {direction}\n"
                    f"Total Seek Count: {total_seek_count}\n"
                    f"Average Response Time: {avg_response_time:.2f}")
    plt.gcf().text(0.15, 0.9, metrics_text, fontsize=10, color='red',
                   verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    plt.tight_layout()
    plt.show()


N = int(input("Number of cylinders: "))  # Number of cylinders
mean = N / 2
std_dev = N / 5

# Initial position of the disk head
initial_position = int(input("Initial position of the disk head: "))

#Direction
direction = input("Specify the head direction (right or left): ")

# Number of requests
num_requests = 100000
requests = [int(min(max(random.gauss(mean, std_dev), 0), N)) for _ in range(num_requests)]


seek_sequence, total_seek_count, avg_response_time = scan_disk_scheduling(requests, initial_position, direction, N)

# Plot the seek sequence with metrics
plot_disk_scheduling(requests, seek_sequence, initial_position, total_seek_count, avg_response_time, direction)

#We can see the requests and seek sequences, but because the large amount of requests(100000) we comment this part.
#print("Requests: ", requests)
#print("Seek sequence: ", seek_sequence)
print("Total seek count: ", total_seek_count)
print("Average response time: ", avg_response_time)