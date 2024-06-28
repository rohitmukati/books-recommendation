from flask import Flask,render_template,request
import pickle
import pandas
import numpy as np

popular_df = pandas.read_pickle(open('popular.pkl','rb'))
pt = pandas.read_pickle(open('pt.pkl','rb'))
books = pandas.read_pickle(open('books.pkl','rb'))
similarity_score = pandas.read_pickle(open('similarity_scores.pkl','rb'))





##Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')



@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)






@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/content')
def content():
    return render_template('content.html', book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-S'].values),
                           votes = list(popular_df['num_ratings'].values),
                           ratings = list(popular_df['avg_ratings'].values),
                           )

if __name__ == '__main__':
    app.run(debug="True")