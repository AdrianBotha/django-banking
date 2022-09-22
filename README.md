# django-banking

### Project Introduction and Walkthrough
    This is a demo app that allows for the scalable uploading and retrieving of CSV information.
    In this demo, I focused heavily on the scalability. To achieve this, I used the following goals and tactics. 
    1. The CSV upload API must be asynchronous. Running it synchronously will result in timeouts on larger files.
    2. To achieve this, I delegate the processing of CSVs to a celery task. In hindsight, a simple Redis Queue might've been easier.
    3. When processing CSVs, all the thinking is done through basic SQL queries. 
        The raw CSV data is first imported into a temp table. Then this temp table is inserting into the actual trades table after some manipulation.
        Having to loop over the CSV rows in Python and individually figuring out DB relations or calling other APIs would be incredibly expensive.
    4. To allow for this. All the necessary data is pre-populated into the DB. This includes countries, currencies and possible spellings.
    5. These relations also help with the querying of data. As searching a country by an ID is more performant than searching by a text.

    There are a few shortcommings with this approach that I'll explain at the end of the README. For now, let's see it in action.


### Create venv
    virtualenv django-banking-venv -p python3.9
    --- OR ---
    python3.9 -m venv django-banking-venv
    
    source django-banking-venv/bin/activate


### Create database

#### Connect to psql depending on your preferences
    sudo su - postgres
    psql -d postgres
    (optional) CREATE USER banker WITH PASSWORD 'banker';
    
    CREATE DATABASE django_banking WITH OWNER banker ENCODING UTF8;
    GRANT ALL PRIVILEGES ON DATABASE django_banking TO banker;
    \c django_banking
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO banker;
    \q


### Create app.ini

#### This is esentually a .env file.
    cp app.ini.template app.ini
    vi app.ini
    (Confirm the database settings look correct)


### Set Up Database
    cd src
    python manage.py migrate
    python manage.py loaddata main
    python manage.py update_countries
    python manage.py update_currencies
    (This will take about 3 minutes, definitely room for improvement there)


### Install Requirements
    source django-banking-venv/bin/activate
    cd src
    pip install -r requirements.txt


### Launch Server
    source django-banking-venv/bin/activate
    cd src
    python manage.py runserver


### Launch Celery to Process Uploads
    (open new terminal separate from runserver terminal)
    source django-banking-venv/bin/activate
    cd src
    celery --app django_banking.tasks worker --loglevel=INFO


### API Examples

#### Upload CSV
    curl --location --request POST 'http://localhost:8000/trades/csv-upload/' \
    --form 'file=@"/path-to-csv/small.csv"'
    (You should recieve a 200 return. Celery should then be immediately busy importing the CSV)

#### Query Rows

##### Return All
    curl --location --request GET 'http://localhost:8000/trades/'

##### Filter on Country
    curl --location --request GET 'http://localhost:8000/trades/?country=ZA'

##### Filter on Date
    curl --location --request GET 'http://localhost:8000/trades/?date=2020/01/17'



### Shortcomings and Areas for Improvements

#### User Feedback
    The biggest problem with an asynchronous upload is that the user doesn't immediately know if there CSV has been imported or not.
    To mend this, I would create a user dashboard where they can see the progress and results of their CSV uploads.

#### Handling of Invalid Data
    Another issue is that the SQL import quietly skips rows with invalid data.
    To mend this, I would add a step to the CSV import process that checks the CSV against the imported data to find missing rows.
    These missing rows can then be added to the previously mentioned dashboard to notify the user where they went wrong.

#### Missing AED
    For the life of me I can't get any data for the AED currency using the provided endpoint.
    This means that any CSV rows with this currency fail to import.
    A possible fix would be to look at other APIs for info on this currency.

#### Slow Currency Import
    The currency importer is way slower than I'd like due to its heavy reliance on the Django ORM.
    To mend this, I would improve the speed by first building a csv of currencies from the API and then import that in a single sql statemnt.
    However, the idea of this import is to only really run it once, then update it daily. So speed might not be too important.

#### Missing Currency Rate Dates
    It seems the currency API has missing dates, I assumed this meant the value didn't change on these dates.
    I filled in these missing dates to make the CSV import more performant.
    However, I would definitely double check this assumption if I were to go live with this project.

#### Non Chunked CSVImports
    The CSV import currently uploads all the data in one giant chunk, which likely won't scale well.
    I would look into chunkifying the data into groups of around 100 before importing it to reduce the load on the database.


### Closing Statemnt
    Thanks again for viewing this project, it was fun to wrap my head around the requiremnts.
    I'm also open to any discussions or feedback.
