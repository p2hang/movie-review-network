# movie-review-network
Movie Review Network Analysis

### Hypothesis
- If the shortest distance between two movies are smaller,
the features of two movies are similar.

  - Distance: Determined by the score and helpfulness of a review

  - Feature of a movie: Extracted from tf-idf on reviews, where all review of one movie is a document.

### Related Work
- Papadopoulos, Fragkiskos, et al. "Popularity versus similarity in growing networks." Nature 489.7417 (2012): 537-540.
  - Besides popularity, similarity is another dimension of attractiveness.

- Hongyuan Zha, Xiaofeng He, Chris Ding, Horst Simon, Ming Gu. "Bipartite Graph Partitioning and Data Clustering"
  - Bipartite Graph partitioning it another way for data clustering analysis, besides features extraction and matrix factorization.

- Thiago de Paulo Faleiros, Alneu de Andrade Lopes. "Bipartite Graph for Topic Extraction"
  - Bipartite Graph propagation is a useful method for topic extraction and clustering.

- Julian McAuley, Jure Leskovec. "Hidden Factors and Hidden Topics: Understanding Rating Dimensions with Review Text",
  - Develop statistical models that combine latent dimensions in rating data with topics in review text.

- Julian McAuley, Jure Leskovec. "Modeling the Evolution of User Expertise through Online Reviews"
  - Develop a unsupervised model for evolution of users' appreciation ability through their reviews.

### Result
- [The correlation graph]
