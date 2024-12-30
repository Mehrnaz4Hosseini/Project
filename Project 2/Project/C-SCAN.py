import random
import matplotlib.pyplot as plt

# C-SCAN algorithm implementation
def c_scan_disk_scheduling(requests, head, direction, disk_size):

    requests.sort()  
    seek_sequence = []
    total_seek_time = 0
    response_times = []
    
    # Separate requests into those less than and greater than the initial head position
    right = [r for r in requests if r >= head]
    left = [r for r in requests if r < head]
    
    # Serve requests based on direction
    if direction == "right":
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
        
        if left:
            #add disk_size-1 and 0 for the plot
            seek_sequence.append(disk_size-1)
            seek_sequence.append(0)

            total_seek_time += abs(head - (disk_size - 1))  # Seek to the end of the disk
            head = 0  # Jump to the start
            total_seek_time += disk_size - 1  # jump from end to start
        
        # Process the remaining requests on the left
        for r in left:
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
    
    elif direction == "left":
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
        
        if right:
            #add disk_size-1 and 0 for the plot
            seek_sequence.append(0)
            seek_sequence.append(disk_size-1)
            
            total_seek_time += head  # Seek to the beginning (0)
            head = disk_size - 1  # Jump to the end
            total_seek_time += disk_size - 1  # jump from start to end
        
        # Process the remaining requests on the right
        for r in reversed(right):
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
    
    # Calculate average response time
    avg_response_time = sum(response_times) / len(requests)
    
    return seek_sequence, total_seek_time, avg_response_time


def plot_disk_scheduling(requests, seek_sequence, initial_head, total_seek_count, avg_response_time, direction):
    
    plot_sequence = [initial_head] + seek_sequence

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(plot_sequence)), plot_sequence, marker='o', linestyle='-', color='blue')


    plt.title("Disk Scheduling: C-SCAN Algorithm")
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



# Set up a normal distribution for cylinder numbers
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


seek_sequence, total_seek_count, avg_response_time = c_scan_disk_scheduling(requests, initial_position, direction, N)


# Plot the seek sequence with metrics
plot_disk_scheduling(requests, seek_sequence, initial_position, total_seek_count, avg_response_time, direction)


if N-1 in seek_sequence :
    seek_sequence.remove(N-1) 
if 0 in seek_sequence:
    seek_sequence.remove(0) 

#We can see the requests and seek sequences, but because the large amount of requests(100000) we comment this part.
#print("Requests: ", requests)
#print("Seek sequence: ", seek_sequence)
print("Total seek count: ", total_seek_count)
print("Average response time: ", avg_response_time)
