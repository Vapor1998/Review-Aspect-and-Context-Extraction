from pyabsa import AspectTermExtraction as ATEPC
import joblib

class LLM:

    def __init__(self):
        self.model = ATEPC.AspectExtractor("multilingual")

    def predict(self, text):
        output = self.model.predict(text)
        return output


# Create an instance of your large language model
#llm_instance = LLM()

# joblib.dump(llm_instance, 'modeldump.pkl')
#
# print('Done')
