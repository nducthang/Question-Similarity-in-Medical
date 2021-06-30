from ruamel import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from utils import save_vocabulary
from utils import build, preprocessing
from CNN import CNN
import tensorflow as tf

# Load config
config = yaml.safe_load(open('./src/CNN/config.yaml'))

# Load data
df_data = pd.read_csv(config['TRAIN_DATA'])[:500]

# build vocabulary
df_data, vocabulary, word_to_num, num_to_word = build(df_data)

# save
save_vocabulary(config['VOCABULARY'], vocabulary, word_to_num, num_to_word)

# split data
df_train, df_val = train_test_split(df_data, test_size=0.2)
df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)

# pre data
train_it = preprocessing(df_train, word_to_num)
val_it = preprocessing(df_val, word_to_num)

if __name__ == '__main__':
    num_word = len(vocabulary)

    model = CNN(config['INPUT_LENGTH'], num_word)

    model.summary()

    model.compile(loss="binary_crossentropy",
                  optimizer="adam", metrics=["accuracy"])

    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=config['MODEL_PATH'],
        monitor='val_accuracy',
        mode='max',
        save_weights_only=True,
        save_best_only=True
    )

    model.fit([train_it['question1'], train_it['question2']], train_it['labels'],
              batch_size=config['BATCH_SIZE'],
              epochs=config['EPOCHS'],
              validation_data=(
        [val_it['question1'], val_it['question2']], val_it['labels']),
        validation_batch_size=4*config['BATCH_SIZE'],
        callbacks=[model_checkpoint_callback]
    )
