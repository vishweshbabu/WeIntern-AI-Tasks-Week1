import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Weights and Biases Initialization
        self.W1 = np.random.randn(hidden_size, input_size) * 0.01
        self.b1 = np.zeros((hidden_size, 1))
        self.W2 = np.random.randn(output_size, hidden_size) * 0.01
        self.b2 = np.zeros((output_size, 1))

    # Implement activation functions
    def relu(self, Z):
        return np.maximum(0, Z)

    def softmax(self, Z):
        expZ = np.exp(Z - np.max(Z, axis=0, keepdims=True)) # Prevents overflow
        return expZ / np.sum(expZ, axis=0, keepdims=True)

    # Implement forward propagation[cite: 3]
    def forward_prop(self, X):
        self.Z1 = np.dot(self.W1, X) + self.b1
        self.A1 = self.relu(self.Z1)
        self.Z2 = np.dot(self.W2, self.A1) + self.b2
        self.A2 = self.softmax(self.Z2)
        return self.A2

    # Calculate loss[cite: 3]
    def compute_loss(self, Y, A2):
        m = Y.shape[1]
        loss = -1 / m * np.sum(Y * np.log(A2 + 1e-8))
        return loss

    # Calculate accuracy[cite: 3]
    def get_accuracy(self, predictions, Y_labels):
        return np.sum(predictions == Y_labels) / Y_labels.size

    # Training the Network using Backpropagation
    def train(self, X, Y_one_hot, Y_labels, epochs=500, learning_rate=0.1):
        losses = []
        m = X.shape[1]
        
        for i in range(epochs):
            # Forward Pass
            A2 = self.forward_prop(X)
            loss = self.compute_loss(Y_one_hot, A2)
            losses.append(loss)
            
            # Backward Pass
            dZ2 = A2 - Y_one_hot
            dW2 = 1 / m * np.dot(dZ2, self.A1.T)
            db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)
            
            dZ1 = np.dot(self.W2.T, dZ2) * (self.Z1 > 0) # ReLU derivative
            dW1 = 1 / m * np.dot(dZ1, X.T)
            db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)
            
            # Update weights
            self.W1 -= learning_rate * dW1
            self.b1 -= learning_rate * db1
            self.W2 -= learning_rate * dW2
            self.b2 -= learning_rate * db2

            # Print progress every 100 epochs
            if i % 100 == 0:
                predictions = np.argmax(A2, axis=0)
                acc = self.get_accuracy(predictions, Y_labels)
                print(f"Epoch {i}: Loss = {loss:.4f}, Accuracy = {acc:.4f}")

        # Visualize results[cite: 3]
        plt.plot(losses)
        plt.title("Neural Network Training Loss (MNIST Data)")
        plt.xlabel("Epochs")
        plt.ylabel("Cross-Entropy Loss")
        plt.show()

if __name__ == "__main__":
    print("Loading MNIST data... Please wait.")
    
    try:
        # 1. CSV ஃபைலை படிக்கிறோம் (pandas யூஸ் பண்ணி)
        data = pd.read_csv('train.csv')
        
        # 2. டேட்டாவை NumPy Array ஆக மாற்றி, ஷஃபிள் பண்றோம்
        data = np.array(data)
        np.random.shuffle(data)
        
        # 3. Features (X) மற்றும் Labels (Y) ஆக பிரிக்கிறோம்
        # ட்ரைனிங் வேகமாக நடக்க முதல் 10000 டேட்டாவை மட்டும் எடுத்துக்கிறோம்
        data_train = data[0:10000].T 
        Y_train_labels = data_train[0] # முதல் வரிசை label
        X_train = data_train[1:785] # மீதமுள்ள 784 வரிசைகளும் பிக்சல்ஸ்
        
        # 4. பிக்சல் மதிப்புகளை 0 முதல் 1 வரை மாத்துறோம் (Normalization)
        X_train = X_train / 255.0
        
        # 5. Labels-ஐ One-Hot Encoding ஃபார்மேட்க்கு மாத்துறோம்
        output_size = 10
        num_examples = Y_train_labels.shape[0]
        Y_train_one_hot = np.zeros((output_size, num_examples))
        for i in range(num_examples):
            Y_train_one_hot[int(Y_train_labels[i]), i] = 1

        # 6. Neural Network-ஐ உருவாக்கி ட்ரெயின் பண்றோம்
        input_size = 784
        hidden_size = 128
        
        nn = SimpleNeuralNetwork(input_size, hidden_size, output_size)
        print("Data loaded successfully! Starting Training...")
        
        # 1000 epochs-க்கு ட்ரெயின் பண்றோம்
        nn.train(X_train, Y_train_one_hot, Y_train_labels, epochs=1000, learning_rate=0.1)
        
    except FileNotFoundError:
        print("Error: 'train.csv' file not found. Please make sure the Kaggle MNIST dataset is in the same folder as this script.")