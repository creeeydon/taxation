from datetime import datetime
import streamlit as st
import pandas as pd

st.title('Лабораторная работа №1. Транспортный налог')
st.divider()

def user_input_features():
    st.sidebar.header('Введите значения')
    st.sidebar.divider()
    date_reg = st.sidebar.date_input('Дата регистрации', value=datetime(2021, 8, 29), format="DD/MM/YYYY")
    date_vip = st.sidebar.date_input('Дата выпуска', value=datetime(2020, 1, 10), format="DD/MM/YYYY")
    cost = st.sidebar.number_input('Стоимость', 1, 10000000000, 1150000, 1000)
    power = st.sidebar.number_input('Мощность двигателя', 1, 1500, 100)
    data = {'date_reg': date_reg,
            'date_vip': date_vip,
            'cost': cost,
            'power': power}
    table = pd.DataFrame(data, index=[0])
    return table

def calc_tax(input: pd.DataFrame):
    date_reg = input.at[0, 'date_reg']
    date_vip = input.at[0, 'date_vip']
    cost = input.at[0, 'cost']
    power = input.at[0, 'power']
    koef = 1.0
    stavka = 1.0

    if power > 250:
        stavka = 110.0

    if power <= 250:
        stavka = 47.0

    if power <= 200:
        stavka = 28.0

    if power <= 150:
        stavka = 14.0

    if power <= 100:
        stavka = 8.0

    if 10000000 <= cost <= 15000000 and 2023 - date_vip.year <= 10:
        koef = 3.0

    if 15000000 <= cost and 2023 - date_vip.year <= 20:
        koef = 3.0

    month = date_reg.month-1
    if date_reg.day > 15:
        month += 1

    monthHaving = ((12 - month) / 12.0)
    tax = power * stavka * monthHaving * koef
    tempVar = {'Ставка': stavka,
                'Пропустили': month,
                'Повышающий коэффициент': koef,
                'Владение': monthHaving}
    temp = pd.DataFrame(tempVar, index=[""])
    temp.set_index('Ставка',inplace=True)
    st.header('Составляющие')
    st.write(temp)

    avans = [0.0, 0.0, 0.0]
    i = 0
    for j in range(3, 10, 3):
        if month - j < 0:
            avans[i] = 0.25 * stavka * power * ((j - month) / 3.0) * koef
            month = j
            i = i + 1
        else:
            i = i + 1

    sumAvan = 0
    for i in range(len(avans)):
        sumAvan+=avans[i]

    lastTax = tax - sumAvan
    tax = [tax, avans[0], avans[1], avans[2], lastTax]
    return tax

df = user_input_features()
tax = calc_tax(df)

st.header('Транспортный налог')
st.code(str(tax.pop(0)) + " рублей")
st.header('Выходные данные')
prepaids = {'Кв. 1': tax.pop(0),
            'Кв. 2': tax.pop(0),
            'Кв. 3': tax.pop(0),
            'Налог': tax.pop(0)}
output = pd.DataFrame(prepaids, index=[""])
output.set_index('Кв. 1', inplace=True)
st.write(output)