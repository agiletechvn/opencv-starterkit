import numpy as np
import copy
import traceback

from intent_model.preprocessing import NLTKTokenizer
from intent_model.multiclass import KerasMulticlassModel


class IntentAgent:
    def __init__(self, config):
        self.config = copy.deepcopy(config)
        self.agent = None
        self.classes = None
        self.preprocessor = None

    def init_agent(self):
        self.config['model_from_saved'] = True
        self.agent = KerasMulticlassModel(self.config)
        self.classes = self.agent.classes
        self.preprocessor = NLTKTokenizer()

    def _run_score(self, observation):
        task = observation[0]
        infer_result = self.agent.infer(self.preprocessor.infer(task))
        prediction = self.classes[np.argmax(infer_result)]
        return prediction

    def answer(self, input_task):
        try:
            if isinstance(input_task, list):
                result = self._run_score(input_task)
                return result
            elif isinstance(input_task, int):
                result = 'There is no Intent Classifier testing API provided'
                return result
            else:
                return {"ERROR": "Parameter error - {} belongs to unknown type".format(
                    str(input_task))}
        except Exception as e:
            print(e)
            return {"ERROR": "{}".format(traceback.extract_stack())}
