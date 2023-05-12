import streamlit as st
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Input, Flatten
from tensorflow.random import set_seed
from tensorflow.keras.backend import clear_session
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

st.markdown("<h2 style='text-align: center; color: white; font-weight: bold;'>LHP Capstone Project - Text Recognition </h2>",
            unsafe_allow_html=True)
st.divider()

st.markdown("<h3 style='text-align: center; color: #FFFAF4; text-decoration: underline;'>Loss & Accuracy Graph</h3>",
            unsafe_allow_html=True)

# example_graph = True
# if example_graph:
#     image_loss = "D:\CAPSTONE_AI\mc4ai-project-charrecognition\streamlit-app\loss.png"
#     st.image(image_loss, caption="Loss Graph with Epochs = 1000")
#     image_accuracy = "D:\CAPSTONE_AI\mc4ai-project-charrecognition\streamlit-app\precise.png"
#     st.image(image_accuracy, caption="Accuracy Graph with Epochs = 1000")

# Sidebar titles
st.sidebar.subheader('Configuration')
st.sidebar.caption('_Have fun!_')

# sidebar sliders
train_choice = st.sidebar.slider(
    'Choose the number of train pictures you want to use:', 100, 3410 - 100)
epoch_choice = st.sidebar.slider(
    'Choose the number of epochs:', 1, 100)

# sidebar checkbox
loss_function_option = [
    "categorical_crossentropy (Recommended)", 'CE', 'MAE', 'MSE']
loss_choice = st.sidebar.selectbox(
    "Choose your loss function: ", loss_function_option)

# validate options
config_finish = st.sidebar.button("Set Config")
if config_finish:
    # LOAD DATASET
    dataset = np.load("../np_dataset.npy")
    labels = np.load("../labels.npy")

    # SPLIT DATASET
    train_choice = int(train_choice)
    test_choice = int(3410 - train_choice)
    X_train, X_test, y_train, y_test = train_test_split(
        dataset, labels, test_size=test_choice, train_size=train_choice)

    # ONE-HOT ENCODING
    y_train_ohe = to_categorical(y_train, num_classes=62, dtype=int)
    y_test_ohe = to_categorical(y_test, num_classes=62, dtype=int)

    # INITIALIZE MODEL
    loss_choice = loss_choice.split()[0]
    clear_session()
    set_seed(42)
    np.random.seed(42)

    model = Sequential()
    model.add(Input(shape=X_train.shape[1:]))
    model.add(Flatten())
    model.add(Dense(62, activation='softmax'))
    model.compile(loss=f"{loss_choice}",
                  optimizer='adam', metrics='accuracy')

    # DRAW LOSS AND ACCURACY GRAPH
    epoch_choice = int(epoch_choice)
    with st.spinner("Please wait for model to load"):
        history = model.fit(X_train, y_train_ohe, epochs=epoch_choice)

    fig, axs = plt.subplots(figsize=(12, 4), ncols=2)
    axs[0].set_title("Loss")
    axs[0].plot(history.history["loss"])
    axs[1].set_title("Accuracy")
    axs[1].plot(history.history["accuracy"])
    # example_graph = not example_graph
    st.pyplot(fig)
    model.save(
        "D:\CAPSTONE_AI\mc4ai-project-charrecognition\streamlit-app\sequential_model.h5")
