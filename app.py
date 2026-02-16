"""
Teen Health & Biology Education App with AI-Powered Recommendations
A Flask application that uses Groq AI to generate personalized health guidance.
Designed for IB MYP Personal Project with biology focus.
"""

from flask import Flask, render_template, request
import math
import os
from groq import Groq

app = Flask(__name__)

# ============================================
# PUT YOUR GROQ API KEY HERE
# Get your free API key from: https://console.groq.com
# ============================================
GROQ_API_KEY = "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"  # REPLACE THIS WITH YOUR ACTUAL API KEY
# ============================================

# Initialize Groq client
# First try to get from environment variable, then fall back to hardcoded key
api_key = os.environ.get("GROQ_API_KEY", GROQ_API_KEY)

if api_key == "your_api_key_here":
    print("⚠️  WARNING: Please set your Groq API key in the code!")
    print("📝 Get your free API key from: https://console.groq.com")
    print("✏️  Edit app.py and replace 'your_api_key_here' with your actual key")
else:
    print("✅ Groq API key loaded successfully!")

client = Groq(api_key=api_key)

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI using the formula: BMI = weight(kg) / (height(m) * height(m))
    
    Args:
        weight_kg (float): Weight in kilograms
        height_cm (float): Height in centimeters
    
    Returns:
        float: BMI value rounded to 1 decimal place
    """
    height_m = height_cm / 100  # Convert cm to meters
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 1)

def get_bmi_category(bmi, age):
    """
    Determine BMI category based on value and age.
    
    Args:
        bmi (float): Calculated BMI value
        age (int): Age of the teenager
    
    Returns:
        str: BMI category
    """
    if age < 16:
        if bmi < 16.5:
            return "Underweight"
        elif bmi < 23:
            return "Healthy weight"
        elif bmi < 27:
            return "Overweight"
        else:
            return "Obese"
    else:
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Healthy weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def generate_ai_health_guidance(age, gender, height, weight, bmi, category):
    """
    Use Groq AI to generate personalized health guidance for teenagers.
    
    Args:
        age (int): Age of the teenager
        gender (str): Gender
        height (float): Height in cm
        weight (float): Weight in kg
        bmi (float): Calculated BMI
        category (str): BMI category
    
    Returns:
        dict: AI-generated health guidance
    """
    
    prompt = f"""You are a health educator specializing in adolescent development and biology. 
Generate personalized, age-appropriate health guidance for a {age}-year-old {gender} teenager.

BMI Information:
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi}
- Category: {category}

Please provide:

1. BIOLOGICAL EXPLANATION (2-3 sentences):
Explain what their BMI category means in terms of adolescent growth and development. Focus on biological processes like growth spurts, hormonal changes, and nutrient needs.

2. PERSONALIZED NUTRITION PLAN:
- Daily calorie range appropriate for their age and activity level
- Specific food recommendations for healthy adolescent development
- Foods to emphasize and foods to limit
- Meal timing suggestions

3. HYDRATION TIPS:
- Specific daily water intake recommendation
- Why hydration is important for their age group
- Practical tips for staying hydrated

4. SLEEP GUIDANCE:
- Recommended sleep hours for their age
- How sleep affects growth hormone release and development
- Tips for better sleep hygiene

5. PHYSICAL ACTIVITY PLAN:
- Type and duration of activities suitable for their age
- How exercise supports bone density and muscle development
- Specific activity suggestions they might enjoy

6. WEEKLY ACTION PLAN:
Create a simple 7-day action plan with daily goals covering nutrition, hydration, sleep, and activity.

Keep everything:
- Age-appropriate and encouraging
- Based on scientific evidence about adolescent development
- Practical and actionable
- Positive in tone (avoid fear-based messaging)
- Educational about the biology behind the recommendations

