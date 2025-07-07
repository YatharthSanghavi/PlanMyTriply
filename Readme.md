# PlanMyTriply AI 🌎

An AI-powered travel planning platform that creates personalized travel itineraries based on your preferences, interests, and travel style.


## Features 🚀

- **AI-Powered Planning**: Get personalized travel itineraries created by advanced AI
- **Smart Recommendations**: Discover hidden gems and local favorites
- **Detailed Itineraries**: Day-by-day plans with activities, restaurants, and accommodations
- **Travel Guides**: Access expert-written travel guides and tips
- **Budget Management**: Plans tailored to your budget level
- **Local Insights**: Cultural tips and authentic experiences

## Tech Stack 💻

- **Backend**: Python, Flask
- **AI Integration**: Google's Gemini AI
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Bootstrap 5, Custom CSS
- **Icons**: Bootstrap Icons

## Prerequisites 📋

- Python 3.8+
- Supabase account
- Gemini API key
- Tavily API key

## Environment Variables 🔑

Create a `.env` file in the root directory with:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_SUPABASE_URL=your_supabase_url
```

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/YatharthSanghavi/PlanMyTriply.git
cd PlanMyTriply
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
- Create a new project in Supabase
- Run the migration files in the `supabase/migrations` directory

4. Start the development server:
```bash
python app.py
```

## Project Structure 📁

```
PlanMyTriply/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── static/
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── templates/           # HTML templates
└── supabase/
    └── migrations/      # Database migrations
```

## Features in Detail 🎯

### AI Travel Planning
- Personalized itinerary generation
- Activity recommendations
- Budget optimization
- Local insights and tips

### Travel Guides
- Expert-written content
- Destination insights
- Cultural tips
- Local recommendations

### User Experience
- Intuitive interface
- Real-time updates
- Mobile-responsive design
- Social sharing capabilities

## API Integrations 🔌

- **Gemini AI**: For intelligent travel planning
- **Tavily**: For travel information search
- **Supabase**: For database management

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](https://github.com/yatharthsanghvi/PlanMyTriply/blob/main/LICENSE) file for details.

## Acknowledgments 👏

- Google Gemini AI for powering our travel recommendations
- Supabase for database infrastructure
- Bootstrap for UI components

Made with ❤️ by [Yatharth Sanghavi]
