from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListItem, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from typing import Dict, Any

def create_pitch_deck_pdf(pitch_deck_data: Dict[str, Any]) -> bytes:
    """Create a PDF from the pitch deck data."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_LEFT
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )
    
    # Build the PDF content
    story = []
    
    # Title Slide
    story.append(Paragraph(pitch_deck_data['title_slide']['company_name'], title_style))
    story.append(Paragraph(pitch_deck_data['title_slide']['tagline'], content_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Logo: {pitch_deck_data['title_slide']['logo_description']}", content_style))
    story.append(Spacer(1, 30))
    
    # Problem Slide
    story.append(Paragraph("Problem", slide_title_style))
    story.append(Paragraph(pitch_deck_data['problem_slide']['main_problem'], content_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Key Pain Points:", content_style))
    pain_points = [ListItem(Paragraph(point, content_style)) for point in pitch_deck_data['problem_slide']['key_pain_points']]
    story.append(ListFlowable(pain_points, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Current Solutions:", content_style))
    solutions = [ListItem(Paragraph(solution, content_style)) for solution in pitch_deck_data['problem_slide']['current_solutions']]
    story.append(ListFlowable(solutions, bulletType='bullet'))
    story.append(Spacer(1, 30))
    
    # Solution Slide
    story.append(Paragraph("Solution", slide_title_style))
    story.append(Paragraph(pitch_deck_data['solution_slide']['main_solution'], content_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Key Features:", content_style))
    features = [ListItem(Paragraph(feature, content_style)) for feature in pitch_deck_data['solution_slide']['key_features']]
    story.append(ListFlowable(features, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(f"Unique Value: {pitch_deck_data['solution_slide']['unique_value']}", content_style))
    story.append(Spacer(1, 30))
    
    # Market Slide
    story.append(Paragraph("Market", slide_title_style))
    story.append(Paragraph(f"Target Market: {pitch_deck_data['market_slide']['target_market']}", content_style))
    story.append(Paragraph(f"Market Size: {pitch_deck_data['market_slide']['market_size']}", content_style))
    story.append(Paragraph(f"Growth Potential: {pitch_deck_data['market_slide']['growth_potential']}", content_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Market Trends:", content_style))
    trends = [ListItem(Paragraph(trend, content_style)) for trend in pitch_deck_data['market_slide']['market_trends']]
    story.append(ListFlowable(trends, bulletType='bullet'))
    story.append(Spacer(1, 30))
    
    # Business Model Slide
    story.append(Paragraph("Business Model", slide_title_style))
    story.append(Paragraph(f"Revenue Model: {pitch_deck_data['business_model_slide']['revenue_model']}", content_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Key Metrics:", content_style))
    metrics = [ListItem(Paragraph(metric, content_style)) for metric in pitch_deck_data['business_model_slide']['key_metrics']]
    story.append(ListFlowable(metrics, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Cost Structure:", content_style))
    costs = [ListItem(Paragraph(cost, content_style)) for cost in pitch_deck_data['business_model_slide']['cost_structure']]
    story.append(ListFlowable(costs, bulletType='bullet'))
    story.append(Spacer(1, 30))
    
    # Go-to-Market Slide
    story.append(Paragraph("Go-to-Market Strategy", slide_title_style))
    story.append(Paragraph(f"Strategy: {pitch_deck_data['go_to_market_slide']['strategy']}", content_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Channels:", content_style))
    channels = [ListItem(Paragraph(channel, content_style)) for channel in pitch_deck_data['go_to_market_slide']['channels']]
    story.append(ListFlowable(channels, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Timeline:", content_style))
    timeline = [ListItem(Paragraph(milestone, content_style)) for milestone in pitch_deck_data['go_to_market_slide']['timeline']]
    story.append(ListFlowable(timeline, bulletType='bullet'))
    story.append(Spacer(1, 30))
    
    # Team Slide
    story.append(Paragraph("Team", slide_title_style))
    story.append(Paragraph("Key Roles:", content_style))
    roles = [ListItem(Paragraph(role, content_style)) for role in pitch_deck_data['team_slide']['key_roles']]
    story.append(ListFlowable(roles, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Team Strengths:", content_style))
    strengths = [ListItem(Paragraph(strength, content_style)) for strength in pitch_deck_data['team_slide']['team_strengths']]
    story.append(ListFlowable(strengths, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Hiring Plan:", content_style))
    hiring = [ListItem(Paragraph(hire, content_style)) for hire in pitch_deck_data['team_slide']['hiring_plan']]
    story.append(ListFlowable(hiring, bulletType='bullet'))
    story.append(Spacer(1, 30))
    
    # Financials Slide
    story.append(Paragraph("Financials", slide_title_style))
    story.append(Paragraph(f"Funding Needed: {pitch_deck_data['financials_slide']['funding_needed']}", content_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Use of Funds:", content_style))
    uses = [ListItem(Paragraph(use, content_style)) for use in pitch_deck_data['financials_slide']['use_of_funds']]
    story.append(ListFlowable(uses, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Financial Projections:", content_style))
    projections = [ListItem(Paragraph(projection, content_style)) for projection in pitch_deck_data['financials_slide']['financial_projections']]
    story.append(ListFlowable(projections, bulletType='bullet'))
    story.append(Spacer(1, 30))
    
    # Call to Action
    story.append(Paragraph("Call to Action", slide_title_style))
    story.append(Paragraph("Next Steps:", content_style))
    steps = [ListItem(Paragraph(step, content_style)) for step in pitch_deck_data['call_to_action']['next_steps']]
    story.append(ListFlowable(steps, bulletType='bullet'))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(f"Contact Info: {pitch_deck_data['call_to_action']['contact_info']}", content_style))
    story.append(Paragraph(f"Investment Terms: {pitch_deck_data['call_to_action']['investment_terms']}", content_style))
    
    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue() 