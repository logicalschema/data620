import os
import pandas as pd
import sys
import numpy
import re 
from email.parser import BytesParser, Parser
from email.policy import default

# Assumes that ham and spam have been uncompressed and reside in the
# same directory as this Python file

HAM = 'ham'
SPAM = 'spam'
NEWLINE = '\n'

SOURCES = [
	('ham/', HAM),
	('spam/', SPAM)
]

SKIP_FILES = {'cmds'}

# Get the Total number of files
TOTAL_FILES = 0

files = os.listdir("ham/")
TOTAL_FILES = len(files) 
files = os.listdir("spam/")
TOTAL_FILES += len(files)




def progress(i, end_val, bar_length=50):
    '''
    Print a progress bar of the form: Percent: [#####      ]
    i is the current progress value expected in a range [0..end_val]
    bar_length is the width of the progress bar on the screen.
    '''
    percent = float(i) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def read_files(path):
    '''
    Generator of pairs (filename, filecontent)
    for all files below path whose name is not in SKIP_FILES.
    The content of the file is of the form:
        header....
        <emptyline>
        body...
    This skips the headers and returns body only.
    '''
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            if file_name not in SKIP_FILES:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    past_header, lines = False, []
                    with open(file_path, "rb") as f:
                    	msg = BytesParser(policy=default).parse(f)
                    yield file_path, msg

def build_data_frame(l, path, classification):
    rows = []
    index = []
    for i, (file_name, email) in enumerate(read_files(path)):
        if ((i+l) % 100 == 0):
            progress(i+l, TOTAL_FILES, 50)
        rows.append({'email': email, 'class': classification})
        index.append(file_name)
   
    data_frame = pd.DataFrame(rows, index=index)
    return data_frame, len(rows)

def load_data():
    data = pd.DataFrame({'email': [], 'class': []})
    l = 0
    for path, classification in SOURCES:
        data_frame, nrows = build_data_frame(l, path, classification)
        data = data.append(data_frame)
        l += nrows
    data = data.reindex(numpy.random.permutation(data.index))
    return data


data = load_data()


# message must be email.ByteParser 
def email_items(message):
	fromEmail = str(message['from']) 
	toEmail = str(message['to'])
	subjectEmail = str(message['subject'])
	contentType = message.get_content_type()
	content = ""

	if message.is_multipart():
		for payload in message.get_payload():
			content = content + str(payload.get_payload())
	else:
		content = message.get_payload()


	return fromEmail, toEmail, subjectEmail, content, contentType


data['From'], data['To'], data['Subject'], data['Content'], data['ContentType'] = zip(*data['email'].apply(lambda x:
	email_items(x)
	))


print(data['ContentType'].unique())
print(data['class'].unique())
print(len(data.index))

