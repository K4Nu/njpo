import pickle
from time import perf_counter
import pandas as pd
import fastparquet
import openpyxl
from decorator import timer_decor
arr1={i:"test" for i in range(1,101)}
arr2={i:"test" for i in range(1,10001)}
arr3={i:"test" for i in range (1,100001)}

@timer_decor
def pickle_writer(data,num):
    with open(f"pickle_file_{num}.pkl","wb") as file:
        pickle.dump(data,file)
        file.flush()

@timer_decor
def pickle_reader(num):
    with open(f"pickle_file_{num}.pkl", "rb") as file:
        data=pickle.load(file)

@timer_decor
def parquet_writer(data,num):
    df=pd.DataFrame.from_dict(data,orient='index',columns=["Value"])
    fastparquet.write(f"parquet_{num}.parq",df)

@timer_decor
def parquet_reader(num):
    pf=fastparquet.ParquetFile(f'parquet_{num}.parq')
    df=pf.to_pandas()

@timer_decor
def xlsx_writer(data,num):
    wb=openpyxl.Workbook()
    ws=wb.active
    ws.append(["Key","Value"])

    for k,v in data.items():
        ws.append([k,v])

    wb.save(f'output_{num}.xlsx')


@timer_decor
def xlsx_reader(num):
    wb_obj=openpyxl.load_workbook(f"output_{num}.xlsx")
    sheet=wb_obj.active

xlsx_reader(1)
xlsx_reader(2)
xlsx_reader(3)


