import tkinter as tk
import tkinter.font as font
import requests
import random
import html


# This is a class for creating a quiz app with multiple and True/False questions
class QuizApp(tk.Tk):
    def __init__(self, data):
        """
        This is the initialization function for a Quiz class that sets up the initial state of the quiz.
        
        :param data: This parameter is a dictionary containing the questions and answers for the quiz.
        """
        super().__init__()

        self.data = data
        self.question_index = 0
        self.score = 0

        self.title('Quiz')
        self.geometry('600x400')

        self.create_widgets()

    def create_widgets(self):
        """
        This function creates a set of buttons with answer options for a quiz question, including one
        correct answer and several incorrect answers.
        """
        self.question_label = tk.Label(
            self,
            text=self.data[self.question_index]['question'],
            font=("Helvetica", 13),
            wraplength=400
        )
        self.question_label.pack(pady=20)

        self.answer_label = tk.Label(self, text='', font=("Helvetica", 5))
        self.answer_label.pack(pady=5)

        # Generate a random index where a correct answer will be placed
        correct_answer_index = random.randint(
            0, 
            len(self.data[self.question_index]['incorrect_answers'])
        )

        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        for i, option in enumerate(self.data[self.question_index]['incorrect_answers']):
            # Place the correct answer
            if i == correct_answer_index:
                button = tk.Button(
                    self,
                    text=self.data[self.question_index]['correct_answer'],
                    command=lambda: self.check_answer(
                        self.data[self.question_index]['correct_answer']
                    ),
                    width=20,
                    height=2,
                    wraplength=140
                )
                button.pack(pady=10)
                button['font'] = myFont

            # Place incorrect answers
            button = tk.Button(
                self,
                text=option,
                command=lambda option=option: self.check_answer(option),
                width=20,
                height=2,
                wraplength=140
            )
            button.pack(pady=10)
            button['font'] = myFont
        
        # if last answer is correct, add it
        if correct_answer_index == len(self.data[self.question_index]['incorrect_answers']):
            button = tk.Button(
                self,
                text=self.data[self.question_index]['correct_answer'],
                command=lambda: self.check_answer(
                    self.data[self.question_index]['correct_answer']
                ),
                width=20,
                height=2,
                wraplength=140
            )
            button.pack(pady=10)
            button['font'] = myFont

    def check_answer(self, choice):
        """
        This function checks the user's answer, updates the score, and displays the next question or the
        final score with an exit button.
        
        :param choice: The user's choice for the current question
        """
        if choice == self.data[self.question_index]['correct_answer']:
            self.score += 1
        self.question_index += 1

        if self.question_index < len(self.data):
            self.question_label.config(
                text=self.data[self.question_index]['question'])

            for widget in self.winfo_children():
                widget.destroy()

            self.create_widgets()
        else:
            for widget in self.winfo_children():
                widget.destroy()

            score_text = f'Your final score: {self.score}/10'
            score_label = tk.Label(self, text=score_text,
                                   font=("Helvetica", 25))
            score_label.pack(pady=80)

            myFont = font.Font(family='Helvetica', size=15, weight='bold')

            exit_button = tk.Button(
                self, 
                text='Exit', 
                command=self.quit, 
                height=1, 
                width=10
            )
            exit_button.pack(pady=60)
            exit_button['font'] = myFont


def get_questions():
    """
    This function returns a list of 10 trivia questions (5 boolean and 5 multiple choice) in a randomized order. 
    The questions are obtained from Open Trivia Database API. 
    The function also unescapes any HTML entities in the questions and answers.
    """

    url_bool = 'https://opentdb.com/api.php?amount=5&type=boolean'
    url_multiple = 'https://opentdb.com/api.php?amount=5&type=multiple'

    response_bool = requests.get(url_bool)
    response_multiple = requests.get(url_multiple)

    data_bool = response_bool.json()['results']
    data_multiple = response_multiple.json()['results']

    questions = data_multiple + data_bool
    random.shuffle(questions)

    # unescape any HTML entities in the questions and answers
    for i in range(len(questions)):
        questions[i]['question'] = html.unescape(questions[i]['question'])

        # if the question is multiple type, we unescape any HTML entities
        if questions[i]['type'] == 'multiple':
            questions[i]['correct_answer'] = html.unescape(
                questions[i]['correct_answer']
            )

            parsed_incorrect_answers = []
            for incorrect in questions[i]['incorrect_answers']:
                parsed_incorrect_answers.append(html.unescape(incorrect))

            questions[i]['incorrect_answers'] = parsed_incorrect_answers

    return questions


if __name__ == '__main__':
    questions = get_questions()
    app = QuizApp(questions)
    app.mainloop()
