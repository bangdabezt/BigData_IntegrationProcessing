from flask import Flask, render_template, request
from gemini import query_sth
import pandas as pd

app = Flask(__name__)

# Load the CSV data into a DataFrame
data = pd.read_csv('./data/merge.csv')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    question = request.form.get('question')
    answer = ""
    show_table = True

    # If no query is provided, return all records
    if not query:
        results = data
    else:
        # Filter the results based on the provided query across all fields
        results = data[
            data['isbn'].str.contains(query, case=False, na=False) |
            data['book_title'].str.contains(query, case=False, na=False) |
            data['author'].str.contains(query, case=False, na=False) |
            data['publisher'].str.contains(query, case=False, na=False) |
            data['year'].astype(str).str.contains(query, case=False, na=False)
        ]

    # Provide an answer based on the question
    if question:
        show_table = False  # Hide the table if a question is asked
        answer = query_sth(question)

    return render_template('home.html', query=query, question=question, results=results.to_dict(orient='records'), answer=answer, show_table=show_table)

if __name__ == '__main__':
    app.run(debug=True)
