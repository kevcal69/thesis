import json
import math

from representation.models import Case
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
from pybrain.structure import TanhLayer
from representation.models import Case
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader

def trainDataSet():
    cases = Case.objects.exclude(geocode__isnull=True, geocode__grid=-1)

    print "Data Representation"
    ds = SupervisedDataSet(5245, 5245)
    for w in xrange(0,52):
        print "Start week w",
        dataset_input = [0 for i in xrange(0,5245)]
        dataset_output = [0 for i in xrange(0,5245)]
        for i in xrange(0,5245):
            dataset_input[i] = cases.filter(geocode__grid=i, morbidity__week=w).count()
            dataset_output[i] = 1 if (cases.filter(geocode__grid=i, morbidity__week=w+1).count() > 0 or cases.filter(geocode__grid=i, morbidity__week=w+2).count() > 0) else 0
        ds.addSample( (dataset_input), (dataset_output))
        print " - done week w"
    # tstdata, trndata = ds.splitWithProportion(0.25)
    print "Train"
    net = buildNetwork( 5245, 1000, 5245, bias=True)
    trainer = BackpropTrainer(net, ds, learningrate=0.1, momentum=0.99)

    terrors = trainer.trainUntilConvergence(verbose = None, validationProportion = 0.33, maxEpochs = 1000, continueEpochs = 10 )
    # print terrors[0][-1],terrors[1][-1]
    fo = open("data.txt", "w")
    for input, expectedOutput in ds:
        output = net.activate(input)
        count = 0
        for q in xrange(0, 5245):
            print math.floor(output[q]), math.floor(expectedOutput[q])
            if math.floor(output[q]) == math.floor(expectedOutput[q]):
                count+=1    
        m = count/5245
        fo.write("{0} ::  {1}".format(count, m));
    # do train

def dataFile():
    print "Start processing"
    cases = Case.objects.exclude(geocode__isnull=True, geocode__grid=-1)
    ds = {}
    index = 0
    for w in xrange(0,52):
        print "Start week {}".format(w) 
        dataset_input = [0 for i in xrange(0,1316)]
        dataset_output = [0 for i in xrange(0,1316)]
        for i in xrange(0,1316):
            dataset_input[i] = cases.filter(geocode__grid=i, morbidity__week=w).count()
            dataset_output[i] = 1 if (cases.filter(geocode__grid=i, morbidity__week=w+1).count() > 0 or cases.filter(geocode__grid=i, morbidity__week=w+2).count() > 0) else 0
        ds[index] = {'input' : dataset_input, 'output' : dataset_output}    
        index+=1
    with open('new_data2.txt', 'w') as outfile:
        json.dump(ds, outfile)

def test2():
    i = 1
    w = 2
    cases2 = Case.objects.exclude(geocode__isnull=True, geocode__grid=-1)
    cases3 = Case.objects.exclude(geocode__isnull=True, geocode__grid=-1)
    m = 1 if (cases2.filter(geocode__grid=i, morbidity__week=w).count() > 0 or cases3.filter(geocode__grid=i, morbidity__week=w).count() > 0) else 0
    print m

def run_data():
    with open('new_data2.txt') as data_file:
        data = json.load(data_file)
    ds = SupervisedDataSet(1316, 1316)
    for i in xrange(0, 51):
        print "Adding {}th data sample".format(i),
        input = tuple(data[str(i)]['input'])
        output = tuple(data[str(i)]['output'])        
        # print len(input), len(output)
        ds.addSample( input, output)
        print ":: Done"

    print "Train"
    net = buildNetwork( 1316, 100, 1316, bias=True, )
    trainer = BackpropTrainer(net, ds)

    terrors = trainer.trainUntilConvergence(verbose = True, validationProportion = 0.33, maxEpochs = 20, continueEpochs = 10 )
    # print terrors[0][-1],terrors[1][-1]
    fo = open("results2.txt", "w")
    for input, expectedOutput in ds:
        output = net.activate(input)
        count = 0
        for q in xrange(0, 1316):
            print output[q], expectedOutput[q]
            if math.floor(output[q]) == math.floor(expectedOutput[q]):
                count+=1    
        m = float(count)/1316.00
        print "{0} ::  {1}".format(count, m)
        fo.write("{0} ::  {1}\n".format(count, m))


def dataFile2():
    print "Start processing"
    cases = Case.objects.exclude(geocode__isnull=True, geocode__grid=-1)
    ds = []
    index = 0
    for w in xrange(1, 53):
        print "Start week {}".format(w)
        for grid in xrange(1, 1317):
            input = [cases.filter(geocode__grid=grid, morbidity__week=w).count(), w, grid]
            output = 1 if (cases.filter(geocode__grid=grid, morbidity__week=w+1).count() > 0 or cases.filter(geocode__grid=grid, morbidity__week=w+2).count() > 0) else 0
            print input, output
            ds.append([tuple(input), output])
    with open('new_data1.txt', 'w') as outfile:
        json.dump(ds, outfile)


