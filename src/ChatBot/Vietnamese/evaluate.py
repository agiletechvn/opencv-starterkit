import json
from os import listdir
from os.path import join
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from engine.thanhtu import ThanhTu
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def scoring(question, answers):
    bot_answer = ThanhTu.reply("local", question)
    if len(answers) == 0:
        answer = ""
        return 0, bot_answer, answer
    bleus = [(answer, sentence_bleu([bot_answer.lower().split()], answer.lower().split(), weights=[1, 0, 0, 0])) for
             answer in answers]
    answer, bleu = max(bleus, key=lambda x: x[1])
    return bleu, bot_answer, answer


def evaluate_file(filepath):
    print("")
    print(filepath)
    talks = json.load(open(filepath))
    output = {
        "talk": 0,
        "question": 0
    }
    scores = []
    for talk in talks:
        output["talk"] += 1
        questions = talk["question"]
        for question in questions:
            output["question"] += 1
            bleu, bot_answer, answer = scoring(question, talk["answer"])
            scores.append(bleu)
            if bleu < 0.8:
                print("\nQuestion :", question)
                print("Correct  :", answer)
                print("Actual   :", bot_answer)
                print("Bleu     : ", bleu)
                print()
    output["score"] = np.mean(scores)
    return output


ThanhTu.reply("local", ":build ThanhTu")
ThanhTu.reply("local", ":reset")
ThanhTu.reply("local", ":trace")


def evaluate(files):
    output = [evaluate_file(filepath) for filepath in files]
    df = pd.DataFrame(output, columns=["talk", "question", "score"])
    print(df)
    print("Score:", df["score"].mean())


TEST_FOLDER = "data/test"
files = []
for file in listdir(TEST_FOLDER):
    files.append(join(TEST_FOLDER, file))

evaluate(files)
