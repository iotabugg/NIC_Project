# EMS Portal

## Steps to run this app on your machine

### Prerequisites
- Python 3.14+
- Node.js (required for Tailwind CSS)
- PostgreSQL

### Setup

1. Clone the repo
```bash
   git clone <repo-url>
   cd project
```

2. Create and activate virtual environment
```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux/macOS
   .venv\Scripts\activate           # Windows
```

3. Install Python dependencies
```bash
   pip install -r requirements.txt
```

4. Create a `.env` file in the project root

5. Run database migrations
```bash
   python manage.py migrate
```

6. Create a superuser
```bash
   python manage.py createsuperuser
```

7. Set up Tailwind CSS
```bash
   python manage.py tailwind init
   python manage.py tailwind install
```

### Running the app

You need **two terminals** running simultaneously:

**Terminal 1 — Tailwind compiler**
```bash
source .venv/bin/activate
python manage.py tailwind start
```

**Terminal 2 — Django server**
```bash
source .venv/bin/activate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/login/` in your browser.