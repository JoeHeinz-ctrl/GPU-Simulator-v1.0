"""
CO4: I/O Interfacing Simulation
Demonstrates: Input/Output device interaction and interfacing

This module simulates I/O operations:
1. Input devices (keyboard, file)
2. Output devices (display, file)
3. I/O controllers
4. DMA (Direct Memory Access)
5. Buffering
"""

import time
from typing import Any, List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IORequest:
    """Represents an I/O request"""
    device_type: str
    operation: str  # 'read' or 'write'
    data: Any
    timestamp: float
    status: str = 'pending'


class IOController:
    """
    Simulates I/O Controller
    
    COA Concept Mapping:
    - I/O Controller: Manages communication between CPU and I/O devices
    - I/O Buffer: Temporary storage for data transfer
    - Device Status Register: Tracks device state
    - DMA: Direct Memory Access for efficient data transfer
    """
    
    def __init__(self, device_name: str, verbose: bool = True):
        self.device_name = device_name
        self.verbose = verbose
        self.buffer = []
        self.status = "READY"
        self.requests_processed = 0
        self.total_bytes_transferred = 0
    
    def check_device_status(self) -> str:
        """
        Check device status
        
        COA Concept: Device Status Register
        """
        if self.verbose:
            print(f"[{self.device_name}] Status: {self.status}")
        return self.status
    
    def read_from_device(self, size: int) -> Any:
        """
        Read data from I/O device
        
        COA Concept: Input Operation
        """
        self.status = "BUSY"
        
        if self.verbose:
            print(f"\n[{self.device_name}] READ Operation")
            print(f"  Device Status: {self.status}")
            print(f"  Requesting {size} bytes...")
        
        # Simulate I/O delay
        time.sleep(0.2)
        
        # Simulate reading data
        data = f"Data from {self.device_name} ({size} bytes)"
        self.buffer.append(data)
        self.total_bytes_transferred += size
        
        if self.verbose:
            print(f"  ✓ Data read: {data}")
            print(f"  ✓ Stored in I/O buffer")
        
        self.status = "READY"
        self.requests_processed += 1
        
        return data
    
    def write_to_device(self, data: Any) -> bool:
        """
        Write data to I/O device
        
        COA Concept: Output Operation
        """
        self.status = "BUSY"
        
        if self.verbose:
            print(f"\n[{self.device_name}] WRITE Operation")
            print(f"  Device Status: {self.status}")
            print(f"  Writing data: {data}")
        
        # Simulate I/O delay
        time.sleep(0.2)
        
        # Simulate writing data
        data_size = len(str(data))
        self.total_bytes_transferred += data_size
        
        if self.verbose:
            print(f"  ✓ Data written successfully ({data_size} bytes)")
        
        self.status = "READY"
        self.requests_processed += 1
        
        return True
    
    def get_statistics(self) -> Dict:
        """Get I/O statistics"""
        return {
            'device': self.device_name,
            'status': self.status,
            'requests_processed': self.requests_processed,
            'bytes_transferred': self.total_bytes_transferred
        }


