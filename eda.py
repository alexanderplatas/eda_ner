# Easy data augmentation techniques for NER tasks

import random

random.seed(1)

# stop words list
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our',
              'ours', 'ourselves', 'you', 'your', 'yours',
              'yourself', 'yourselves', 'he', 'him', 'his',
              'himself', 'she', 'her', 'hers', 'herself',
              'it', 'its', 'itself', 'they', 'them', 'their',
              'theirs', 'themselves', 'what', 'which', 'who',
              'whom', 'this', 'that', 'these', 'those', 'am',
              'is', 'are', 'was', 'were', 'be', 'been', 'being',
              'have', 'has', 'had', 'having', 'do', 'does', 'did',
              'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
              'because', 'as', 'until', 'while', 'of', 'at',
              'by', 'for', 'with', 'about', 'against', 'between',
              'into', 'through', 'during', 'before', 'after',
              'above', 'below', 'to', 'from', 'up', 'down', 'in',
              'out', 'on', 'off', 'over', 'under', 'again',
              'further', 'then', 'once', 'here', 'there', 'when',
              'where', 'why', 'how', 'all', 'any', 'both', 'each',
              'few', 'more', 'most', 'other', 'some', 'such', 'no',
              'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
              'very', 's', 't', 'can', 'will', 'just', 'don',
              'should', 'now', '']


########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
########################################################################

# for the first time you use wordnet
# import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.corpus import wordnet


def synonym_replacement(conll, n):
    # Get new file name
    new_file_name = conll.split("\n")[0].split(' ')[1] + '_SR'

    # Get lines with no stopwords
    random_lines_list = list(line for line in conll.split('\n') if line.split(' ')[0].lower() not in stop_words)[1:]

    # Randomize lines
    random.shuffle(random_lines_list)

    # Start replacing synonyms
    num_replaced = 0
    for random_line in random_lines_list:

        synonyms = get_synonyms(random_line.split(' ')[0])

        # If it has synonyms
        if len(synonyms) >= 1:

            # Choose random synonym
            synonym = random.choice(list(synonyms))

            new_conll = ''
            offset = 0

            # Replace
            for line in conll.split('\n'):

                # Replace word with its synonym
                if line == random_line:

                    # If synonym has more than 1 word
                    for word in synonym.split(' '):
                        new_conll += f'{word} {offset}-{offset + len(word)} {line.split(" ")[2]}\n'
                        offset += len(word) + 1

                        # print(f"** Replaced {random_line.split(' ')[0]} with {synonym}")

                    num_replaced += 1

                elif line != '':

                    word = line.split(' ')[0]

                    # If line is the header
                    if line.split(' ')[2] == '-':
                        new_conll += f'{word} {new_file_name} {line.split(" ")[2]}\n'

                    else:
                        new_conll += f'{word} {offset}-{offset + len(word)} {line.split(" ")[2]}\n'
                        offset += len(word) + 1

            conll = new_conll

        # Only replace up to n words
        if num_replaced >= n: break

    return conll


def get_synonyms(word):

    if len(word) < 2:
        return []

    synonyms = set()

    # For each synonym
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():

            # Add name to synonyms list
            synonym = l.name().replace("_", " ").replace("-", " ").lower()
            synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm1234567890'])
            synonyms.add(synonym)

    # Remove word from synonyms
    if word in synonyms:
        synonyms.remove(word)

    return list(synonyms)


########################################################################
# Random deletion
# Randomly delete words from the sentence with probability p
########################################################################

def random_deletion(conll, p):

    # Get list of lines with no empty lines
    lines_list = list(filter(None, conll.split('\n')))

    # Write file header and new name
    new_file_name = lines_list[0].split(' ')[1] + '_RD'
    new_conll = lines_list[0].split(" ")[0] + f' {new_file_name} -\n'
    offset = 0

    # Start deleting lines with probability p
    for line in lines_list[1:]:

        if random.uniform(0, 1) > p and line != '\n' and line != '':

            # Adjust offset
            word = line.split(" ")[0]
            new_conll += f'{word} {offset}-{offset + len(word)} {line.split(" ")[2]}\n'
            offset += len(word) + 1

        # else:
            # print(f'** Deleted: {line.split(" ")[0]}')

    # if you end up deleting all words, just return a random word
    if new_conll.split('\n')[1] == '':
        # Get random index
        rand_int = random.randint(1, len(lines_list) - 1)

        # Write random line
        word = lines_list[rand_int].split(' ')[0]
        tag = lines_list[rand_int].split(' ')[2]
        new_conll += f'{word} {0}-{len(word)} {tag}'

    return new_conll


########################################################################
# Random swap
# Randomly swap two words in the sentence n times
########################################################################

