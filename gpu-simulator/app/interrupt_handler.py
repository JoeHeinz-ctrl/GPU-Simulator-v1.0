"""
CO3: Interrupt Handling Module
Demonstrates interrupt processing and context switching
"""

from dataclasses import dataclass
from typing import Dict, Any, Callable, Optional
from enum import Enum
import time
import asyncio


class InterruptType(Enum):
    """Types of interrupts"""
    TIMER = "TIMER"
    IO_COMPLETE = "IO_COMPLETE"
    USER_TRIGGERED = "USER_TRIGGERED"
    ERROR = "ERROR"


@dataclass
class InterruptRequest:
    """Represents an interrupt request"""
    interrupt_type: InterruptType
    priority: int
    timestamp: float
    data: Optional[Dict[str, Any]] = None


class InterruptHandler:
    """
    Simulates interrupt handling mechanism
    Demonstrates: Interrupt detection, context switching, ISR execution
    """
    
    def __init__(self):
        self.interrupt_queue = []
        self.interrupt_enabled = True
        self.current_context = None
        self.interrupt_count = 0
        self.isr_handlers = {}
        self.execution_log = []
        
    def register_isr(self, interrupt_type: InterruptType, handler: Callable):
        """Register an Interrupt Service Routine (ISR)"""
        self.isr_handlers[interrupt_type] = handler
        
    def trigger_interrupt(self, interrupt_type: InterruptType, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Trigger an interrupt
        Returns: Interrupt trigger information
        """
        if not self.interrupt_enabled:
            return {
                "success": False,
                "message": "Interrupts are disabled",
                "interrupt_type": interrupt_type.value
            }
        
        interrupt_req = InterruptRequest(
            interrupt_type=interrupt_type,
            priority=self._get_priority(interrupt_type),
            timestamp=time.time(),
            data=data
        )
        
        self.interrupt_queue.append(interrupt_req)
        self.interrupt_count += 1
        
        return {
            "success": True,
            "message": f"Interrupt {interrupt_type.value} triggered",
            "interrupt_type": interrupt_type.value,
            "priority": interrupt_req.priority,
            "queue_size": len(self.interrupt_queue)
        }
    
    def _get_priority(self, interrupt_type: InterruptType) -> int:
        """Get interrupt priority (lower number = higher priority)"""
        priorities = {
            InterruptType.ERROR: 1,
            InterruptType.TIMER: 2,
            InterruptType.IO_COMPLETE: 3,
            InterruptType.USER_TRIGGERED: 4
        }
        return priorities.get(interrupt_type, 5)
    
    async def handle_interrupt(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle pending interrupt with full context switching
        Returns: Complete interrupt handling trace
        """
        if not self.interrupt_queue:
            return {
                "success": False,
                "message": "No pending interrupts"
            }
        
        # Sort by priority
        self.interrupt_queue.sort(key=lambda x: x.priority)
        interrupt_req = self.interrupt_queue.pop(0)
        
        handling_log = []
        
        # Step 1: Save current context
        handling_log.append({
            "step": "SAVE_CONTEXT",
            "message": "Saving current execution context",
            "saved_state": {
                "pc": current_state.get("pc", 0),
                "accumulator": current_state.get("accumulator", 0.0),
                "registers": current_state.get("registers", {})
            }
        })
        
        self.current_context = current_state.copy()
        await asyncio.sleep(0.1)  # Simulate context save time
        
        # Step 2: Disable interrupts (prevent nested interrupts)
        handling_log.append({
            "step": "DISABLE_INTERRUPTS",
            "message": "Interrupts disabled during ISR execution"
        })
        
        self.interrupt_enabled = False
        await asyncio.sleep(0.05)
        
        # Step 3: Execute ISR
        isr_result = None
        if interrupt_req.interrupt_type in self.isr_handlers:
            handling_log.append({
                "step": "EXECUTE_ISR",
                "message": f"Executing ISR for {interrupt_req.interrupt_type.value}",
                "interrupt_type": interrupt_req.interrupt_type.value
            })
            
            await asyncio.sleep(0.2)  # Simulate ISR execution time
            
            # Call the registered ISR
            isr_handler = self.isr_handlers[interrupt_req.interrupt_type]
            isr_result = isr_handler(interrupt_req.data)
            
            handling_log.append({
                "step": "ISR_COMPLETE",
                "message": f"ISR completed successfully",
                "result": isr_result
            })
        else:
            handling_log.append({
                "step": "ISR_ERROR",
                "message": f"No ISR registered for {interrupt_req.interrupt_type.value}"
            })
        
        await asyncio.sleep(0.05)
        
        # Step 4: Restore context
        handling_log.append({
            "step": "RESTORE_CONTEXT",
            "message": "Restoring previous execution context",
            "restored_state": self.current_context
        })
        
        await asyncio.sleep(0.1)
        
        # Step 5: Re-enable interrupts
        handling_log.append({
            "step": "ENABLE_INTERRUPTS",
            "message": "Interrupts re-enabled, resuming normal execution"
        })
        
        self.interrupt_enabled = True
        
        return {
            "success": True,
            "interrupt_type": interrupt_req.interrupt_type.value,
            "priority": interrupt_req.priority,
            "handling_log": handling_log,
            "isr_result": isr_result,
            "context_restored": True
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current interrupt handler status"""
        return {
            "interrupts_enabled": self.interrupt_enabled,
            "pending_interrupts": len(self.interrupt_queue),
            "total_interrupts_handled": self.interrupt_count,
            "registered_isrs": [itype.value for itype in self.isr_handlers.keys()]
        }
    
    def clear_interrupts(self):
        """Clear all pending interrupts"""
        self.interrupt_queue.clear()


# Sample ISR handlers for demonstration
def timer_isr(data: Optional[Dict]) -> str:
    """Sample Timer ISR"""
    return "Timer interrupt handled - System time updated"


def io_complete_isr(data: Optional[Dict]) -> str:
    """Sample I/O Complete ISR"""
    device = data.get("device", "unknown") if data else "unknown"
    return f"I/O operation completed on device: {device}"


def user_triggered_isr(data: Optional[Dict]) -> str:
    """Sample User-Triggered ISR"""
    return "User-triggered interrupt processed"


def error_isr(data: Optional[Dict]) -> str:
    """Sample Error ISR"""
    error_msg = data.get("error", "Unknown error") if data else "Unknown error"
    return f"Error handled: {error_msg}"
