import csv
file_dest = open("intents.json", "w")

rowcount = 0
for row in open('chatbotquestion.csv'):
    rowcount += 1


opener = '''
    {
        "intents":[
'''
file_dest.write(opener)
count = 0
with open('chatbotquestion.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        stringline = f'''{{
            "tag": "{row[0]}",
        '''
        stringline_input = '"input":['
        for i in range(2, len(row)):
            if i == len(row) - 1:
                stringline_input += f'''"{row[i]}"'''
            else:
                stringline_input += f'''"{row[i]}",'''

        stringline_input += "],"

        stringline += stringline_input
        stringline += f'''
        "responses":["{row[1]}"]
        }}'''

        if(count != rowcount - 1):
            stringline += ","
        count += 1
        file_dest.write(stringline)

closer = '''
        ]
    }
'''
file_dest.write(closer)
file_dest.close()
