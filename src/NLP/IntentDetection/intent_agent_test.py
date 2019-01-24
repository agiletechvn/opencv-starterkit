import yaml
from intent_agent import IntentAgent

if __name__ == "__main__":
    with open('./snips_pretrained/snips_config.yaml') as config_yaml:
        config = yaml.load(config_yaml)

    agent = IntentAgent(config)
    agent.init_agent()

    task = ["I want you to add 'I love you, baby' to my playlist"]
    result = agent.answer(task)

    print(result)
