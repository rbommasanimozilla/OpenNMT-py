#from tqdm import tqdm
#import nltk
#from nltk import tokenize
#import jsonlines


def truncate_lines(input_file, output_file):
    g = open(output_file, 'w', encoding = 'utf-8')
    with open(input_file, encoding='utf-8') as f:
        for line in f:
            g.write(truncate_line(line) + '\n')
    f.close()
    g.close()


def truncate_line(line):
    bound = 1000
    tokens = line.split()
    if len(tokens) > bound:
        tokens = tokens[0:bound]
    return ' '.join(tokens)


def sentence_tag(line):
    sents = tokenize.sent_tokenize(line)
    s = "<t> "
    for sent in sents:
        s = s + sent + " </t> <t> "
    s = s[:-5]
    return s


def end_token(line):
    dm_single_close_quote = u'\u2019' # unicode
    dm_double_close_quote = u'\u201d'
    END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', dm_single_close_quote, dm_double_close_quote, ")"]
    if line=="": return line
    if line[-1] in END_TOKENS: return line
    return line + " ."


def get_newsroom(data, query):
    return list(map(lambda x: x[query], data))


def make_files(input, outputprefix):
    with jsonlines.open(input) as reader:
        data = [obj for obj in reader]
    summaries = get_newsroom(data, 'summary')
    texts = get_newsroom(data, 'text')
    titles = get_newsroom(data, 'title')
    #sfile = open(outputprefix + '.txt.tgt', 'w', encoding='utf-8')
    #txfile = open(outputprefix + '.txt.src', 'w', encoding='utf-8')
    #tifile = open(outputprefix + '.txt.ttl', 'w', encoding='utf-8')
    sum_length = 0
    sum_count = 0
    for _, s in tqdm(enumerate(summaries)):
        s = s.replace('\n\n\n ', ' ')
        s = s.replace('\n\n\n', ' ')
        s = s.replace('\n\n ', ' ')
        s = s.replace('\n\n', ' ')
        s = s.replace('\n ', ' ')
        s = s.replace('\r ', ' ')
        s = s.replace('\n', '')
        s = s.replace('\r', '')
        if s == "": s = "BLANK SUMMARY"
        s = end_token(s)
        s = sentence_tag(s)
        sum_length += len(s.split())
        sum_count += 1
        #sfile.write(s + '\n')
    print(max(list(map(lambda x: len(x.split()), summaries))))
    print(sum_length,sum_count,sum_length/sum_count)
    #sfile.close()
    sum_length = 0
    sum_count = 0
    for _, text in tqdm(enumerate(texts)):
        text = text.replace('\n\n\n ', ' ')
        text = text.replace('\n\n\n', ' ')
        text = text.replace('\n\n ', ' ')
        text = text.replace('\n\n', ' ')
        text = text.replace('\n ', ' ')
        text = text.replace('\r ', ' ')
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        if text == "": text = "BLANK TEXT"
        text = end_token(text)
        sum_length += len(text.split())
        sum_count += 1
        #txfile.write(text + '\n')
    print(max(list(map(lambda x: len(x.split()), texts))))
    print(sum_length,sum_count,sum_length/sum_count)
    #txfile.close()
    for title in titles:
        title = title.replace('\n\n\n ', ' ')
        title = title.replace('\n\n\n', ' ')
        title = title.replace('\n\n ', ' ')
        title = title.replace('\n\n', ' ')
        title = title.replace('\n ', ' ')
        title = title.replace('\r ', ' ')
        title = title.replace('\n', '')
        title = title.replace('\r', '')
        if title == "": title = "BLANK TITLE"
        title = end_token(title)
        #tifile.write(title + '\n')
    #tifile.close()


if __name__ == "__main__":
    #nltk.download('punkt')
    #make_files('train-stats.jsonl', 'train')
    #make_files('dev-stats.jsonl', 'val')
    #make_files('test-stats.jsonl', 'test')
    truncate_lines('/snakepit/shared/data/cornell/newsroom-tagged/val.txt.srcp','/snakepit/jobs/1184/keep/val.txt.srcp.trunc')