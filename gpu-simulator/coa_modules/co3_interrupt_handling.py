"""
CO3: Interrupt Handling Simulation
Demonstrates: Interrupt mechanism in computer systems

This module simulates how a CPU handles interrupts:
1. Normal execution
2. Interrupt occurs
3. Save current state
4. Execute Interrupt Service Routine (ISR)
5. Restore state and resume
"""

import time
import random
from typing import Callable, Any, List
from dataclasses import dataclass


@dataclass
class InterruptContext:
    """Stores CPU state during interrupt"""
    program_counter: int
    accumulator: float
    registers: dict
    timestamp: float


class InterruptHandler:
    """
    Simulates interrupt handling mechanism
    
    COA Concept Mapping:
    - Interrupt Vector Table (IVT): Maps interrupt types to handlers
    - Interrupt Service Routine (ISR): Code executed when interrupt occurs
    - Context Switching: Save/restore CPU state
    - Interrupt Priority: Handle multiple interrupts
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.interrupt_vector_table = {}
        self.interrupt_queue = []
        self.context_stack = []
        self.interrupts_handled = 0
        self.interrupt_enabled = True
    
    def register_interrupt_handler(self, interrupt_type: str, handler: Callable):
        """
        Register an Interrupt Service Routine (ISR)
        
        COA Concept: Interrupt Vector Table (IVT)
        Maps interrupt types to their handler functions
        """
        self.interrupt_vector_table[interrupt_type] = handler
        if self.verbose:
            print(f"✓ Registered ISR for interrupt type: '{interrupt_type}'")
    
    def trigger_interrupt(self, interrupt_type: str, data: Any = None):
        """
        Trigger an interrupt
        
        COA Concept: Interrupt Request (IRQ)
        Hardware/software signals CPU to handle interrupt
        """
        if not self.interrupt_enabled:
            if self.verbose:
                print(f"⚠ Interrupt '{interrupt_type}' ignored (interrupts disabled)")
            return
        
        self.interrupt_queue.append({
            'type': interrupt_type,
            'data': data,
            'timestamp': time.time()
        })
        
        if self.verbose:
            print(f"\n{'!'*60}")
            print(f"⚡ INTERRUPT TRIGGERED: {interrupt_type}")
            print(f"{'!'*60}")
    
    def save_context(self, pc: int, accumulator: float, registers: dict) -> InterruptContext:
        """
        Save current CPU state
        
        COA Concept: Context Switching
        Save registers, PC, and flags before handling interrupt
        """
        context = InterruptContext(
            program_counter=pc,
            accumulator=accumulator,
            registers=registers.copy(),
            timestamp=time.time()
        )
        self.context_stack.append(context)
        
        if self.verbose:
            print(f"\n[SAVE CONTEXT]")
            print(f"  Program Counter: {pc}")
            print(f"  Accumulator: {accumulator}")
            print(f"  Registers: {registers}")
            print(f"  ✓ Context saved to stack")
        
        return context
    
    def restore_context(self) -> InterruptContext:
        """
        Restore previous CPU state
        
        COA Concept: Context Switching
        Restore saved state after interrupt handling
        """
        if not self.context_stack:
            raise RuntimeError("No context to restore")
        
        context = self.context_stack.pop()
        
        if self.verbose:
            print(f"\n[RESTORE CONTEXT]")
            print(f"  Program Counter: {context.program_counter}")
            print(f"  Accumulator: {context.accumulator}")
            print(f"  Registers: {context.registers}")
            print(f"  ✓ Context restored from stack")
        
        return context
    
    def handle_interrupt(self, interrupt_info: dict, current_state: dict) -> Any:
        """
        Handle a single interrupt
        
        COA Concept: Interrupt Service Routine (ISR) execution
        """
        interrupt_type = interrupt_info['type']
        interrupt_data = interrupt_info['data']
        
        if interrupt_type not in self.interrupt_vector_table:
            if self.verbose:
                print(f"⚠ No handler registered for interrupt: {interrupt_type}")
            return None
        
        if self.verbose:
            print(f"\n{'─'*60}")
            print(f"HANDLING INTERRUPT: {interrupt_type}")
            print(f"{'─'*60}")
        
        # Save current context
        context = self.save_context(
            current_state.get('pc', 0),
            current_state.get('accumulator', 0.0),
            current_state.get('registers', {})
        )
        
        # Disable interrupts during ISR (prevent nested interrupts)
        self.interrupt_enabled = False
        
        if self.verbose:
            print(f"\n[EXECUTE ISR]")
            print(f"  Interrupts disabled")
            print(f"  Executing handler for '{interrupt_type}'...")
        
        # Execute Interrupt Service Routine
        handler = self.interrupt_vector_table[interrupt_type]
        result = handler(interrupt_data)
        
        if self.verbose:
            print(f"  ✓ ISR completed")
            print(f"  Result: {result}")
        
        # Re-enable interrupts
        self.interrupt_enabled = True
        
        if self.verbose:
            print(f"  Interrupts re-enabled")
        
        # Restore context
        restored_context = self.restore_context()
        
        self.interrupts_handled += 1
        
        if self.verbose:
            print(f"\n{'─'*60}")
            print(f"✓ INTERRUPT HANDLED SUCCESSFULLY")
            print(f"  Resuming execution from PC={restored_context.program_counter}")
            print(f"{'─'*60}\n")
        
        return result
    
    def process_interrupts(self, current_state: dict) -> List[Any]:
        """Process all pending interrupts"""
        results = []
        
        while self.interrupt_queue:
            interrupt_info = self.interrupt_queue.pop(0)
            result = self.handle_interrupt(interrupt_info, current_state)
            results.append(result)
        
        return results
    
    def get_statistics(self) -> dict:
        """Get interrupt handling statistics"""
        return {
            'interrupts_handled': self.interrupts_handled,
            'pending_interrupts': len(self.interrupt_queue),
            'interrupt_enabled': self.interrupt_enabled
        }


def simulate_computation_with_interrupts(data_size: int = 1000):
    """
    Simulate a computation that gets interrupted
    
    Demonstrates:
    - Normal execution
    - Interrupt occurrence
    - Context saving
    - ISR execution
    - Context restoration
    - Resumption of execution
    """
    print("\n" + "="*70)
    print("CO3 DEMONSTRATION: INTERRUPT HANDLING SIMULATION")
    print("="*70)
    print("\nCOA Concepts Demonstrated:")
    print("• Interrupt Request (IRQ)")
    print("• Interrupt Service Routine (ISR)")
    print("• Context Switching (Save/Restore)")
    print("• Interrupt Vector Table (IVT)")
    print("• Interrupt Enable/Disable")
    print("="*70)
    
    # Create interrupt handler
    handler = InterruptHandler(verbose=True)
    
    # Define Interrupt Service Routines
    def timer_interrupt_handler(data):
        """ISR for timer interrupt"""
        print(f"\n  [ISR: TIMER] Timer interrupt occurred")
        print(f"  [ISR: TIMER] Performing time-critical task...")
        time.sleep(0.2)
        print(f"  [ISR: TIMER] Timer task completed")
        return "Timer handled"
    
    def io_interrupt_handler(data):
        """ISR for I/O interrupt"""
        print(f"\n  [ISR: I/O] I/O device ready")
        print(f"  [ISR: I/O] Processing I/O request: {data}")
        time.sleep(0.2)
        print(f"  [ISR: I/O] I/O operation completed")
        return f"I/O handled: {data}"
    
    def error_interrupt_handler(data):
        """ISR for error interrupt"""
        print(f"\n  [ISR: ERROR] Error detected: {data}")
        print(f"  [ISR: ERROR] Logging error and recovering...")
        time.sleep(0.2)
        print(f"  [ISR: ERROR] Error handled, system stable")
        return "Error recovered"
    
    # Register ISRs in Interrupt Vector Table
    print("\n" + "─"*70)
    print("INITIALIZING INTERRUPT VECTOR TABLE")
    print("─"*70)
    handler.register_interrupt_handler("TIMER", timer_interrupt_handler)
    handler.register_interrupt_handler("IO_READY", io_interrupt_handler)
    handler.register_interrupt_handler("ERROR", error_interrupt_handler)
    print("─"*70)
    
    # Simulate main computation
    print("\n" + "="*70)
    print("STARTING MAIN COMPUTATION")
    print("="*70)
    
    results = []
    current_state = {
        'pc': 0,
        'accumulator': 0.0,
        'registers': {'R1': 0, 'R2': 0, 'R3': 0}
    }
    
    for i in range(10):
        print(f"\n[MAIN] Processing iteration {i+1}/10...")
        print(f"[MAIN] PC={current_state['pc']}, ACC={current_state['accumulator']:.2f}")
        
        # Simulate computation
        current_state['accumulator'] += i * 1.5
        current_state['pc'] += 1
        time.sleep(0.3)
        
        # Randomly trigger interrupts during execution
        if i == 3:
            handler.trigger_interrupt("TIMER", None)
            handler.process_interrupts(current_state)
        
        if i == 6:
            handler.trigger_interrupt("IO_READY", "disk_read_complete")
            handler.process_interrupts(current_state)
        
        if i == 8:
            handler.trigger_interrupt("ERROR", "division_by_zero")
            handler.process_interrupts(current_state)
        
        results.append(current_state['accumulator'])
    
    print("\n" + "="*70)
    print("MAIN COMPUTATION COMPLETED")
    print("="*70)
    print(f"Final Accumulator Value: {current_state['accumulator']:.2f}")
    print(f"Final Program Counter: {current_state['pc']}")
    
    # Display statistics
    stats = handler.get_statistics()
    print("\n" + "="*70)
    print("INTERRUPT HANDLING STATISTICS")
    print("="*70)
    print(f"Total Interrupts Handled: {stats['interrupts_handled']}")
    print(f"Pending Interrupts: {stats['pending_interrupts']}")
    print(f"Interrupts Enabled: {stats['interrupt_enabled']}")
    print("="*70)
    
    return handler, results


if __name__ == "__main__":
    simulate_computation_with_interrupts()
