import random
import math
import string
import collections

unigram_model = dict()
frequencies_unigram = dict()
smoothed_unigram_model = dict()

bigram_model = dict()
frequencies_bigram = dict()
smoothed_bigram_model = dict()

trigram_model = dict()
frequencies_trigram = dict()
smoothed_trigram_model = dict()

# preprocessing of data such as removing punctiations, making every char lower etc.
def preprocess(folderPath, temp_list):
    count = 0                   #for changing size of train data. If you want to see faster result uncomment 21, 24, 25 and 38. lines
    with open(folderPath, "r") as f:
        for line in f.readlines():
            if(count == 1000):      # you can change the number of lines which program reads from file
                 break
            if("|" in line):            #for the words in the last sentences of every part
                temp_line_list = line.split()
                temp_line_list.pop()
                temp_word = temp_line_list[len(temp_line_list)-1]
                temp_line_list.pop()
                new_line = ""
                for item in temp_line_list:
                    new_line += " " + item
                new_line = new_line.replace("XXXXX", temp_word)         # replace XXXXX with the correct word
                line = new_line
            line = line.translate(str.maketrans('', '', string.punctuation + string.digits))    #remove punctions and unnecessary digits
            temp_list.append(line.rstrip('\n').lower())                 #make them lower
            count += 1
    return temp_list

# simple sentences to words function
def sentences_to_words(sentences_list):
    temp_list = list()
    for sentence in sentences_list:
        sentence = sentence.split()
        for word in sentence:
            temp_list.append(word)
    return temp_list

# for adding <s> and </s> to the sentences
def add_sentence_start_end(sentences_list):
    temp_list = list()
    for sentence in sentences_list:
        sentence = "<s>" + sentence + "</s>"
        temp_list.append(sentence)
    return temp_list

# starter function
# Input: Path of training file
# Output: Preprocessed sentences of training file with <s> and </s>
def dataset(folderPath):
    temp_list = list()
    temp_list = preprocess(folderPath, temp_list)
    return temp_list

# for finding frequencies of ngrams.
# Input: unigram n = 1, for bigram n = 2, for trigram n = 3.
# Output: returns dictionary
def find_frequencies(n):
    all_pairs = list()
    for sentence in sentences_list_with_start_end:
        words = sentence.split()
        pairs = zip(*[words[i:] for i in range(n)])             # creating pairs for Ngram
        all_pairs.append([" ".join(pair) for pair in pairs])
    frequencies_dict = dict()
    for pair in all_pairs:
        for pai in pair:
            if (pai in frequencies_dict):                   # If this pair is already exist in the dict: increase the value by +1
                newFrequency = frequencies_dict[pai] + 1
                frequencies_dict.update({pai: newFrequency})
            else:                                           # If this pair is not already exist in the dict: create and make its value 1
                frequencies_dict.update({pai: 1})
    return frequencies_dict

# Generating Ngrams
# Input: unigram n = 1, for bigram n = 2, for trigram n = 3.
# Output: Ngram models (ordered dictionary)
def NGram(n):
    if(n==1):   #unigram
        for word, count in frequencies_unigram.items():
            unigram_model[word] = count / sum(frequencies_unigram.values())
        sorted_y = sorted(unigram_model.items(), key=lambda kv: kv[1])
        sorted_model_unigram = collections.OrderedDict(sorted_y)
        return sorted_model_unigram

    if (n==2):
        for pair, count in frequencies_bigram.items():
            words = pair.split()
            bigram_model[pair] = count / frequencies_unigram[words[0]]
        sorted_z = sorted(bigram_model.items(), key=lambda kv: kv[1])
        sorted_model_bigram = collections.OrderedDict(sorted_z)
        return sorted_model_bigram

    if (n==3):
        for pair, count in frequencies_trigram.items():
            words = pair.split()
            bigram_pair = words[0] + " " + words[1]
            trigram_model[pair] = count / frequencies_bigram[bigram_pair]
        sorted_z = sorted(trigram_model.items(), key=lambda kv: kv[1])
        sorted_model_trigram = collections.OrderedDict(sorted_z)
        return sorted_model_trigram

# For generating the next word randomly according to model
# Input: Dictionary (model which is looking forward to next word)
# Output: String (generated next word)
def next(dict):
    total = 0
    for key, value in dict.items():
        total += float(value)
    random_probability = random.uniform(0, total)       # create random number
    temp = 0
    for word, probability in dict.items():
        if temp + float(probability) > random_probability: # When you reach the random number take the word.
            return word
        temp += float(probability)              # else keep looking for word.

