# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 07:45:45 2023

@author: Yuta
"""

#pip install faker, pip install Faker[locales]
from typing import Callable, Any
from faker import Faker
from faker.providers import BaseProvider

import random
#import string
import os
from openpyxl import Workbook
from datetime import date

#f = Faker()

#print(f.name())
#print(f.address())
#print(f.phone_number())



class RandomChar(BaseProvider):
    def generate_random_id(self) -> str:
        return ''.join(str(random.randint(1, 999999)).zfill(6))

class ChiNhanh(BaseProvider):
    def generate_CN(self) -> str:
        branches = ['CN01', 'CN02', 'CN03']
        return random.choice(branches)

class VNPhoneNumber(BaseProvider):
    def vn_phone_number(self):
        formats = ['+84#########', '+84#######'] #sdt di dong, sdt ban
        return self.numerify(self.random_element(formats))



def person_data_generator(faker: Faker) -> list[str]:
    # Kiểm tra nếu ngày sinh trước 1/1/1972 hoặc sau 1/1/2002 thì tạo lại ngày sinh
    dob = faker.date_of_birth()
    while dob <= date(1972, 1, 1) or dob >= date(2002, 1, 1):
        dob = faker.date_of_birth()
        
    return [faker.generate_random_id(), #ma faker.generate_random_id()
            faker.name(),  #ten
            str(random.randint(100000000, 999999999)).zfill(12), #cccd
            random.randint(0, 1), #gioitinh          
            #faker.date_of_birth().strftime('%Y-%m-%d'), #ngaysinh
            #(faker.date_of_birth() - timedelta(days=1)) if faker.date_of_birth() >= date(2002, 1, 1)  else faker.date_of_birth(),
            dob, #ngaysinh
            faker.country(),
            faker.address(),
            faker.vn_phone_number(),
            faker.email(),
            faker.generate_CN()]




def generate_excel(filename: str,
                   row_num: int,
                   generator: Callable[[Faker], list[Any]],
                   faker: Faker,
                   header: list[str]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.append(header)
    for n in range(1, row_num):
        ws.append(generator(faker))
    wb.save(filename)
    
    
def fake_data_plan() -> None:
    faker: Faker = Faker()
    faker.add_provider(RandomChar)
    faker.add_provider(ChiNhanh)
    faker.add_provider(VNPhoneNumber)

    # Tạo workbook mới
    wb = Workbook()
    # Tạo worksheet mới
    ws = wb.active

    # Thiết lập header rows
    header_rows = ['ID', 'Ten', 'CCCD', 'GioiTinh','NgaySinh','QueQuan','DiaChi','SDT','Mail','ChiNhanh']
    ws.append(header_rows)

    # Thiết lập số dòng cần tạo
    row_num = 1000

    # Tạo dữ liệu và ghi vào worksheet
    for n in range(row_num):
        row_data = person_data_generator(faker)
        ws.append(row_data)

    # Lưu workbook vào file
    #tạo thu muc neu ch ton tai
    #os.makedirs('data_nhan_vien', exist_ok=True)
    filename = os.path.join(os.getcwd(), 'danhsachnhanvien.xlsx')
    #filename = 'data_nhan_vien/danhsachnhanvien.xlsx'
    wb.save(filename)
    


# def fake_data_plan() -> None:
#     fake: Faker = Faker()
#     fake.add_provider(RandomChar)
#     fake.add_provider(ChiNhanh)
#     #for page in range(1, 8):
#     # generate_csv(filename='data_nhan_vien/danh_sach_nhanvien.csv',
#     #              row_num=2,
#     #              generator=person_data_generator,
#     #              faker=fake,
#     #              header=['ID', 'Ten', 'CCCD', 'GioiTinh','NgaySinh','QueQuan','DiaChi','SDT','Mail','ChiNhanh'])


if __name__ == '__main__':
    fake_data_plan()