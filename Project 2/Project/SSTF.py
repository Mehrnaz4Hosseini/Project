import random
import matplotlib.pyplot as plt

# SSTF algorithm implementation
def sstf(requests, initial_position):
    seek_sequence = []
    current_position = initial_position
    seek_count = 0
    pending_requests = requests.copy()
    response_times = []

    while pending_requests:

        # Calculate distances of all pending requests from the current position
        distances = {request: abs(request - current_position) for request in pending_requests}

        # Select the request with the shortest distance
        next_request = min(distances, key=distances.get)
        seek_sequence.append(next_request)
        
        #seek_time = abs(next_request - current_position)
        seek_count += abs(next_request - current_position)
        current_position = next_request
        pending_requests.remove(next_request)

        # Calculate and store the response time for each request
        response_times.append(seek_count)

    # Calculate the average response time
    average_response_time = sum(response_times) / len(response_times)

    return seek_sequence, seek_count, average_response_time


def plot_disk_scheduling(requests,seek_sequence, initial_head, total_seek_count, avg_response_time):
    
    plot_sequence = [initial_head] + seek_sequence

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(plot_sequence)), plot_sequence, marker='o', linestyle='-', color='blue')


    plt.title("Disk Scheduling: SCAN Algorithm")
    plt.xlabel("Sequence Index")
    plt.ylabel("Cylinder Number")
    plt.grid(True)
    plt.xticks([])

    metrics_text = (f"Requests: {requests}\n"
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

# Number of requests
num_requests = 100000
requests = [int(min(max(random.gauss(mean, std_dev), 0), N)) for _ in range(num_requests)]


# Execute and display results
seek_sequence, seek_count, average_response_time = sstf(requests, initial_position)


# Plot the seek sequence with metrics
plot_disk_scheduling(requests,seek_sequence, initial_position, seek_count, average_response_time)

#We can see the requests and seek sequences, but because the large amount of requests(100000) we comment this part.
print("Requests: ", requests)
print("Seek sequence: ", seek_sequence)
print("Total seek count: ", seek_count)
print("Average response time: ", average_response_time)
