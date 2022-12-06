import os
import csv
import openai
import re
import traceback
import time
os.environ["OPENAI_API_KEY"] = "ayush"
openai.api_key = os.getenv("OPENAI_API_KEY")

PREFIX = "This is yelp review. Classify whether it is a positive or a negative review. Positive is 1, and negative is 0."
PARSE_REGEX = "\):\s+([\s\S]*$)"
LABEL_REGEX = "\(1|0\):"
# 2 is positive, 1 is negative


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
                    if any(x in test_label for x in ['positive', '1']):
                        if label == '2':
                            correct += 1
                    elif any(x in test_label for x in ['negative', '0']):
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
        if any(x in test_label for x in ['positive', '1']):
            return '1'
        elif any(x in test_label for x in ['negative', '0']):
            return '0'
        else:
            print("unable to infer anything meaninfgul")
            print("test_label", test_label)
            return '-1'


# 1 = postive, 0 = negative


def read_txt():
    total_run_successfully = 0
    original_sent_result = 0
    mismatch = 0
    try:
        with open("./data/yelp/yelp_bert", 'r') as f:
            for line in f:
                line = line.strip()
                text_match = re.search(PARSE_REGEX, line)
                label_match = re.search(LABEL_REGEX, line)
                #label = label_match.group(0)
                response = {}
                if line != '':
                    time.sleep(1)
                    print(total_run_successfully)
                    if total_run_successfully == 100:
                        break
                if line.startswith("orig sent"):
                    original = text_match.group(1)
                    total_run_successfully += 1
                    response = run_inference(original)
                    original_sent_result = infer_response(response)
                elif line.startswith("adv sent"):
                    adversial = text_match.group(1)
                    total_run_successfully += 1
                    response = run_inference(adversial)
                    adv_result = infer_response(response)
                    if original_sent_result != adv_result:
                        mismatch += 1
                        print("mismatch------------->>>>>")
    except Exception:
        traceback.print_exc()
    print("total_run_successfully")
    print(total_run_successfully)
    print("mismatch")
    print(mismatch)


def run_inference(text):
    prompt = PREFIX + "\n\n" + text
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
    print("------YELP--------GPT3----------")
    # read_csv()
    read_txt()