# For generating sentences.
# Input: Length = number of words in the one sentence. Count = number of sentences. N = Ngram model
# Output: String Array (Generated sentences)
def generate(length, count, n):
    if(n==1):
        sentences_list = list()
        for j in range(count):      # number of sentence
            sentence_list = list()
            for i in range(length): # number of words in the one sentence
                generated_word = next(unigram_model)
                if (generated_word == "<s>" or generated_word == "<s></s>"):    # If generated word is start or end token ignore and create new one
                    while (generated_word == "<s>" or generated_word == "<s></s>"):
                        generated_word = next(unigram_model)
                if (generated_word == "</s>"):      # If generated word is end token
                    if (len(sentence_list) == 0):   # If the first generated word is end token then create new sentence
                        return generate(length, count, n)
                    else:                           # If the generated end token is not the first word then finish the sentence.
                        break
                sentence_list.append(generated_word)
            sentence_list[0] = sentence_list[0].capitalize()            # Make the first char of sentence capitalize.
            sentence = ' '.join(sentence_list)
            sentence += "."                                             # Add dot to the end of the sentence
            sentences_list.append(sentence)
        return sentences_list

    if(n==2):
        sentences_list = list()
        for j in range(count):          # number of sentence
            sentence_list = list()
            current_word = "<s>"        # starting with start token <s>
            next_word = ""
            for i in range(length):     # number of words in the one sentence
                temp_dict = dict()
                for key, value in bigram_model.items():
                    if (key.split()[0] == current_word):        # take the possible next words according to the current word
                        temp_dict.update({key.split()[1]: value})
                next_word = next(temp_dict)
                if (next_word == "</s>"):                   # If the next word is end token then finish the sentence.
                    break
                sentence_list.append(next_word)
                current_word = next_word
            sentence_list[0] = sentence_list[0].capitalize()
            sentence = ' '.join(sentence_list)
            sentence += "."
            sentences_list.append(sentence)
        return sentences_list

    if(n==3):
        sentences_list = list()
        for j in range(count):
            sentence_list = list()
            first_word = "<s>"
            middle_word = ""
            next_word = ""
            bool_flag = True
            for i in range(length):
                temp_dict = dict()
                if (first_word == "<s>" and bool_flag):     # for creating the first sentence of trigram, I look for the bigram
                    for key, value in bigram_model.items():
                        if (key.split()[0] == first_word):
                            temp_dict.update({key.split()[1]: value})
                    next_word = next(temp_dict)
                    middle_word = next_word
                    bool_flag = False
                    if (next_word == "</s>"):
                        break
                else:
                    for key, value in trigram_model.items():
                        if (key.split()[0] == first_word and key.split()[1] == middle_word):
                            temp_dict.update({key.split()[2]: value})
                    first_word = middle_word
                    next_word = next(temp_dict)
                    middle_word = next_word
                    if (next_word == "</s>"):
                        break
                sentence_list.append(next_word)
            sentence_list[0] = sentence_list[0].capitalize()
            sentence = ' '.join(sentence_list)
            sentence += "."
            sentences_list.append(sentence)
        return sentences_list

# For finding probability of given sentence
# Input String: sentence and N: Ngram
# Output Probability of given sentence
def prob(sentence, n):
    if(n==1):
        mle_probability_unigram = 0
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))    # preprocessing of given sentence
        sentence = "<s> " + sentence + " </s>"
        sentence_words = sentence.split()
        sentence_words[1] = sentence_words[1].lower()
        for word in sentence_words:
            mle_probability_unigram += math.log(unigram_model[word], 2)
        return mle_probability_unigram

    if(n==2):
        mle_probability_bigram = 0
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = "<s> " + sentence + " </s>"
        sentence_words = sentence.split()
        sentence_words[1] = sentence_words[1].lower()
        for i in range(len(sentence_words) - 1):
            word_pair = sentence_words[i] + " " + sentence_words[i + 1]
            try:
                mle_probability_bigram += math.log(bigram_model[word_pair], 2)
            except:             # If this pair is not exist in biagram_model than calculate smoothed value.
                mle_probability_bigram += math.log(1 / (frequencies_unigram[sentence_words[i]] + len(bigram_model.keys())), 2)
        return mle_probability_bigram

    if(n==3):
        trigram_pairs = list()
        mle_probability_trigram = 0
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = "<s> " + sentence + " </s>"
        sentence_words = sentence.split()
        sentence_words[1] = sentence_words[1].lower()
        pairs = zip(*[sentence_words[i:] for i in range(3)])
        trigram_pairs.append([" ".join(pair) for pair in pairs])
        for sentence in trigram_pairs:  # loop only once
            for trigram_pair in sentence:
                if (trigram_pair.split()[0] == "<s>"):      # If it is the first word of sentence then check bigram prob since
                                                                # I created the first sentence according to bigram
                    try:
                        mle_probability_trigram += math.log(bigram_model[trigram_pair.split()[0] + " " + trigram_pair.split()[1]], 2)
                    except:             # If this pair is not in the bigram model then calculate smoothed value
                        mle_probability_trigram += math.log(1 / (frequencies_unigram[trigram_pair.split()[0]] + len(unigram_model.keys())), 2)
                else:
                    try:
                        mle_probability_trigram += math.log(trigram_model[trigram_pair], 2)
                    except:         # If this pair is not in the bigram model then calculate smoothed value
                        bigram_pair = trigram_pair.split()[0] + " " + trigram_pair.split()[1]
                        try:
                            mle_probability_trigram += math.log(1 / (frequencies_bigram[bigram_pair] + len(trigram_model.keys())), 2)
                        except:     # If this pair is not in the bigram model then calculate smoothed value
                            mle_probability_trigram += math.log(1 / (sum(frequencies_bigram.values()) + len(trigram_model.keys())), 2)
        return mle_probability_trigram

