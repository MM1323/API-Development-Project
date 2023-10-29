## API Reference
### Getting Started
- **Base URL**: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:500/`, which is set as a proxy in the frontend configuration.
- **Authentication**: This version of the application does not require authentication or API keys

To run in the workspace, you can follow the set up guide found in [the Guide](../Guide.ipynb). Following the guide will set up the backend, DB, and frontend in your workspace.


### Handling Error
Errors are returned as a JSON objects in the following format:
```json
{
    'success':false,
    'message':'Message text',
    'error': 400
}
```
The API will return three error types when requests fails:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable
- 500: Internal server error

### Endpoints
#### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. It also returns a boolen if it was successful.
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions
- Ferches  a list of questions, number of total questions, current category, categories.
- It also returns a boolean if it was successful.
- Request Arguments: None
- Query Parameter(optional): `?page=#`: page number
- Results are paginated in groups of 10. 
- Sample: `curl http://127.0.0.1:5000/questions`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  
  "current_category": 0,
  "total_questions": 19,
  "success": true,
  
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  
}

```

#### DELETE /questions/<int:question_id>
- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Return: a success of operation, deleted question id, and total questions.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/6`

```json
{
  "success": true
  "deleted": 45,
  "totalQuestions": 100
}
```

#### POST /questions
- Create a new  question suing submitted  question and answer text, category id, and difficulty score.
- Request Arguments: question, answer, category, difficulty
- Return a success of operation, created question id, and total questions.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question":"what is my name", "answer":"MM", "category":"5", "difficulty":"2"}' http://127.0.0.1:5000/questions`
```json
{
  "success": true
  "created": 45,
  "totalQuestions": 100,
}
```

#### Post /questions
- Sends a post request in order to search for a specific question by search term
- Request Arguments: searchTerm in jsonObject. Exp: `{'searchTerm': 'this is the term the user is looking for'}`
- Return any questions for whom the search term is a substring of the question, total number of questions.
- Results are paginated in groups of 10.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}' http://127.0.0.1:5000/questions`

```json
{
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Nothing",
      "category": 1,
      "difficulty": 1,
      "id": 26,
      "question": "What is this test?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "total_questions": 8,
  "success": true, 
}

```

#### GET /categories/<category_id>/questions
- Get questions based on category
- Request Arguments: None
- Return a list of questions, number of total questions, current category, categories, success.
- Results are paginated in groups of 10.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": "Art", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "totalQuestions": 8
}

```
#### POST /quizzes
- Get questions to play the quiz
- Request Arguments: list of previous questions, quiz_category
- Return a random questions within the given category, if provided, and that is not one of the previous questions. Also success.
- Sample: `curl http://127.0.0.1:5000/quizzes  -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category": {"id":0, "type":"All"}}'`

```json
{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }, 
  "success": true
}

```

## Testing
To run the tests, run:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

```
