import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader


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
    
class TextClassifierHiddenLayer(nn.Module):
    """
    Una rete di classificazione testuale con uno strato nascosto.
    Input -> Linear(vocab_size, hidden_dim) -> ReLU -> 
    Linear(hidden_dim, num_classes) -> LogSoftmax
    """
    
    def __init__(self, vocab_size, hidden_dim, num_classes):
        """
        Args:
            vocab_size (int): La dimensione del vocabolario (input_size).
            hidden_dim (int): Il numero di neuroni nel layer nascosto.
            num_classes (int): Il numero di classi (output_size).
        """
        super(TextClassifierHiddenLayer, self).__init__()
        
        # 1. Layer da Input a Nascosto
        # Trasforma il vettore BoW [1, vocab_size] in un 
        # vettore di feature nascoste [1, hidden_dim]
        self.input_to_hidden = nn.Linear(vocab_size, hidden_dim)
        
        # 2. Layer da Nascosto a Output
        # Trasforma le feature nascoste [1, hidden_dim] nei
        # punteggi per le classi [1, num_classes]
        self.hidden_to_output = nn.Linear(hidden_dim, num_classes)

    def forward(self, x_bow):
        """
        Args:
            x_bow (Tensor): Tensore di input [batch_size, vocab_size]
        """
        
        # 1. Passa attraverso il primo layer
        hidden = self.input_to_hidden(x_bow)
        
        # 2. Applica un'attivazione non-lineare
        # Senza questa, i due layer collasserebbero in un unico
        # layer lineare, rendendo inutile il layer nascosto.
        hidden_activated = F.relu(hidden)
        
        # 3. Passa attraverso il layer di output
        logits = self.hidden_to_output(hidden_activated)
        
        # 4. Applica LogSoftmax (come da nostra convenzione)
        log_probs = F.log_softmax(logits, dim=1)
        
        return log_probs
    
def create_text_dataloader(train_examples, batch_size=4, shuffle=True):
    """
    Prende i dati testuali grezzi, costruisce i vocabolari,
    vettorizza i dati (Multi-Hot BoW) e restituisce un DataLoader.
    
    Args:
        train_examples (list): Lista di tuple (lista_feature, etichetta_str)
        batch_size (int): Dimensione del batch.
        shuffle (bool): Se mescolare i dati.
        
    Returns:
        tuple: (train_loader, feature_map, label_map, vocab_size, num_classes)
    """
    
    # --- 1. Costruzione Vocabolari ---
    all_features = set()
    all_labels = set()
    for features, label in train_examples:
        all_features.update(features)
        all_labels.add(label)

    feature_map = {feature: i for i, feature in enumerate(sorted(list(all_features)))}
    label_map = {label: i for i, label in enumerate(sorted(list(all_labels)))}

    vocab_size = len(feature_map)
    num_classes = len(label_map)

    # --- 2. Vettorizzazione ---
    X_data_list = []
    y_data_list = []

    for features, label in train_examples:
        # Vettore "multi-hot"
        vector_x = torch.zeros(vocab_size, dtype=torch.float32)
        for f in features:
            if f in feature_map: # Ignora feature non viste (se usassimo un test set)
                vector_x[feature_map[f]] = 1.0
        
        X_data_list.append(vector_x)
        y_data_list.append(label_map[label])

    X_data = torch.stack(X_data_list)
    y_data = torch.LongTensor(y_data_list)

    # --- 3. Creazione DataLoader ---
    dataset = TensorDataset(X_data, y_data)
    train_loader = DataLoader(dataset=dataset, 
                              batch_size=batch_size, 
                              shuffle=shuffle, drop_last=True)
    
    print(f"DataLoader creato. VocabSize={vocab_size}, NumClassi={num_classes}")
    
    return train_loader, feature_map, label_map, vocab_size, num_classes


def get_token_to_hidden_weights(model, token_name, feature_map, verbose=False):
    """
    Estrae il vettore dei pesi che collega un token di input
    al layer nascosto.
    
    Args:
        model (TextClassifierHiddenLayer): Il modello addestrato.
        token_name (str): Il nome del token (es. "pelo").
        feature_map (dict): Il dizionario {'nome_feature': indice}.
        
    Returns:
        torch.Tensor: Un vettore 1D di (hidden_dim,)
                      o None se il token non è valido.
    """
    
    # 1. Trova l'ID del token
    try:
        token_id = feature_map[token_name]
    except KeyError:
        print(f"Errore: Token '{token_name}' non trovato nel vocabolario.")
        return None
        
    # 2. Accedi alla matrice dei pesi del primo layer
    # Questa matrice ha forma [hidden_dim, vocab_size]
    weights = model.input_to_hidden.weight.data
    
    # 3. Estrai la colonna corrispondente al nostro token
    # (tutte le righe, colonna 'token_id')
    token_weights_vector = weights[:, token_id]
    
    if verbose:
        print(f"--- Pesi per '{token_name.upper()}' (-> Hidden Layer) ---")
        print(f"Forma del Vettore: {token_weights_vector.shape}")
        print(f"Valori: {token_weights_vector}")
    
    return token_weights_vector