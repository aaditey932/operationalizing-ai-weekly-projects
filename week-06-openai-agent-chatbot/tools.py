"""
Additional tools and utilities for the OpenAI Agents SDK demo.
"""

from agents import function_tool
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

@function_tool
def get_company_info(info_type: str) -> Dict[str, Any]:
    """Get company information like hours, policies, contact details."""
    company_data = {
        "hours": {
            "monday_friday": "9:00 AM - 5:00 PM EST",
            "saturday": "10:00 AM - 2:00 PM EST", 
            "sunday": "Closed",
            "holidays": "Closed on major holidays"
        },
        "policies": {
            "return_policy": "30-day return policy for unopened items with receipt",
            "warranty": "1-year manufacturer warranty on all electronics",
            "shipping": "Free shipping on orders over $50, 3-5 business days standard",
            "price_match": "We match competitor prices within 14 days of purchase"
        },
        "contact": {
            "phone": "1-800-DEMO-123",
            "email": "support@demostore.com",
            "chat": "Available on website during business hours",
            "address": "123 Demo Street, Tech City, TC 12345"
        },
        "departments": {
            "general": "Main customer service line",
            "technical": "Technical support specialists", 
            "billing": "Billing and account specialists",
            "returns": "Returns and exchanges"
        }
    }
    
    if info_type.lower() in company_data:
        return {info_type: company_data[info_type.lower()]}
    else:
        return {"available_info": list(company_data.keys())}

@function_tool
def check_order_status(order_id: str) -> Dict[str, Any]:
    """Check the status of a customer order."""
    # Simulated order database
    sample_orders = {
        "ORD001": {
            "order_id": "ORD001",
            "status": "Shipped",
            "tracking_number": "1Z999AA1234567890",
            "estimated_delivery": "March 15, 2025",
            "items": ["Gaming Pro X1 Laptop", "Wireless Mouse"],
            "total": "$1,349.98"
        },
        "ORD002": {
            "order_id": "ORD002", 
            "status": "Processing",
            "tracking_number": None,
            "estimated_delivery": "March 18, 2025",
            "items": ["SmartPhone Pro"],
            "total": "$899.99"
        },
        "ORD003": {
            "order_id": "ORD003",
            "status": "Delivered",
            "tracking_number": "1Z999BB9876543210",
            "estimated_delivery": "March 10, 2025",
            "items": ["Budget Phone Plus", "Phone Case"],
            "total": "$324.98"
        }
    }
    
    if order_id.upper() in sample_orders:
        return sample_orders[order_id.upper()]
    else:
        return {
            "error": "Order not found",
            "message": "Please check your order ID and try again",
            "order_id": order_id
        }

