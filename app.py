from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import google.generativeai as genai
import requests
import json
import os
from datetime import datetime
from markupsafe import Markup
import markdown
from config import GEMINI_API_KEY, TAVILY_API_KEY, DEFAULT_TEMPERATURE, DEFAULT_MAX_OUTPUT_TOKENS
from supabase import create_client, Client
import traceback

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Configure Supabase
supabase: Client = create_client(
    os.getenv("VITE_SUPABASE_URL"),
    os.getenv("VITE_SUPABASE_ANON_KEY")
)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config={
        "temperature": DEFAULT_TEMPERATURE
    }
)

# Configure Markdown with extensions
md = markdown.Markdown(extensions=['extra', 'nl2br', 'sane_lists', 'fenced_code', 'tables'])

# Fallback content in case API fails
fallback_content = {
    "content": 
        """
        # Travel Plan
            
        ## Overview
        Here's a general guide to help you start planning your trip:

        ### Getting Started
        - Research the best time to visit based on weather and local events
        - Check visa requirements and travel documents
        - Look up local transportation options
        - Consider your accommodation preferences

        ### Planning Tips
        - Book accommodations in advance
        - Research local customs and etiquette
        - Check travel advisories
        - Make a list of must-see attractions
        - Consider local transportation options

        ### Safety and Preparation
        - Keep emergency contact numbers handy
        - Make copies of important documents
        - Check travel insurance options
        - Research local healthcare facilities
        - Stay updated on local conditions

        Please try again later for a more detailed, personalized travel plan.""",
            "sources": [
                {
                    "name": "Travel Advisory",
                    "url": "https://travel.state.gov/content/travel.html"
                }
            ]
}

def format_markdown_content(content):
    """Format the content with proper markdown structure"""
    # Convert markdown to HTML using the markdown library
    html_content = md.convert(content)
    return html_content

def search_travel_info(query, destination):
    """Enhanced Tavily API to search for travel information"""
    url = "https://api.tavily.com/search"
    
    # Craft more specific search queries for better results
    search_queries = [
        f"top attractions in {destination} travel guide",
        f"{destination} local restaurants and cuisine guide",
        f"where to stay in {destination} best neighborhoods",
        f"{destination} travel tips local customs",
        f"{destination} transportation options for tourists"
    ]
    
    all_results = []
    
    # Make multiple targeted searches
    for search_query in search_queries:
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": search_query,
            "search_depth": "advanced",
            "include_domains": [
                "tripadvisor.com", "lonelyplanet.com", "timeout.com", 
                "booking.com", "airbnb.com", "wikitravel.org", 
                "travel.state.gov", "cntraveler.com", "atlasobscura.com"
            ],
            "max_results": 3
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            results = response.json()
            if results and "results" in results:
                all_results.extend(results["results"])
        except requests.exceptions.RequestException as e:
            print(f"Tavily API Error for query '{search_query}': {e}")
    
    # Deduplicate results based on URL
    unique_results = {}
    for result in all_results:
        if result["url"] not in unique_results:
            unique_results[result["url"]] = result
    
    return list(unique_results.values())

def save_travel_plan(travel_params, content, sources):
    """Save the travel plan to Supabase"""
    try:
        data = {
            "destination": travel_params['destination'],
            "days": int(travel_params['days']),
            "people": int(travel_params['people']),
            "accommodation": travel_params['accommodation'],
            "activities": travel_params['activities'],
            "interests": travel_params['interests'],
            "budget": travel_params.get('budget', 'medium'),
            "content": content,
            "sources": sources
        }
        
        result = supabase.table('travel_plans').insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error saving travel plan to Supabase: {e}")
        return None

