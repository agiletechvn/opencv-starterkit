#!/usr/bin/env python3

import sys
import numpy as np
import yaml

from intent_model.preprocessing import NLTKTokenizer
from intent_model.multiclass import KerasMulticlassModel


def infer(phrase):
    global preprocessor, classes, model
    try:
        predictions = model.infer(preprocessor.infer(phrase))
    except Exception:
        print('Error', file=sys.stderr)
        return 0, 'error'
    return np.max(predictions), classes[np.argmax(predictions)]


# Initializing preprocessor
preprocessor = NLTKTokenizer()

# Reading parameters
with open('./snips_pretrained/snips_config.yaml') as config_yaml:
    opt = yaml.load(config_yaml)


# Infering is possible only for saved intent_model
opt['model_from_saved'] = True

# Initializing intent_model
model = KerasMulticlassModel(opt)

# Initializing classes
classes = model.classes

print("Model is ready! You now can enter requests.")
for query in sys.stdin:
    print(infer(query))
