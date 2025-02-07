# Chat-with-CSV-using-API

A powerful tool that enables natural language conversations with CSV data through an API interface.

## Features

- Upload and process CSV files
- Natural language querying of CSV data
- RESTful API endpoints for data interaction
- Interactive chat-like interface for data exploration

## Getting Started

1. Clone the repository:

git clone https://github.com/manjunathan1999/Chat-with-CSV-using-API.git


2. Install required dependencies:

pip install -r requirements.txt


3. Change configuration settings in constants.py


4. Add the table name which you want to query in the chatcsvcourpus.py file


5. Add the username and password and db_url in the sql/sqlconnector.py file


6. Run the application:

uvicorn main:app --reload


7. Access the API documentation at http://localhost:8000/docs


8. Use the API endpoints to interact with CSV data


## Usage ##
1. Execute the sql query using the /execute-sql endpoint
2. Ingest the CSV data using the /ingest endpoint
3. Query the CSV data using the /query endpoint
4. Explore the chat-like interface for data exploration
5. Just send { "type" : "table1" } in json body to get the table as csv file and then send the csv file to the /ingest endpoint to ingest the data into the database 
6. For query use { "type" : "table1", "query" : "your_query" } in json body to get the result of the query



## Future Enhancements ##

1. Improve the chat interface for better user experience
2. Implement user authentication and authorization
3. Enhance error handling and logging
