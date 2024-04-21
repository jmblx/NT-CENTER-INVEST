from difflib import SequenceMatcher
import pandas as pd
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
stemmer = SnowballStemmer("russian")

def preprocess_text(text):
    tokens = word_tokenize(text, language='russian')
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)

file_path = 'dataset_without_links.csv'
data = pd.read_csv(file_path)

# Предобработка вопросов в датасете
data['processed_question'] = data['question'].apply(preprocess_text)

def match_question(user_query, data=data):
    """
    Сравнивает запрос пользователя с обработанными вопросами из датасета и возвращает самый подходящий ответ.
    """
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    processed_query = preprocess_text(user_query)
    data['similarity'] = data['processed_question'].apply(lambda x: similarity(x, processed_query))
    
    threshold = 0.75 * data['similarity'].max()
    relevant_data = data[data['similarity'] >= threshold].copy()
    relevant_data.sort_values('similarity', ascending=False, inplace=True)
    
    if not relevant_data.empty:
        top_match = relevant_data.iloc[0]
        return f"{top_match['answer']}"
    else:
        return "Подходящих ответов не найдено."
