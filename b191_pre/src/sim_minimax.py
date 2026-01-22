from collections import deque


class BusSimulation:
    """
    Simulates a bus system where riders wait in line and are assigned to different
    types of services. Services include short-term (shuttle) and long-term (bus)
    with different capacities and durations.
    """
    
    def __init__(self, riders, num_short, num_long, max_wait, short_runtime, long_runtime):
        """
        Initialize the simulation system.
        
        Args:
            riders: List of riders waiting in queue
            num_short: Number of short-term services available
            num_long: Number of long-term services available
            max_wait: Maximum wait count for vowel riders
            short_runtime: Runtime for short-term services
            long_runtime: Runtime for long-term services
        """
        self.vowels = set('AEIOU')
        self.waiting_queue = deque(riders)
        
        # Track wait counts for riders with names starting with vowels
        self.vowel_wait_counts = {r: 0 for r in riders if r[0] in self.vowels}
        
        self.num_short = num_short
        self.num_long = num_long
        self.short_runtime = short_runtime
        self.long_runtime = long_runtime
        
        self.available_short = num_short
        self.available_long = num_long
        
        # Track currently active services
        self.active_services = []

    def is_vowel_rider(self, rider):
        """Check if rider's name starts with a vowel"""
        return rider[0] in self.vowels

    def process_turn(self):
        """
        Process one turn:
        1. Assign waiting riders to available services
        2. Update remaining time for active services
        3. Complete services return riders to waiting queue
        """
        assigned = False
        queue_snapshot = list(self.waiting_queue)
        i = 0
        
        # Assign riders to services
        while i < len(queue_snapshot) and not assigned:
            rider = queue_snapshot[i]
            
            # Priority: assign to long-term service if available
            if self.available_long > 0:
                self.available_long -= 1
                service_riders = [self.waiting_queue.popleft()]
                if self.waiting_queue:
                    service_riders.append(self.waiting_queue.popleft())
                self.active_services.append(('long', self.long_runtime, service_riders))
                assigned = True
                
            # Otherwise try short-term service
            elif self.available_short > 0:
                # Vowel riders have special limits
                if self.is_vowel_rider(rider) and self.vowel_wait_counts.get(rider, 0) < 2:
                    self.vowel_wait_counts[rider] += 1
                    i += 1
                else:
                    self.available_short -= 1
                    self.waiting_queue.popleft()
                    self.active_services.append(('short', self.short_runtime, [rider]))
                    assigned = True
            else:
                break

        # Update all active services' remaining time
        for i in range(len(self.active_services) - 1, -1, -1):
            service_type, time_remaining, service_riders = self.active_services[i]
            self.active_services[i] = (service_type, time_remaining - 1, service_riders)
            
            # Service completed, release resources
            if self.active_services[i][1] <= 0:
                for rider in service_riders:
                    self.waiting_queue.append(rider)
                    if rider in self.vowel_wait_counts:
                        self.vowel_wait_counts[rider] = 0
                del self.active_services[i]
                
                # Release corresponding service resources
                if service_type == 'short':
                    self.available_short += 1
                else:
                    self.available_long += 1

    def display_state(self, turn):
        """Display system state at the start of each turn"""
        print(f"Turn {turn}:")
        print(f"  Waiting Queue: {list(self.waiting_queue)}")
        print(f"  Active Services: {[(t, tl, r) for t, tl, r in self.active_services]}")
        print("-" * 40)

    def run_simulation(self, num_turns):
        """Run the simulation for specified number of turns"""
        for turn in range(1, num_turns + 1):
            self.display_state(turn)
            self.process_turn()


def main():
    """
    Main function: initialize and run the simulation.
    Uses 20 letters (A-T) as riders, 5 short-term and 1 long-term services.
    """
    riders = list("ABCDEFGHIJKLMNOPQRSTUV")
    num_short = 5
    num_long = 1
    short_runtime = 5
    long_runtime = 4

    simulation = BusSimulation(riders, num_short, num_long, 2, short_runtime, long_runtime)
    simulation.run_simulation(20)


if __name__ == "__main__":
    main()
