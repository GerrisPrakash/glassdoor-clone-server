
## Run Locally
git clone git@github.com:GerrisPrakash/glassdoor-clone-server.git
cd glassdoor-clone-server
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver