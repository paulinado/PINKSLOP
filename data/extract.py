import jsonlines

def extract_questions(jsonl_file_path):
    with jsonlines.open(jsonl_file_path) as f:
        questions = []
        for line in f.iter():
            question = line["question"]
            questions.append(question)

    return questions

def write_questions_to_txt(questions, txt_file_path):
    with open(txt_file_path, "w") as f:
        for question in questions:
            f.write(question + "\n")

if __name__ == "__main__":
    jsonl_file_path = "train.jsonl"
    txt_file_path = "train.txt"

    questions = extract_questions(jsonl_file_path)
    write_questions_to_txt(questions, txt_file_path)

