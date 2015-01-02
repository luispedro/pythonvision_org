---
title: Classification example
permalink: examples/classification
categories: tutorials
---

Imagine you want to classify a collection of images into two groups. For
simplicity, we can call one *positive* and the other *negative*. If
these are, for example, scans of documents, they might be documents
where there is text versus blank pages (this was the original
motivation); or it might be something else entirely.

Here is a possible solution, using mahotas and milk.

1.  Start by creating two directories: `positives/` and `negatives/`
    where you will manually pick out a few examples of positive and
    negative.
2.  I will assume that the rest of the data is in an unlabeled/
    directory
3.  Compute features for all of the images in positives and negatives
    learn a classifier.
4.  Use that classifier on the unlabeled images

In the code below I used [jug](http://luispedro.org/software/jug) to
give you the possibility of running it on multiple processors, but the
code also works if you remove every line which mentions `TaskGenerator`:

    from glob import glob
    import mahotas
    import mahotas.features
    import milk
    from jug import TaskGenerator


    @TaskGenerator
    def features(imname):
        img = mahotas.imread(imname)
        return mahotas.features.haralick(img).mean(0)

    @TaskGenerator
    def learn_model(features, labels):
        learner = milk.defaultclassifier()
        return learner.train(features, labels)

    @TaskGenerator
    def classify(model, features):
         return model.apply(features)

    positives = glob('positives/*.jpg')
    negatives = glob('negatives/*.jpg')
    unlabeled = glob('unlabeled/*.jpg')


    features = map(features, negatives + positives)
    labels = [0] * len(negatives) + [1] * len(positives)

    model = learn_model(features, labels)

    labeled = [classify(model, features(u)) for u in unlabeled]

This uses texture features, which is probably good enough, but you can
play with other features in mahotas.features if you’d like (or try
`mahotas.surf`, but that gets more complicated).

(I originally wrote this as a response to a question on Stackoverflow
[http://stackoverflow.com/q/5426482/248279]).

