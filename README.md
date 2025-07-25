# My django_quote_api

This is a simple project I built using Django. It gives you a random inspirational quote and also stops people from asking for too many quotes too quickly.

## What it Does (Features):

*Get a Random Quote:*
    * You can go to `/api/quote/` and it will send you a random quote, like this:
        ```json
       		{"quote": "The only way to do great work is to love what you do. - Steve Jobs"}
        ```
*Rate Limiting (Don't Ask Too Much!):*
    * I've set it up so one person (identified by their IP address) can only ask for 5 quotes every minute.
    * If someone asks more than 5 times in a minute, they'll get an error message like this:
        ```json
        	{"error": "Rate limit exceeded. Try again in X seconds."}
        ```
        	(The `X` will tell them how many seconds to wait.)



## How I Built It (Technical Stuff):

**Language & Framework:** I used Python with Django.
**No Database:** For the rate limiting, I didn't use a database. I just kept track of requests right in the computer's memory.
**Logging:** Every time someone asks for a quote, I log (record) their IP address and if their request was successful or blocked.
***Stays Safe:** I made sure that even if many people ask at the same time, the rate limiting works correctly without issues.



## Extra that I Added (Bonus):

* **API Documentation:** You can see all the details of the API in a nice web page at `/api/schema/swagger-ui/`.
* **Testing:** I wrote some tests to make sure the rate limiting works just as it should.



## How to Get It Running (Setup):

1.  **Get the code:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git]::  https://github.com/SaiLochana16/django_quote_api 
    cd django_quote_api
    ```
2.  **Set up the environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install necessary things:**
    ```bash
    pip install -r requirements.txt
    ```
    (You might need to create this file by running `pip freeze > requirements.txt` first).
4.  **Start the server:**
    ```bash
    python manage.py runserver
    ```
    Now, the API should be running at `http://127.0.0.1:8000/api/quote/`.



## Important Notes & My Choices:

**Why no database for rate limiting?** The task asked me to use the computer's memory for this. This works fine for a simple setup, but if this API were used by many people all over the internet, or if the server had to restart often, the limits would reset. For a bigger project, we'd usually use something like Redis to store this information.
**How I control requests:** I built my own special "middleware" in Django. This piece of code checks every request before it even gets to the part that gives out quotes.
**Finding your IP:** My code tries to figure out your computer's IP address the best way it can, even if you're behind a proxy server.

## How to Test It:

* **Get a quote:**
    ```bash
    curl [http://127.0.0.1:8000/api/quote/](http://127.0.0.1:8000/api/quote/)
    ```
* **Test the limit (try this 6 or more times very quickly!):**
    ```bash
    curl -v [http://127.0.0.1:8000/api/quote/](http://127.0.0.1:8000/api/quote/)
    ```
    On the 6th try (or soon after), you should see the "429 Too Many Requests" error.

## The Main Address for the API

The main place to get a quote is: `http://127.0.0.1:8000/api/quote/`

You can also see the API documentation here: `http://127.0.0.1:8000/api/schema/swagger-ui/`
