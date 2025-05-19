import time
import aiohttp
import asyncio
import threading
import numpy as np
import tensorflow as tf
import concurrent.futures
from functools import lru_cache


class Pokefier:
    def __init__(self, num_interpreters=8):
        self.labels = eval(open("source/names.txt", "r").read())
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=num_interpreters
        )
        self.interpreter_pool = [
            self._initialize_interpreter() for _ in range(num_interpreters)
        ]
        self.interpreter_lock = threading.Lock()
        self.cache_lock = threading.Lock()
        self.prediction_cache = {}
        self.cache_timeout = 300

    def _remove_alpha_channel(self, image):
        return image[:, :, :3]

    def _preprocess_input_image(self, image):
        img = tf.image.resize(image, [224, 224]) / 255.0
        return img

    async def _prepare_image_for_prediction(self, image_url):
        with self.cache_lock:
            if image_url in self.prediction_cache:
                cache_entry = self.prediction_cache[image_url]
                if time.time() - cache_entry["timestamp"] < self.cache_timeout:
                    return cache_entry["data"], True

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                image_data = await response.read()

        image = tf.image.decode_image(image_data, channels=3).numpy()
        preprocessed_image = self._preprocess_input_image(image)

        return preprocessed_image, False

    async def predict_pokemon_from_url(self, image_url):
        preprocessed_data, is_cached = await self._prepare_image_for_prediction(
            image_url
        )

        if is_cached:
            return preprocessed_data

        with self.interpreter_lock:
            if not self.interpreter_pool:
                interpreter = self._initialize_interpreter()
            else:
                interpreter = self.interpreter_pool.pop()

        try:
            predicted_pokemon = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self._predict_pokemon_sync,
                interpreter,
                preprocessed_data.numpy() if not is_cached else preprocessed_data,
            )

            with self.cache_lock:
                self.prediction_cache[image_url] = {
                    "data": predicted_pokemon,
                    "timestamp": time.time(),
                }
                self._clean_cache()

            return predicted_pokemon

        finally:
            with self.interpreter_lock:
                self.interpreter_pool.append(interpreter)

    def _clean_cache(self):
        now = time.time()
        expired_keys = [
            key
            for key, value in self.prediction_cache.items()
            if now - value["timestamp"] > self.cache_timeout
        ]
        for key in expired_keys:
            del self.prediction_cache[key]

    def _initialize_interpreter(self):
        tflite_model_path = "source/pokefire.tflite"
        interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
        interpreter.allocate_tensors()
        return interpreter

    def _predict_pokemon_sync(self, interpreter, image):
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        input_data = tf.convert_to_tensor([image], dtype=tf.float32)
        interpreter.set_tensor(input_details[0]["index"], input_data)

        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]["index"])

        prediction_scores = output_data[0]
        predictions = [
            (self.labels[i], round(score * 100, 1))
            for i, score in enumerate(prediction_scores)
        ]

        predictions.sort(key=lambda x: x[1], reverse=True)

        return predictions[:3]
