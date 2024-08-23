from re import L
import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        score = nn.as_scalar(self.run(x))
        if score >= 0:
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        converge = False
        while not converge:
            converge = True
            for x, y in dataset.iterate_once(batch_size=1):
                label = nn.as_scalar(y)
                p = self.get_prediction(x)
                if p != label:
                    converge = False
                    self.w.update(x, label)


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

        self.W1 = nn.Parameter(1, 64)
        self.b1 = nn.Parameter(1, 64)
        self.W2 = nn.Parameter(64, 1)
        self.b2 = nn.Parameter(1, 1)


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        h = nn.ReLU(nn.AddBias(nn.Linear(x, self.W1), self.b1))
        return nn.AddBias(nn.Linear(h, self.W2), self.b2)


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        lr = 0.01
        loss = float('inf')

        while loss >= .015:
            for x, y in dataset.iterate_once(batch_size=50):  

                loss = self.get_loss(x, y)
                
                gradients = nn.gradients(loss, [self.W1, self.b1, self.W2, self.b2])
                loss = nn.as_scalar(loss)

                self.W1.update(gradients[0], -lr)
                self.b1.update(gradients[1], -lr)
                self.W2.update(gradients[2], -lr)
                self.b2.update(gradients[3], -lr)
                

                



class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here

        "*** YOUR CODE HERE ***"
        self.W1 = nn.Parameter(784, 128)
        self.b1 = nn.Parameter(1, 128)
        self.W2 = nn.Parameter(128, 10)
        self.b2 = nn.Parameter(1, 10)


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h = nn.ReLU(nn.AddBias(nn.Linear(x, self.W1), self.b1))
        return nn.AddBias(nn.Linear(h, self.W2), self.b2)


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
    
        lr = 0.1
        accuracy = 0.0

        while accuracy < 0.98:
            t_loss = 0.0
            for x, y in dataset.iterate_once(batch_size=100):  

                loss = self.get_loss(x, y)
                t_loss += nn.as_scalar(loss)
                gradients = nn.gradients(loss, [self.W1, self.b1, self.W2, self.b2])

                self.W1.update(gradients[0], -lr)
                self.b1.update(gradients[1], -lr)
                self.W2.update(gradients[2], -lr)
                self.b2.update(gradients[3], -lr)

            accuracy = dataset.get_validation_accuracy() 
            if accuracy >= 0.971:
                break

            




class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        
        "*** YOUR CODE HERE ***"
        self.W0 = nn.Parameter(self.num_chars, 256)
        self.b0 = nn.Parameter(1, 256)
        self.W1 = nn.Parameter(256, 256)
        self.b1 = nn.Parameter(1, 256)
        self.W2 = nn.Parameter(256, len(self.languages))
        self.b2 = nn.Parameter(1, len(self.languages))


    

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h = nn.Linear(nn.DataNode(xs[0].data), self.W0)
        for i in xs:
            h = nn.ReLU(nn.AddBias(nn.Linear(nn.Add(nn.Linear(i, self.W0), h), self.W1), self.b1))
        return nn.AddBias(nn.Linear(h, self.W2), self.b2)




    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(xs), y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"

        lr = 0.01
        accuracy = 0.0

        while accuracy < 0.85:
            for x, y in dataset.iterate_once(batch_size=100):  

                loss = self.get_loss(x, y)
                gradients = nn.gradients(loss, [self.W0, self.b0, self.W1, self.b1, self.W2, self.b2])
                
                self.W0.update(gradients[0], -lr)
                self.b0.update(gradients[1], -lr)
                self.W1.update(gradients[2], -lr)
                self.b1.update(gradients[3], -lr)
                self.W2.update(gradients[4], -lr)
                self.b2.update(gradients[5], -lr)

            

            accuracy = dataset.get_validation_accuracy() 
            if accuracy >= 0.835:
                break 
