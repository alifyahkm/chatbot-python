import requests
import csv
result_data = []


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open('akurasi_nlp.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0

    for row in csv_reader:
        if line_count != 0:

            response = requests.post(
                'http://34.71.238.90:3000/chatbot', json={"question": row[1]})

            json_data = response.json()

            hasil = ""
            kesimpulan = ""

            if(json_data["answer"].strip() == row[2].strip()):
                hasil = "Valid karena tidak sesuai dengan hasil yang di harapkan"
                kesimpulan = "Valid"

            else:
                hasil = "Tidak valid karena tidak sesuai dengan hasil yang di harapkan"
                kesimpulan = "Tidak Valid"

            result_data.append([
                row[1],
                row[2],
                json_data["answer"],
                hasil,
                kesimpulan
            ])

        line_count += 1


f = open("hasil_test.csv", "w+")
f.write("Pertanyaan;Jawaban;Hasil;Kesimpulan\n")

print("Hasil Test : ")


count = 1

valid_count = 0
invalid_count = 0

for data in result_data:
    print(f'''
Tes {count}
    - Pertanyaan : {data[0]}
    - Jawaban Yang Diharapkan : {data[1]}
    - Jawaban yang dihasilkan : {data[2]}
    - Hasil : {data[3]}
    - Kesimpulan : {data[4]}''')
    if (data[4] == "Valid"):
        print(bcolors.OKGREEN + u'\u2714' + bcolors.ENDC +
              bcolors.OKCYAN + f" Test {count} valid!" + bcolors.ENDC)
        valid_count += 1
    else:
        print(bcolors.FAIL + u'\u274c' +
              f" Test {count} tidak valid!" + bcolors.ENDC)
        invalid_count += 1

    f.write(f"{data[0]};{data[1]};{data[3]};{data[4]}\n")
    count += 1

f.close()


print(bcolors.OKCYAN + f"\nTotal Data Valid : {valid_count}" + bcolors.ENDC)
print(bcolors.FAIL + f"Total Data Tidak Valid: {invalid_count}" + bcolors.ENDC)
