from langchain.chat_models import ChatOpenAI
from typing import Dict, Any, List
import json

def calculate_burn_rate(capital: float, monthly_expenses: float) -> Dict[str, Any]:
    """Calculate burn rate and runway based on capital and monthly expenses."""
    llm = ChatOpenAI(temperature=0)
    
    # Define the function schema
    function_schema = {
        "name": "calculate_burn_rate",
        "description": "Calculate burn rate and runway for a startup",
        "parameters": {
            "type": "object",
            "properties": {
                "runway_months": {
                    "type": "number",
                    "description": "Number of months the startup can operate with current capital"
                },
                "burn_rate": {
                    "type": "number",
                    "description": "Monthly burn rate in currency units"
                },
                "warning_level": {
                    "type": "string",
                    "enum": ["critical", "warning", "healthy"],
                    "description": "Warning level based on runway"
                },
                "recommendation": {
                    "type": "string",
                    "description": "Recommendation based on the calculation"
                }
            },
            "required": ["runway_months", "burn_rate", "warning_level", "recommendation"]
        }
    }
    
    # Create the prompt
    prompt = f"""Calculate the burn rate and runway for a startup with:
    - Capital: ${capital:,.2f}
    - Monthly Expenses: ${monthly_expenses:,.2f}
    
    Consider:
    - Runway should be calculated as capital divided by monthly expenses
    - Warning levels:
      * critical: < 3 months
      * warning: 3-6 months
      * healthy: > 6 months
    - Provide a recommendation based on the warning level
    
    Return the result as a JSON object with the following structure:
    {json.dumps(function_schema['parameters']['properties'], indent=2)}
    """
    
    # Get the response
    response = llm.invoke(prompt)
    
    try:
        # Parse the response as JSON
        result = json.loads(response.content)
        
        # Handle potential nested dictionary
        if isinstance(result, dict) and 'result' in result:
            result = result['result']
        
        # Ensure all numeric values are floats
        if isinstance(result['runway_months'], (int, float)):
            result['runway_months'] = float(result['runway_months'])
        else:
            raise ValueError("Invalid runway_months value")
            
        if isinstance(result['burn_rate'], (int, float)):
            result['burn_rate'] = float(result['burn_rate'])
        else:
            raise ValueError("Invalid burn_rate value")
            
        return result
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Fallback calculation
        runway_months = round(capital / monthly_expenses, 1)
        warning_level = "critical" if runway_months < 3 else "warning" if runway_months < 6 else "healthy"
        recommendation = "Please recalculate with valid inputs."
        
        return {
            "runway_months": float(runway_months),
            "burn_rate": float(monthly_expenses),
            "warning_level": warning_level,
            "recommendation": recommendation
        }

