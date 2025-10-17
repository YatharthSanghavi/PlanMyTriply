# PlanMyTriply AI 🌎

An AI-powered travel planning platform that creates personalized travel itineraries based on your preferences, interests, and travel style. Built with modern web technologies and enhanced with advanced features.

## 🎯 Key Features

### Core Features
- **AI-Powered Planning**: Get personalized travel itineraries created by Google's Gemini AI
- **Smart Recommendations**: Discover hidden gems and local favorites with Tavily search integration
- **Detailed Itineraries**: Day-by-day plans with activities, restaurants, and accommodations
- **Travel Guides**: Access expert-written travel guides and tips
- **Hotel Search**: Find and compare hotels with AI-powered recommendations
- **Budget Management**: Plans tailored to your budget level with integrated budget calculator

### New Enhanced Features ✨
- **🌙 Dark Mode**: Toggle between light and dark themes with persistent preference
- **📄 PDF Export**: Export your travel plans as beautifully formatted PDFs
- **🔗 Easy Sharing**: Share plans via Email, WhatsApp, or direct link
- **💰 Budget Calculator**: Estimate trip costs with detailed breakdowns
- **💱 Currency Converter**: Real-time currency conversion for budget planning
- **🔍 Smart Autocomplete**: Intelligent destination suggestions as you type
- **⚡ Performance Optimized**: Caching, compression, and lazy loading for faster experience
- **🔒 Enhanced Security**: Security headers and input validation
- **📱 Fully Responsive**: Optimized for all devices from mobile to desktop
- **♿ Accessibility**: ARIA labels and keyboard navigation support

## 💻 Tech Stack

### Backend
- **Framework**: Flask (Python)
- **AI Integration**: Google Gemini 2.0 Flash
- **Search**: Tavily API for travel information
- **Database**: Supabase (PostgreSQL)
- **PDF Generation**: ReportLab
- **Compression**: Flask-Compress

### Frontend
- **Templates**: Jinja2
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JS with modern features
- **Fonts**: Plus Jakarta Sans

## 📋 Prerequisites

- Python 3.8+
- Supabase account
- Google Gemini API key
- Tavily API key

## 🔑 Environment Variables

Create a `.env` file in the root directory with:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_SUPABASE_URL=your_supabase_url
FLASK_SECRET_KEY=your_secret_key_for_sessions
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/YatharthSanghavi/PlanMyTriply.git
cd PlanMyTriply
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
- Create a new project in Supabase
- Run the migration files in the `supabase/migrations` directory

5. Start the development server:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
PlanMyTriply/
├── app.py                 # Main Flask application with all routes
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css    # Enhanced custom styles with dark mode
│   └── js/
│       └── main.js      # JavaScript utilities and features
├── templates/           # Jinja2 HTML templates
│   ├── base.html       # Base template with navigation and footer
│   ├── index.html      # Homepage with stats
│   ├── planner.html    # Trip planner with budget calculator
│   ├── plan.html       # Plan view with sharing and export
│   └── ...             # Other templates
└── supabase/
    └── migrations/      # Database migrations
```

## 🎯 Key API Endpoints

### Public Endpoints
- `GET /` - Homepage
- `GET /planner` - Travel planner form
- `POST /generate_plan` - Generate AI travel plan
- `GET /generate_plan?plan_id={id}` - View saved plan
- `GET /plans` - Browse all plans
- `GET /hotel-search` - Hotel search form
- `GET /hotel-searches` - Browse hotel searches

### API Endpoints
- `POST /api/validate-destination` - Validate destination input
- `GET /api/popular-destinations` - Get popular destinations
- `GET /api/plan/<id>/share` - Get shareable link
- `GET /api/plan/<id>/export/pdf` - Export plan as PDF
- `GET /api/currency/convert` - Convert currency
- `POST /api/budget-calculator` - Calculate trip budget
- `GET /api/stats` - Get application statistics

## 🎨 Features in Detail

### AI Travel Planning
- Personalized itinerary generation based on preferences
- Activity recommendations tailored to interests
- Budget optimization with smart suggestions
- Local insights and cultural tips
- Multi-day detailed planning

### Budget Calculator
- Real-time cost estimation
- Category-wise breakdown (accommodation, food, transport, activities)
- Per-person and per-day calculations
- Three budget levels: Budget, Medium, Luxury

### PDF Export
- Server-side PDF generation
- Professional formatting
- Includes all plan details and metadata
- Optimized for printing

### Dark Mode
- System preference detection
- Manual toggle with persistent storage
- Smooth transitions
- All components fully themed

## 🔒 Security Features

- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- Input validation and sanitization
- Request timeouts to prevent hanging
- Environment variables for sensitive data
- Secure session management

## ⚡ Performance Optimizations

- Response caching for API calls (24-hour TTL for travel info)
- Gzip compression for all responses
- Lazy loading for images
- Debounced API calls
- Efficient database queries

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📱 Mobile Responsiveness

Fully responsive design with:
- Mobile-first approach
- Touch-friendly interfaces
- Optimized layouts for all screen sizes
- Fast loading on mobile networks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering our travel recommendations
- Tavily for comprehensive travel information search
- Supabase for database infrastructure
- Bootstrap for UI components
- The open-source community

## 📧 Support

For support, email yatharthsanghavi@gmail.com or open an issue on GitHub.

---

Made with ❤️ by [Yatharth Sanghavi](https://github.com/YatharthSanghavi)
