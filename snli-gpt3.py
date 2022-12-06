import os
import csv
import openai
import re
import traceback
import time
os.environ["OPENAI_API_KEY"] = "nakul"
openai.api_key = os.getenv("OPENAI_API_KEY")

SUFFIX = "Does the hypothesis is neutral, contradicts, or entails the premise? If it contradicts output contradiction, if it is neutral output neutral and if it entails output entailment."
SUFFIX2 = "Return the textual entailment output for the above premise and hypothesis."
FEWSHOT = "premise: A person in a black and green outfit is riding a bicycle.\nhypothesis: a colorfully dressed child rides a bike.\n\ntextual entailment output:entailment\n###\n\npremise: A person rolls down a hill riding a wagon as another watches .\nhypothesis: A child in a wagon rolls down a hill .\n\ntextual entailment output:neutral\n###\n\npremise: A man in a black tank top wearing a red plaid hat.\nhypothesis: A man wearing football pads .\n\ntextual entailment output:contradiction\n###\n\npremise: Families with strollers waiting in front of a carousel.\nhypothesis: Families have some dogs in front of a carousel.\n\ntextual entailment output:contradiction\n###\n\npremise: A person with dark hair in a white shirt is sitting in a chair in water with a `` swim at your own risk '' sign on the wall .\nhypothesis: a person is relaxing on his day off.\n\ntextual entailment output:neutral\n###\n\npremise: pedestrian walking on the street.\nhypothesis: A person walking inside a building.\n\ntextual entailment output:contradiction\n###\n\npremise: A man on a bicycle , wearing cycle gear , riding at a fast past down paved trail surrounded by tree 's and grass .\nhypothesis: He is heading to the cabin down the trail .\n\ntextual entailment output:neutral\n###\n\npremise: A young child climbing a stack of logs even though the sign warns against it .\nhypothesis: A kid climbing some logs.\n\ntextual entailment output:entailment"
PARSE_REGEX = "\):\s+([\s\S]*$)"
LABEL_REGEX = "\(entailment|contradiction|neutral\):"
PREM_REGEX = ":\s+([\s\S]*$)"