def get_travel_plan(plan_id):
    """Retrieve a travel plan from Supabase"""
    try:
        result = supabase.table('travel_plans').select("*").eq('id', plan_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error retrieving travel plan: {e}")
        return None

def format_date(date_str):
    """Convert string date to formatted date string"""
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%B %d, %Y")
        return None
    except Exception:
        return None

def generate_travel_plan(travel_params):
    """Generate a travel plan using Gemini API with enhanced prompt"""
    
    # Search for additional information using Tavily
    search_results = search_travel_info(
        f"travel guide for {travel_params['destination']}", 
        travel_params['destination']
    )
    
    # Extract useful information from search results
    search_info = ""
    sources = []
    
    if search_results:
        for i, result in enumerate(search_results):
            search_info += f"\nSource {i+1}: {result['title']}\n"
            search_info += f"URL: {result['url']}\n"
            search_info += f"Content: {result['content'][:300]}...\n\n"
            
            sources.append({
                "name": result['title'],
                "url": result['url']
            })
    
    # Build enhanced prompt for Gemini
    prompt = f"""
    Create a detailed travel itinerary in proper markdown format with clear sections and bullet points. Use the following structure:

    # {travel_params['destination']} Travel Plan

    ## Destination Overview
    - Brief introduction to {travel_params['destination']}
    - Best time to visit
    - Local currency and basic phrases
    - Weather expectations

    ## Before You Go
    - Visa requirements
    - Health and safety tips
    - Packing recommendations
    - Transportation to/from airport

    ## Accommodations
    - Recommended places to stay based on {travel_params['accommodation']} preference
    - Location advantages
    - Approximate rates
    - Booking tips

    ## Day-by-Day Itinerary

    ### Day 1
    - Morning activities
      * Specific locations
      * Timing
      * Tips
    - Afternoon activities
      * Detailed stops
      * Recommendations
    - Evening activities
      * Dinner options
      * Entertainment

    [Continue similar format for each day]

    ## Local Transportation
    - Getting around options
    - Costs
    - Tips and recommendations

    ## Dining Guide
    - Must-try local dishes
    - Restaurant recommendations
      * Budget options
      * Mid-range choices
      * Special experiences
    - Food safety tips

    ## Budget Breakdown
    - Daily estimates
      * Accommodation: {travel_params['accommodation']}
      * Meals
      * Activities
      * Transportation
    - Money-saving tips
    - Total budget range

    ## Local Tips
    - Cultural etiquette
    - Safety advice
    - Common phrases
    - Best photo spots

    Use the following details:
    - Duration: {travel_params['days']} days
    - Group size: {travel_params['people']} people
    - Accommodation preference: {travel_params['accommodation']}
    - Activities: {travel_params['activities']}
    - Interests: {travel_params['interests']}
    - Budget level: {travel_params.get('budget', 'Not specified')}

    Additional research information:
    {search_info}

    IMPORTANT FORMATTING RULES:
    1. Use proper markdown headings (# for main title, ## for sections, ### for subsections)
    2. Use bullet points (-) for all lists
    3. Use nested bullet points (* or -) for sub-items
    4. Add blank lines between sections
    5. Keep content organized and easy to read
    6. Use bold (**) for important information
    7. Include specific details and recommendations
    """
    
    try:
        response = model.generate_content(prompt)
        # Save the plan to Supabase
        saved_plan = save_travel_plan(travel_params, response.text, sources)
        
        # Convert markdown to HTML using the markdown library
        html_content = format_markdown_content(response.text)
        
        return {
            "content": html_content,
            "sources": sources,
            "plan_id": saved_plan['id'] if saved_plan else None
        }
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return fallback_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planner')
def planner():
    """New route for the dedicated planner page"""
    return render_template('planner.html')

@app.route('/generate_plan', methods=['GET', 'POST'])
def generate_plan():
    if request.method == 'GET':
        # Handle viewing existing plan
        plan_id = request.args.get('plan_id')
        if plan_id:
            plan_data = get_travel_plan(plan_id)
            if plan_data:
                # Convert stored content to HTML
                html_content = format_markdown_content(plan_data['content'])
                # Format the date using the new helper function
                formatted_date = format_date(plan_data.get('created_at'))
                
                return render_template('plan.html',
                                    plan=Markup(html_content),
                                    sources=plan_data.get('sources', []),
                                    params={
                                        'destination': plan_data['destination'],
                                        'days': plan_data['days'],
                                        'people': plan_data['people'],
                                        'accommodation': plan_data['accommodation'],
                                        'activities': plan_data['activities'],
                                        'interests': plan_data['interests'],
                                        'budget': plan_data['budget']
                                    },
                                    plan_id=plan_id,
                                    generated_date=formatted_date)
            return redirect(url_for('planner'))

    # Store form data in session for plan regeneration if needed
    for key in request.form:
        session[key] = request.form.get(key)
    
    travel_params = {
        'destination': request.form.get('destination', ''),
        'days': request.form.get('days', '3'),
        'people': request.form.get('people', '1'),
        'accommodation': request.form.get('accommodation', 'mid-range'),
        'activities': request.form.get('activities', 'sightseeing'),
        'interests': request.form.get('interests', 'culture, food'),
        'budget': request.form.get('budget', 'medium')
    }
    
    # Validate inputs
    if not travel_params['destination']:
        return render_template('planner.html', error="Please provide a destination")
    
    # Show loading page while generating
    if request.form.get('ajax') == 'true':
        return jsonify({"status": "processing"})
    
    # Generate the travel plan
    result = generate_travel_plan(travel_params)
    
    return render_template('plan.html', 
                          plan=Markup(result["content"]), 
                          sources=result.get("sources", []),
                          params=travel_params,
                          plan_id=result.get("plan_id"),
                          generated_date=datetime.now().strftime("%B %d, %Y"))

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/regenerate', methods=['POST'])
def regenerate_plan():
    # Retrieve stored parameters from session
    travel_params = {
        'destination': session.get('destination', ''),
        'days': session.get('days', '3'),
        'people': session.get('people', '1'),
        'accommodation': session.get('accommodation', 'mid-range'),
        'activities': session.get('activities', 'sightseeing'),
        'interests': session.get('interests', 'culture, food'),
        'budget': session.get('budget', 'medium')
    }
    
    # Generate a new plan with the same parameters
    result = generate_travel_plan(travel_params)
    
    return render_template('plan.html', 
                          plan=Markup(result["content"]), 
                          sources=result.get("sources", []),
                          params=travel_params,
                          plan_id=result.get("plan_id"),
                          generated_date=datetime.now().strftime("%B %d, %Y"))

@app.route('/plans')
def list_plans():
    """Route to display all saved travel plans"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 9  # Number of plans per page
        
        # Get total count
        count_result = supabase.table('travel_plans').select('id', count='exact').execute()
        total_plans = count_result.count if hasattr(count_result, 'count') else len(count_result.data)
        
        # Calculate pagination
        total_pages = max((total_plans + per_page - 1) // per_page, 1)  # At least 1 page
        offset = (page - 1) * per_page
        
        # Get paginated results
        result = supabase.table('travel_plans').select("*").order('created_at', desc=True).range(offset, offset + per_page - 1).execute()
        plans = result.data if result.data else []
        
        # Convert string timestamps to datetime objects
        for plan in plans:
            if isinstance(plan['created_at'], str):
                plan['created_at'] = datetime.fromisoformat(plan['created_at'].replace('Z', '+00:00'))
        
        return render_template('plans.html',
                             plans=plans,
                             current_page=page,
                             total_pages=total_pages,
                             prev_page=page-1 if page > 1 else None,
                             next_page=page+1 if page < total_pages else None)
    except Exception as e:
        print(f"Error fetching travel plans: {e}")
        return render_template('plans.html',
                             plans=[],
                             current_page=1,
                             total_pages=1,
                             prev_page=None,
                             next_page=None,
                             error="Failed to fetch travel plans")

@app.route('/travel-guides')
def travel_guides():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 9  # Number of guides per page
        
        # Get total count
        count_result = supabase.table('travel_guides').select('id', count='exact').execute()
        total_guides = count_result.count if hasattr(count_result, 'count') else len(count_result.data)
        
        # Calculate pagination
        total_pages = max((total_guides + per_page - 1) // per_page, 1)  # At least 1 page
        offset = (page - 1) * per_page
        
        # Get paginated results
        result = supabase.table('travel_guides').select("*").order('created_at', desc=True).range(offset, offset + per_page - 1).execute()
        guides = result.data if result.data else []

        # Get unique categories
        categories = set(guide['category'] for guide in guides)
        
        return render_template('travel_guides.html',
                             guides=guides,
                             categories=categories,
                             current_page=page,
                             total_pages=total_pages,
                             prev_page=page-1 if page > 1 else None,
                             next_page=page+1 if page < total_pages else None)
    except Exception as e:
        print(f"Error fetching travel guides: {e}")
        return render_template('travel_guides.html',
                             guides=[],
                             categories=set(),
                             current_page=1,
                             total_pages=1,
                             prev_page=None,
                             next_page=None,
                             error="Failed to fetch travel guides")

@app.route('/travel-guides/create', methods=['GET', 'POST'])
def create_guide():
    if request.method == 'POST':
        try:
            data = {
                'title': request.form['title'],
                'content': request.form['content'],
                'excerpt': request.form['excerpt'],
                'author': request.form.get('author', 'Anonymous'),
                'category': request.form['category'],
                'tags': request.form['tags'].split(',') if request.form['tags'] else [],
                'icon': request.form.get('icon', 'compass'),
                'default_bg_color': request.form.get('default_bg_color', '#4F46E5')
            }
            
            result = supabase.table('travel_guides').insert(data).execute()
            
            if result.data:
                flash('Guide published successfully!', 'success')
                return redirect(url_for('travel_guides'))
            flash('Failed to create guide', 'error')
            return render_template('create_guide.html', error="Failed to create guide")
        except Exception as e:
            print(f"Error creating travel guide: {e}")
            flash('An error occurred while creating the guide', 'error')
            return render_template('create_guide.html', error="An error occurred while creating the guide")
    
    return render_template('create_guide.html')

@app.route('/travel-guides/<guide_id>')
def view_guide(guide_id):
    try:
        result = supabase.table('travel_guides').select("*").eq('id', guide_id).single().execute()
        if result.data:
            return render_template('view_guide.html', guide=result.data)
        return redirect(url_for('travel_guides'))
    except Exception as e:
        print(f"Error fetching travel guide: {e}")
        return redirect(url_for('travel_guides'))

@app.route('/hotel-search', methods=['GET', 'POST'])
def hotel_search():
    if request.method == 'POST':
        try:
            location = request.form.get('location')
            guests = request.form.get('guests', '2')
            preferences = request.form.get('preferences', '')
            budget = request.form.get('budget', 'medium')

            # Validate required fields
            if not location:
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('hotel_search'))

            # Search for hotel information using Tavily
            tavily_query = f"best hotels in {location} for {guests} guests with {budget} budget"
            if preferences:
                tavily_query += f" with {preferences} preferences"
            
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": tavily_query,
                "search_depth": "advanced",
                "include_domains": [
                    "booking.com", "hotels.com", "expedia.com", 
                    "tripadvisor.com", "kayak.com"
                ],
                "max_results": 5
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            hotel_results = response.json()

            if not hotel_results.get('results'):
                raise Exception("No results found from Tavily API")

            # Prepare search details section
            search_details = f"""
            ## Search Details
            - **Location**: {location}
            - **Guests**: {guests}
            - **Budget Level**: {budget}"""

            if preferences:
                search_details += f"\n- **Preferences**: {preferences}"

            # Prepare external sources section
            external_sources = "\n## External Sources"
            for result in hotel_results.get('results', []):
                external_sources += f"\n- [{result.get('title')}]({result.get('url')})\n  {result.get('snippet')}"

            # Generate hotel recommendations using Gemini
            prompt = f"""
            Create a detailed hotel recommendation guide in markdown format for:
            Location: {location}
            Guests: {guests}
            Preferences: {preferences}
            Budget: {budget}

            Use this structure:

            # Hotel Recommendations for {location}

            ## Overview
            [Brief introduction about {location} and its hotel scene]

            ## Top Recommended Hotels

            ### 1. [Hotel Name]
            - **Price Range**: [Budget details]
            - **Location**: [Area description]
            - **Key Features**:
              * [Feature 1]
              * [Feature 2]
              * [Feature 3]
            - **Best For**: [Type of travelers]
            - **Pros**:
              * [Pro 1]
              * [Pro 2]
            - **Cons**:
              * [Con 1]
              * [Con 2]

            [Repeat format for 4 more hotels]

            ## Location Guide
            - **Best Areas to Stay**:
              * [Area 1]: [Description]
              * [Area 2]: [Description]
              * [Area 3]: [Description]

            ## Price Analysis
            - **Budget Options**: [Price range and what to expect]
            - **Mid-Range Options**: [Price range and what to expect]
            - **Luxury Options**: [Price range and what to expect]

            {search_details}

            {external_sources}

            Use the following search results to enhance recommendations:
            {json.dumps(hotel_results.get('results', []), indent=2)}
            """

            response = model.generate_content(prompt)
            if not response or not response.text:
                raise Exception("No response from Gemini API")

            # Save the search to the database
            search_data = {
                'location': location,
                'guests': int(guests),
                'preferences': preferences,
                'budget': budget,
                'recommendations': response.text,
                'search_results': hotel_results.get('results', [])
            }
            
            result = supabase.table('hotel_searches').insert(search_data).execute()
            if not result.data:
                raise Exception("Failed to save search to database")

            # Redirect to the view page for the new search
            return redirect(url_for('view_hotel_search', search_id=result.data[0]['id']))

        except requests.exceptions.RequestException as e:
            print(f"Tavily API Error: {str(e)}")
            print(f"Response: {e.response.text if hasattr(e, 'response') else 'No response'}")
            flash('Error connecting to hotel search service. Please try again.', 'error')
        except Exception as e:
            print(f"Error in hotel search: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            flash('An error occurred while searching for hotels. Please try again.', 'error')
        
        return redirect(url_for('hotel_search'))

    return render_template('hotel_search.html')

@app.route('/hotel-searches')
def hotel_searches():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 6  # Number of searches per page
        
        # Get total count
        count_result = supabase.table('hotel_searches').select('id', count='exact').execute()
        total_searches = count_result.count if hasattr(count_result, 'count') else len(count_result.data)
        
        # Calculate pagination
        total_pages = max((total_searches + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page
        
        # Get paginated results
        result = supabase.table('hotel_searches').select("*").order('created_at', desc=True).range(offset, offset + per_page - 1).execute()
        searches = result.data if result.data else []
        
        # Convert string timestamps to datetime objects
        for search in searches:
            if isinstance(search['created_at'], str):
                search['created_at'] = datetime.fromisoformat(search['created_at'].replace('Z', '+00:00'))
        
        return render_template('hotel_searches.html',
                             searches=searches,
                             current_page=page,
                             total_pages=total_pages,
                             prev_page=page-1 if page > 1 else None,
                             next_page=page+1 if page < total_pages else None)
    except Exception as e:
        print(f"Error fetching hotel searches: {e}")
        return render_template('hotel_searches.html',
                             searches=[],
                             current_page=1,
                             total_pages=1,
                             prev_page=None,
                             next_page=None,
                             error="Failed to fetch hotel searches")

@app.route('/hotel-search/<search_id>')
def view_hotel_search(search_id):
    try:
        result = supabase.table('hotel_searches').select("*").eq('id', search_id).single().execute()
        if result.data:
            # Convert markdown to HTML if recommendations exist
            if result.data.get('recommendations'):
                recommendations = md.convert(result.data['recommendations'])
                result.data['recommendations'] = Markup(recommendations)
            return render_template('view_hotel_search.html', search=result.data)
        return redirect(url_for('hotel_searches'))
    except Exception as e:
        print(f"Error fetching hotel search: {e}")
        return redirect(url_for('hotel_searches'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)