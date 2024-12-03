# quests/quest7.py

import tkinter as tk
from quests.quest import Quest
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from visualization import Visualization
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from PIL import Image, ImageOps
import io

class Quest7(Quest):
    def __init__(self, ui):
        super().__init__(quest_id=7, description="Train a neural network to recognize handwritten digits.", difficulty=7, ui=ui)
        # Hyperparameters
        self.lr = tk.DoubleVar(value=0.01)
        self.hidden_size = tk.IntVar(value=64)
        self.epochs = tk.IntVar(value=10)
        # Initialize network parameters (weights and biases)
        self.init_network()
        # Load data
        self.load_data()
        # Training state
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
        self.training_epoch = 0
        self.simulation_running = False
        # Visualization elements
        self.canvas = None
        self.fig = None
        self.ax_loss = None
        self.ax_accuracy = None
        self.line_train_loss = None
        self.line_val_loss = None
        self.line_train_acc = None
        self.line_val_acc = None
        # Drawing canvas for user input
        self.drawing_canvas = None
        self.user_digit = None
        self.prediction_label = None

    def start(self):
        # Clear the content_frame
        for widget in self.ui.content_frame.winfo_children():
            widget.destroy()
    
        self.quest_frame = tk.Frame(self.ui.content_frame)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)
    
        ttk.Label(self.quest_frame, text=self.description, style="Quest.Title.TLabel").pack(pady=20)
    
        self.control_frame = tk.Frame(self.quest_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
    
        # Sliders for hyperparameters
        ttk.Label(self.control_frame, text="Learning Rate:", style="Quest.TLabel").pack(pady=5)
        self.lr_slider = tk.Scale(self.control_frame, from_=0.001, to=1.0, orient=tk.HORIZONTAL, variable=self.lr, length=200, resolution=0.001)
        self.lr_slider.pack(pady=5)
    
        ttk.Label(self.control_frame, text="Hidden Neurons:", style="Quest.TLabel").pack(pady=5)
        self.hidden_size_slider = tk.Scale(self.control_frame, from_=10, to=200, orient=tk.HORIZONTAL, variable=self.hidden_size, length=200, resolution=1)
        self.hidden_size_slider.pack(pady=5)
    
        ttk.Label(self.control_frame, text="Epochs:", style="Quest.TLabel").pack(pady=5)
        self.epochs_slider = tk.Scale(self.control_frame, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.epochs, length=200, resolution=1)
        self.epochs_slider.pack(pady=5)
    
        ttk.Button(self.control_frame, text="Start Training", command=self.start_training, style="Quest.TButton").pack(pady=10)
        ttk.Button(self.control_frame, text="Reset Training", command=self.reset_training, style="Quest.TButton").pack(pady=10)
        ttk.Button(self.control_frame, text="Skip Quest", command=self.skip_quest, style="Quest.TButton").pack(pady=10)
    
        # Drawing canvas for user digit input
        ttk.Label(self.control_frame, text="Draw a Digit:", style="Quest.TLabel").pack(pady=5)
        self.create_drawing_canvas()
    
        # Message Label
        self.message_label = None
    
        # Plot area
        self.plot_frame = tk.Frame(self.quest_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
        # Initialize the plot
        self.create_plot()

    def create_plot(self):
        (self.canvas, self.fig,
        self.ax_loss, self.line_train_loss,
        self.ax_val_loss, self.line_val_loss,
        self.ax_accuracy, self.line_train_acc,
        self.ax_val_acc, self.line_val_acc) = Visualization.create_loss_accuracy_plots(self.plot_frame)

    def init_network(self):
        input_size = 64  # Adjusted for 8x8 images from the digits dataset
        output_size = 10  # 10 classes
        hidden_size = self.hidden_size.get()
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def load_data(self):
        # Load digits dataset
        digits = load_digits()
        X = digits.images  # Shape (1797, 8, 8)
        y = digits.target  # Shape (1797,)
        # Flatten images
        X = X.reshape(-1, 64)
        # Normalize pixel values
        X = X / 16.0
        # Split into training and validation sets
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    def reset_training(self):
        # Stop any ongoing training
        self.simulation_running = False
        
        # Reinitialize network parameters
        self.init_network()
        
        # Reset training and validation metrics
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
        
        # Reset time and epoch counters
        self.time_elapsed = 0.0
        self.training_epoch = 0
        
        # Clear plots
        if self.line_train_loss and self.line_val_loss:
            self.line_train_loss.set_data([], [])
            self.line_val_loss.set_data([], [])
        if self.line_train_acc and self.line_val_acc:
            self.line_train_acc.set_data([], [])
            self.line_val_acc.set_data([], [])
        
        # Reset plot axes
        self.ax_loss.set_xlim(0, self.epochs.get())
        self.ax_loss.set_ylim(0, 1)
        self.ax_accuracy.set_xlim(0, self.epochs.get())
        self.ax_accuracy.set_ylim(0, 1)
        
        # Redraw plots
        self.canvas.draw()
        
        # Clear any existing messages
        if self.message_label:
            self.message_label.destroy()
            self.message_label = None

    def create_drawing_canvas(self):
        # Frame for drawing
        drawing_frame = tk.Frame(self.control_frame)
        drawing_frame.pack(pady=10)
        
        # Canvas for drawing
        self.drawing_canvas = tk.Canvas(drawing_frame, width=200, height=200, bg='white', cursor='cross')
        self.drawing_canvas.pack()
        
        # Bind mouse events to the canvas
        self.drawing_canvas.bind("<B1-Motion>", self.draw)
        
        # Buttons for clearing and testing the drawing
        button_frame = tk.Frame(self.control_frame)
        button_frame.pack(pady=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Drawing", command=self.clear_drawing, style="Quest.TButton")
        clear_button.pack(side=tk.LEFT, padx=5)
        
        test_button = ttk.Button(button_frame, text="Test Your Digit", command=self.test_user_digit, style="Quest.TButton")
        test_button.pack(side=tk.LEFT, padx=5)
        
        # Prediction result label
        self.prediction_label = ttk.Label(self.control_frame, text="Draw a digit and click 'Test Your Digit'", style='Quest.TLabel')
        self.prediction_label.pack(pady=5)
        
    def draw(self, event):
        # Draw a small oval (dot) where the mouse moves
        x, y = event.x, event.y
        r = 4  # Radius of the dot
        self.drawing_canvas.create_oval(x - r, y - r, x + r, y + r, fill='black')
        
    def clear_drawing(self):
        self.drawing_canvas.delete("all")
        self.prediction_label.config(text="Draw a digit and click 'Test Your Digit'")
        
    def test_user_digit(self):
        # Get the drawing from the canvas
        self.drawing_canvas.update()
        ps = self.drawing_canvas.postscript(colormode='color')
        
        # Convert postscript image to PIL Image
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Invert image (PIL uses white as background)
        img = ImageOps.invert(img)
        
        # Resize to 8x8 as per the digits dataset
        img = img.resize((8, 8), Image.ANTIALIAS)
        
        # Convert image to numpy array
        img_array = np.array(img)
        
        # Normalize pixel values to [0,1]
        img_array = img_array / 255.0
        
        # Flatten the image
        img_flat = img_array.flatten()
        
        # Reduce the resolution to match the digits dataset (optional)
        # The digits dataset has 8x8 images with pixel values from 0 to 16
        img_flat = (img_flat * 16).astype(int)
        
        # Prepare input for the network
        X_test = img_flat.reshape(1, -1) / 16.0  # Normalize
        
        # Forward pass
        z1 = np.dot(X_test, self.W1) + self.b1
        a1 = self.relu(z1)
        z2 = np.dot(a1, self.W2) + self.b2
        a2 = self.softmax(z2)
        
        # Prediction
        prediction = np.argmax(a2, axis=1)[0]
        
        # Update prediction label
        self.prediction_label.config(text=f"Predicted Digit: {prediction}")

    def train_epoch(self):
        # Retrieve hyperparameters
        learning_rate = self.lr.get()
        hidden_size = self.hidden_size.get()
        
        # Shuffle training data
        permutation = np.random.permutation(self.X_train.shape[0])
        X_train_shuffled = self.X_train[permutation]
        y_train_shuffled = self.y_train[permutation]
        
        # One-hot encode labels
        y_train_one_hot = np.zeros((y_train_shuffled.size, 10))
        y_train_one_hot[np.arange(y_train_shuffled.size), y_train_shuffled] = 1
        
        # Forward pass
        z1 = np.dot(X_train_shuffled, self.W1) + self.b1  # (N, hidden_size)
        a1 = self.relu(z1)                               # (N, hidden_size)
        z2 = np.dot(a1, self.W2) + self.b2              # (N, 10)
        a2 = self.softmax(z2)                            # (N, 10)
        
        # Compute loss (cross-entropy)
        m = y_train_one_hot.shape[0]
        loss = -np.sum(y_train_one_hot * np.log(a2 + 1e-8)) / m
        self.train_losses.append(loss)
        
        # Compute accuracy
        predictions = np.argmax(a2, axis=1)
        accuracy = np.mean(predictions == y_train_shuffled)
        self.train_accuracies.append(accuracy)
        
        # Backward pass
        dz2 = (a2 - y_train_one_hot) / m                  # (N, 10)
        dW2 = np.dot(a1.T, dz2)                           # (hidden_size, 10)
        db2 = np.sum(dz2, axis=0, keepdims=True)          # (1, 10)
        
        da1 = np.dot(dz2, self.W2.T)                      # (N, hidden_size)
        dz1 = da1 * self.relu_derivative(z1)              # (N, hidden_size)
        dW1 = np.dot(X_train_shuffled.T, dz1)             # (input_size, hidden_size)
        db1 = np.sum(dz1, axis=0, keepdims=True)          # (1, hidden_size)
        
        # Update weights and biases
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        
        # Validation pass
        z1_val = np.dot(self.X_val, self.W1) + self.b1
        a1_val = self.relu(z1_val)
        z2_val = np.dot(a1_val, self.W2) + self.b2
        a2_val = self.softmax(z2_val)
        
        # Compute validation loss
        y_val_one_hot = np.zeros((self.y_val.size, 10))
        y_val_one_hot[np.arange(self.y_val.size), self.y_val] = 1
        loss_val = -np.sum(y_val_one_hot * np.log(a2_val + 1e-8)) / self.y_val.size
        self.val_losses.append(loss_val)
        
        # Compute validation accuracy
        predictions_val = np.argmax(a2_val, axis=1)
        accuracy_val = np.mean(predictions_val == self.y_val)
        self.val_accuracies.append(accuracy_val)
        
        # Update plots
        self.update_plots()

    def update_plots(self):
        # Update Loss Plot
        self.line_train_loss.set_data(range(1, len(self.train_losses)+1), self.train_losses)
        self.line_val_loss.set_data(range(1, len(self.val_losses)+1), self.val_losses)
        self.ax_loss.set_xlim(0, max(10, len(self.train_losses)))
        self.ax_loss.set_ylim(0, max(max(self.train_losses, default=1), max(self.val_losses, default=1)) + 0.5)
        
        # Update Accuracy Plot
        self.line_train_acc.set_data(range(1, len(self.train_accuracies)+1), self.train_accuracies)
        self.line_val_acc.set_data(range(1, len(self.val_accuracies)+1), self.val_accuracies)
        self.ax_accuracy.set_xlim(0, max(10, len(self.train_accuracies)))
        self.ax_accuracy.set_ylim(0, 1)
        
        # Redraw canvas
        self.canvas.draw()

    def start_training(self):
        if self.simulation_running:
            return  # Prevent multiple trainings at once
        self.simulation_running = True
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
        self.init_network()  # Re-initialize network parameters
        self.training_epoch = 0
        self.max_epochs = self.epochs.get()
        self.train_next_epoch()

    def train_next_epoch(self):
        if self.training_epoch < self.max_epochs and self.simulation_running:
            self.train_epoch()
            self.training_epoch += 1
            self.ui.root.after(100, self.train_next_epoch)  # Adjust the delay as needed
        else:
            self.simulation_running = False
            self.check_success()

    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, z):
        return (z > 0).astype(float)

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def check_success(self):
        # Check the latest validation accuracy
        if len(self.val_accuracies) == 0:
            self.display_message("No validation accuracy recorded.", error=True)
            return
        
        latest_val_accuracy = self.val_accuracies[-1] * 100  # Convert to percentage
        
        # Define success threshold
        success_threshold = 90.0  # 90%
        
        if latest_val_accuracy >= success_threshold:
            self.display_message(f"Success! Validation Accuracy: {latest_val_accuracy:.2f}%", success=True)
            self.ui.root.after(2000, self.end_quest)
        else:
            self.display_message(f"Validation Accuracy: {latest_val_accuracy:.2f}%. Try adjusting hyperparameters.", error=True)

    def display_message(self, message, error=False, success=False):
        # Remove existing message label if any
        if self.message_label:
            self.message_label.destroy()
        
        # Determine message color based on type
        if success:
            color = 'green'
        elif error:
            color = 'red'
        else:
            color = 'black'
        
        # Create and display the message label
        self.message_label = ttk.Label(self.control_frame, text=message, style='Quest.TLabel')
        self.message_label.configure(foreground=color)
        self.message_label.pack(pady=5)

    def skip_quest(self):
        self.ui.game_engine.skip_current_quest()

    def end_quest(self):
        # Do not destroy the quest_frame here
        super().end_quest()


