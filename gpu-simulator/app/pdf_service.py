"""
PDF Export Service for GPU Quantum Compute Simulator
Generates professional technical reports with performance metrics and visualizations
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage
)
from io import BytesIO
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from PIL import Image as PILImage


class PDFExportService:
    """Service for generating PDF reports from simulation data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#76B900'),
            spaceAfter=30,
            alignment=1
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#00D4FF'),
            spaceBefore=20,
            spaceAfter=12
        ))
    
    def generate_report(
        self,
        simulation_data: Dict[str, Any],
        chart_images: Dict[str, str],
        thread_viz_image: str,
        console_logs: List[str],
        report_title: str = "GPU Quantum Compute Simulation Report"
    ) -> bytes:
        """Generate complete PDF report"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        story.extend(self._render_cover_page(report_title))
        story.append(PageBreak())
        story.extend(self._render_performance_section(simulation_data))
        story.append(Spacer(1, 0.3 * inch))
        story.extend(self._render_charts_section(chart_images))
        story.append(PageBreak())
        story.extend(self._render_execution_logs(console_logs))
        
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    
    def _render_cover_page(self, title: str) -> List:
        """Generate cover page"""
        elements = []
        elements.append(Spacer(1, 2 * inch))
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("Professional Performance Analysis Report", self.styles['Heading3']))
        elements.append(Spacer(1, 1 * inch))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"<b>Generated:</b> {timestamp}", self.styles['Normal']))
        return elements
    
    def _render_performance_section(self, metrics: Dict[str, Any]) -> List:
        """Render performance metrics table"""
        elements = []
        elements.append(Paragraph("Performance Metrics Summary", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2 * inch))
        
        table_data = [
            ['Metric', 'Value'],
            ['Dataset Size', f"{metrics.get('dataset_size', 0):,} elements"],
            ['Operation', metrics.get('operation', 'N/A')],
            ['CPU Time', f"{metrics.get('cpu_execution_time', 0):.4f}s"],
            ['GPU Time', f"{metrics.get('gpu_execution_time', 0):.4f}s"],
            ['Speedup', f"{metrics.get('speedup_ratio', 0):.2f}x"],
            ['Throughput', f"{metrics.get('throughput', 0):,} ops/s"]
        ]
        
        table = Table(table_data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#76B900')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        return elements
    
    def _render_charts_section(self, chart_images: Dict[str, str]) -> List:
        """Render charts from base64 images"""
        elements = []
        elements.append(Paragraph("Performance Visualizations", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2 * inch))
        
        for chart_name, base64_data in chart_images.items():
            if not base64_data:
                continue
            try:
                image_data = self._decode_base64_image(base64_data)
                if image_data:
                    chart_title = chart_name.replace('_', ' ').title()
                    elements.append(Paragraph(f"<b>{chart_title}</b>", self.styles['Heading4']))
                    elements.append(Spacer(1, 0.1 * inch))
                    img = RLImage(image_data, width=5.5 * inch, height=3.5 * inch)
                    elements.append(img)
                    elements.append(Spacer(1, 0.3 * inch))
            except Exception as e:
                elements.append(Paragraph(f"<i>Chart error: {str(e)}</i>", self.styles['Normal']))
        return elements
    
    def _render_execution_logs(self, logs: List[str]) -> List:
        """Render console logs"""
        elements = []
        elements.append(Paragraph("Execution Console Logs", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2 * inch))
        
        if logs:
            display_logs = logs[-30:] if len(logs) > 30 else logs
            for log in display_logs:
                sanitized = self._sanitize_text(log)
                elements.append(Paragraph(sanitized, self.styles['Code']))
                elements.append(Spacer(1, 0.05 * inch))
        else:
            elements.append(Paragraph("<i>No logs available</i>", self.styles['Normal']))
        return elements
    
    def _decode_base64_image(self, base64_string: str) -> Optional[BytesIO]:
        """Decode base64 to image"""
        try:
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            image_bytes = base64.b64decode(base64_string)
            pil_image = PILImage.open(BytesIO(image_bytes))
            if pil_image.mode in ('RGBA', 'LA', 'P'):
                pil_image = pil_image.convert('RGB')
            output = BytesIO()
            pil_image.save(output, format='PNG')
            output.seek(0)
            return output
        except:
            return None
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    def _add_page_number(self, canvas_obj, doc):
        """Add page numbers"""
        page_num = canvas_obj.getPageNumber()
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.drawRightString(letter[0] - 72, 0.5 * inch, f"Page {page_num}")
        canvas_obj.restoreState()