class DMAController:
    """
    Simulates Direct Memory Access (DMA) Controller
    
    COA Concept: DMA allows I/O devices to transfer data directly to/from
    memory without CPU intervention, improving efficiency
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.transfers_completed = 0
    
    def dma_transfer(self, source: str, destination: str, data: Any, size: int):
        """
        Perform DMA transfer
        
        COA Concept: Direct Memory Access
        Transfers data without CPU intervention
        """
        if self.verbose:
            print(f"\n{'─'*60}")
            print(f"DMA TRANSFER INITIATED")
            print(f"{'─'*60}")
            print(f"  Source: {source}")
            print(f"  Destination: {destination}")
            print(f"  Data Size: {size} bytes")
            print(f"  CPU freed for other tasks during transfer")
        
        # Simulate DMA transfer
        time.sleep(0.3)
        
        if self.verbose:
            print(f"  ✓ DMA transfer completed")
            print(f"  ✓ {size} bytes transferred")
            print(f"{'─'*60}")
        
        self.transfers_completed += 1
        return True


class IOInterfaceSimulator:
    """
    Main I/O Interface Simulator
    
    Demonstrates complete I/O subsystem interaction
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.keyboard = IOController("KEYBOARD", verbose)
        self.display = IOController("DISPLAY", verbose)
        self.disk = IOController("DISK", verbose)
        self.dma = DMAController(verbose)
        self.io_requests = []
    
    def get_user_input(self, prompt: str) -> str:
        """
        Simulate keyboard input
        
        COA Concept: Input Device Interfacing
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"INPUT DEVICE: KEYBOARD")
            print(f"{'='*60}")
        
        # Check device status
        self.keyboard.check_device_status()
        
        # Get input
        user_input = input(f"{prompt}: ")
        
        # Simulate input processing
        self.keyboard.read_from_device(len(user_input))
        
        return user_input
    
    def display_output(self, data: Any):
        """
        Simulate display output
        
        COA Concept: Output Device Interfacing
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"OUTPUT DEVICE: DISPLAY")
            print(f"{'='*60}")
        
        # Check device status
        self.display.check_device_status()
        
        # Write to display
        self.display.write_to_device(data)
        
        # Show output
        print(f"\n[DISPLAY OUTPUT]")
        print(f"{'─'*60}")
        print(f"{data}")
        print(f"{'─'*60}")
    
    def read_from_disk(self, filename: str, size: int) -> str:
        """
        Simulate disk read operation
        
        COA Concept: Secondary Storage I/O
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"SECONDARY STORAGE: DISK READ")
            print(f"{'='*60}")
            print(f"  File: {filename}")
        
        # Check device status
        self.disk.check_device_status()
        
        # Read from disk
        data = self.disk.read_from_device(size)
        
        return data
    
    def write_to_disk(self, filename: str, data: Any):
        """
        Simulate disk write operation
        
        COA Concept: Secondary Storage I/O
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"SECONDARY STORAGE: DISK WRITE")
            print(f"{'='*60}")
            print(f"  File: {filename}")
        
        # Check device status
        self.disk.check_device_status()
        
        # Write to disk
        self.disk.write_to_device(data)
    
    def perform_dma_transfer(self, source: str, dest: str, data: Any):
        """
        Perform DMA transfer between devices
        
        COA Concept: Direct Memory Access
        """
        size = len(str(data))
        self.dma.dma_transfer(source, dest, data, size)
    
    def get_io_statistics(self) -> Dict:
        """Get comprehensive I/O statistics"""
        return {
            'keyboard': self.keyboard.get_statistics(),
            'display': self.display.get_statistics(),
            'disk': self.disk.get_statistics(),
            'dma_transfers': self.dma.transfers_completed
        }


def demonstrate_io_interfacing():
    """
    Demonstration function for CO4
    Shows complete I/O interfacing simulation
    """
    print("\n" + "="*70)
    print("CO4 DEMONSTRATION: I/O INTERFACING SIMULATION")
    print("="*70)
    print("\nCOA Concepts Demonstrated:")
    print("• Input Device Interfacing (Keyboard)")
    print("• Output Device Interfacing (Display)")
    print("• Secondary Storage I/O (Disk)")
    print("• I/O Controllers")
    print("• Device Status Registers")
    print("• DMA (Direct Memory Access)")
    print("• I/O Buffering")
    print("="*70)
    
    # Create I/O interface simulator
    io_sim = IOInterfaceSimulator(verbose=True)
    
    # 1. Get user input (Keyboard I/O)
    print("\n" + "="*70)
    print("DEMONSTRATION 1: KEYBOARD INPUT")
    print("="*70)
    dataset_size = io_sim.get_user_input("Enter dataset size (e.g., 1000)")
    operation = io_sim.get_user_input("Enter operation (ADD/MUL/SUB/DIV)")
    
    # 2. Process and display output (Display I/O)
    print("\n" + "="*70)
    print("DEMONSTRATION 2: DISPLAY OUTPUT")
    print("="*70)
    result_data = f"""
Simulation Configuration:
  Dataset Size: {dataset_size}
  Operation: {operation}
  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  Status: Ready for execution
"""
    io_sim.display_output(result_data)
    
    # 3. Disk I/O operations
    print("\n" + "="*70)
    print("DEMONSTRATION 3: DISK I/O OPERATIONS")
    print("="*70)
    
    # Write to disk
    simulation_data = {
        'dataset_size': dataset_size,
        'operation': operation,
        'timestamp': datetime.now().isoformat()
    }
    io_sim.write_to_disk("simulation_config.dat", str(simulation_data))
    
    # Read from disk
    read_data = io_sim.read_from_disk("simulation_config.dat", 256)
    
    # 4. DMA Transfer
    print("\n" + "="*70)
    print("DEMONSTRATION 4: DMA TRANSFER")
    print("="*70)
    io_sim.perform_dma_transfer("DISK", "MEMORY", simulation_data)
    
    # Display I/O statistics
    print("\n" + "="*70)
    print("I/O SUBSYSTEM STATISTICS")
    print("="*70)
    stats = io_sim.get_io_statistics()
    
    for device, device_stats in stats.items():
        if device != 'dma_transfers':
            print(f"\n{device.upper()}:")
            for key, value in device_stats.items():
                print(f"  {key}: {value}")
    
    print(f"\nDMA Transfers Completed: {stats['dma_transfers']}")
    print("="*70)
    
    return io_sim, dataset_size, operation


if __name__ == "__main__":
    demonstrate_io_interfacing()
