# The model training code is lost, the saved model itself is outdated and can't be converted to tf-lite or onnx.
# Tensorflow is too big for PythonAnywhere. Therefore, the generator feature is disabled for now.
# import tensorflow as tf
# import numpy as np
# from random import choice

# vocab = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '▶', '☑', '☝', '☠', '☢', '⚠', '✅', '✈', '❌', '️', '🌹', '🍋', '🎁', '🎉', '🎵', '🏓', '🐜', '👉', '👋', '💀', '📈', '📡', '📢', '📺', '🔔', '🔥', '🔰', '🔴', '🖌', '😠', '🚨', '🟥', '🟨', '🤓', '🧱', '🧲', '\U000e0000']
# char2idx = {u:i for i, u in enumerate(vocab)}
# idx2char = np.array(vocab)

# v = [c for c in vocab if c not in {"\\", ">", "=", "\U000e0000", '️', "_", "/", "^", "}", "|", "&", "?", "]", ",", "-", ".", ")", "%", ":"}]

# MODEL_PATH = "/home/Terraa/xQcowTitles/static/main/GeneratorModel"

# def load_generator_model():
#     return tf.keras.models.load_model(MODEL_PATH)

# def getRandomChar():
#     return choice(v)

# def generate_text(model, start_string: str, temperature: float, min_length: int):
#     input_eval = [char2idx[s] for s in start_string]
#     input_eval = tf.expand_dims(input_eval, 0)

#     text_generated = []
#     model.reset_states()
#     c = len(start_string)
#     while True:
#         predictions = model(input_eval)
#         predictions = tf.squeeze(predictions, 0)

#         predicted_id = tf.random.categorical(predictions / temperature, num_samples=1)[-1,0].numpy()

#         input_eval = tf.expand_dims([predicted_id], 0)

#         predicted_char = idx2char[predicted_id]

#         if c >= min_length and predicted_char == " " or c > min_length + 20:
#             break

#         text_generated.append(predicted_char)
#         c += 1

#     return start_string + ''.join(text_generated)
