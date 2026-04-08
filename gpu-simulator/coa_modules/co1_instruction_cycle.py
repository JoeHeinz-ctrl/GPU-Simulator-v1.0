"""
CO1: Instruction Cycle Simulation
Demonstrates: Fetch-Decode-Execute cycle for floating-point operations

This module simulates the basic instruction cycle that occurs in a CPU:
1. FETCH: Retrieve instruction from memory
2. DECODE: Interpret the instruction
3. EXECUTE: Perform the operation
"""

import time
from typing import List, Tuple, Any
from dataclasses import dataclass


@dataclass
class Instruction:
    """Represents a single instruction"""
    opcode: str  # Operation code (ADD, MUL, SUB, DIV)
    operand1: float  # First operand
    operand2: float  # Second operand
    result: float = 0.0  # Result after execution


class InstructionCycleSimulator:
    """
    Simulates the instruction cycle for floating-point operations
    
    COA Concept Mapping:
    - Program Counter (PC): Tracks current instruction
    - Instruction Register (IR): Holds current instruction
    - Arithmetic Logic Unit (ALU): Performs operations
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.program_counter = 0
        self.instruction_register = None
        self.instructions: List[Instruction] = []
        self.execution_log = []
    
    def load_program(self, instructions: List[Instruction]):
        """Load instructions into instruction memory"""
        self.instructions = instructions
        self.program_counter = 0
        if self.verbose:
            print(f"\n{'='*60}")
            print("CO1: INSTRUCTION CYCLE SIMULATION")
            print(f"{'='*60}")
            print(f"✓ Loaded {len(instructions)} instructions into memory")
            print(f"{'='*60}\n")
    
    def fetch(self) -> Instruction:
        """
        FETCH Stage: Retrieve instruction from memory
        
        COA Concept:
        - PC (Program Counter) points to next instruction
        - Instruction is loaded into IR (Instruction Register)
        """
        if self.program_counter >= len(self.instructions):
            raise IndexError("Program Counter exceeded instruction memory")
        
        instruction = self.instructions[self.program_counter]
        self.instruction_register = instruction
        
        if self.verbose:
            print(f"[FETCH] PC={self.program_counter}")
            print(f"        Fetching instruction from memory address {self.program_counter}")
            print(f"        IR ← Memory[{self.program_counter}]")
        
        time.sleep(0.1)  # Simulate fetch delay
        return instruction
    
    def decode(self, instruction: Instruction) -> Tuple[str, float, float]:
        """
        DECODE Stage: Interpret the instruction
        
        COA Concept:
        - Control Unit decodes the opcode
        - Identifies operation type and operands
        - Prepares ALU for execution
        """
        opcode = instruction.opcode
        operand1 = instruction.operand1
        operand2 = instruction.operand2
        
        if self.verbose:
            print(f"[DECODE] Opcode: {opcode}")
            print(f"         Operand1: {operand1}")
            print(f"         Operand2: {operand2}")
            print(f"         Control Unit → ALU: Prepare for {opcode} operation")
        
        time.sleep(0.1)  # Simulate decode delay
        return opcode, operand1, operand2
    
    def execute(self, opcode: str, operand1: float, operand2: float) -> float:
        """
        EXECUTE Stage: Perform the operation in ALU
        
        COA Concept:
        - ALU (Arithmetic Logic Unit) performs computation
        - Result is stored in accumulator/register
        """
        if self.verbose:
            print(f"[EXECUTE] ALU performing {opcode} operation")
        
        # Simulate ALU operations
        if opcode == "ADD":
            result = operand1 + operand2
            operation_str = f"{operand1} + {operand2}"
        elif opcode == "MUL":
            result = operand1 * operand2
            operation_str = f"{operand1} × {operand2}"
        elif opcode == "SUB":
            result = operand1 - operand2
            operation_str = f"{operand1} - {operand2}"
        elif opcode == "DIV":
            result = operand1 / operand2 if operand2 != 0 else 0
            operation_str = f"{operand1} ÷ {operand2}"
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        if self.verbose:
            print(f"          {operation_str} = {result}")
            print(f"          Result stored in accumulator")
        
        time.sleep(0.1)  # Simulate execution delay
        return result
    
    def run_instruction_cycle(self, instruction: Instruction) -> float:
        """
        Complete instruction cycle: Fetch → Decode → Execute
        
        This is the fundamental cycle that repeats for every instruction
        """
        if self.verbose:
            print(f"\n{'─'*60}")
            print(f"Instruction {self.program_counter + 1}: {instruction.opcode} {instruction.operand1}, {instruction.operand2}")
            print(f"{'─'*60}")
        
        # Stage 1: FETCH
        fetched_instruction = self.fetch()
        
        # Stage 2: DECODE
        opcode, op1, op2 = self.decode(fetched_instruction)
        
        # Stage 3: EXECUTE
        result = self.execute(opcode, op1, op2)
        
        # Update instruction with result
        instruction.result = result
        
        # Increment Program Counter
        self.program_counter += 1
        
        if self.verbose:
            print(f"[UPDATE] PC ← PC + 1 (PC = {self.program_counter})")
            print(f"         Final Result: {result}")
        
        # Log execution
        self.execution_log.append({
            'instruction': f"{opcode} {op1}, {op2}",
            'result': result,
            'pc': self.program_counter - 1
        })
        
        return result
    
    def run_program(self) -> List[float]:
        """Execute all instructions in the program"""
        results = []
        
        while self.program_counter < len(self.instructions):
            instruction = self.instructions[self.program_counter]
            result = self.run_instruction_cycle(instruction)
            results.append(result)
        
        if self.verbose:
            print(f"\n{'='*60}")
            print("PROGRAM EXECUTION COMPLETE")
            print(f"{'='*60}")
            print(f"Total instructions executed: {len(results)}")
            print(f"Final PC value: {self.program_counter}")
            print(f"{'='*60}\n")
        
        return results
    
    def get_execution_summary(self) -> dict:
        """Get summary of instruction execution"""
        return {
            'total_instructions': len(self.instructions),
            'instructions_executed': self.program_counter,
            'execution_log': self.execution_log
        }


def demonstrate_instruction_cycle():
    """
    Demonstration function for CO1
    Shows instruction cycle for floating-point operations
    """
    print("\n" + "="*70)
    print("CO1 DEMONSTRATION: INSTRUCTION CYCLE SIMULATION")
    print("="*70)
    print("\nCOA Concepts Demonstrated:")
    print("• Fetch-Decode-Execute Cycle")
    print("• Program Counter (PC)")
    print("• Instruction Register (IR)")
    print("• Arithmetic Logic Unit (ALU)")
    print("• Control Unit")
    print("="*70)
    
    # Create sample program
    program = [
        Instruction("ADD", 10.5, 20.3),
        Instruction("MUL", 5.0, 3.0),
        Instruction("SUB", 100.0, 25.5),
        Instruction("DIV", 50.0, 2.0),
        Instruction("ADD", 15.5, 15.5),
    ]
    
    # Create simulator
    simulator = InstructionCycleSimulator(verbose=True)
    
    # Load and run program
    simulator.load_program(program)
    results = simulator.run_program()
    
    # Display results
    print("\n" + "="*70)
    print("EXECUTION RESULTS")
    print("="*70)
    for i, (instruction, result) in enumerate(zip(program, results)):
        print(f"Instruction {i+1}: {instruction.opcode} {instruction.operand1}, {instruction.operand2} → {result}")
    print("="*70)
    
    return simulator, results


if __name__ == "__main__":
    demonstrate_instruction_cycle()
