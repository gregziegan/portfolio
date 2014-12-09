## Pandora Ad Classification

Greg Ziegan & MJ Harkins



## Why Pandora?

The company I work for, Vertical Knowledge, works on consulting projects for hedge funds, government departments, and other private agencies.

Hedge funds want something from us: _insights_


A company like Pandora is a freemium service. It provides a usable platform for free users and incentives to premium members.


Pandora needs to sustain and profit from even its free service. 

The premium members are charged a fee but this revenue does not provide the company with large enough profits.


In order to sustain its free service, Pandora will show advertisements from companies who believe these ads will somehow coax the user into visiting their company site.


If we can discover the distribution of ads shown by these external companies, we may have a roughly accurate view of what companies have invested in Pandora, and the amount they have invested compared to others.


And that leaves us with thousands of screenshots of advertisments to classify.



### But wait, why not just follow the ad's link?

* We do not want to alter traffic to these sites. We are classifying across hundreds of stations and geographically distributed IP's

* Why not just look at the link's url? The ads are embedded in the audio player (making the links hard to find) and are often shortened and made unrecognizable



## Classification: The Approach

We will take a moment here to cite Gary Doran, as he has helped us greatly in understanding unsupervised feature detection and multiple instance algorithms.


## Steps to Success
1. Image Segmentation
2. Feature Preparation
3. Kernel Selection
4. SVM and MISVM
5. Profit



## Image Segmentation


Here are some example advertisements:

![Pandora Ad 1](static/presentations/ad-talk-imgs/pandora_ad_1.jpg)


![Pandora Ad 2](static/presentations/ad-talk-imgs/pandora_ad_2.jpg)


![Pandora Ad 3](static/presentations/ad-talk-imgs/pandora_ad_3.jpg)


We used each pixel's RGB color values as features for clustering.


We sent the pixel data for each image through an implementation of the k-means clustering algorithm.


We tried three algorithms from the scikit-image library:

* Quickshift
* SLIC
* Felzenswalb's


### Quickshift

"Segments image using quickshift clustering in Color-(x,y) space.

Produces an oversegmentation of the image using the quickshift mode-seeking algorithm."


![Pandora Quickshift Ad 1](static/presentations/ad-talk-imgs/pandora_ad_quickshift.png)


We thought quickshift meant quick. It was not.

The algorithm took ~5 seconds to segment an image... total clustering time: 40 minutes :(


We tried another of the three, SLIC, and it gave fantastic results.

![Pandora SLIC Ad 1](static/presentations/ad-talk-imgs/pandora_ad_slic.png)


Better yet, it took less than a quarter of a second to cluster.


### SLIC
"Segments image using k-means clustering in Color-(x,y,z) space."


![Pandora SLIC Ad 2](static/presentations/ad-talk-imgs/pandora_ad_2_slic.png)


![Pandora SLIC Ad 3](static/presentations/ad-talk-imgs/pandora_ad_3_slic.png)


We were very happy with SLIC and after reviewing the third algorithm we decided against it since we couldn't pronounce it.



## Feature Preparation


Once we had clusters, we took the average RGB value for each cluster as a feature for the training set.


### An additional approach


We discussed adding Gabor wavelets to the clustering algorithms and using the refined clusters' RGB values/texture features as the example set.


This proved unnecessary due to excellent results with vanilla SLIC segmentation.


However, another task at Vertical Knowledge would deal with recognizing objects with texture, orientation, and depth.

It is very likely more complicated features, including Gabor wavelets, would be needed to classify such an image.



## Kernel Selection


### Contenders:

* Linear
* RBF (Radial Basis Function)
* NSK (Normalized Set Kernel)
* EMD (Earth Mover's Distance)


Linear was quickly ruled out.


The RBF kernel creates gaussian bubble around the data giving some smoothness to the data.


The NSK can wrap a base kernel and better normalize the features than a vanilla RBG kernel.


The EMD kernel is also implemented by Gary.

It uses EMD, which measures the distance between two probability distributions.


We decided on NSK since RBF is a common kernel and already exists in the misvm repository.



# SVM


Using a standard support vector machine, we classified the examples with the following results:

![SVM Results](static/presentations/ad-talk-imgs/svm_roc.png)


* Accuracy: 0.95
* Precision: 0.90
* Recall: 0.98
* AROC: 0.99



# MISVM

(Results Pending)


The multiple instance learner is still being tested on the data set.

We're currently getting warnings and all zeroes for predictions.


It's not nearly as quick as the SVM, as it considers all the instances in a bag with a single image.


The results are showing that some parameter is not tuned correctly.

We're confident the algorithm will perform at least as well as the SVM since Gary's implementation has been used and resulted in 99% accuracy on a similar data set.



# Conclusions


We were both extremely excited to see such high accuracy from a standard SVM.


However, this result is only from one company where we had ~190 example images.


There are 20 other companies with above 30 examples, but many from there on have under 5 examples to train on.


This project will need to shift focus in implementation to take on a state of Active Learning.


We discussed having the SVM be retrained at each new labeled instance.

Another possibility was to provide a feature of the time the ad was found, weighting more recent ads as more important while still keeping a reasonable training set size.


But while the MISVM tooks magnitudes longer, the SVM took less than a minute on 515 images. This means the first suggestion of retraining is very feasible for the time being.



# FIN