def read_csv():
    total_csv_count = 38_000
    total_run_successfully = 0
    correct = 0
    try:
        with open("./data/yelp/test.csv", 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                sentence = row[1]
                label = row[0]
                response = run_inference(sentence)
                if 'choices' in response:
                    total_run_successfully += 1
                    test_label = response["choices"][0]["text"].strip(
                        '\n').lower()
                    if any(x in test_label for x in ['positive', '2']):
                        if label == '2':
                            correct += 1
                    elif any(x in test_label for x in ['negative', '1']):
                        if label == '1':
                            correct += 1
                    else:
                        print("mismatch")
                if total_run_successfully == 1000:
                    break
    except:
        print("Error")
        print("total_run_successfully")
        print(total_run_successfully)
        print("correct")
        print(correct)
    print("total_run_successfully")
    print(total_run_successfully)
    print("correct")
    print(correct)


def infer_response(response):
    if 'choices' in response:
        test_label = response["choices"][0]["text"].strip('\n').lower()
        return test_label


# 1 = postive, 0 = negative


def read_txt():
    total_run_successfully = 0
    # original_sent_result = 0
    mismatch = 0
    orig_prem = ""
    orig_hypo = ""
    adv_hypo = ""
    try:
        with open("./data/snli/snli_bert", 'r') as f:
            for line in f:
                line = line.strip()
                text_match = re.search(PREM_REGEX, line)
                # label_match = re.search(LABEL_REGEX, line)
                #label = label_match.group(0)
                response = {}
                # print(total_run_successfully)
                if line == '':
                    # print(orig_prem)
                    # print(orig_hypo)
                    # print(adv_hypo)
                    orig_resp = run_inference(orig_prem, orig_hypo)
                    time.sleep(1)
                    adv_resp = run_inference(orig_prem, adv_hypo)
                    time.sleep(1)
                    print(infer_response(orig_resp))
                    print(infer_response(adv_resp))
                    if infer_response(orig_resp) != infer_response(adv_resp):
                        mismatch += 1
                        print("mismatch------------->>>>>")

                    total_run_successfully += 1
                    print(total_run_successfully)
                    if total_run_successfully == 100:
                        break
                    continue
                else:
                    if line.startswith("orig premise:"):
                        orig_prem = text_match.group(1)
                    elif line.startswith("orig hypo"):
                        orig_hypo = text_match.group(1)
                    elif line.startswith("adv hypo"):
                        adv_hypo = text_match.group(1)

    except Exception:
        traceback.print_exc()
    print("total_run_successfully")
    print(total_run_successfully)
    print("mismatch")
    print(mismatch)


def read_orignal():
    total_run_successfully = 0
    # original_sent_result = 0
    mismatch = 0
    orig_prem = ""
    orig_hypo = ""
    adv_hypo = ""
    label = ""
    try:
        with open("./data/snli/snli_bert", 'r') as f:
            for line in f:
                line = line.strip()
                text_match = re.search(PREM_REGEX, line)
                label_match = re.search(LABEL_REGEX, line)
                # label = label_match.group(0)
                # response = {}
                # print(total_run_successfully)
                if line == '':
                    # print(orig_prem)
                    # print(orig_hypo)
                    # print(adv_hypo)
                    if total_run_successfully >= 10:
                        orig_resp = run_inference(orig_prem, orig_hypo)
                        time.sleep(1.2)
                        print(infer_response(orig_resp))
                        print(label)
                        if infer_response(orig_resp) not in label:
                            mismatch += 1
                            print("mismatch------------->>>>>")

                    total_run_successfully += 1
                    print(total_run_successfully)
                    if total_run_successfully == 110:
                        break
                    continue
                else:
                    if line.startswith("orig premise:"):
                        orig_prem = text_match.group(1)
                    elif line.startswith("orig hypo"):
                        orig_hypo = text_match.group(1)
                        label = label_match.group(0)
                        # print(label_match)
                        # print(label)
                    elif line.startswith("adv hypo"):
                        adv_hypo = text_match.group(1)

    except Exception:
        traceback.print_exc()
    print("total_run_successfully")
    print(total_run_successfully)
    print("mismatch")
    print(mismatch)

def few_adv():
    total_run_successfully = 0
    # original_sent_result = 0
    mismatch = 0
    orig_prem = ""
    orig_hypo = ""
    adv_hypo = ""
    label = ""
    try:
        with open("./data/snli/snli_bert", 'r') as f:
            for line in f:
                line = line.strip()
                text_match = re.search(PREM_REGEX, line)
                label_match = re.search(LABEL_REGEX, line)
                # label = label_match.group(0)
                # response = {}
                # print(total_run_successfully)
                if line == '':
                    # print(orig_prem)
                    # print(orig_hypo)
                    # print(adv_hypo)
                    if total_run_successfully >= 10:
                        orig_resp = run_inference(orig_prem, adv_hypo)
                        time.sleep(1.2)
                        print(infer_response(orig_resp))
                        print(label)
                        if infer_response(orig_resp) not in label:
                            mismatch += 1
                            print("mismatch------------->>>>>")

                    total_run_successfully += 1
                    print(total_run_successfully)
                    if total_run_successfully == 110:
                        break
                    continue
                else:
                    if line.startswith("orig premise:"):
                        orig_prem = text_match.group(1)
                    elif line.startswith("orig hypo"):
                        orig_hypo = text_match.group(1)
                        label = label_match.group(0)
                        # print(label_match)
                        # print(label)
                    elif line.startswith("adv hypo"):
                        adv_hypo = text_match.group(1)

    except Exception:
        traceback.print_exc()
    print("total_run_successfully")
    print(total_run_successfully)
    print("mismatch")
    print(mismatch)

def run_inference(prem, hypo):
    # prompt = "premise: " + prem + "\n" + "hypothesis: " + hypo + "\n\n" + SUFFIX2
    prompt = FEWSHOT + "premise: " + prem + "\n" + "hypothesis: " + hypo + "\n\n" + "textual entailment output:"
    # print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response


if __name__ == "__main__":
    print("------SNLI--------GPT3----------")
    # read_csv()
    # read_orignal()
    few_adv()
