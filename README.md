# Parse CSV file
1. Reading the CSV every day 
2. Storing the updated data in a DB 
3. Exposing a single API to get a list of products by a producer. You should include some kind of pagination mechanism in your implementation


## Read CSV file
To read the CSV file every day we can use multiple ways:
- Using a cron job to run a script that reads the CSV file and updates the DB
- Using a scheduler like Celery to run a task that reads the CSV file and updates the DB
- Using a cloud service like AWS SQS, make consumers that read the CSV file and update the DB

For this task, for the sake of simplicity, I will implement a cron job that reads the CSV file locally and updates the DB.
You can find the script in the `app/scripts` folder.

I made example CI but didn't make github actions.