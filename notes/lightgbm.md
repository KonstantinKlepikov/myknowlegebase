---
description: Градиент бустинг фреймворк LightGBM
---
# Lightgbm

Градиент бустинг фреймворк LightGBM для [[machine-learning]]

LightGBM is a gradient boosting framework that uses tree based learning algorithms. It is designed to be distributed and efficient with the following advantages:

- Faster training speed and higher efficiency.
- Lower memory usage.
- Better accuracy.
- Support of parallel, distributed, and GPU learning.
- Capable of handling large-scale data.

[Ссылка на документацию](https://lightgbm.readthedocs.io/en/latest/index.html)

## Python quik start

[Статья](https://lightgbm.readthedocs.io/en/latest/Python-Intro.html)

`pip install lightgbm`

```python
import lightgbm as lgb
```

The LightGBM Python module can load data from:

- LibSVM (zero-based)/TSV/CSV/ XT format file
- NumPy 2D array(s), pandas DataFrame, H2O DataTable’s Frame, SciPy sparse matrix
- LightGBM binary file
- LightGBM `Sequence` object(s)

The data is stored in a `Dataset` object.

To load a LibSVM **(zero-based)** text file or a LightGBM binary file into Dataset:

```python
train_data = lgb.Dataset('train.svm.bin')
```

To load a **numpy array** into Dataset:

```python
import numpy as np

data = np.random.rand(500, 10)  # 500 entities, each contains 10 features
label = np.random.randint(2, size=500)  # binary target
train_data = lgb.Dataset(data, label=label)
```

To load a **scipy.sparse.csr_matrix array** into Dataset:

```python
import scipy
csr = scipy.sparse.csr_matrix((dat, (row, col)))
train_data = lgb.Dataset(csr)
```

Load from **Sequence objects**. We can implement `Sequence` interface to read binary files. The following example shows reading HDF5 file with `h5py`:

```python
import h5py

class HDFSequence(lgb.Sequence):
    def __init__(self, hdf_dataset, batch_size):
        self.data = hdf_dataset
        self.batch_size = batch_size

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data)

f = h5py.File('train.hdf5', 'r')
train_data = lgb.Dataset(HDFSequence(f['X'], 8192), label=f['Y'][:])
```

**Saving Dataset into a LightGBM binary file will make loading faster:**

```python
train_data = lgb.Dataset('train.svm.txt')
train_data.save_binary('train.bin')
```

**Create validation data**. In LightGBM, the validation data should be aligned with training data.

```python
validation_data = train_data.create_valid('validation.svm')
# or
validation_data = lgb.Dataset('validation.svm', reference=train_data)
```

**Specific feature names and categorical features**:

```python
train_data = lgb.Dataset(data, label=label, feature_name=['c1', 'c2', 'c3'], categorical_feature=['c3'])
```

LightGBM can use categorical features as input directly. It doesn’t need to convert to one-hot encoding, and is much faster than one-hot encoding (about 8x speed-up). But you should convert your categorical features to int type before you construct Dataset.

**Weights can be set when needed**:

```python
w = np.random.rand(500, )
train_data = lgb.Dataset(data, label=label, weight=w)
# or
train_data = lgb.Dataset(data, label=label)
w = np.random.rand(500, )
train_data.set_weight(w)
```

And you can use `Dataset.set_init_score()` to set initial score, and `Dataset.set_group()` to set group/query data for ranking tasks.

**Setting parameters**:

```python
# Booster parameters
param = {'num_leaves': 31, 'objective': 'binary'}
param['metric'] = 'auc'
# You can also specify multiple eval metrics
param['metric'] = ['auc', 'binary_logloss']
```

**Training**:

Training a model requires a parameter list and data set

```python
num_round = 10
bst = lgb.train(param, train_data, num_round, valid_sets=[validation_data])

# After training, the model can be saved
json_model = bst.dump_model()

# A saved model can be loaded
bst = lgb.Booster(model_file='model.txt')  # init model
```

**Training with 5-fold CV**:

```python
lgb.cv(param, train_data, num_round, nfold=5)
```

**Early Stopping**:

If you have a validation set, you can use early stopping to find the optimal number of boosting rounds. Early stopping requires at least one set in `valid_sets`. If there is more than one, it will use all of them except the training data

```python
bst = lgb.train(param, train_data, num_round, valid_sets=valid_sets, early_stopping_rounds=5)
bst.save_model('model.txt', num_iteration=bst.best_iteration)
```

The model will train until the validation score stops improving. Validation score needs to improve at least every `early_stopping_rounds` to continue training

**Prediction**:

```python
# 7 entities, each contains 10 features
data = np.random.rand(7, 10)
ypred = bst.predict(data)
```

If early stopping is enabled during training, you can get predictions from the best iteration with `bst.best_iteration`

## Как устроен LightGBM

[Читай тут](https://lightgbm.readthedocs.io/en/latest/Features.html)

## Параметры

[Читай тут](https://lightgbm.readthedocs.io/en/latest/Parameters.html)

[Интерактивный список параметров с пописанием](https://lightgbm.readthedocs.io/en/latest/Parameters.html)

Format

```python
params = {
   "monotone_constraints": [-1, 0, 1]
}
```

### Parameters Tuning

- [Autotuning with FLAWL](https://github.com/microsoft/FLAML)
- [Autotuning with Optuna](https://github.com/microsoft/FLAML)

Несколько подходов, достыпныз в lightgbm:

- [Tune Parameters for the Leaf-wise (Best-first) Tree](https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html#tune-parameters-for-the-leaf-wise-best-first-tree)
- [For Faster Speed](https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html#for-faster-speed)
- [For Better Accuracy](https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html#for-better-accuracy)
- [Deal with Over-fitting](https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html#deal-with-over-fitting)

[Полностю статья](https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html#deal-with-over-fitting)

## Python API

[см.тут](https://lightgbm.readthedocs.io/en/latest/Python-API.html)

## GPU tutorial

[см.тут](https://lightgbm.readthedocs.io/en/latest/GPU-Tutorial.html#lightgbm-gpu-tutorial)

## Advanced Topics

[см.тут](https://lightgbm.readthedocs.io/en/latest/Advanced-Topics.html)

- Missing Value Handle
- Categorical Feature Support
- LambdaRank
- Cost Efficient Gradient Boosting


[//begin]: # "Autogenerated link references for markdown compatibility"
[machine-learning]: ../lists/machine-learning "Machine-learning"
[//end]: # "Autogenerated link references"