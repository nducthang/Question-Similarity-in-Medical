from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input, MaxPooling1D, Conv1D, Conv2D, Embedding, Dot
from keras.layers.merge import Concatenate


def CNN(input_length, num_word):
    input1 = Input((input_length,))
    input2 = Input((input_length,))

    Embedding_matrix = Embedding(
        num_word, 300, input_length=input_length, name="embedding")

    z1 = Embedding_matrix(input1)
    z2 = Embedding_matrix(input2)

    Conv = Conv1D(filters=200,
                  kernel_size=3,
                  padding="valid",
                  activation="relu",
                  strides=1)
    conv1 = Conv(z1)
    conv2 = Conv(z2)
    conv1 = MaxPooling1D(pool_size=2)(conv1)
    conv2 = MaxPooling1D(pool_size=2)(conv2)
    conv1 = Flatten()(conv1)
    conv2 = Flatten()(conv2)
    similar_score = Dense(4800, activation=None)(conv1)
    similar_score = Dot(1)([similar_score, conv2])
    z = Concatenate()([conv1, similar_score, conv2])
    z = Dropout(0.8)(z)
    z = Dense(100, activation="relu")(z)
    model_output = Dense(1, activation="sigmoid")(z)
    return Model([input1, input2], model_output)
