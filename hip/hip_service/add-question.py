import time
from client import Database, Answer
from sqlalchemy import event

# Function to be passed as a callback, needs access to the Database instance
def make_answer_added_callback(database):
    def my_answer_added_callback(mapper, connection, target):
        print(f"New answer added with ID: {target.id} for Question ID: {target.question_id}")
        # Now do something with the answer
    # Return the callback function
    return my_answer_added_callback

if __name__ == "__main__":
    db = Database("sqlite:///QA.db")
    # Register the callback function to listen for new answers being added
    event.listen(Answer, 'after_insert', make_answer_added_callback(db))
    # Delete questions q1 and q2 if they exist
    # db.delete_answer("q1")
    # db.delete_answer("q2")
    # db.delete_question("q1")
    # db.delete_question("q2")

    db.create_question(id="q1", label="What is the capital of France?",
                       type="select", value="France is a country in Europe. Its capital is Paris.", options=["Paris", "London", "Berlin", "Madrid"], image="https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg")
    db.create_question(id="q2", label="What is the capital of Germany?",
                          type="text", value="Germany is a country in Europe. Its capital is Berlin.", image="https://upload.wikimedia.org/wikipedia/en/b/ba/Flag_of_Germany.svg")
    
    # db.create_answer(id="q1", answer="Paris", question_id="q1")
    # db.create_answer(id="q2", answer="Berlin", question_id="q2")
