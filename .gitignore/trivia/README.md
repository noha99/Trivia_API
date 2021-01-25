
# API DOCUMENTATION

## show categories
Returns json data about a all cateories i  saved in database.

**URL**  /categories

**Method** ['GET']

*Success Response:*   
Code: 200   
Content: 
```json
{
    "categories":[
        {
            "id": 5,
            "type": "Entertainment"
        }
    ],
    "success": true
}
```

## Show Paginating Questions
**URL** /questions

**Method** ['GET']

*Success Response:*   
Code: 200   
Content: 
```json
{
    "questions":[
        {
            "answer": "Apollo 13",
            "category": "5",
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
    ],
    "success": true,
    "total": 19
}
```

## Delete a Question
**URL** /questions/<question_id>   
**URL Params**   
*Required*: question_id=[integer]  
**Method** ['DELETE']

*Success Response:*   
Code: 200   
Content: 
```json
{
    "success": true,
    "deleted_questions":
    {
        "answer": "Apollo 13",
        "category": "5",
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
    
}
```

## Add Question
**URL** /questions    
**Method** ['POST']

*Request:*
```json
{
    "answer": "Apollo 13",
    "category": "5",
    "difficulty": 4,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"    
}
```
*Success Response:*   
Code: 200   
Content: 
```json
{
    "success": true,
    "question":
    {
        "answer": "Apollo 13",
        "category": "5",
        "difficulty": 4,
        "id": 44,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
    
}
```

## Search for Question
**URL** /search    
**Method** ['POST']

*Request:*
```json
{
    "searchTerm": "What"    
}
```
*Success Response:*   
Code: 200   
Content: 
```json
{
    "success": true,
    "questions":[
        {
            "answer": "Apollo 13",
            "category": "5",
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
    ]
    
}
```

## Show all Questions with a specific Category 
**URL** /categories/<int:id>/questions  
**URL Params**   
*Required*: id=[integer]  
**Method** ['POST']

*Success Response:*   
Code: 200   
Content: 
```json
{
    "success": true,
    "questions":
    {
        "answer": "Apollo 13",
        "category": "5",
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
    
}
```

## Play Quiz
**URL** /quizzes   
**Method** ['POST']

*Success Response:*   
Code: 200   
Content: 
```json
{
    "quiz_category": {
		"id":2,
		"type":"Art"
	},
    "previous_questions": [
    	{
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ]
}
```