# AI Fitness Partner

An intelligent fitness companion that provides personalized workout plans, nutrition advice, and motivation through AI-powered agents.

## Project Structure

```
AI-Fitness-Partner/
├── frontend/                # Next.js frontend
│   ├── pages/              # Page components
│   ├── public/             # Static assets
│   └── ...
├── backend/                # Flask backend
│   ├── api/               # API routes
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
└── agents/                # AI Agents (CAMEL)
    ├── health_analyst.py
    ├── fitness_coach.py
    ├── nutritionist.py
    ├── motivator.py
    ├── trainer.py
    └── data_analyst.py
```

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=your_database_url
   OPENAI_API_KEY=your_openai_api_key
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## Deployment

### Deploying to Vercel

1. Fork this repository to your GitHub account

2. Create a new project on Vercel:
   - Go to [Vercel](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure the project:
     - Build Command: `cd frontend && npm run build`
     - Output Directory: `frontend/.next`
     - Install Command: `cd frontend && npm install`

3. Environment Variables:
   Add the following environment variables in Vercel project settings:
   ```
   NEXT_PUBLIC_API_URL=your_backend_api_url
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=your_database_url
   ```

4. Deploy:
   - Click "Deploy"
   - Vercel will automatically build and deploy your project
   - Your app will be available at `https://your-project-name.vercel.app`

## Features

- Personalized workout plans based on user goals and preferences
- AI-powered fitness coaching
- Progress tracking and analytics
- Nutrition guidance
- Motivational support
- Real-time workout feedback

## Technology Stack

- Frontend: Next.js, React
- Backend: Flask
- Database: SQLAlchemy
- AI: OpenAI GPT-4
- Authentication: JWT

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