# For finding smoothed probability of given sentence
# Input String: sentence and N: Ngram
# Output smoothed probability of given sentence
def sprob(sentence, n):             # This function is almost same with prob function: only difference is this function uses
                                        # smoothed models
    if (n == 1):
        smoothed_probability_unigram = 0
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = "<s> " + sentence + " </s>"
        sentence_words = sentence.split()
        sentence_words[1] = sentence_words[1].lower()
        for word in sentence_words:
            smoothed_probability_unigram += math.log(smoothed_unigram_model[word], 2)
        return smoothed_probability_unigram

    if (n == 2):
        smoothed_probability_bigram = 0
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = "<s> " + sentence + " </s>"
        sentence_words = sentence.split()
        sentence_words[1] = sentence_words[1].lower()
        for i in range(len(sentence_words) - 1):
            word_pair = sentence_words[i] + " " + sentence_words[i + 1]
            try:
                smoothed_probability_bigram += math.log(smoothed_bigram_model[word_pair], 2)
            except:
                smoothed_probability_bigram += math.log(
                    1 / (frequencies_unigram[sentence_words[i]] + len(smoothed_bigram_model.keys())), 2)
        return smoothed_probability_bigram

    if (n == 3):
        trigram_pairs = list()
        smoothed_probability_trigram = 0
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = "<s> " + sentence + " </s>"
        sentence_words = sentence.split()
        sentence_words[1] = sentence_words[1].lower()
        pairs = zip(*[sentence_words[i:] for i in range(3)])
        trigram_pairs.append([" ".join(pair) for pair in pairs])
        for sentence in trigram_pairs:  # loop only once
            for trigram_pair in sentence:
                try:
                    smoothed_probability_trigram += math.log(smoothed_trigram_model[trigram_pair], 2)
                except:
                    bigram_pair = trigram_pair.split()[0] + " " + trigram_pair.split()[1]
                    try:
                        smoothed_probability_trigram += math.log(
                            1 / (frequencies_bigram[bigram_pair] + len(smoothed_trigram_model.keys())), 2)
                    except:
                        smoothed_probability_trigram += math.log(1 / (0 + len(smoothed_trigram_model.keys())), 2)
        return smoothed_probability_trigram

# For finding perplexity of given sentence
# Input String: sentence and N: Ngram
# Output perplexity of given sentence
def ppl(sentence, n):
    if (n == 1):
        sentence_word_count = len(sentence.split())
        perplexity_unigram = math.pow(2, (prob(sentence, n) * (-1)) / sentence_word_count)
        return perplexity_unigram

    if (n == 2):
        sentence_word_count = len(sentence.split())
        perplexity_bigram = math.pow(2, (prob(sentence, n) * (-1)) / sentence_word_count)
        return perplexity_bigram

    if (n == 3):
        sentence_word_count = len(sentence.split())
        perplexity_trigram = math.pow(2, (prob(sentence, n) * (-1)) / sentence_word_count)
        return perplexity_trigram

