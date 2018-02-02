import os
from forum_analyzer.preprocessor.trash_preprocessor import trash_preprocessing

PREDICTOR_PATH = os.path.join(os.path.dirname(__file__), "..", "resources")
if not os.path.exists(os.path.join(PREDICTOR_PATH, 'trash_model')):
    trash_preprocessing.train_preprocessor(path=PREDICTOR_PATH + '/')
