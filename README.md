##  Product Recommendation Engine

### Problem Statement
One of the top strategic objectives for e-commerce businesses today is personalization.  There are many techniques to deliver personalized recommendations to users, including content based filtering, user-user collaborative filtering, item-item collaborative filtering, and hybrid approaches.  None have achieved the level of performance as matrix factorization, which is a collaborative filtering recommender model that learns probabilistic distribution of user-item preferences by decomposing the user-item interaction matrix into the product of two lower dimensionality rectangular matrices.

Building any of these models in isolation is fairly straightforward, but deploying to production when dealing with massive datasets and the need for low-latency real world predictions presents some different challenges. In this project, I build a matrix factorization model to recommend new products to returning users of an e-commerce site, with a focus on productionizing the model and delivering low latency (< 100 ms) recommendations.

### Project Summary
* Applied matrix factorization algorithm to generate recommended items for users returning to an e-commerce website, using the awesome 'implicit' Python package. 
* Created Flask webservice to make app responsive to requests to train model and predict new items for a given user. 
* Containerized app with Docker so it can be run from any machine/environment.

## Code and resources used
* Python Version: 3.8
* Packages: flask, pandas, numpy, sklearn, implicit
* Dependencies: Docker

## App Architecture
![app architecture](https://github.com/bdbacik/product_recommender/blob/main/images/app_architecture.png)

## Deployment 
In terminal, set current directory to folder with app contents
> $ cd /path/to/app

Build image and run container with docker compose 
> docker-compose -f docker-compose.dev.yml up --build

To train the model (this will take a few minutes since the matrix has almost 1 billion cells)
> $ curl http://localhost:5000/train

Once model is trained, get predictions with a user with request of the form
> $ curl -d '{"user_id_hash":"b9cbac77a336d62efd54404d2bccaecd"}' -H "Content-Type:application/json" -X POST http://localhost:5000/reco

Output will be a dictionary with keys score, item_name, item_id, brand name and values for the top 5 results for the requested user 
