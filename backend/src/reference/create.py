from collections import Counter
import pymorphy3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def extract_keywords(text):
    words = word_tokenize(text.lower())
    russian_stopwords = set(stopwords.words('russian'))
    russian_stopwords.add('банка')
    return [word for word in words if word.isalnum() and word not in russian_stopwords]

def get_normal_form(word):
    morph = pymorphy3.MorphAnalyzer()
    return morph.parse(word)[0].normal_form

def find_most_similar_list(keywords, other_lists):
    keyword_counter = Counter(get_normal_form(word) for word in keywords)
    max_similarity = 0
    most_similar_list = []
    for keyword_list in other_lists:
        list_counter = Counter(get_normal_form(word) for word in keyword_list)
        similarity = sum((list_counter & keyword_counter).values())
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_list = keyword_list
    return most_similar_list

def main():
    text = "Все сообщения от банка приходят с номера с буквенным значением CENTRINVEST. Никогда не звоните по вопросам обслуживания..."
    keywords = extract_keywords(text)

    other_lists = [
        ['сообщения', 'важные', 'приходят', 'автоматически'],
        ['сообщения', 'номера', 'буквенное', 'значение'],
        ['вопросам', 'о', 'обслуживания', 'карт'],
        ['звоните', 'по', 'важным', 'вопросам']
    ]

    most_similar_list = find_most_similar_list(keywords, other_lists)
    print("Самый похожий список:", most_similar_list)

if __name__ == "__main__":
    main()
