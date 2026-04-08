"""
CO1: Instruction Cycle Simulation Module
Demonstrates Fetch-Decode-Execute cycle for educational purposes
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum
import time


class InstructionType(Enum):
    """Supported instruction types"""
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    LOAD = "LOAD"
    STORE = "STORE"


@dataclass
class Instruction:
    """Represents a single instruction"""
    opcode: str
    operand1: float
    operand2: float = 0.0
    
    def __str__(self):
        return f"{self.opcode} {self.operand1}, {self.operand2}"


class InstructionCycleSimulator:
    """
    Simulates the instruction cycle: Fetch → Decode → Execute
    Educational implementation for demonstrating CPU instruction processing
    """
    
    def __init__(self):
        self.pc = 0  # Program Counter
        self.ir = None  # Instruction Register
        self.accumulator = 0.0  # Accumulator register
        self.memory = []  # Instruction memory
        self.execution_log = []  # Log of execution steps
        
    def load_program(self, instructions: List[Instruction]):
        """Load instructions into memory"""
        self.memory = instructions
        self.pc = 0
        self.accumulator = 0.0
        self.execution_log = []
        
    def fetch(self) -> Dict[str, Any]:
        """
        FETCH stage: Retrieve instruction from memory
        Returns: Step information for UI display
        """
        if self.pc >= len(self.memory):
            return {
                "stage": "FETCH",
                "status": "complete",
                "message": "Program execution complete",
                "pc": self.pc
            }
        
        self.ir = self.memory[self.pc]
        
        return {
            "stage": "FETCH",
            "status": "success",
            "message": f"Fetched instruction from memory address {self.pc}",
            "pc": self.pc,
            "instruction": str(self.ir),
            "details": {
                "memory_address": self.pc,
                "instruction_register": str(self.ir)
            }
        }
    
    def decode(self) -> Dict[str, Any]:
        """
        DECODE stage: Interpret the instruction
        Returns: Step information for UI display
        """
        if self.ir is None:
            return {
                "stage": "DECODE",
                "status": "error",
                "message": "No instruction to decode"
            }
        
        return {
            "stage": "DECODE",
            "status": "success",
            "message": f"Decoded instruction: {self.ir.opcode}",
            "opcode": self.ir.opcode,
            "operand1": self.ir.operand1,
            "operand2": self.ir.operand2,
            "details": {
                "operation": self.ir.opcode,
                "source_operand_1": self.ir.operand1,
                "source_operand_2": self.ir.operand2,
                "control_signals": f"ALU_OP={self.ir.opcode}, ENABLE=1"
            }
        }
    
    def execute(self) -> Dict[str, Any]:
        """
        EXECUTE stage: Perform the operation
        Returns: Step information for UI display
        """
        if self.ir is None:
            return {
                "stage": "EXECUTE",
                "status": "error",
                "message": "No instruction to execute"
            }
        
        result = 0.0
        operation_desc = ""
        
        # Perform ALU operation
        if self.ir.opcode == "ADD":
            result = self.ir.operand1 + self.ir.operand2
            operation_desc = f"{self.ir.operand1} + {self.ir.operand2} = {result}"
        elif self.ir.opcode == "SUB":
            result = self.ir.operand1 - self.ir.operand2
            operation_desc = f"{self.ir.operand1} - {self.ir.operand2} = {result}"
        elif self.ir.opcode == "MUL":
            result = self.ir.operand1 * self.ir.operand2
            operation_desc = f"{self.ir.operand1} × {self.ir.operand2} = {result}"
        elif self.ir.opcode == "DIV":
            if self.ir.operand2 != 0:
                result = self.ir.operand1 / self.ir.operand2
                operation_desc = f"{self.ir.operand1} ÷ {self.ir.operand2} = {result}"
            else:
                return {
                    "stage": "EXECUTE",
                    "status": "error",
                    "message": "Division by zero error"
                }
        else:
            return {
                "stage": "EXECUTE",
                "status": "error",
                "message": f"Unknown opcode: {self.ir.opcode}"
            }
        
        self.accumulator = result
        self.pc += 1  # Increment program counter
        
        return {
            "stage": "EXECUTE",
            "status": "success",
            "message": f"Executed {self.ir.opcode} operation",
            "result": result,
            "accumulator": self.accumulator,
            "pc": self.pc,
            "details": {
                "alu_operation": operation_desc,
                "result_stored": f"Accumulator = {result}",
                "program_counter": f"PC incremented to {self.pc}"
            }
        }
    
    def execute_single_instruction(self) -> List[Dict[str, Any]]:
        """
        Execute one complete instruction cycle (Fetch → Decode → Execute)
        Returns: List of all three stages for UI animation
        """
        steps = []
        
        # Fetch
        fetch_result = self.fetch()
        steps.append(fetch_result)
        
        if fetch_result["status"] == "complete":
            return steps
        
        # Small delay for visualization
        time.sleep(0.1)
        
        # Decode
        decode_result = self.decode()
        steps.append(decode_result)
        
        time.sleep(0.1)
        
        # Execute
        execute_result = self.execute()
        steps.append(execute_result)
        
        return steps
    
    def run_program(self) -> Dict[str, Any]:
        """
        Execute entire program and return complete execution log
        Returns: Complete execution trace for UI display
        """
        self.execution_log = []
        instruction_count = 0
        
        while self.pc < len(self.memory):
            instruction_steps = self.execute_single_instruction()
            self.execution_log.extend(instruction_steps)
            instruction_count += 1
            
            # Safety check
            if instruction_count > 1000:
                break
        
        return {
            "success": True,
            "total_instructions": instruction_count,
            "final_pc": self.pc,
            "final_accumulator": self.accumulator,
            "execution_log": self.execution_log
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current CPU state"""
        return {
            "program_counter": self.pc,
            "accumulator": self.accumulator,
            "instruction_register": str(self.ir) if self.ir else "Empty",
            "memory_size": len(self.memory)
        }


def create_sample_program() -> List[Instruction]:
    """Create a sample program for demonstration"""
    return [
        Instruction("ADD", 10.0, 5.0),
        Instruction("MUL", 3.0, 4.0),
        Instruction("SUB", 20.0, 8.0),
        Instruction("DIV", 100.0, 4.0),
        Instruction("ADD", 15.5, 24.5),
    ]