@function_tool
def get_product_reviews(product_name: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Get customer reviews for a product."""
    # Simulated review database
    reviews_db = {
        "gaming pro x1": [
            {
                "reviewer": "TechEnthusiast92",
                "rating": 5,
                "title": "Excellent gaming performance!",
                "review": "This laptop handles all the latest games at high settings. The 144Hz display is amazing and the RTX 4060 runs everything smoothly.",
                "date": "March 5, 2025",
                "verified_purchase": True
            },
            {
                "reviewer": "StudentGamer",
                "rating": 4,
                "title": "Great laptop, but gets warm",
                "review": "Love the performance and display quality. Only downside is it gets quite warm during intensive gaming sessions.",
                "date": "March 1, 2025", 
                "verified_purchase": True
            },
            {
                "reviewer": "ProGamer2024",
                "rating": 5,
                "title": "Perfect for competitive gaming",
                "review": "The 144Hz display gives me a real advantage in FPS games. Build quality is solid and keyboard feels great.",
                "date": "February 28, 2025",
                "verified_purchase": True
            }
        ],
        "smartphone pro": [
            {
                "reviewer": "PhotoLover",
                "rating": 5,
                "title": "Camera quality is outstanding",
                "review": "The 108MP camera takes incredible photos, even in low light. Battery life easily lasts a full day.",
                "date": "March 8, 2025",
                "verified_purchase": True
            },
            {
                "reviewer": "BusinessUser",
                "rating": 4,
                "title": "Great phone for work",
                "review": "Fast performance, good display, and excellent build quality. 5G works great in my area.",
                "date": "March 3, 2025",
                "verified_purchase": True
            }
        ]
    }
    
    product_key = product_name.lower()
    reviews = reviews_db.get(product_key, [])
    
    if not reviews:
        return [{"message": f"No reviews found for '{product_name}'"}]
    
    return reviews[:limit]

@function_tool
def schedule_callback(customer_phone: str, preferred_time: str, issue_summary: str) -> Dict[str, Any]:
    """Schedule a callback for the customer."""
    # Simulate callback scheduling
    callback_id = f"CB{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Parse preferred time (simplified)
    try:
        # Add some basic time validation
        time_slots = [
            "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
            "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"
        ]
        
        if preferred_time not in time_slots:
            preferred_time = "Next available time"
            
        return {
            "callback_id": callback_id,
            "status": "Scheduled",
            "phone_number": customer_phone,
            "scheduled_time": preferred_time,
            "issue_summary": issue_summary,
            "message": f"Callback scheduled successfully! ID: {callback_id}",
            "estimated_wait": "2-4 hours"
        }
    except Exception as e:
        return {
            "status": "Error",
            "message": "Unable to schedule callback. Please contact customer service directly.",
            "error": str(e)
        }

@function_tool
def get_store_locations(zip_code: str = None, city: str = None) -> List[Dict[str, Any]]:
    """Find store locations near the customer."""
    # Simulated store database
    stores = [
        {
            "store_id": "ST001",
            "name": "Tech City Main Store",
            "address": "123 Main St, Tech City, TC 12345",
            "phone": "(555) 123-4567",
            "hours": "Mon-Sat 10AM-8PM, Sun 12PM-6PM",
            "services": ["Sales", "Technical Support", "Returns"],
            "distance": "2.3 miles"
        },
        {
            "store_id": "ST002", 
            "name": "Digital Plaza Location",
            "address": "456 Digital Ave, Tech City, TC 12346",
            "phone": "(555) 234-5678",
            "hours": "Mon-Fri 9AM-7PM, Sat 10AM-6PM, Sun Closed",
            "services": ["Sales", "Business Solutions"],
            "distance": "5.7 miles"
        },
        {
            "store_id": "ST003",
            "name": "Suburban Tech Center", 
            "address": "789 Suburb Rd, Techburg, TC 12347",
            "phone": "(555) 345-6789",
            "hours": "Mon-Sat 11AM-7PM, Sun 1PM-5PM",
            "services": ["Sales", "Technical Support", "Repairs"],
            "distance": "8.1 miles"
        }
    ]
    
    # In a real implementation, you'd filter by location
    # For demo, return all stores with a note about search
    search_note = ""
    if zip_code:
        search_note = f" near {zip_code}"
    elif city:
        search_note = f" near {city}"
    
    return {
        "search_query": f"Stores{search_note}",
        "stores": stores,
        "total_found": len(stores)
    }

def setup_tools():
    """Setup and return all available tools for agents."""
    return {
        "company_info": get_company_info,
        "order_status": check_order_status,
        "product_reviews": get_product_reviews,
        "schedule_callback": schedule_callback,
        "store_locations": get_store_locations
    }

# Utility functions for the Streamlit app
def format_agent_response(response: str, agent_name: str = None) -> str:
    """Format agent response for better display in Streamlit."""
    if agent_name:
        return f"**{agent_name}:** {response}"
    return response

def get_example_queries_by_agent():
    """Get example queries organized by agent type."""
    return {
        "Product Questions": [
            "I need a laptop for gaming under $1000",
            "What phones do you have with good cameras?",
            "Can you compare your laptop options?",
            "What are the reviews for the Gaming Pro X1?"
        ],
        "Technical Support": [
            "My WiFi keeps disconnecting",
            "My computer is running very slowly",
            "The application keeps crashing",
            "I can't connect to the internet"
        ],
        "Billing & Account": [
            "I have a question about my bill",
            "I was charged twice for my order",
            "How do I update my payment method?",
            "What's my account balance?"
        ],
        "General Support": [
            "What are your store hours?",
            "What's your return policy?",
            "I need to check my order status",
            "Where are your store locations?"
        ]
    }