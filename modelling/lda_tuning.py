import gensim
import pandas as pd
from sklearn.model_selection import train_test_split

cleaned_col = 'cleaned'
cleaned_file = 'cleaned.csv'
random_state = 36118

def get_dict_corpus(X):
    # Extract the 'content' column as a list of sentences
    data = [str(sent).split() for sent in X[cleaned_col].tolist()]
    # Dictionary mapping of word to id
    dictionary = gensim.corpora.Dictionary(data)  
    # Preprocessed corpus of documents
    corpus = [dictionary.doc2bow(doc) for doc in data]  
    return dictionary, corpus

def get_coh_score(lda_model, corpus):
    coherence_scores = []
    # Get the topics with the highest coherence score the coherence for each topic.
    for _, coherence_score in lda_model.top_topics(corpus):
        coherence_scores.append(coherence_score)

    average_coherence = sum(coherence_scores) / len(coherence_scores)
    return average_coherence

def print_results(lda_model, corpus):
    # Print best coherence score (a relative value)
    print('Coherence score:', get_coh_score(lda_model, corpus))
    # Print model parameters  
    print('Best hyperparameters:')
    print("Number of Topics:", lda_model.num_topics)
    # Check if `alpha` is symmetric
    if len(lda_model.alpha) == lda_model.num_topics:
        print("Alpha: Symmetric")  # Symmetric if the length of `alpha` equals `num_topics`
    else:
        print("Alpha: Asymmetric")
    # Check if `eta` is symmetric
    if len(set(lda_model.eta)) == 1:
        print("Eta: Symmetric")  # Symmetric if the length of unique values in `eta` equals 1
    else:
        print("Eta: Asymmetric")
    print("Iterations:", lda_model.iterations)    

def train(X):
    # Prepare the corpus and dictionary
    dictionary, corpus = get_dict_corpus(X)
    # Define the hyperparameter search space
    hyperparameters = {
        'num_topics': [3, 5, 7],  # Number of topics
        'alpha': ['symmetric', 'asymmetric'],  # Dirichlet prior for document-topic distribution
        'eta': ['symmetric', 'auto'],  # Dirichlet prior for topic-word distribution, auto=asymmetric
        'iterations': [50, 100, 200]  # Number of iterations
    }

    best_model = None
    best_coherence_score = -float('inf')

    # Design an optimization strategy (i.e., grid search)
    for num_topics in hyperparameters['num_topics']:
        for alpha in hyperparameters['alpha']:
            for eta in hyperparameters['eta']:
                for iterations in hyperparameters['iterations']:
                    # Fit LDA model with the current hyperparameter configuration
                    lda_model = gensim.models.ldamodel.LdaModel(
                        corpus=corpus,
                        id2word=dictionary,
                        num_topics=num_topics,
                        alpha=alpha,
                        eta=eta,
                        iterations=iterations,
                        random_state=random_state
                    )
                    
                    # Get Coherence score with the LDA model
                    coherence_score = get_coh_score(lda_model, corpus)

                    # Update the best model if the current model performs better
                    if coherence_score > best_coherence_score:
                        best_coherence_score = coherence_score
                        best_model = lda_model        

    print('---Train results---')
    print_results(best_model, corpus)

    return best_model

def eval(lda_model, val_data):
    # Evaluate coherence score with validation dataset
    _, corpus = get_dict_corpus(val_data)
    print('---Validation results---')
    print_results(lda_model, corpus)

def get_best_model(df, eval=False):
    # Default no eval as no prediction on new data
    if eval:
        # Split the DataFrame into train and validation sets
        train_data, val_data = train_test_split(df, test_size=0.2, random_state=random_state)
        # Train the model
        best_model = train(train_data)
        # Evaluate the best model on a separate test set
        eval(best_model, val_data)
    else:
        best_model = train(df)

    return best_model