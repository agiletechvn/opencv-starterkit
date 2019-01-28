import numpy as np
import os
import mdv
import re
from bert_serving.client import BertClient
from termcolor import colored
from imgcat import imgcat

# config like this:
mdv.term_columns = 60

topk = 5
prefix_q = '##### **Q:** '
stop_prefix = '<h2 align="center">:zap: Benchmark</h2>'
start = False
questions = []
answers = []


def start_client(port=5555, port_out=5556):

    # port for pushing data from client to server
    # port_out for publishing results from server to client
    with BertClient(port=port, port_out=port_out) as bc:
        doc_vecs = bc.encode(questions)
        try:
            while True:
                query = input(colored('your question: ', 'green'))
                query_vec = bc.encode([query])[0]
                # compute simple dot product as score
                score = np.sum(query_vec * doc_vecs, axis=1)
                topk_idx = np.argsort(score)[::-1][:topk]
                idx = topk_idx[0]
                print('> %s\t%s' % (colored('%.1f' %
                                            score[idx], 'cyan'), colored(questions[idx], 'yellow')))
                format_answer(answers[idx])

                print('top %d questions similar to "%s"' %
                      (topk, colored(query, 'green')))
                for idx in topk_idx:
                    print('> %s\t%s' % (colored('%.1f' %
                                                score[idx], 'cyan'), colored(questions[idx], 'yellow')))
        except KeyboardInterrupt:
            print("Goodbye...")
            pass


def format_answer(answer):
    lines = answer.splitlines()
    for line in lines:
        m = re.search('(?<=src=")[^"\?]+', line)
        if m:
            imgcat(open("bert-as-service/"+m.group(0)))
        else:
            formatted = mdv.main(md=line, c_theme=...)
            print(formatted)


with open('bert-as-service/README.md') as fp:
    for v in fp:
        v_strip = v.strip()
        if v_strip.startswith(stop_prefix):
            print('Done processing')
            index = len(questions)
            answers[index-1] += v_strip + "\n"
            break
        if v_strip.startswith(prefix_q):
            v_line = v_strip.replace(prefix_q, '').strip()
            start = True
            questions.append(v_line)
            continue
        if start:
            if v_strip:
                index = len(questions)
                if len(answers) < index:
                    answers.append(v_strip)
                else:
                    answers[index-1] += v_strip + "\n"

    start_client()
