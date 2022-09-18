from __future__ import print_function
import pandas as pd
import re
import tabula


class Parser:
    def __init__(self):
        self.file_obj = ""
        self.password = ""

    def start(self, bank_name, input_path, password):
        bank_name = bank_name
        self.file_obj = open(input_path, 'rb')
        self.password = password

        if bank_name == 'sbi':
            return self.sbi()
        elif bank_name == 'pbn':
            return self.pnb()
        elif bank_name == 'bob':
            return self.bob()
        else:
            print('Not yet available for this ' + bank_name)

    def sbi(self):
        df = tabula.read_pdf(self.file_obj, output_format="dataframe", pages='all', spreadsheet=True)
        df['Description'] = df['Description'].apply(lambda x: x.replace("\r", " "))
        df['Ref No./Cheque\rNo.'] = df['Ref No./Cheque\rNo.'].apply(lambda x: str(x).replace("\r", " "))
        sbi_df = df
        return sbi_df

    def pnb(self):
        pnb_df = tabula.read_pdf(self.file_obj, output_format="dataframe", pages='all', spreadsheet=True)
        pnb_df['Narration'] = pnb_df['Narration'].apply(lambda x: x.replace("\r", " "))
        return pnb_df

    def bob(self):
        df = tabula.read_pdf(self.file_obj, output_format="dataframe", pages='all', spreadsheet=True, password=self.password)
        # df.head()
        header = ["S.No", "Date", "Description", "Cheque No", "Debit", "Credit", "Balance", "Value Date"]
        temp_list = []
        row_num = 1
        pattern = re.compile("^\d+$")  # to check S.No

        for idx, row in df.iterrows():
            temp_dict = {}
            if row_num == 1:
                pass
            else:
                if pattern.match(idx[0]):
                    for i, item in enumerate(idx):
                        temp_dict[header[i]] = item
                    temp_dict[header[-1]] = idx[1]
            #         print (len(idx))
            #         print ((row))
            if (temp_dict):
                temp_list.append(temp_dict)
            row_num += 1

        bob_df = pd.DataFrame(temp_list)
        del bob_df['S.No']
        bob_df = bob_df[["Date", "Value Date", "Description", "Cheque No", "Debit", "Credit", "Balance"]]
        return bob_df