def random_swap(conll, n):

    # Swap if sentence has more than 1 word
    if len(list(filter(None, conll.split('\n')))) > 2:

        new_file_name = conll.split('\n')[0].split(' ')[1] + '_RS'

        for _ in range(n):
            conll = swap_word(conll, new_file_name)

    return conll


def swap_word(conll, new_file_name):

    # Get list of lines with no empty lines
    lines_list = list(filter(None, conll.split('\n')))

    # Get random index 1
    random_idx_1 = random.randint(1, len(lines_list) - 1)
    random_idx_2 = random_idx_1

    # Get random index 2
    while random_idx_1 == random_idx_2: random_idx_2 = random.randint(1, len(lines_list) - 1)

    # Write file header
    new_conll = lines_list[0].split(" ")[0] + f' {new_file_name} -\n'

    offset = 0

    # Start swapping (random_idx_1 <-> random_idx_2)
    for i, line in enumerate(lines_list[1:]):

        if line != '\n' and line != '':

            if i + 1 == random_idx_1:
                word = lines_list[random_idx_2].split(' ')[0]
                tag = lines_list[random_idx_2].split(' ')[2]

            elif i + 1 == random_idx_2:
                word = lines_list[random_idx_1].split(' ')[0]
                tag = lines_list[random_idx_1].split(' ')[2]

            else:
                word = line.split(' ')[0]
                tag = line.split(' ')[2]

            # Adjust offset
            new_conll += f'{word} {offset}-{offset + len(word)} {tag}\n'
            offset += len(word) + 1

    # print(f'** Swapped: {lines_list[random_idx_1].split(" ")[0]} <--> {lines_list[random_idx_2].split(" ")[0]}')

    return new_conll


########################################################################
# Random insertion
# Randomly insert n words into the sentence
########################################################################

def random_insertion(conll, n):

    new_file_name = conll.split('\n')[0].split(' ')[1] + '_RI'

    for _ in range(n):
        conll = add_word(conll, new_file_name)

    return conll


def add_word(conll, new_file_name):

    # Get list of lines with no empty lines
    lines_list = list(filter(None, conll.split('\n')))

    # Write file header
    new_conll = lines_list[0].split(" ")[0] + f' {new_file_name} -\n'

    synonyms = []
    random_word = ''
    synonym_tag = ''

    # 10 attempts to find a word with synonyms
    counter = 9

    # Find a synonym of a random word
    while len(synonyms) < 1:

        random_index = random.randint(1, len(lines_list) - 1)

        # Get random word from file
        random_word = lines_list[random_index].split(' ')[0]

        # Save tag
        synonym_tag = lines_list[random_index].split(' ')[2]

        # Get synonyms of random word
        synonyms = get_synonyms(random_word)

        counter -= 1
        if counter == 0:
            return conll

    # Get a random synonym
    random_synonym = synonyms[0]

    # Get a random index
    random_idx = random.randint(0, len(lines_list) - 1)

    offset = 0

    # Start insert (random_idx <- random_synonym)
    for i, line in enumerate(lines_list[1:]):

        if i == random_idx:

            # If synonym has more than 1 word
            for word in random_synonym.split(' '):
                new_conll += f'{word} {offset}-{offset + len(word)} {synonym_tag}\n'
                offset += len(word) + 1

            # print(f'** Inserted: {random_synonym} (synonym of {random_word})')

        word = line.split(" ")[0]
        new_conll += f'{word} {offset}-{offset + len(word)} {line.split(" ")[2]}\n'
        offset += len(word) + 1

    return new_conll


########################################################################
# main data augmentation function
########################################################################

def eda(conll, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, alpha_rd=0.1, num_aug=3):

    num_words = len(conll.split('\n'))

    num_techniques_to_apply = 0
    if alpha_sr > 0: num_techniques_to_apply += 1
    if alpha_ri > 0: num_techniques_to_apply += 1
    if alpha_rs > 0: num_techniques_to_apply += 1
    if alpha_rd > 0: num_techniques_to_apply += 1

    augmented_sentences = []

    # sr
    if alpha_sr > 0:
        n_sr = max(1, int(alpha_sr * num_words))
        for _ in range(int(num_aug / num_techniques_to_apply)):
            augmented_sentences.append(synonym_replacement(conll, n_sr))

    # ri
    if alpha_ri > 0:
        n_ri = max(1, int(alpha_ri * num_words))
        for _ in range(int(num_aug / num_techniques_to_apply)):
            augmented_sentences.append(random_insertion(conll, n_ri))

    # rs
    if alpha_rs > 0:
        n_rs = max(1, int(alpha_rs * num_words))
        for _ in range(int(num_aug / num_techniques_to_apply)):
            augmented_sentences.append(random_swap(conll, n_rs))

    # rd
    if alpha_rd > 0:
        for _ in range(int(num_aug / num_techniques_to_apply)):
            augmented_sentences.append(random_deletion(conll, alpha_rd))

    return augmented_sentences
