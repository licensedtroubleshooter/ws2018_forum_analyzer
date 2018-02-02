import os
from forum_analyzer.preprocessor.sentiment_preprocessor import sentiment_preprocessing

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "resources")
if not os.path.exists(MODEL_PATH + '/predictor_stop_wng_md_clear'):
    sentiment_preprocessing.train_preprocessor(path=MODEL_PATH + '/')
