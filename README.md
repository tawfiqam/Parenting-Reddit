# Pseudonymous Parents: Comparing Parenting Roles and Identities on the Mommit and Daddit Subreddits
This repository contains the code used in our analysis of Parenting subreddits. In our CHI paper, we used unsupervised machine learning techniques - namely, Latent Dirichlet Analysis (LDA) and Word2Vec. 

The following figure shows how we trained an LDA model for the aggregated model of r/Parenting, r/Mommit and r/Daddit as well as independent LDA models for r/Daddit and r/Mommit. In addition, independent Word2Vec models for r/Mommit and r/Daddit was trained to differentiate similar topics discussed by users of the two subreddits. 

![alt text](http://www-personal.umich.edu/~tawfiqam/ParentingLDAWord2vecFigure.png)

This repository contains four Python notebooks: (1) Reddit_Final; (2) Daddit_Final; (3) Mommit_Final and (4) LDA heatmap_Final. The first three show how we carried out the LDA analysis for all three subreddits, then independent LDA models for Daddit and Mommit independently. Each of the Daddit and Mommit notebooks also show how we trained independent Word2Vec models for each of the corpora. 

The code also shows how jaccard similarity was calculated for each of the subreddit comments. Following is the definition of how the score for each of the comments was calculated. 

![alt text](http://www-personal.umich.edu/~tawfiqam/jaccard_similarity.png)

LDA heatmap_Final shows how we created heatmaps of select topic scores throughout all three subreddits. Following is an example:

![alt text](http://www-personal.umich.edu/~tawfiqam/LDATopicHeatExampleNew.png)

If you'd like to know more about our research, you can find our paper [here](http://www-personal.umich.edu/~tawfiqam/Ammari_Reddit_Parenting_CHI_2018.pdf).

