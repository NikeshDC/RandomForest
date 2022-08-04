import myRandomForest
import csv
import random

result_path = 'accuracy_'

def load_dataset_csv(dataset_path, _delimeter = ','):
    dataset = []
    with open(dataset_path) as dataset_file:
        datasetc = csv.reader(dataset_file, delimiter=_delimeter)
        for row in datasetc:
            if len(row) != 0:
                dataset.append(row)
            else:
                print('empty row')
    return dataset

def split_dataset(dataset, test_proportion = 0.25):
    #slits the dataset into training and test samples with test proportion equal to test_proportion
    train_data = dataset[:]
    test_data = []
    test_size = int(test_proportion * len(dataset))
    for i in range(test_size):
        r = random.randrange(0, len(train_data))
        t = train_data.pop(r)
        test_data.append(t)
    return train_data, test_data

if __name__ == "__main__":
    m_features = 5
    test_proportion = 0.3
    result_path += str(m_features) + '_' + str(test_proportion) + '.txt'
## change "<your path>" to the path where data set file is present; data is required in csv format
    datapath = '<dataset path>'
    dataset = load_dataset_csv(datapath, ',')
    traindata, testdata = split_dataset(dataset,test_proportion)
##    print("training",traindata)
##    print("test",testdata)
##    for row in dataset:
##        print(row)
##    for treesize in range(1,10):
##        rf = myRandomForest.RandomForestClassifier(traindata,treesize,m_features)
##        rf.build()
##        p = rf.test(testdata) * 100
##        print(f'Trees:{treesize}  Accuracy:{p}%')
##    for treesize in range(10,100,10):
##        rf = myRandomForest.RandomForestClassifier(traindata,treesize,m_features)
##        rf.build()
##        p = rf.test(testdata) * 100
##        print(f'Trees:{treesize}  Accuracy:{p}%')
##    for treesize in range(100,1001,100):
##        rf = myRandomForest.RandomForestClassifier(traindata,treesize,m_features)
##        rf.build()
##        p = rf.test(testdata) * 100
##        print(f'Trees:{treesize}  Accuracy:{p}%')

    accuracy_treesize = {}
    for treesize in range(1,10):
        accuracy_treesize[treesize] = 0
    for treesize in range(10,101,10):
        accuracy_treesize[treesize] = 0
##    for treesize in range(100,401,100):
##        accuracy_treesize[treesize] = 0

    iterations = 50
    
    for i in range(iterations):
        print(f'I:{i}')
        for treesize in range(1,10):
            rf = myRandomForest.RandomForestClassifier(traindata,treesize,m_features)
            rf.build()
            p = rf.test(testdata) 
            accuracy_treesize[treesize] += p
            print(f'Trees:{treesize}  Accuracy:{p*100}%')
        for treesize in range(10,101,10):
            rf = myRandomForest.RandomForestClassifier(traindata,treesize,m_features)
            rf.build()
            p = rf.test(testdata)
            accuracy_treesize[treesize] += p
            print(f'Trees:{treesize}  Accuracy:{p*100}%')
##        for treesize in range(100,401,100):
##            rf = myRandomForest.RandomForestClassifier(traindata,treesize,m_features)
##            rf.build()
##            p = rf.test(testdata)
##            accuracy_treesize[treesize] += p
##            print(f'Trees:{treesize}  Accuracy:{p*100}%')

    for acc in accuracy_treesize:
        accuracy_treesize[acc] /= iterations

    with open(result_path, 'w') as accuracy_save_file:
        for acc in accuracy_treesize:
            accuracy_save_file.write(f'{acc},{accuracy_treesize[acc]}\n')
        

    input()


#import dataset
#split into training and test set
#incrementally increase random forest size
#perform random forest training usinf bagging only
#classify test set and find accuracy
#output the accuracy and noof_forest to result file

#set randomfeature to p/3 and perform with bagging of feature set above once again
