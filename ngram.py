import nltk
from nltk.model import NgramModel
from nltk.corpus import brown, gutenberg, PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
from nltk.probability import LidstoneProbDist
from nltk.tag.simplify import simplify_wsj_tag
from collections import defaultdict
from mtools import *
from scipy import stats

estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
tokenizer = RegexpTokenizer("[\w']+")


def average_entropy_storeys(model, filename):
  with open(filename, 'r') as f:
    entropies = []
    for l in f:
      word_list = tokenizer.tokenize(l)
      if len(word_list) > 1:
        entropies.append(model.entropy(word_list))
    return ((sum(entropies) - 0.0) / len(entropies), entropies)


def average_pos_entropy_storeys(model, filename):
  with open(filename, 'r') as f:
    entropies = []
    for l in f:
      word_list = nltk.word_tokenize(l)
      if len(word_list) > 1:
        simplified = [simplify_wsj_tag(t) for _, t in nltk.pos_tag(word_list)]
        entropies.append(model.entropy(simplified))
  return ((sum(entropies) - 0.0) / len(entropies), entropies)


def average_entropy(model, filename):
  '''Get the average entropy of sentences in this file'''
  with open(filename) as f:
    entropies = []
    lines = f.read()
    for l in nltk.sent_tokenize(lines):
     word_list = tokenizer.tokenize(l)
     if len(word_list) > 1:
      entropies.append(model.entropy(word_list))
  return ((sum(entropies) - 0.0) / len(entropies), entropies)


def average_pos_entropy(model, filename):
  '''Get the average entropy of sentences in this file'''
  with open(filename) as f:
    entropies = []
    lines = f.read()
    for l in nltk.sent_tokenize(lines):
     word_list = nltk.word_tokenize(l)
     if len(word_list) > 1:
      simplified = [simplify_wsj_tag(t) for _, t in nltk.pos_tag(word_list)]
      entropies.append(model.entropy(simplified))
  return ((sum(entropies) - 0.0) / len(entropies), entropies)


def pos_distribution(filename):
  pos_counts = defaultdict(int)
  with open(filename) as f:
    lines = f.read()
    for l in nltk.sent_tokenize(lines):
      for word, tag in nltk.pos_tag(nltk.word_tokenize(l)):
        pos_counts[tag] += 1
  return mgroup.dict.percentage_sum(pos_counts)


def pos_distribution_sents(sents):
  pos_counts = defaultdict(int)
  for sentence in sents:
    for word, tag in nltk.pos_tag(sentence):
      pos_counts[tag] += 1
  return mgroup.dict.percentage_sum(pos_counts)


def num_words(filename):
  lengths = []
  with open(filename) as f:
    lines = f.read()
    for l in nltk.sent_tokenize(lines):
      lengths.append(len(nltk.word_tokenize(l)))
  return (sum(lengths) - 0.0) / len(lengths)

# Get POS Distribution

# posb = pos_distribution_sents(brown.sents(categories=['fiction']))
# pos1 = pos_distribution('data/sentences/storeys.txt')
# pos2 = pos_distribution('data/sentences/foldingstory.txt')
# pos3 = pos_distribution('data/sentences/protagonize.txt')
# pos4 = pos_distribution('data/sentences/ficly.txt')
# for k in posb.keys():
#   if k in pos1 and k in pos2 and k in pos3 and k in pos4:
#     print k, posb[k], pos1[k], pos2[k], pos3[k], pos4[k]


# Get NGram Sentence Entropy

bro = brown.words(categories=['fiction'])
bro2 = brown.words(categories=['news'])
gut = gutenberg.words()
# gutc = PlaintextCorpusReader('/Volumes/My Passport/Downloads/gutenberg-c',
#   r'(?!\.).*\.txt').words()  # Children's stories

for i in [1, 2, 3]:
  model = NgramModel(i, bro, estimator=estimator)
  print average_entropy_storeys(model, 'data/sentences/storeys_nofirst.txt')
  print average_entropy(model, 'data/sentences/foldingstory.txt')
  print average_entropy(model, 'data/sentences/protagonize.txt')
  print average_entropy(model, 'data/sentences/ficly2.txt')

  a = average_entropy_storeys(model, 'data/sentences/storeys_nofirst.txt')[1]
  b = average_entropy(model, 'data/sentences/foldingstory.txt')[1]
  c = average_entropy(model, 'data/sentences/protagonize.txt')[1]
  d = average_entropy(model, 'data/sentences/ficly2.txt')[1]
  print stats.ttest_ind(a, b)
  print stats.ttest_ind(a, c)
  print stats.ttest_ind(a, d)

# # Storeys Fiction vs. News
# for i in [1, 2, 3]:
#   bropos = brown.tagged_words(categories=['fiction'], simplify_tags=True)
#   bropos = [b for a, b in bropos]
#   bropos2 = brown.tagged_words(categories=['news'], simplify_tags=True)
#   bropos2 = [b for a, b in bropos2]
#   model1 = NgramModel(i, bro, estimator=estimator)
#   model2 = NgramModel(i, bro2, estimator=estimator)
#   modelpos1 = NgramModel(i, bropos, estimator=estimator)
#   modelpos2 = NgramModel(i, bropos2, estimator=estimator)
#   a = average_entropy_storeys(model1, 'data/sentences/storeys_nofirst.txt')[1]
#   b = average_entropy_storeys(model2, 'data/sentences/storeys_nofirst.txt')[1]
#   pa = average_entropy_storeys(modelpos1, 'data/sentences/storeys_nofirst.txt')[1]
#   pb = average_entropy_storeys(modelpos2, 'data/sentences/storeys_nofirst.txt')[1]
#   print pa
#   print pb
#   print "Storeys Fiction vs News Word", i, stats.ttest_rel(a, b)
#   print "Storeys Fiction vs News POS", i, stats.ttest_rel(pa, pb)

#
# Get NGram POS Sentence Entropy
#

bropos = brown.tagged_words(categories=['fiction'], simplify_tags=True)
bropos = [b for a, b in bropos]

for i in [1, 2, 3]:
  model = NgramModel(1, bropos, estimator=estimator)
  print average_pos_entropy_storeys(model, 'data/sentences/storeys_nofirst.txt')
  print average_pos_entropy(model, 'data/sentences/foldingstory.txt')
  print average_pos_entropy(model, 'data/sentences/protagonize.txt')
  print average_pos_entropy(model, 'data/sentences/ficly2.txt')

  a = average_pos_entropy_storeys(model, 'data/sentences/storeys_nofirst.txt')[1]
  b = average_pos_entropy(model, 'data/sentences/foldingstory.txt')[1]
  c = average_pos_entropy(model, 'data/sentences/protagonize.txt')[1]
  d = average_pos_entropy(model, 'data/sentences/ficly2.txt')[1]
  print stats.ttest_ind(a, b)
  print stats.ttest_ind(a, c)
  print stats.ttest_ind(a, d)

#
# Get NumWords
#

# print "NUMWORDS"
# print num_words('data/sentences/storeys.txt')
# print num_words('data/sentences/foldingstory.txt')
# print num_words('data/sentences/protagonize.txt')
# print num_words('data/sentences/ficly2.txt')

# MISC

# print model.entropy(['The', 'man', 'was', 'found', 'dead'])
# print model.entropy(['However', 'a', 'dragon', 'appeared', 'nearby'])
# print model.entropy(['Fluggard', 'Hogwarts', 'Harry', 'Potter', 'Meow'])

# lengths = [len(s) for s in brown.sents(categories=['fiction'])]
# print (sum(lengths) - 0.0) / len(lengths)

