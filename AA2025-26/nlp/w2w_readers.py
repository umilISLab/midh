from wordbags import Bow
from wordvec import Word2WordPrediction
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import pandas as pd 
import numpy as np
import torch


class WordEmbeddings:
    def __init__(self, words: Bow, model: Word2WordPrediction):
        self.bow = words
        self.w2w = model
        self.sigma = cosine_similarity(self.w2w.vectors, self.w2w.vectors)
        self.sim = pd.DataFrame(self.sigma, 
                                index=self.bow.vocabulary, 
                                columns=self.bow.vocabulary)
        
    def __getitem__(self, word: str):
        return self.w2w.get_vector(self.bow[word])
    
    def most_similar(self, word: str, topk: int = 10):
        return self.sim.loc[word].sort_values(ascending=False).head(topk)
    
    def predict(self, word: str, topk: int = 10):
        vector = np.zeros(self.bow.size)
        vector[self.bow.word2idx[word]] = 1
        y_pred = pd.Series(self.w2w(torch.Tensor(vector)).detach().numpy(), 
                        index=self.bow.vocabulary
                        ).sort_values(ascending=False).head(topk)
        return y_pred
    
    def vectors(self, words: List[str]):
        return self.w2w.vectors[[self.bow[w] for w in words]]
    
    def analogy(self, a: str, b: str, c: str):
        positive = self.vectors([a, c]).sum(axis=0)
        negative = self.vectors([b]).sum(axis=0)
        answer = positive - negative 
        sigma = cosine_similarity(np.array([answer]), self.w2w.vectors)
        i = np.argmax(sigma[0])
        return self.bow.idx2word[i], answer
    
    def vector_similarity(self, query: np.ndarray, topk: int = 10):
        sigma = cosine_similarity(np.array([query]), self.w2w.vectors)
        output = pd.Series(sigma[0], index=self.bow.vocabulary)
        return output.sort_values(ascending=False).head(topk)
    
    def search(self, positive: List[str], negative: List[str] = None, 
            topk: int = 10):
        positive_v = self.vectors(positive).sum(axis=0)
        if negative is not None:
            negative_v = self.vectors(negative).sum(axis=0)
            answer_v = positive_v - negative_v 
        else:
            answer_v = positive_v
        sigma = cosine_similarity(np.array([answer_v]), self.w2w.vectors)
        output = pd.Series(sigma[0], index=self.bow.vocabulary)
        return output.sort_values(ascending=False).head(topk)
    
    def spot_odd_one(self, words: List[str]):
        word_v = self.vectors(words=words)
        center_v = word_v.mean(axis=0)
        sigma = cosine_similarity(np.array([center_v]), word_v)
        return pd.Series(sigma[0], index=words).sort_values(ascending=True)
        
    def common_meanings(self, words: List[str], topk: int = 10):
        word_v = self.vectors(words=words)
        center_v = word_v.mean(axis=0)
        return self.vector_similarity(center_v, topk=topk)
        
        
