import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template, jsonify
import gensim.downloader as api
import regex as re
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load the Word2Vec model
model = api.load("word2vec-google-news-300")

# Function to get data from Excel file
def get_data():
    xls = pd.ExcelFile('MacPherson Feeding Logs.xlsx')
    carbon_index = pd.read_excel(xls, 'Emission Carbon Index')
    df2 = pd.read_excel(xls, 'Sep to Dec 2023')
    df3 = pd.read_excel(xls, 'Jan to Jun 2024')

    # Set the new header for carbon_index
    new_header = carbon_index.iloc[0]  # This is the first row for the header
    carbon_index = carbon_index[1:]  # Take the data less the header row
    carbon_index.columns = new_header  # Set the header row as the dataframe header

    # Drop the 'S/N' column
    carbon_index.drop('S/N', axis=1, inplace=True)

    tank1 = df2['Tank 1']
    return carbon_index, df2, df3, tank1

# Function to remove 'distilled water' segment
def remove_distilled_water(text):
    return re.sub(r'\d+g of distilled water,?\s*', '', text)

# Function to create a quantity dictionary
def quantity_dictionary(row):
    if pd.notna(row):
        numerical_values = re.findall(r'\d+', row)
        return numerical_values
    return []

# Function to split text and filter unwanted words
def split_text(row):
    unwanted_words = {'of', 'dry', 'dried', 'wet', 'crushed', 'tops', 'tops,', 'skins', 'skins,', 'coffee'}
    if pd.notna(row):
        if isinstance(row, list):
            row = ' '.join(row)
        words = row.split(" ")
        filtered_words = [word for word in words if not any(char.isdigit() for char in word) and word.lower() not in unwanted_words]
        cleaned_list = [item.strip(',') for item in filtered_words if item.strip(',')]
        return cleaned_list
    return []

# Function to process the data
def data_processing(tank1):
    carbon_index, df2, df3, tank1 = get_data()
    food_dict = carbon_index['Food Name'].to_dict()
    food_info = carbon_index.set_index('Food Name').T.to_dict('list')

    tank1 = tank1.str.replace('1 spoon', '15g')
    tank1 = pd.DataFrame(tank1)
    tank1['Tank 1'] = tank1['Tank 1'].str.replace('\n', ', ').str.replace('(', ' ').str.replace(')', ' ')
    tank1['Tank 1'] = tank1['Tank 1'].astype(str)
    tank1['Tank 1'] = tank1['Tank 1'].apply(remove_distilled_water)

    quantity_dict = tank1['Tank 1'].apply(quantity_dictionary)
    df_split = tank1['Tank 1'].apply(split_text)

    for i in range(len(df_split)):
        for j in range(len(df_split[i])):
            if df_split[i][j] == "grinds":
                df_split[i][j] = "Coffee Grounds"
            if df_split[i][j] == "grounds":
                df_split[i][j] = "Grounded Coffee"

    processed_sentences = df_split.copy()
    return food_dict, food_info, tank1, quantity_dict, processed_sentences

# Function to get vector for a phrase
def get_phrase_vector(phrase, model):
    words = phrase.lower().split()
    vectors = [model[word] for word in words if word in model]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(model.vector_size)

# Function to train the model
def model_training(model, food_dict):
    word_list_vectors = {phrase: get_phrase_vector(phrase, model) for phrase in food_dict.values()}
    return word_list_vectors

# Function to process the list
def process_list(word_list, model, word_list_vectors):
    return [find_most_similar_phrase(word, model, word_list_vectors) for word in word_list]

# Function to find the most similar phrase
def find_most_similar_phrase(phrase, model, word_list_vectors):
    phrase_vector = get_phrase_vector(phrase, model)
    similarities = {key: cosine_similarity([phrase_vector], [vector])[0][0] for key, vector in word_list_vectors.items()}
    sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
    most_similar_phrase = sorted_similarities[0][0] if sorted_similarities and sorted_similarities[0][1] > 0.5 else None
    return most_similar_phrase

# Function to calculate word similarity and carbon values
def word_similarity(processed_sentences, food_info, quantity_dict, model, word_list_vectors):
    data = {'Tank 1': processed_sentences}
    df = pd.DataFrame(data)
    df['Replaced Phrases'] = df['Tank 1'].apply(lambda x: process_list(x, model, word_list_vectors))

    for row in df['Replaced Phrases']:
        for item in row:
            if item is None:
                row.remove(item)

    row_list = []
    for index_number, row in enumerate(df['Replaced Phrases']):
        row_values = 0
        if row is not None:
            for dict_number, item in enumerate(row):
                carbon_value = food_info[item][0]
                quantity = float(quantity_dict[index_number][dict_number])
                row_values += carbon_value * quantity
        row_list.append(row_values)

    df['Carbon Value (g)'] = row_list
    return df

@app.route('/')
def index():
    return render_template('carbon.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_data = request.form['compostInput']
    # Here you would process the input_data as required
    carbon_index, df2, df3, tank1 = get_data()
    food_dict, food_info, tank1, quantity_dict, processed_sentences = data_processing(tank1)
    word_list_vectors = model_training(model, food_dict)
    df = word_similarity(processed_sentences, food_info, quantity_dict, model, word_list_vectors)
    carbon_value = df['Carbon Value (g)'].sum()
    return jsonify({'Total Carbon Value (g)': carbon_value})

if __name__ == '__main__':
    app.run(port=5002, debug=True)
