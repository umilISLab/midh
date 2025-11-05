import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleLinearNetwork(nn.Module):
    """
    A neural network with only an input and an output layer.
    No hidden layers. This is essentially a linear model.
    """
    def __init__(self, input_size, num_classes):
        super(SimpleLinearNetwork, self).__init__()
        self.linear_layer = nn.Linear(input_size, num_classes)

    def forward(self, x):
        out = self.linear_layer(x)
        log_probs = F.log_softmax(out, dim=1)
        return log_probs