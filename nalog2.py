from datetime import datetime
import streamlit as st
import pandas as pd

st.title('Лабораторная работа №2. Земельный налог')
st.divider()


def user_input_features():
    st.sidebar.header('Введите значения')
    st.sidebar.divider()
    date_start = st.sidebar.date_input('Дата установки права собственности', value=datetime(2021, 1, 1),
                                       format="DD/MM/YYYY")
    date_stop = st.sidebar.date_input('Дата прекращения права собственности', value=datetime(2021, 12, 31),
                                      format="DD/MM/YYYY")
    part = st.sidebar.number_input('Доля владения, %', 1, 100, 100, 1)
    cost = st.sidebar.number_input('Кадастровая стоимость, руб.', 1, 10000000000, 1000000, 1000)
    rate = st.sidebar.radio('Ставка', [
        "0,3% / Селькохозяйственное назначение, жилищный фонд, жилищное строительство, личное хозяйство",
        "1,5% / Прочее"])
    purpose = st.sidebar.radio('Назначение (Повышающий коэффициент)',
                               ["Жилищное строительство (превышение 3х летнего срока строительства) / x4",
                                "Жилищное строительство / x2",
                                "Индивидуальное жилищное строительство (по истечении 10 лет) / x2",
                                "Другое / x1"], index=3)
    data = {'date_start': date_start,
            'date_stop': date_stop,
            'part': part,
            'cost': cost,
            'rate': rate,
            'purpose': purpose}
    table = pd.DataFrame(data, index=[0])
    return table


def calculate_rate(rate):
    if str(rate).count("0,3") == 1:
        return 0.003
    elif str(rate).count("1,5") == 1:
        return 0.015
    else:
        return 0


def calculate_koef(purpose):
    if str(purpose).count("x4") == 1:
        return 4
    elif str(purpose).count("x2") == 1:
        return 2
    elif str(purpose).count("x1") == 1:
        return 1
    else:
        return 0


def calc_tax(input: pd.DataFrame):
    date_start = input.at[0, 'date_start']
    date_stop = input.at[0, 'date_stop']
    part = input.at[0, 'part'] / 100
    cost = input.at[0, 'cost']
    rate = calculate_rate(input.at[0, 'rate'])
    coeff = calculate_koef(input.at[0, 'purpose'])

    months_having = [3, 3, 3, 3]
    month_start = date_start.month
    if date_start.day > 15:
        month_start += 1
    month_stop = date_stop.month
    if date_stop.day <= 15:
        month_stop -= 1

    for i in range(1, 13):
        if i < month_start:
            months_having[int((i - 1) / 3)] -= 1
        if i > month_stop:
            months_having[int((i - 1) / 3)] -= 1

    avans = [0.0, 0.0, 0.0, 0.0]
    summary = 0.0
    for i in range(len(avans)):
        avans[i] = 1 / 4 * cost * rate * (months_having[i] / 3) * part * coeff
        summary += avans[i]

    input_dict = {'Ставка': rate,
                  'Повышающий коэф': coeff,
                  'Доля': "{:.0%}".format(part),
                  'Кад.стоимость': cost,
                  'Кварталы': ','.join(str(i) for i in months_having)
                  }
    input_table = pd.DataFrame(input_dict, index=[""])
    input_table.set_index('Ставка', inplace=True)
    st.header('Составляющие')
    st.write(input_table)
    tax = [summary, avans[0], avans[1], avans[2], avans[3]]
    return tax


df = user_input_features()
tax = calc_tax(df)
st.header('Земельный налог')
st.code(str(tax.pop(0)) + " рублей")
st.header('Выходные данные')
prepaids = {'Кв. 1': tax.pop(0),
            'Кв. 2': tax.pop(0),
            'Кв. 3': tax.pop(0),
            'Налог': tax.pop(0)}
output = pd.DataFrame(prepaids, index=[""])
output.set_index('Кв. 1', inplace=True)
st.write(output)