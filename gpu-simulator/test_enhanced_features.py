"""
Test script for enhanced simulation features
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.pdf_service import PDFExportService
from app.optimization_service import OptimizationService
import base64


def test_pdf_service():
    """Test PDF generation"""
    print("Testing PDF Export Service...")
    
    service = PDFExportService()
    
    # Mock simulation data
    simulation_data = {
        'dataset_size': 50000,
        'operation': 'vector_add',
        'cpu_execution_time': 0.125,
        'gpu_execution_time': 0.025,
        'speedup_ratio': 5.0,
        'efficiency_percentage': 62.5,
        'throughput': 2000000,
        'thread_block_info': {
            'num_blocks': 8,
            'block_size': 6250,
            'total_elements': 50000
        }
    }
    
    # Mock chart images (empty for now)
    chart_images = {
        'time_chart': '',
        'speedup_chart': ''
    }
    
    # Mock console logs
    console_logs = [
        '[12:00:00] System ready',
        '[12:00:05] Dataset initialized: 50,000 elements',
        '[12:00:10] CPU simulation completed in 0.125s',
        '[12:00:15] GPU simulation completed in 0.025s',
        '[12:00:16] Speedup: 5.0x'
    ]
    
    try:
        pdf_bytes = service.generate_report(
            simulation_data=simulation_data,
            chart_images=chart_images,
            thread_viz_image='',
            console_logs=console_logs
        )
        
        print(f"✓ PDF generated successfully: {len(pdf_bytes)} bytes")
        
        # Save to file for inspection
        with open('test_report.pdf', 'wb') as f:
            f.write(pdf_bytes)
        print("✓ PDF saved to test_report.pdf")
        
        return True
    except Exception as e:
        print(f"✗ PDF generation failed: {e}")
        return False


def test_optimization_service():
    """Test optimization service"""
    print("\nTesting Optimization Service...")
    
    service = OptimizationService()
    
    try:
        suggestions = service.get_optimization_suggestions()
        
        print(f"✓ CPU Cores: {suggestions['cpu_cores']}")
        print(f"✓ Available Memory: {suggestions['available_memory_gb']}GB")
        print(f"✓ Recommended Processes: {suggestions['recommended_processes']}")
        print(f"✓ Recommended Dataset Size: {suggestions['recommended_dataset_size']:,}")
        
        return True
    except Exception as e:
        print(f"✗ Optimization service failed: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Enhanced Simulation Features Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("PDF Service", test_pdf_service()))
    results.append(("Optimization Service", test_optimization_service()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed!"))
