'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2): # Good to go
    sum1 = 0
    sum2 = 0
    for key in vec1:
        sum1 += vec1[key]**2
    for key in vec2:
        sum2 += vec2[key]**2

    num = 0
    for key in vec1:
        if key in vec2:
            num += vec1[key]*vec2[key]

    similarity = num / math.sqrt(sum1 * sum2)

    return similarity

import copy

# sentences will be a list composed of lists which represent sentences
# Example: [["I", "am", "a", "dude"], ["I", "like", "icecream"]]
def build_semantic_descriptors(sentences): # needs some tweaking
    dict = {}
    for i in range(len(sentences)):
        sentence_set = sorted(set(sentences[i]))
        list_thing = sorted(list(sentence_set))
        for n in range(len(list_thing)):
            word = list_thing[n]

            if word not in dict.keys():
                dict[word] = {}

            sentence_copy = copy.deepcopy(list_thing) # make a deep copy of the sentence list
            sentence_copy.remove(word)

            for k in range(len(sentence_copy)):
                if sentence_copy[k] not in dict[word].keys():
                    dict[word][sentence_copy[k]] = 1
                elif sentence_copy[k] in dict[word].keys():
                    dict[word][sentence_copy[k]] += 1
                else:
                    pass
    return dict

def build_semantic_descriptors_from_files(filenames):
    placeholder = []
    for file_i in filenames:
        file = open(file_i, "r", encoding="latin1")
        data = file.read()
        sentence = ""
        for i in range(len(data)):
            if data[i].isalpha():
                sentence += data[i].lower()
            elif data[i].isnumeric():
                sentence += data[i]
            elif data[i] == "." or data[i] == "?" or data[i] == "!":
                sentence += "."
            elif data[i] == "," or data[i] == ";" or data[i] == ":" or data[i] == "-":
                sentence += " "
            elif data[i] == "--":
                sentence += " "
            elif data[i] == " ":
                sentence += data[i]

        sentence = sentence.lower()
        list_of_sentences = sentence.split(".") # create a list where each element is a string representing each sentence

        for sentence in list_of_sentences:
            list_words = sentence.split()
            placeholder.append(list_words)
        del placeholder[-1]

    semantic = build_semantic_descriptors(placeholder)
    return semantic


def most_similar_word(word, choices, semantic_descriptors, similarity_fn): # fix this and edit the code
    similarities_value = []
    words = []
    for each_option in choices:
        if each_option in semantic_descriptors.keys():
            candidate = semantic_descriptors[word]
            option = semantic_descriptors[each_option]
            cos_sim = similarity_fn(candidate, option)
            words.append(each_option)
            similarities_value.append(cos_sim)
        else:
            words.append(each_option)
            similarities_value.append(-1)

    most_value = max(similarities_value)
    index = similarities_value.index(most_value)
    most_similar = words[index]
    return most_similar

def run_similarity_test(filename, semantic_descriptors, similarity_fn): # Fix this entire function
    file = open(filename, "r", encoding="latin1")
    sentences = file.read().split("\n")
    correct = 0
    tot = 0
    for i in range(len(sentences)):
        sentence = sentences[i].split()
        if sentence == [] or sentence == [""]: # if the sentence is a blank, skip it
            continue
        else:
            contestant = sentence[0]
            answer = sentence[1]
            options = sentence[2:]

            guess = most_similar_word(contestant, options, semantic_descriptors, cosine_similarity)
            tot += 1
            if guess == answer:
                correct += 1
    percent  = (correct/tot) * 100
    return percent


if __name__ == "__main__":
    #print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))
#     L = [["i", "am", "a", "sick", "man"],
# ["i", "am", "a", "spiteful", "man"]]
#     print(build_semantic_descriptors(L))
#     filename2 = r"C:\Users\YamHo Jobs\PyZo Projects\Projects\Project 3\text2.txt"
#     build_semantic_descriptors_from_files([filename, filename2])
#     print(most_similar_word("sahel", ["yoonho", "icecream", "hamza"], {'sahel': {'hi': 1, 'my': 1, 'name': 1, 'is': 1, 'hamza': 1}, 'yoonho': {'hello': 1, 'my': 1, 'name': 1, 'is': 1}, 'i':{'like': 3, 'to': 1, 'eat': 2, 'icecream': 1, 'but': 1, 'it': 2, 'hurts': 1, 'my': 2, 'stomach': 1, 'so': 2, 'dont': 1, 'too': 1, 'much': 2, 'chicken': 1, 'a': 1, 'lot': 1, 'that': 1, 'ate': 1, 'pet': 1, 'duck': 1}, 'icecream': {'i': 1, 'like': 1, 'to': 1, 'eat': 1, 'but': 1, 'it': 1, 'hurts': 1, 'my': 1, 'stomach': 1}, 'hamza': {'hi': 1, 'my': 1, 'name': 1, 'is': 1, 'sahel': 1}}, cosine_similarity))
    filename = r"C:\Users\YamHo Jobs\PyZo Projects\Projects\Project 3\text.txt"
    WP  = r"C:\Users\YamHo Jobs\PyZo Projects\Projects\Project 3\wp.txt"
    SW = r"C:\Users\YamHo Jobs\PyZo Projects\Projects\Project 3\sw.txt"
    sem_descriptors = build_semantic_descriptors_from_files([WP, SW])
    res = run_similarity_test(filename, sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")