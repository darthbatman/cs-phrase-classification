# cs-phrase-classification

![python (scoped)](https://img.shields.io/badge/python-%3E%3D3.7.6-brightgreen.svg)

## Description

Classification of phrases as phrases inside or outside the domain of computer science.

## Usage

### Installation

Install the dependencies with the following command.

`pip install -r requirements.txt`

### Execution

The codebase is comprised of files that build the dataset and build a model to classify phrases.

`get_dblp_titles.py` is used to extract the titles of articles from the DBLP dataset.

`get_noun_phrases.py` is used to extract noun phrases from titles.

`hand_label_phrases.py` is used to hand label phrases and allows the user to view Google's suggested queries for each phrase.

`build_dataset.py` is used to aggregate features for a set of labeled phrases.

`combined_metric_svm.py` is used to fit an SVM (support vector machine) to a dataset of phrases.

`combined_metric_decision_tree.py` is used to fit a decision tree to a dataset of phrases.

`pca.py` is used to perform PCA (principal component analysis) on a dataset of phrases.

## Authors

* Rishi Masand