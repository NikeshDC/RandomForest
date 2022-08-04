import random

class DecisionTreeClassifier:
    class Node:
        def __init__(self, attrib):
            self.attrib = attrib
            self.branch = {}

        def addbranch(self, val, sub_tree):
            self.branch[val] = sub_tree

    class Leaf:
        def __init__(self, value):
            self.value = value
            
    #using random subspace at each split
    def __init__(self, training_sample, examples, m_features, attrib_values, target_vals):
        #the last element of each training_sample is target value
        self.training_sample = training_sample
        self.attrib_values = attrib_values   #each attribute and its associated possible values; attrib_value[attrib] = possible values of attrib
        self.target_vals = target_vals       #posssible target values
        self.m_features = m_features
        #self.choose_attrib = choose_attrib
        self.attrib_size = len(training_sample[0]) - 1
##        print("As: ",self.attrib_size)
        self.tree = self.build_tree(examples, [])

    def choose_attrib(self, attribs, examples):
        #chose attribute based on gini impurity
        total_gini = self.gini_value(examples)
        n = len(examples)
        max_gini = -1.0
        for attrib in attribs:
            ginival = 0.0
            for val in self.attrib_values[attrib]:
                example_attrib_val = []
                for ex in examples:
                    if val == self.training_sample[ex][attrib]:
                        example_attrib_val.append(ex)
                ni = len(example_attrib_val)
                ginival += ni/n * self.gini_value(example_attrib_val)
            impurity_red = total_gini - ginival
            if impurity_red > max_gini:
                max_gini = impurity_red
                chosen = attrib
        return chosen
        
    def gini_value(self, examples):
        gini = 1.0
        n = len(examples)
        if n == 0:
            return 1.0
        val_proportions = {}
        for val in self.target_vals:
            val_proportions[val] = 0
        for ex in examples:
            val_proportions[self.training_sample[ex][-1]] += 1
        for val in self.target_vals:
            val_proportions[val] = val_proportions[val] / n
            gini -= val_proportions[val]
        return gini

    def same_classification(self, examples):
        #if all target value of examples is same they give same classification 
        tval = self.training_sample[examples[0]][-1]
        for ex in examples:
            tvalc = self.training_sample[ex][-1]
            if tvalc != tval:
                return None
        return tval

    def getRandAttrib(self, notInclude):
        attrib_list = []
        for i in range(self.m_features):
            a = random.randrange(self.attrib_size)
            if a not in attrib_list and a not in notInclude:
                attrib_list.append(a)
        return attrib_list

    def build_tree(self, examples, attribs_already_considered):
        #examples is list of index to training_sample drawn with replacement
        attribs = self.getRandAttrib(attribs_already_considered)
##        if len(examples) == 0:
##            return default
        classification = self.same_classification(examples)
        if classification!= None:
            return self.Leaf(classification)
        elif len(attribs) == 0:
            #return majority value if no attribute left to check
            list_targets = [self.training_sample[i][-1] for i in examples]
            return self.Leaf(max(list_targets, key = list_targets.count))
        else:
            best = self.choose_attrib(attribs, examples)
            treenode = self.Node(best)
            for val in self.attrib_values[best]:
                examples_val = []
                for ex in examples:
                    if self.training_sample[ex][best] == val:
                        examples_val.append(ex)
                if len(examples_val) == 0:
                    list_targets_val = [self.training_sample[i][-1] for i in examples]
                    m = max(list_targets_val, key = list_targets_val.count)
                    treenode.addbranch(val, self.Leaf(m)) #m is subtree
                else:
                    subtree = self.build_tree(examples_val, attribs_already_considered + [best])
                    treenode.addbranch(val, subtree)
            return treenode

    def predict(self, attribs_val):
        #find target value based on provided attribute values
        p = self.tree
        #decision = None
        while True:
            if isinstance(p, self.Leaf):
                decision = p.value
                break
            else:
                p = p.branch[attribs_val[p.attrib]]   #go down the brach of current node/attribute whose value matches that of given attribute value
        return decision

    def display_tree(self, tree):
        if not isinstance(tree, DecisionTreeClassifier.Leaf):
            print(f'TrNode: A:{tree.attrib}', end = ' ')
            for b in tree.branch:
                bn = tree.branch[b]
                if not isinstance(bn, DecisionTreeClassifier.Leaf):
                    bn = bn.attrib
                    print(f'V:{b} B:{bn}', end = ' ')
                else:
                    bn = bn.value
                    print(f'V:{b} L:{bn}', end = ' ')
            print('')
            for b in tree.branch:
                if not isinstance(bn, DecisionTreeClassifier.Leaf):
                    bn = tree.branch[b]
                    self.display_tree(bn)

    def display(self):
        self.display_tree(self.tree)
        

                
            
