import os
from time import time
from baseAnalysis import BaseAnalysis 
import pandas as pd
from processor.dataProcessor import DataProcessor
from reporter.reportGenerator import DynamicReport

class Analysis(BaseAnalysis):

    def __init__(self):
        try:
            filepath = './online_retail_II.xlsx'
            # Load and preprocess data
            df_1 = pd.read_excel(filepath, sheet_name='Year 2009-2010')
            df_2 = pd.read_excel(filepath, sheet_name='Year 2010-2011')

            df = pd.concat([df_1, df_2], ignore_index=True)
            df = df.dropna(subset=['InvoiceDate', 'Customer ID'])
            df = df[~df['Invoice'].astype(str).str.startswith('c')]
            df = df[df['Quantity'] > 0]
            df = df[df['Price'] > 0]
            df['Revenue'] = df['Quantity'] * df['Price']
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
            df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
            self.df = df
            os.makedirs("assets", exist_ok=True)
        except Exception as e:
            print(f"Error during data loading and preprocessing: {e}")
            self.df = pd.DataFrame()

    def _load_app(self):
        data_processor = DataProcessor(self.df)
        do = True

        print("*" * 50, "Welcome to UCI Online Retail Analysis", "*" * 60)
        print("*" * 150)

        print("\n What kind of analysis would you like to perform?:")
        print("1. Level 1 analysis")
        print("2. Level 2 analysis")
        print("3. Level 3 analysis")
        print("Use 4, to quit")

        print("*" * 150)
        while do:
            option = input("Enter your choice- 1,2,3 or 4 : ").strip().lower()
            try:
                if option == "1":
                    report_data = data_processor.handle_level_1() 
                    report = DynamicReport(level="Level-1", author="Mohit Basantani", data_source="UCI ML Repo")
                    report.generate("static/Level1_report.pdf", report_data)
                    print("\U0001F4D6 Report generated Successfully for Level-1 analysis")
                    print("*" * 150)
                elif option == "2":
                    report_data = data_processor.handle_level_1()
                    report_data_1 = data_processor.handle_level_2()
                    report_data.update(report_data_1)
                    report = DynamicReport(level="Level-2", author="Mohit Basantani", data_source="UCI ML Repo")
                    report.generate("static/Level2_report.pdf", report_data)
                    print("\U0001F4D6 Report generated Successfully for Level-2 analysis")
                    print("*" * 150)
                elif option == "3":
                    report_data = data_processor.handle_level_3()
                    report_data_1 = data_processor.handle_level_1()
                    report_data_2 = data_processor.handle_level_2()
                    report_data.update(report_data_1)
                    report_data.update(report_data_2)
                    report = DynamicReport(level="Level-3", author="Mohit Basantani", data_source="UCI ML Repo")
                    report.generate("static/Level3_report.pdf", report_data)
                    print("\U0001F4D6 Report generated Successfully for Level-3 analysis")
                    print("*" * 150)
                elif option == "4":
                    print("Exiting the analysis. Goodbye!")
                    do = False    
                else:
                    print("Invalid option selected.")
            except Exception as e:
                print(f"Error during analysis: {e}")

    def run_analysis(self):
        print("Welcome to Report Generator", end="\n")
        self._load_app() 


if __name__ == "__main__":
    analysis = Analysis()
    analysis.run_analysis()