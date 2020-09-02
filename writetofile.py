import xlsxwriter


def write_csv(header, words, fileout):
    with open(fileout, 'w', newline ='') as filecsv:
        print(header, file=filecsv)
        for line in words:
            print(' '.join(line), file=filecsv)


def write_exel(header, words, fileout):
    with xlsxwriter.Workbook(fileout) as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, row_data in enumerate(words):
            for col_num, col_data in enumerate(row_data):
              worksheet.write(row_num, col_num, col_data)