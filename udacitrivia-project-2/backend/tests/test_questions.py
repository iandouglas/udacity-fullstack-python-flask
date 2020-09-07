import json
from models import Question, Category


def test_get_paginated_questions_page_1(client):
    """
    1. Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).

    /questions?page=${this.state.page}
    expects result.questions, result.total_questions, result.categories, result.current_category

    according to https://knowledge.udacity.com/questions/281844 we can ignore current_category and set it to null/None
    """

    for path in ['/questions', '/questions?page=1']:
        response = client.get(path)

        assert '200 OK' == response.status
        data = json.loads(response.data.decode('utf-8'))

        assert 'total_questions' in data
        assert data['total_questions'].__class__ == int
        assert 10 == len(data['total_questions'])

        assert 'categories' in data
        assert data['categories'].__class__ == list
        assert 6 == len(data['categories'])

        assert 'current_category' in data
        assert data['current_category'] is None

        assert 'questions' in data
        assert data['questions'].__class__ == list
        assert 10 == len(data['questions'])

        first_question = data['questions'][0]
        assert first_question.__class__ == dict
        assert 'question' in first_question
        assert first_question['question'].__class__ == str
        assert first_question['question'] == "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        assert 'answer' in first_question
        assert first_question['answer'].__class__ == str
        assert first_question['answer'] == 'Maya Angelou'
        assert 'category' in first_question
        assert first_question['category'].__class__ == str
        assert first_question['category'] == 'History'
        assert 'difficulty' in first_question
        assert first_question['difficulty'].__class__ == int
        assert first_question['difficulty'] == 2


'''
2. Create an endpoint to DELETE question using a question ID. 
  
./src/components/QuestionView.js:108:          url: `/questions/${id}`, //TODO: update request URL
'''

'''
3. Create an endpoint to POST a new question,  which will require the question and answer text, category, and difficulty score.

./src/components/FormView.js:37:      url: '/questions', //TODO: update request URL
sends question, answer, difficulty, category
'''

'''
4. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 

./src/components/QuestionView.js:81:      url: `/questions`, //TODO: update request URL
sends searchTerm
expects result.questions, result.total_questions, result.current_category
'''

'''
5. Create a GET endpoint to get questions based on category. 
  
./src/components/QuestionView.js:63:      url: `/categories/${id}/questions`, //TODO: update request URL
# looks for result.questions array, result.total_questions, result.current_category
'''

'''
6. Create a POST endpoint to get questions to play the quiz. 
This endpoint should take category and previous question parameters 
and return a random questions within the given category, 
if provided, and that is not one of the previous questions. 

./src/components/QuizView.js:51:      url: '/quizzes', //TODO: update request URL
sends previousQuestions, quizCategory
expects question
'''