def run_data1():
    with open('new_data1.txt') as data_file:
        data = json.load(data_file)
    output = set([i[2] for i in [d[0] for d in data if d[1] == 1]])
    print output
    m = [d[0] for d in data]
    print (max([d for a, s, d in m]), min([d for a, s, d in m]), float(max([d for a, s, d in m])-min([d for a,s,d in m])))
    case = [min([a for a, s, d in m]), float(max([a for a, s, d in m])-min([a for a,s,d in m]))]
    week = [min([s for a, s, d in m]), float(max([s for a, s, d in m])-min([s for a,s,d in m]))]
    grid = [min([d for a, s, d in m]), float(max([d for a, s, d in m])-min([d for a,s,d in m]))]
    ds = SupervisedDataSet(3, 1)
    import random
    random.shuffle(data)
    print len(data)
    for i in xrange(0, len(data)):
        # print "Adding {}th data sample".format(i),
        x1 = float(data[i][0][0] - case[0])/case[1]
        x2 = float(data[i][0][1] - week[0])/week[1]
        x3 = float(data[i][0][2] - grid[0])/grid[1]
        input = (x1, x2, x3)
        output = data[i][1]
        ds.addSample(input, output)
        # print ":: Done"

    print "Train"
    # net = buildNetwork(3, 3, 1, bias=True)\
    net = NetworkReader.readFrom('dengue_network.xml')
    tstdata, trndata = ds.splitWithProportion( 0.33 )
    trainer = BackpropTrainer(net, trndata)
    # terrors = trainer.trainUntilConvergence(verbose = True, validationProportion = 0.33, maxEpochs = 100, continueEpochs = 10 )


    # mse = [0]
    # acceptable_error = .00001
    # for i in xrange(0,1000):
    #     print i," ",
    #     mse_c = trainer.train()
    #     if (mse_c < acceptable_error):
    #         break
    #     mse.append(mse_c)
    #     print mse_c

    threshold = [0.25, 0.30]
    for t in threshold:
        print "Testing threshold :", t
        true_positive = 0.0
        true_negative = 0.0
        false_positive = 0.0
        false_negative = 0.0

        data_to_write = []
        data_to_write_input = []
        for input, expectedOutput in tstdata:
            o = net.activate(input)
            output = 1.0 if o[0] > t else 0.0
            data_to_write.append((int((input[0]*case[1]) + case[0]), int((input[1]*week[1]) + week[0]),int((input[2]*grid[1]) + grid[0]), output))
            if (output == expectedOutput):
                if output == 1.0:
                    true_positive += 1.0
                else:
                    true_negative += 1.0
            else:
                if output == 1.0:
                    false_positive += 1.0
                else:
                    false_negative += 1.0
        # NetworkWriter.writeToFile(net, 'dengue_network1.xml')
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        f = (2 * precision * recall)/(precision + recall)
        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)

        def getKey(item):
            return item[1]
        data_to_write = sorted(data_to_write,  key=getKey)
        counts = {
            # "MSE" : mse,
            # "DATA": data_to_write,
            "Threshold": t,
            "Precision": precision,
            "Recall": recall,
            "F-Measure": f,
            "Accuracy": accuracy,
            "Values": {
                "True Positive": true_positive,
                "True Negative": true_negative,
                "False Positive": false_positive,
                "False Negative": false_negative
            }
        }
        print "Accuracy :", accuracy
        print "Precision :", precision
        print "Recall :", recall
        print "F-Measure :", f
        print counts
        # errors = {
        #     "terrors" : terrors
        # }
        # with open('data8.json', 'w') as outfile:
        #     json.dump(counts, outfile, indent=4)
    exit()


def graph_training():
    import matplotlib.pyplot as plt
    with open('data3.json') as outfile:
        mData = json.load(outfile)
    # mse = mData['MSE'][1:]
    # xtraining = [i for i in xrange(0,len(mse))]
    # plt.plot(xtraining,mse)
    # plt.show()
    mse = mData['MSE'][1:]
    xtraining = [i for i in xrange(0, len(mse))]
    plt.plot(xtraining, mse)
    plt.show()
    exit()


def vali():
    from pybrain.tools.validation import ModuleValidator
    from pybrain.tools.validation import CrossValidator
    with open('new_data1.txt') as data_file:
        data = json.load(data_file)
    m = [d[0] for d in data]
    case = [min([a for a, s, d in m]), float(max([a for a, s, d in m])-min([a for a, s, d in m]))]
    week = [min([s for a, s, d in m]), float(max([s for a, s, d in m])-min([s for a, s, d in m]))]
    grid = [min([d for a, s, d in m]), float(max([d for a, s, d in m])-min([d for a, s, d in m]))]
    ds = SupervisedDataSet(3, 1)
    import random
    random.shuffle(data)
    print len(data)
    for i in xrange(0, len(data)):
        # print "Adding {}th data sample".format(i),
        x1 = float(data[i][0][0] - case[0])/case[1]
        x2 = float(data[i][0][1] - week[0])/week[1]
        x3 = float(data[i][0][2] - grid[0])/grid[1]
        input = (x1, x2, x3)
        output = data[i][1]
        ds.addSample(input, output)
        # print ":: Done"

    print "Train"
    net = buildNetwork(3, 3, 1, bias=True)
    tstdata, trndata = ds.splitWithProportion( 0.33 )
    trainer = BackpropTrainer(net, trndata)
    mse = []
    modval = ModuleValidator()
    for i in range(100):
        trainer.trainEpochs(1)
        trainer.trainOnDataset(dataset=trndata)
        cv = CrossValidator(trainer, trndata, n_folds=10, valfunc=modval.MSE)
        mse_val = cv.validate()
        print "MSE %f @ %i" % (mse_val, i)
        mse.append(mse_val)

    with open('cross_validation.json', 'w') as outfile:
            json.dump(mse, outfile, indent=4)