def generate_business_model_canvas(problem: str, solution: str, target_group: str) -> Dict[str, Any]:
    """Generate a Business Model Canvas based on the problem, solution, and target group."""
    llm = ChatOpenAI(temperature=0.7)  # Increased temperature for more creative responses
    
    # Define the function schema
    function_schema = {
        "name": "generate_business_model_canvas",
        "description": "Generate a Business Model Canvas for a startup",
        "parameters": {
            "type": "object",
            "properties": {
                "key_partners": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key partners and suppliers needed to make the business model work"
                },
                "key_activities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key activities needed to create and deliver the value proposition"
                },
                "key_resources": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key resources needed to create and deliver the value proposition"
                },
                "value_proposition": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Products and services that create value for the target group"
                },
                "customer_relationships": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Types of relationships established with customers"
                },
                "channels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "How the value proposition is delivered to customers"
                },
                "customer_segments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Different groups of customers the business aims to reach"
                },
                "cost_structure": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Main costs incurred to operate the business model"
                },
                "revenue_streams": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Ways the business generates revenue"
                }
            },
            "required": [
                "key_partners", "key_activities", "key_resources", "value_proposition",
                "customer_relationships", "channels", "customer_segments",
                "cost_structure", "revenue_streams"
            ]
        }
    }
    
    # Create the prompt
    prompt = f"""You are a business model expert. Generate a detailed Business Model Canvas for a startup with the following information:

Problem Statement:
{problem}

Solution:
{solution}

Target Group:
{target_group}

Instructions:
1. Generate a comprehensive Business Model Canvas with specific, actionable items for each section
2. Each section should have 3-5 detailed points
3. Focus on practical, implementable aspects
4. Consider both immediate and future needs
5. Include both qualitative and quantitative elements where relevant
6. Ensure all sections are logically connected and support the overall business model

Return the result as a JSON object with the following structure:
{json.dumps(function_schema['parameters']['properties'], indent=2)}

Make sure to:
- Be specific and detailed in each section
- Provide concrete examples and actionable items
- Consider the unique aspects of the problem and solution
- Think about both short-term and long-term aspects
- Include both strategic and operational elements
"""
    
    # Get the response
    response = llm.invoke(prompt)
    
    try:
        # Parse the response as JSON
        result = json.loads(response.content)
        
        # Handle potential nested dictionary
        if isinstance(result, dict) and 'result' in result:
            result = result['result']
        
        # Validate that all required sections are present and are lists
        for section in function_schema['parameters']['required']:
            if section not in result or not isinstance(result[section], list):
                raise ValueError(f"Invalid or missing section: {section}")
            
            # Ensure each section has at least 2 items
            if len(result[section]) < 2:
                raise ValueError(f"Section {section} has insufficient items")
        
        return result
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error generating BMC: {str(e)}")
        print(f"Response content: {response.content}")
        
        # Return a more helpful template
        return {
            "key_partners": [
                "Technology partners for core solution components",
                "Local distribution and installation partners",
                "Maintenance and support service providers"
            ],
            "key_activities": [
                "Research and development of the core solution",
                "Installation and setup of the system",
                "Ongoing maintenance and support",
                "Customer training and education"
            ],
            "key_resources": [
                "Technical expertise and IP",
                "Manufacturing and supply chain",
                "Customer support team",
                "Installation and maintenance equipment"
            ],
            "value_proposition": [
                "Reliable and affordable solution to the core problem",
                "Easy to implement and maintain",
                "Scalable and adaptable to different needs",
                "Comprehensive support and training"
            ],
            "customer_relationships": [
                "Personal assistance and support",
                "Training and education programs",
                "Community building and knowledge sharing",
                "Regular maintenance and updates"
            ],
            "channels": [
                "Direct sales team",
                "Partner network",
                "Online platform",
                "Local service centers"
            ],
            "customer_segments": [
                "Primary target group as specified",
                "Secondary markets with similar needs",
                "Early adopters and innovators",
                "Strategic partners and resellers"
            ],
            "cost_structure": [
                "Research and development costs",
                "Manufacturing and supply chain",
                "Sales and marketing expenses",
                "Customer support and maintenance"
            ],
            "revenue_streams": [
                "Product sales and licensing",
                "Subscription and service fees",
                "Maintenance and support contracts",
                "Training and consulting services"
            ]
        }

