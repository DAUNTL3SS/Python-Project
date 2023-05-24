# Course Project CS340 - PART B - Vaggelis Chasiotis - SPRING I 2023
# This project is about creating an artificial neural network in order to solve a classification problem. Enjoy!
# *EXTRA WORK* CREATING A NEURAL NETWORK FROM SCRATCH USING BACK PROPOGATION WITH NUMPY LIBRARY

# Libraries
import random
import numpy as np
import matplotlib.pyplot as plt


# File created for reading the training data file
def file_reader(training_file):
    inputs = []
    outputs = []
    with open(training_file) as f:
        for line in f:
            line = line.strip()
            if line:
                bits, label = line.split(',')
                inputs.append([int(bit) for bit in bits])
                outputs.append([int(label)])
    return np.array(inputs), np.array(outputs)


# File created for reading the input data file
def file_reader1(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    inputs = np.array([list(map(int, line.strip())) for line in lines])
    return inputs


# ANN back propopgation algorithm from scratch
class Network(object):
    # Layers and weights
    def __init__(self, hidden_size):
        self.input_size = 10
        self.output_size = 2
        self.hidden_size = hidden_size

        self.W1 = np.random.randn(self.input_size, self.hidden_size)  # input-hidden layer weights
        self.W2 = np.random.randn(self.hidden_size, self.output_size)  # hidden-output layer weights

    # Feed forward algorithm
    def feedforward(self, inputs):
        # dot product of inputs and first set of weights
        self.z = np.dot(inputs, self.W1)
        # activation function
        self.z2 = self.sigmoid(self.z)
        # dot product of hidden layer and second set of weights
        self.z3 = np.dot(self.z2, self.W2)
        predicted_output = self.sigmoid(self.z3)
        return predicted_output

    # sigmoid activation function
    def sigmoid(self, sig, deriv=False):
        if deriv:
            return sig * (1 - sig)
        return 1 / (1 + np.exp(-sig))

    # back propogation algorithm
    def backpropagation(self, inputs, outputs, predicted_output, learningRate=1):
        output_error = outputs - predicted_output
        output_delta = output_error * self.sigmoid(predicted_output, deriv=True)

        z2_error = output_delta.dot(self.W2.T)
        z2_delta = z2_error * self.sigmoid(self.z2, deriv=True)

        self.W1 += inputs.T.dot(z2_delta) * learningRate  # Adjusting the input-hidden layer weights
        self.W2 += self.z2.T.dot(output_delta) * learningRate  # Adjusting the hidden-output layer weights

    # training algorithm
    def train(self, inputs, outputs, learning_rate):
        predicted_output = self.feedforward(inputs)
        self.backpropagation(inputs, outputs, predicted_output, learning_rate)

    # classification function
    def classify(self, inputs):
        predicted_output = self.feedforward(inputs)
        labels = np.zeros(predicted_output.shape)
        labels[predicted_output >= 0.5] = 1
        return labels

    # saving weights function
    def save_weights(self, file_name='weights.txt'):
        with open(file_name, 'w') as f:
            np.savetxt(f, self.W1, fmt='%s')
            np.savetxt(f, self.W2, fmt='%s')

    # loading weights function
    def load_weights(self, file_name='weights.txt'):
        with open(file_name) as f:
            self.W1 = np.loadtxt(f)
            self.W2 = np.loadtxt(f)


# function that generates the bit strings and saves them in a file
def generate_data_files():
    numbers = []
    for i in range(1024):
        binary = bin(i)[2:].zfill(10)
        numbers.append(binary)

    with open("bit_strings.txt", "w") as f:
        for number in numbers:
            f.write(number + "\n")

    num_lines = len(numbers)
    num_unlabelled = int(num_lines * 0.8)
    unlabelled_indices = random.sample(range(num_lines), num_unlabelled)

    # saving 80% of the bit strings in this file
    with open("training_data_unlabelled.txt", "w") as f:
        for i in unlabelled_indices:
            f.write(numbers[i] + "\n")

    # saving the remaining 20% of the bit strings in this file
    with open("input_data.txt", "w") as f:
        for i in range(num_lines):
            if i not in unlabelled_indices:
                f.write(numbers[i] + "\n")

    # labelling the bits based on the number 1s and saving them in this file
    with open("training_data_labelled.txt", "w") as f:
        for number in numbers:
            left_count = number[:5].count("1")
            right_count = number[5:].count("1")
            if left_count > right_count:
                f.write(number + ",10\n")
            elif left_count < right_count:
                f.write(number + ",01\n")
            else:
                f.write(number + ",11\n")


# choosing topology function
def choose_network_topology():
    try:
        hidden_layer_size = int(input("Enter the size of the hidden layer: "))
        network = Network(hidden_layer_size)
        print(f"A neural network with topology 10-{hidden_layer_size}-2 has been created.")
        return network
    except ValueError:
        print("Please enter the size in an integer.")


# network training function
def train_network(network, training_file='training_data_labelled.txt', learning_rate=0.1, num_epochs=100):
    inputs, outputs = file_reader(training_file)
    inputs = inputs / np.amax(inputs)
    outputs = outputs / np.amax(outputs)

    progress_file = open('training_progress.txt', 'w')

    for epoch in range(num_epochs):
        network.train(inputs, outputs, learning_rate)
        cost = np.mean(np.abs(network.feedforward(inputs) - outputs))
        progress_file.write(f'{epoch}, {cost}\n')

    progress_file.close()

    # generate report
    predicted_outputs = network.feedforward(inputs)
    accuracy = 1 - np.mean(np.abs(predicted_outputs - outputs))
    confusion_matrix = np.dot(outputs.T, predicted_outputs)
    report = f'Accuracy: {accuracy}\nConfusion Matrix:\n{confusion_matrix}'
    print(report)

    return network


# classifying data function
def classify_test_data(network, input_file='input_data.txt', output_file='training_output.txt'):
    inputs = file_reader1(input_file)
    inputs = inputs / np.amax(inputs)
    predicted_outputs = network.feedforward(inputs)

    with open(output_file, 'w') as f:
        for i in range(len(inputs)):
            line = ''.join([str(int(x)) for x in inputs[i]])
            if predicted_outputs[i][0] > predicted_outputs[i][1]:
                line += ',10\n'
            elif predicted_outputs[i][0] < predicted_outputs[i][1]:
                line += ',01\n'
            else:
                line += ',11\n'
            f.write(line)


# display progress function
def display_training_progress():
    data = np.loadtxt('training_progress.txt', delimiter=',')
    plt.plot(data[:, 0], data[:, 1])
    plt.xlabel('Epoch')
    plt.ylabel('Cost')
    plt.tight_layout()
    plt.show()


# PROGRAM STARTS HERE!
def show_menu():
    network = None
    while True:
        # Error trapping on user input
        try:
            print("\nARTIFICIAL NEURAL NETWORK MENU\n------------------------------------")
            print("\t1. Generate data files")
            print("\t2. Choose network topology")
            print("\t3. Train network")
            print("\t4. Classify test data")
            print("\t5. Display training progress graph")
            print("\t6. Exit")
            print("------------------------------------")
            choice = input("\nEnter your choice (1-6): ")
        except ValueError:
            print("Please enter a correct integer number!")
        else:
            # Option 1 Code
            if choice == "1":
                print("You've entered option 1...")
                print("\nIn this option, the program creates a file where it holds the generated bit strings.\n"
                      "Then, it created two additional files, where it saves randomly 80% and 20% of the data\n"
                      "respectively. Finally it uses the 80% file to classify the bits based on their numbers.")
                # Calling the file generator method
                generate_data_files()
                print("\nNow the data is generated and tested!")
                print()
                enter = input("Press anything to continue...")
                continue
            # Option 2 Code
            elif choice == "2":
                print("You've entered option 2...")
                print(
                    "\nIn this option, the program asks for user input for the number of neurons in the hidden layer.\n"
                    "After the input, the program will then display the network topology of the program.\n")
                # Calling the network topology method
                network = choose_network_topology()
                print()
                enter = input("Press anything to continue...")
                continue
            # Option 3 Code
            elif choice == "3":
                # Condition to run option 3 is to have run option 2 beforehand
                if not network:
                    print("Please choose a network topology first.")
                    continue
                print("You've entered option 3...")
                print("\nThis option allows the user to initiate a training pass\n"
                      "after inputting the learning rate and number of epochs")
                # Error trapping for wrong user inputs for every variable that requires an input (all 3)
                try:
                    training_file = input("\nPlease enter the filename containing the training data"
                                          "(Press enter for default:'training_data_labelled.txt'): ")
                    print("This module only works for training_data_labelled.txt only...")
                    training_file = 'training_data_labelled.txt'
                except ValueError:
                    print("File chosen = training_data_labelled.txt")
                    training_file = 'training_data_labelled.txt'

                try:
                    epochs = int(input("\nPlease enter the number of epochs you want to train the model for"
                                       "(Press enter for default: 100): "))
                except ValueError:
                    epochs = 100
                    print("Number of epochs = " + str(epochs) + "\n")

                try:
                    learningRate = int(input("Please enter the number of the learning rate"
                                             "(Press enter for default: 0.1): "))
                    print("This module can only train with a 0.1 learning rate...")
                except ValueError:
                    learningRate = 0.1
                    print("Learning rate chosen = " + str(learningRate) + "\n")

                # Printing the result
                print("You've chosen file 'training_data_labelled.txt', number of epochs: "+str(epochs)+" at a learning rate of: "+str(learningRate)+".\n")
                # Calling the network training function
                train_network(network, training_file, learningRate, epochs)
                print()
                enter = input("Press anything to continue...")
                continue
            # Option 4 Code
            elif choice == "4":
                print("You've entered option 4...")
                print("This option classifies test data of the file input_data.txt and saves them in a new file")
                # Calling the classify data method
                classify_test_data(network)
                print("\nClassification is done and saved in a file!")
                print()
                enter = input("Press anything to continue...")
                continue
            # Option 5 Code
            elif choice == "5":
                print("You've entered option 5")
                print("This option a graph of the number of training costs by the number of epochs is displayed")
                display_training_progress()
            # Option 6 Code
            elif choice == "6":
                print("Thank you for using the program...Bye!")
                break
            else:
                print("Invalid choice, please try again.")

show_menu()
