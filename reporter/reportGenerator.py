from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime
import pandas as pd

class DynamicReport:
    def __init__(self, level: str, author="Analyst", data_source=""):
        self.level = level.upper()
        self.author = author
        self.data_source = data_source
        self.styles = getSampleStyleSheet()
        self._init_styles()

    def _init_styles(self):
        self.title_style = ParagraphStyle(
            name="Title", parent=self.styles['Heading1'], alignment=TA_CENTER
        )
        self.centered_h2 = ParagraphStyle(
            name="CenteredHeading2", parent=self.styles['Heading2'], alignment=TA_CENTER
        )
        self.normal_center = ParagraphStyle(
            name="NormalCenter", parent=self.styles["Normal"], alignment=TA_CENTER
        )

    def _add_title_page(self):
        """Create the title page of the report."""
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name='TitleStyle', parent=styles['Title'], alignment=1)
        info_style = ParagraphStyle(name='InfoStyle', parent=styles['Normal'], alignment=1)

        story = []
        story.append(Spacer(1, 100))
        story.append(Paragraph("Sales Data Analysis Report - Online Retail", title_style))
        story.append(Spacer(1, 40))
        story.append(Paragraph(f"Author: {self.author}", info_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Date Generated: {datetime.today().strftime('%B %d, %Y')}", info_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Data Source: UCI Machine Learning Repository", info_style))
        story.append(PageBreak())
        return story    

    def _cover_page(self):
        story = []
        story.append(Paragraph(f"{self.level} ANALYSIS", self.title_style))
        story.append(Spacer(1, 10))
        return story

    def _add_description(self, text):
        return [Paragraph("Dataset Description", self.styles["Heading2"]),
                Spacer(1, 6),
                Paragraph(text, self.styles["BodyText"]),
                Spacer(1, 10)]

    def _add_table(self, title, data, col_names, col_widths):
        story = [Paragraph(title, self.styles["Heading2"]), Spacer(1, 6)]

        # Wrap all cells in Paragraph
        wrapped_data = [[Paragraph(str(cell), self.styles["BodyText"]) for cell in row] for row in [col_names] + data]

        table = Table(wrapped_data, colWidths=col_widths, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))
        return story

    def _add_facts(self, facts):
        story = [Paragraph("Interesting Facts", self.styles["Heading2"]), Spacer(1, 6)]
        for key, value in facts.items():
            story.append(Paragraph(f"• {value}", self.styles["BodyText"]))
            story.append(Spacer(1, 6))
        story.append(PageBreak())    
        return story

    def _add_analysis_images(self, image_paths, max_count):
        story = []
        for i, (title, path) in enumerate(image_paths.items()):
            if i >= max_count:
                break
            story.append(Paragraph(title, self.centered_h2))
            story.append(Spacer(1, 6))
            story.append(Image(path, width=5.8 * inch, height=3.2 * inch))
            story.append(Spacer(1, 70))
        return story

    def generate(self, output_file, data):
        story = self._add_title_page()

        story += self._cover_page()

        # Common sections for all levels
        story += self._add_description(data["description"])

        col_desc_data = [[k, v] for k, v in data["columns_description"].items()]
        story += self._add_table("Column Descriptions", col_desc_data, ["Column", "Description"], [120, 380])

        col_types_data = [[k, v] for k, v in data["data_types"].items()]
        story += self._add_table("Data Types", col_types_data, ["Column", "Type"], [120, 120])

        story += self._add_facts(data["facts"])  # Always 2 for base

        # Add analysis images if Level-2 or Level-3
        plots_dict = {
        "Top 10 Countries By Revenue": "assets/top_10_countries_revenue.png",
         "Monthly Revenue Trend": "assets/monthly_revenue_trend.png",
         "Top Products By Quantity": "assets/top_10_products_quantity.png",
         "Monthly Revenue by Country": "assets/monthly_revenue_by_country.png",
         "Correlation Matrix": "assets/correlation_matrix.png",
         "Quantity KDE Curvre": "assets/quantity_kde_curve.png",
         "Revenue Box Plot": "assets/revenue_boxplot.png"
        }
        image_paths = data.get("plots", plots_dict)  # Dict: {"Title": "path/to/img"}
        if self.level == "LEVEL-2":
            story += self._add_analysis_images(image_paths, max_count=3)
        elif self.level == "LEVEL-3":
            story += self._add_analysis_images(image_paths, max_count=7)

        doc = SimpleDocTemplate(output_file, pagesize=A4)
        doc.build(story)