def generate_pitch_deck(problem: str, solution: str, target_group: str, business_model: str = "", market_size: str = "", funding_needed: str = "") -> Dict[str, Any]:
    """Generate a pitch deck outline based on the business information."""
    llm = ChatOpenAI(temperature=0.7)
    
    # Define the function schema
    function_schema = {
        "name": "generate_pitch_deck",
        "description": "Generate a pitch deck outline for a startup",
        "parameters": {
            "type": "object",
            "properties": {
                "title_slide": {
                    "type": "object",
                    "properties": {
                        "company_name": {"type": "string"},
                        "tagline": {"type": "string"},
                        "logo_description": {"type": "string"}
                    },
                    "required": ["company_name", "tagline", "logo_description"]
                },
                "problem_slide": {
                    "type": "object",
                    "properties": {
                        "main_problem": {"type": "string"},
                        "key_pain_points": {"type": "array", "items": {"type": "string"}},
                        "current_solutions": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["main_problem", "key_pain_points", "current_solutions"]
                },
                "solution_slide": {
                    "type": "object",
                    "properties": {
                        "main_solution": {"type": "string"},
                        "key_features": {"type": "array", "items": {"type": "string"}},
                        "unique_value": {"type": "string"}
                    },
                    "required": ["main_solution", "key_features", "unique_value"]
                },
                "market_slide": {
                    "type": "object",
                    "properties": {
                        "target_market": {"type": "string"},
                        "market_size": {"type": "string"},
                        "growth_potential": {"type": "string"},
                        "market_trends": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["target_market", "market_size", "growth_potential", "market_trends"]
                },
                "business_model_slide": {
                    "type": "object",
                    "properties": {
                        "revenue_model": {"type": "string"},
                        "key_metrics": {"type": "array", "items": {"type": "string"}},
                        "cost_structure": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["revenue_model", "key_metrics", "cost_structure"]
                },
                "go_to_market_slide": {
                    "type": "object",
                    "properties": {
                        "strategy": {"type": "string"},
                        "channels": {"type": "array", "items": {"type": "string"}},
                        "timeline": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["strategy", "channels", "timeline"]
                },
                "team_slide": {
                    "type": "object",
                    "properties": {
                        "key_roles": {"type": "array", "items": {"type": "string"}},
                        "team_strengths": {"type": "array", "items": {"type": "string"}},
                        "hiring_plan": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["key_roles", "team_strengths", "hiring_plan"]
                },
                "financials_slide": {
                    "type": "object",
                    "properties": {
                        "funding_needed": {"type": "string"},
                        "use_of_funds": {"type": "array", "items": {"type": "string"}},
                        "financial_projections": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["funding_needed", "use_of_funds", "financial_projections"]
                },
                "call_to_action": {
                    "type": "object",
                    "properties": {
                        "next_steps": {"type": "array", "items": {"type": "string"}},
                        "contact_info": {"type": "string"},
                        "investment_terms": {"type": "string"}
                    },
                    "required": ["next_steps", "contact_info", "investment_terms"]
                }
            },
            "required": [
                "title_slide", "problem_slide", "solution_slide", "market_slide",
                "business_model_slide", "go_to_market_slide", "team_slide",
                "financials_slide", "call_to_action"
            ]
        }
    }
    
    # Create the prompt
    prompt = f"""You are a pitch deck expert. Generate a comprehensive pitch deck outline for a startup with the following information:

Problem Statement:
{problem}

Solution:
{solution}

Target Group:
{target_group}

Additional Information:
Business Model: {business_model if business_model else "Not specified"}
Market Size: {market_size if market_size else "Not specified"}
Funding Needed: {funding_needed if funding_needed else "Not specified"}

Instructions:
1. Generate a detailed pitch deck outline with 9 key slides
2. Each slide should have specific, actionable content
3. Focus on telling a compelling story
4. Include both qualitative and quantitative elements
5. Make the content specific to the business context
6. Ensure all slides are logically connected

Return the result as a JSON object with the following structure:
{json.dumps(function_schema['parameters']['properties'], indent=2)}

Make sure to:
- Create a memorable company name and tagline
- Highlight the most compelling aspects of the problem and solution
- Include specific market data and trends
- Provide clear, actionable next steps
- Make the pitch deck professional and investor-ready
- Include ALL required fields in the response
"""
    
    # Get the response
    response = llm.invoke(prompt)
    
    try:
        # Parse the response as JSON
        result = json.loads(response.content)
        
        # Handle potential nested dictionary
        if isinstance(result, dict) and 'result' in result:
            result = result['result']
        
        # Validate that all required sections are present and have required fields
        for section in function_schema['parameters']['required']:
            if section not in result:
                raise ValueError(f"Missing section: {section}")
            
            # Check required fields in each section
            section_schema = function_schema['parameters']['properties'][section]
            for field in section_schema['required']:
                if field not in result[section]:
                    raise ValueError(f"Missing field {field} in section {section}")
        
        return result
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error generating pitch deck: {str(e)}")
        print(f"Response content: {response.content}")
        
        # Generate a company name based on the solution
        words = solution.split()
        company_name = "".join(word.capitalize() for word in words[:2])
        
        # Return a template structure with all required fields
        return {
            "title_slide": {
                "company_name": company_name,
                "tagline": f"Solving {problem[:50]}...",
                "logo_description": "A modern, minimalist logo representing the solution"
            },
            "problem_slide": {
                "main_problem": problem,
                "key_pain_points": [
                    "Current solutions are too expensive",
                    "Existing options lack reliability",
                    "Complex infrastructure requirements"
                ],
                "current_solutions": [
                    "Traditional internet providers",
                    "Complex mesh networks",
                    "Expensive satellite solutions"
                ]
            },
            "solution_slide": {
                "main_solution": solution,
                "key_features": [
                    "Solar-powered operation",
                    "Easy installation",
                    "Simple management interface",
                    "Reliable connectivity"
                ],
                "unique_value": "Affordable, reliable internet access for businesses in developing regions"
            },
            "market_slide": {
                "target_market": target_group,
                "market_size": market_size or "Growing market in developing regions",
                "growth_potential": "High growth potential as digital adoption increases",
                "market_trends": [
                    "Increasing digital transformation",
                    "Growing demand for connectivity",
                    "Rising adoption of renewable energy"
                ]
            },
            "business_model_slide": {
                "revenue_model": business_model or "Hardware sales + subscription service",
                "key_metrics": [
                    "Number of installations",
                    "Monthly recurring revenue",
                    "Customer retention rate"
                ],
                "cost_structure": [
                    "Hardware manufacturing",
                    "Installation and maintenance",
                    "Customer support",
                    "Marketing and sales"
                ]
            },
            "go_to_market_slide": {
                "strategy": "Direct sales + partner network",
                "channels": [
                    "Local business associations",
                    "Technology partners",
                    "Direct sales team",
                    "Online platform"
                ],
                "timeline": [
                    "Q1: Initial market entry",
                    "Q2: Partner network expansion",
                    "Q3: Scale operations",
                    "Q4: Market leadership"
                ]
            },
            "team_slide": {
                "key_roles": [
                    "CEO/Founder",
                    "CTO",
                    "Operations Director",
                    "Sales Manager"
                ],
                "team_strengths": [
                    "Technical expertise",
                    "Market knowledge",
                    "Local presence",
                    "Industry experience"
                ],
                "hiring_plan": [
                    "Sales team expansion",
                    "Technical support staff",
                    "Local operations team"
                ]
            },
            "financials_slide": {
                "funding_needed": funding_needed or "$2M Series A",
                "use_of_funds": [
                    "Product development",
                    "Market expansion",
                    "Team growth",
                    "Operations scaling"
                ],
                "financial_projections": [
                    "Year 1: $1M revenue",
                    "Year 2: $5M revenue",
                    "Year 3: $15M revenue"
                ]
            },
            "call_to_action": {
                "next_steps": [
                    "Schedule a detailed presentation",
                    "Review financial projections",
                    "Discuss partnership opportunities"
                ],
                "contact_info": "contact@company.com",
                "investment_terms": "Series A: $2M for 20% equity"
            }
        }

def calculate_runway(current_cash: float, burn_rate: float) -> float:
    """Calculate runway in months based on current cash and burn rate."""
    if burn_rate <= 0:
        return 0.0
    return round(current_cash / burn_rate, 1) 