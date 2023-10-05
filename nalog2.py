from datetime import datetime
import streamlit as st
import pandas as pd

def user_input_features():
    sb = st.sidebar
    sb.header('Введите значения')
    sb.divider()
    date_start = sb.date_input('Дата установки права собственности', value=datetime(2021, 1, 1), format="DD/MM/YYYY")
    date_stop = sb.date_input('Дата прекращения права собственности', value=datetime(2021, 12, 31), format="DD/MM/YYYY")
    part = sb.number_input('Доля владения, %', 1, 100, 100, 1)
    cost = sb.number_input('Кадастровая стоимость, руб.', 1, 10000000000, 1000000, 1000)
    rate = sb.radio('Ставка', [
        "0,3% / Селькохозяйственное назначение, жилищный фонд, жилищное строительство, личное хозяйство",
        "1,5% / Прочее"])
    goal = sb.radio('Назначение (Повышающий коэффициент)',
                    ["Жилищное строительство (превышение 3х летнего срока строительства) / x4",
                     "Жилищное строительство / x2",
                     "Индивидуальное жилищное строительство (по истечении 10 лет) / x2", "Другое / x1"], index=3)
    data = {'date_start': date_start, 'date_stop': date_stop, 'part': part, 'cost': cost, 'rate': rate, 'goal': goal}
    return pd.DataFrame(data, index=[0])

def calc_tax(input: pd.DataFrame):
    calculate_rate = lambda rate: 0.003 if str(rate).count("0,3") == 1 else 0.015
    calculate_koef = lambda goal: 4 if str(goal).count("x4") == 1 else 2 if str(goal).count("x2") == 1 else 1
    date_start, date_stop = input.at[0, 'date_start'], input.at[0, 'date_stop']
    part, cost = input.at[0, 'part'] / 100, input.at[0, 'cost']
    rate, cff = calculate_rate(input.at[0, 'rate']), calculate_koef(input.at[0, 'goal'])
    month_start = date_start.month + 1 if date_start.day > 15 else date_start.month
    month_stop = date_stop.month - 1 if date_stop.day <= 15 else date_stop.month
    months_having = [0, 0, 0, 0]
    for i in range(1, 13): months_having[int((i - 1) / 3)] += 1 if month_start <= i <= month_stop else 0
    avans = [0.25 * cost * rate * (months_having[i] / 3) * part * cff for i in range(4)]
    input_table = pd.DataFrame({'Ставка': rate, 'Повышающий коэф': cff, 'Доля': "{:.0%}".format(part),
                  'Кад.стоимость': cost, 'Кварталы': ','.join(str(i) for i in months_having)}, index=[""])
    input_table.set_index('Ставка', inplace=True)
    st.header('Составляющие')
    st.write(input_table)
    return [sum(avans), avans[0], avans[1], avans[2], avans[3]]

st.title('Лабораторная работа №2. Земельный налог')
st.divider()
df = user_input_features()
tax = calc_tax(df)
st.header('Земельный налог')
st.code(str(tax.pop(0)) + " рублей")
st.header('Выходные данные')
output = pd.DataFrame({'Кв. 1': tax.pop(0), 'Кв. 2': tax.pop(0), 'Кв. 3': tax.pop(0), 'Налог': tax.pop(0)}, index=[""])
output.set_index('Кв. 1', inplace=True)
st.write(output)