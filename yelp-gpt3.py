import os
import csv
import openai
os.environ["OPENAI_API_KEY"] = "ayush"
openai.api_key = os.getenv("OPENAI_API_KEY")

PREFIX = "This is yelp review. Classify wether it is a positive or a negative review. Positive is 2, and negative is 1."
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
    read_csv()
