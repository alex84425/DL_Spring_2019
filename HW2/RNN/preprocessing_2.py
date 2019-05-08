from torch.autograd import Variable
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import torch

import pandas as pd
import numpy as np
import os

############# GLOBAL DEF #############
"""
override the dataset class for custom dataset
"""
f_1 = 'paper/ICLR_accepted.csv'
f_2 = 'paper/ICLR_rejected.csv'
N_VEC_SIZE = 10

############# WORD EMBEDDING ###########
word_dict = dict()
word_dict['XXX'] = 0  # padding for the empty word in fixed length sentence
dict_cnt = 1
dbg_cnt = 0
longest_sentence_len = 0
longest_sentence = []


class custom_dataset(Dataset):
    def __init__(self, f_name, file_cnt):
        self.data = pd.read_csv(f_name)
        self.data = np.array(self.data)
        # remove the first number column
        self.data = np.delete(self.data, 0, 1)
        self.data_tensor = self.sentence2tensor()
        print(self.data.shape, self.data)
        if file_cnt == 0:
            self.labels = np.zeros((len(self.data), ), dtype=int)
        else:
            self.labels = np.ones((len(self.data), ), dtype=int)
        #print(self.labels)

    def __getitem__(self, index):
        title = self.data[index]
        title_tensor = self.data_tensor[index]
        label = self.labels[index]
        return title, title_tensor, label

    def __len__(self):
        return len(self.data)

    def sentence2tensor():
        data_to_tensor = list()

        for each_sentence in self.data:
            # print('each_sentence', each_sentence, ' len ', len(each_sentence))
            each_sentence_embed = list()
            for no_bracket_sentence in each_sentence:
                str_sentence = str(no_bracket_sentence)
                no_bracket_sentence = str_sentence.split()
                if str_sentence != 'No Title':
                    # print('has title ', str_sentence)
                    for cnt in range(N_VEC_SIZE):
                        if cnt < len(no_bracket_sentence):
                            if no_bracket_sentence[cnt] in word_dict:
                                query = no_bracket_sentence[cnt]
                            else:
                                query = 'XXX'
                            lookup_tensor = torch.tensor(
                                [word_dict[query]], dtype=torch.long)
                        else:
                            lookup_tensor = torch.tensor(
                                [word_dict['XXX']], dtype=torch.long)

                        word_embed = embeds(lookup_tensor)
                        each_sentence_embed.append(word_embed.detach().numpy())

                    # only append the sentence tensor iff the title is not 'No Title'
                    data_to_tensor.append(np.array(each_sentence_embed))

                #print( word_embed, len(word_embed))

            # print('each_sentence: ', each_sentence, ' mbed tensor: ', each_sentence_embed)

        # print('data_to_tensor type is ', type(data_to_tensor))

        data_to_tensor = np.array(data_to_tensor)
        data_to_tensor = torch.tensor(data_to_tensor)
        # print('data_to_tensor', data_to_tensor)
        print('data_to_tensor type: ', type(data_to_tensor))
        return data_to_tensor


def load_custom_dataset():
    custom_dataset_reject = custom_dataset(f_2, 0)
    custom_dataset_accept = custom_dataset(f_1, 1)
    for title, label in custom_dataset_reject:
        print(title, label)
    return 0


if __name__ == '__main__':
    load_custom_dataset()
