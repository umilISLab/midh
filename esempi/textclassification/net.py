import torch 
from torch import nn
from tqdm import tqdm


class SimplePredictor(nn.Module):
    def __init__(self, input_dim, output_dim, learning_rate: float = 0.005):
        super(SimplePredictor, self).__init__()
        self.output_layer = nn.Linear(input_dim, output_dim)
        self.softmax = nn.Softmax(dim=1)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): Input di dimensione (batch_size, input_dim)
        """
        output = self.softmax(self.output_layer(x))
        return output
    
    def train(self, category_tensor, line_tensor):
        self.optimizer.zero_grad()
        output = self(line_tensor)    
        loss = self.criterion(output, category_tensor)
        loss.backward()
        self.optimizer.step()
        return output, loss.item()
    
    def run_training(self, data_generator: callable, embedding_function: callable, 
                n_iterations: int = 10000, plot_every: int = 100):
        history = []
        current_loss = 0
        run = list(range(1, n_iterations + 1))
        for i in tqdm(run):
            category, line, category_tensor, line_tensor = data_generator(embedding_function)
            output, loss = self.train(category_tensor, line_tensor)
            current_loss += loss
            if i % plot_every == 0:
                history.append(current_loss / plot_every)
                current_loss = 0
        return history
    
    def predict(self, line_tensor):
        with torch.no_grad():
            output = self(line_tensor)
        return output