from decisionTree import DecisionTreeClassifier
import random
 
class RandomForestClassifier:
    def __init__(self, training_sample, n_trees, n_features, n_sample = 0):
        self.training_sample = training_sample
        self.n_trees = n_trees
        self.n_features = n_features
        if n_sample == 0:
            n_sample = len(training_sample)
        self.n_sample = n_sample
        self.decision_trees = []

    def getRandList(self, start, end, size):
        #a list of random numbers between start and end selected with replacement
        randlist = []
        for i in range(size):
            a = random.randrange(start, end)
            randlist.append(a)
        return randlist

    def build(self):
        n = len(self.training_sample)
        attrib_values = []
        for k in range(len(self.training_sample[0])-1):
            attrib_val = list(set([self.training_sample[i][k] for i in range(n)]))
            attrib_values.append(attrib_val)
        target_values = list(set([self.training_sample[i][-1] for i in range(n)]))
        for i in range(self.n_trees):
            examples = self.getRandList(0,n,n)
            tree = DecisionTreeClassifier(self.training_sample, examples, self.n_features, attrib_values, target_values)
            self.decision_trees.append(tree)

    def predict(self, attribs_val):
        #find target value based on provided attribute values
        predictions = []
        for tree in self.decision_trees:
            predictions.append(tree.predict(attribs_val))
        return max(predictions, key = predictions.count)  #return the majority predicted target value

    def test(self, test_sample):
        #returns proportion of correctly identified test examples
        n = len(test_sample) #total number of test examples
        p = 0 #total number of correctly predicted examples 
        for example in test_sample:
            prediction = self.predict(example[:-1])
            if prediction == example[-1]: #last element of example is target value
                p += 1
        return p/n
        
