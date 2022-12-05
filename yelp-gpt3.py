import os
import csv
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


def read_csv():
    with open("./bwq.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            print(row)


response = openai.Completion.create(
    model="text-davinci-003",
    prompt="This is yelp review. Classify wether it is a positive or a negative review. Positive is 2, and negative is 1.\n\nContrary to other reviews, I have zero complaints about the service or the prices. I have been getting tire service here for the past 5 years now, and compared to my experience with places like Pep Boys, these guys are experienced and know what they're doing. Also, this is one place that I do not feel like I am being taken advantage of, just because of my gender. Other auto mechanics have been notorious for capitalizing on my ignorance of cars, and have sucked my bank account dry. But here, my service and road coverage has all been well explained - and let up to me to decide. And they just renovated the waiting room. It looks a lot better than it did in previous years.",
    temperature=0,
    max_tokens=64,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

print(response)