# For creating smoothed Ngrams
# Input: unigram n = 1, for bigram n = 2, for trigram n = 3.
# Output: Smoothed Ngram models (ordered dictionary)
def smoothed_ngram(n):
    if(n==1):
        for word, count in frequencies_unigram.items():
            smoothed_unigram_model[word] = (count + 1) / (
                        sum(frequencies_unigram.values()) + len(frequencies_unigram.keys()))
        sorted_y = sorted(smoothed_unigram_model.items(), key=lambda kv: kv[1])
        sorted_smoothed_model_unigram = collections.OrderedDict(sorted_y)
        return sorted_smoothed_model_unigram

    if(n==2):
        for pair, count in frequencies_bigram.items():
            words = pair.split()
            smoothed_bigram_model[pair] = (count + 1) / (frequencies_unigram[words[0]] + len(bigram_model.keys()))
        sorted_z = sorted(smoothed_bigram_model.items(), key=lambda kv: kv[1])
        sorted_smoothed_model_bigram = collections.OrderedDict(sorted_z)
        return sorted_smoothed_model_bigram

    if(n==3):
        for pair, count in frequencies_trigram.items():
            words = pair.split()
            bigram_pair = words[0] + " " + words[1]
            trigram_model[pair] = (count + 1) / (frequencies_bigram[bigram_pair] + len(trigram_model.keys()))
        sorted_z = sorted(trigram_model.items(), key=lambda kv: kv[1])
        sorted_smoothed_model_trigram = collections.OrderedDict(sorted_z)
        return sorted_smoothed_model_trigram

if __name__ == '__main__':

    folderPath = "/Users/ahmetbayrak/Desktop/assignment1-dataset.txt"

    sentences_list = list()
    sentences_list = dataset(folderPath)

    sentences_list_with_start_end = list()
    sentences_list_with_start_end = add_sentence_start_end(sentences_list)

    all_words_list = list()
    all_words_list = sentences_to_words(sentences_list_with_start_end)



#########

    frequencies_unigram = dict()
    frequencies_unigram = find_frequencies(1)
    unigram_model = NGram(1)
    smoothed_unigram_model = smoothed_ngram(1)

###

    frequencies_bigram = find_frequencies(2)
    bigram_model = NGram(2)
    smoothed_bigram_model = smoothed_ngram(2)

#####

    frequencies_trigram = find_frequencies(3)
    trigram_model = NGram(3)
    smoothed_trigram_model = smoothed_ngram(3)

    generated_sentences_unigram = generate(15, 2, 1)
    generated_sentences_bigram = generate(15, 2, 2)
    generated_sentences_trigram = generate(15, 2, 3)

    result_output = open("result.txt", "w")

    result_output.write("Perplexity of unigram generated sentence:\n")
    result_output.write("For unigram function: " + str(ppl(generated_sentences_unigram[0], 1)) + "\n")
    result_output.write("For bigram function: " + str(ppl(generated_sentences_unigram[0], 2)) + "\n")
    result_output.write("For trigram function: " + str(ppl(generated_sentences_unigram[0], 3)) + "\n")

    result_output.write("Perplexity of bigram generated sentence:\n")
    result_output.write("For unigram function: " + str(ppl(generated_sentences_bigram[0], 1)) + "\n")
    result_output.write("For bigram function: " + str(ppl(generated_sentences_bigram[0], 2)) + "\n")
    result_output.write("For trigram function: " + str(ppl(generated_sentences_bigram[0], 3)) + "\n")

    result_output.write("Perplexity of trigram generated sentence:\n")
    result_output.write("For unigram function: " + str(ppl(generated_sentences_trigram[0], 1)) + "\n")
    result_output.write("For bigram function: " + str(ppl(generated_sentences_trigram[0], 3)) + "\n")
    result_output.write("For trigram function: " + str(ppl(generated_sentences_trigram[0], 2)) + "\n")

    result_output.write("Probability of unigram generated sentences:\n\n")
    for sentence in generated_sentences_unigram:
        result_output.write("Sentence: " + str(sentence) + "\n")
        result_output.write("For unigram function:" + str(prob(sentence, 1)) + "\n")
        result_output.write("For bigram function:" + str(prob(sentence, 2)) + "\n")
        result_output.write("For trigram function:" + str(prob(sentence, 3)) + "\n")
        result_output.write("\n\n")

    result_output.write("\n")

    result_output.write("Probability of bigram generated sentences:\n\n")
    for sentence in generated_sentences_bigram:
        result_output.write("Sentence: " + str(sentence) + "\n")
        result_output.write("For unigram function:" + str(prob(sentence, 1)) + "\n")
        result_output.write("For bigram function:" + str(prob(sentence, 2)) + "\n")
        result_output.write("For trigram function:" + str(prob(sentence, 3)) + "\n")
        result_output.write("\n\n")

    result_output.write("\n")

    result_output.write("Probability of trigram generated sentences:\n\n")
    for sentence in generated_sentences_trigram:
        result_output.write("Sentence: " + str(sentence) + "\n")
        result_output.write("For unigram function:" + str(prob(sentence, 1)) + "\n")
        result_output.write("For bigram function:" + str(prob(sentence, 3)) + "\n")
        result_output.write("For trigram function:" + str(prob(sentence, 2)) + "\n")
        result_output.write("\n\n")

    result_output.write("\n")