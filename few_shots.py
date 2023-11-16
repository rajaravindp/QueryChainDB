few_shots = [
    {
        "Question": "If I want to know the average price of red Model 3 cars, sorted by year, what SQL query should I use?", 
        "SQLQuery": "SELECT AVG(price) AS avg_price, year FROM tsla_listings1 WHERE model = 'Model 3' AND paintjob = 'Red Multi-Coat Paint' GROUP BY year ORDER BY year", 
        "SQLResult": "Result of the SQL query", 
        "Answer": "(31913.333333333333, 2018)"
    },
    {
        "Question": "How many Model 3 cars are there which are blue?", 
        "SQLQuery": "SELECT count(*) FROM tsla_listings1 WHERE model = 'Model 3' AND paintjob LIKE '%Blue%'",
        "SQLResult": "Result of the SQL query",
        "Answer": "79"
    }, 
    {
        "Question": "How much is the mean price of red Model 3 cars?",
        "SQLQuery": "SELECT AVG(price) FROM tsla_listings1 WHERE model = 'Model 3' AND paintjob LIKE '%Red%'",
        "SQLResult": "Result of the SQL query",
        "Answer": "33192.307692307692"
    }

]