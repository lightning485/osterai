# Number of Easter eggs, by classification or regression?
Finding and counting eggs hidden in the grass is a simple scenario where we might want to teach the AI how to "count". The idea is to present pictures showing a known number of eggs to a Artificial Neural Net and then to hope that the output will be correct even for a picture with a number of eggs that the Net has never seen before.

![](./figures/motivation.jpg)

## How it does not work right away
Usually, in classification problems the output of the classifying Net is written in "one-hot encoding" with a vector of the same length as the number of classes. This makes sense, because usually different classes are not in an ordered relation to each other, and maybe one object can belong to several classes. However, in the egg counting example, this leads to a Net that can't decide whether 5 eggs are 4 or 6 eggs. Since it has never seen an example of class 5 and because the way the output is represented does not motivate "interpolation" between the separate classes, this was not the approach to learn counting right away.

![](./figures/outcome_classification.jpg)

![](./figures/score_heatmap_unknown_data.jpg)

## How it does work
If the egg counting problem is formulated as a regression problem, the Net comes up with the answer "5" (after rounding 4.971472) even though it has never seen a picture with 5 eggs during the training phase. I assume that the model learns the density of eggs in the image rather than a hard count. The difference to the classification formulation is that the output is seen more like a single variable which can be interpolated.

![](./figures/outcome_regression.jpg)
![](./figures/histogram_unknown_data.jpg)

When looking at the outputs of the whole training data, one sees the tendency of the Net not to output sharp integers, but to scatter around them. This was not forbidden by the architecture, as it was set up for continous regression, but it is disencouraged in the training because the ground truth is integer-valued. The correct "counting" seems to become the more difficult the more eggs are present in the images.

![](./figures/histogram_known_data.jpg)

## Technical Details

See the jupyter_notebooks folder for the code.

### Synthetic toy data
For the cases "0, 1, 2, 3, 4, 5, 6, and 7 eggs", 2000 images of resolution 256x256 each have been rendered with Blender. A python script was used to distribute them uniformly randomly without overlap. Also the position of a light source was changed randomly and the particle system used for the grass got a new seed value for each frame.

See the data_generation folder for *.blend file (Blender 2.92) and python script. Because of storage limitations, the images are not included in the repo but can be generated again with Blender.

### Network architecture
A simple network (input resolution 64x64 rgb) with two convolutional layers (4 and 8 filters with kernel size) and two dense layers (16 and 8 neurons, starting from a 2048 flattened layer) was chosen, starting with a more complex network and then manually simplyfing it until it was lightweight and still showed acceptable performance. For the classification, the activation function of the output layer was a `softmax` and `None` for the regression.

### Training
The cases "0, 1, 2, 3, 4, 6, and 7 eggs" were used for training with 0.2 validation split. Training was performed in 5 epochs with the `adam` optimizer,  `categorical_crossentropy` loss for the classification (final accuary approximately 95 %), and `mse` loss for the regression (went down to approximately 0.3). It took few minutes on a gaming laptop. The images with "5 eggs" were kept separate for the testing whose results are described above.