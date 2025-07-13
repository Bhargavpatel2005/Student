# 1. Clone the repository
git clone https://github.com/Bhargavpatel2005/Student.git
cd Student

# 2. Checkout to updated branch if needed
git checkout feature/advanced-crud  # only if a separate branch is used

# 3. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt  # or just install Django if requirements not used

# 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Run the server
python manage.py runserver