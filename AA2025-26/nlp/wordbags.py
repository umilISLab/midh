"""Utilities to manage wordbags
"""
from collections import defaultdict
from typing import List
import numpy as np 
from torch.utils.data import DataLoader, TensorDataset
import torch 


class Bow:
    def __init__(self, corpus: List[list],
                min_occurrences: int = 0, 
                max_occurrences: int = 500):
        self.corpus = corpus
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences
        self.vocabulary = defaultdict(lambda: 0)
        for words in self.corpus:
            for word in words:
                self.vocabulary[word] += 1
        # filter
        self.vocabulary = [x for x, y in self.vocabulary.items() if 
                    self.min_occurrences < y < self.max_occurrences]
        self.word2idx = dict([(w, i) for i, w in enumerate(self.vocabulary)])
        self.idx2word = dict([(i, w) for i, w in enumerate(self.vocabulary)])
    
    @property
    def size(self):
        return len(self.vocabulary)
    
    def __getitem__(self, word):
        return self.word2idx[word]    

    def one_hot_skip_gram_dataloader(self,
                        window: int, 
                        batch: int = 4,
                        shuffle: bool = False):
        """Create a dataloader for one hot encoded words
        using skip-gram

        Args:
            window (int): skip-gram window
            batch (int): batch size
            shuffle (bool): if shuffle
        """
        training_set_skip_gram_input = []
        training_set_skip_gram_labels = []
        for words in self.corpus:
            for i, key in enumerate(words):
                if key in self.word2idx.keys():
                    key_vec = np.zeros(len(self.vocabulary))
                    key_vec[self[key]] = 1
                    target_vec = np.zeros(self.size)
                    for target in words[max(0, i-window):i+window+1]:
                        if target in self.word2idx.keys() and key != target:
                            target_vec[self[target]] = 1
                    training_set_skip_gram_input.append(key_vec)
                    training_set_skip_gram_labels.append(target_vec)
        inputs = torch.Tensor(np.array(training_set_skip_gram_input))
        outputs = torch.Tensor(np.array(training_set_skip_gram_labels))
        dataset = TensorDataset(inputs, outputs)
        data_loader = DataLoader(dataset, batch_size=batch, shuffle=shuffle)
        return data_loader, inputs, outputs