Format your response as JSON with these exact keys:
{{
  "explanation": "biological explanation here",
  "nutrition": {{
    "title": "Nutrition Plan",
    "calories": "calorie range",
    "foods_to_eat": ["food1", "food2", "food3"],
    "foods_to_limit": ["food1", "food2"],
    "meal_timing": "timing advice",
    "details": "detailed explanation"
  }},
  "hydration": {{
    "title": "Hydration Guidelines",
    "daily_amount": "amount in liters/cups",
    "importance": "why it matters",
    "tips": ["tip1", "tip2", "tip3"]
  }},
  "sleep": {{
    "title": "Sleep Recommendations",
    "hours": "recommended hours",
    "importance": "biological importance",
    "tips": ["tip1", "tip2", "tip3"]
  }},
  "activity": {{
    "title": "Physical Activity",
    "duration": "daily duration",
    "types": ["activity1", "activity2", "activity3"],
    "benefits": "how it helps development"
  }},
  "weekly_plan": {{
    "monday": "goal for monday",
    "tuesday": "goal for tuesday",
    "wednesday": "goal for wednesday",
    "thursday": "goal for thursday",
    "friday": "goal for friday",
    "saturday": "goal for saturday",
    "sunday": "goal for sunday"
  }}
}}"""

    try:
        if api_key == "your_api_key_here":
            raise Exception("API key not configured")
            
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert health educator specializing in adolescent biology and development. Provide evidence-based, age-appropriate health guidance. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=2500,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Clean the response to extract JSON
        import json
        import re
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group()
        
        guidance = json.loads(response_text)
        return guidance
        
    except Exception as e:
        print(f"⚠️  Error generating AI guidance: {e}")
        print("📋 Using fallback guidance instead...")
        # Return fallback guidance if API fails
        return get_fallback_guidance(category)

def get_fallback_guidance(category):
    """
    Provide fallback guidance if AI generation fails.
    """
    return {
        "explanation": f"Your BMI falls in the {category} category. During adolescence, your body undergoes rapid growth and development, requiring proper nutrition, hydration, and rest to support healthy changes.",
        "nutrition": {
            "title": "Nutrition Plan",
            "calories": "2000-2500 calories daily",
            "foods_to_eat": ["Whole grains", "Lean proteins", "Colorful vegetables", "Fresh fruits", "Dairy or alternatives"],
            "foods_to_limit": ["Sugary drinks", "Processed snacks", "Fast food"],
            "meal_timing": "Eat 3 balanced meals plus 1-2 healthy snacks",
            "details": "Focus on whole, nutrient-dense foods to support growth and development."
        },
        "hydration": {
            "title": "Hydration Guidelines",
            "daily_amount": "8-10 cups (2-2.5 liters)",
            "importance": "Water is essential for cellular functions and nutrient transport",
            "tips": ["Carry a water bottle", "Drink water with meals", "Choose water over sugary drinks"]
        },
        "sleep": {
            "title": "Sleep Recommendations",
            "hours": "8-10 hours nightly",
            "importance": "Growth hormone is released during deep sleep",
            "tips": ["Keep consistent bedtime", "Avoid screens before bed", "Create a dark, cool room"]
        },
        "activity": {
            "title": "Physical Activity",
            "duration": "60 minutes daily",
            "types": ["Walking", "Sports", "Swimming", "Dancing", "Cycling"],
            "benefits": "Strengthens bones, improves cardiovascular health, supports mental wellbeing"
        },
        "weekly_plan": {
            "monday": "Start the week with a nutritious breakfast and 30 minutes of activity",
            "tuesday": "Focus on hydration - track your water intake today",
            "wednesday": "Try a new healthy recipe or vegetable",
            "thursday": "Get to bed 30 minutes earlier than usual",
            "friday": "Review your week's progress and celebrate small wins",
            "saturday": "Do a fun physical activity you enjoy",
            "sunday": "Meal prep healthy snacks for the week ahead"
        }
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route for the application.
    Handles both form display (GET) and form processing (POST).
    """
    if request.method == 'POST':
        # Get form data
        try:
            age = int(request.form['age'])
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            gender = request.form['gender']
            
            # Validate inputs
            if not (10 <= age <= 19):
                return render_template('index.html', 
                                     error="Please enter an age between 10 and 19.")
            if height <= 0 or weight <= 0:
                return render_template('index.html', 
                                     error="Height and weight must be positive numbers.")
            
            # Calculate BMI
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi, age)
            
            # Generate AI-powered health guidance
            print(f"🤖 Generating AI guidance for {age}yo {gender}, BMI: {bmi} ({category})")
            ai_guidance = generate_ai_health_guidance(age, gender, height, weight, bmi, category)
            print("✅ Guidance generated successfully!")
            
            # Pass data to template
            return render_template('index.html',
                                 bmi=bmi,
                                 category=category,
                                 ai_guidance=ai_guidance,
                                 age=age,
                                 height=height,
                                 weight=weight,
                                 gender=gender,
                                 show_result=True)
        
        except ValueError:
            return render_template('index.html', 
                                 error="Please enter valid numbers for all fields.")
    
    # For GET requests, show empty form
    return render_template('index.html', show_result=False)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🏥 Teen Health & Biology Education App")
    print("="*50)
    if api_key == "your_api_key_here":
        print("⚠️  API KEY NOT SET!")
        print("📝 Please edit app.py and add your Groq API key")
        print("🔗 Get free key at: https://console.groq.com")
    else:
        print("✅ Ready to generate AI-powered health guidance!")
    print("🌐 Starting server at http://127.0.0.1:5000/")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    app.run()
