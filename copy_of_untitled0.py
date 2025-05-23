# -*- coding: utf-8 -*-
"""Copy of Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mbPEoCRcF22geknpxRGq_S0VfJyc7OfU
"""

import numpy as np
import pandas as pd
import os

import seaborn as sns
import matplotlib.pyplot as plt

sales=pd.read_csv('/content/sales_pipeline.csv')
products=pd.read_csv('/content/products.csv')
sales_team=pd.read_csv('/content/sales_teams.csv')

sales.duplicated().sum()
sales.drop_duplicates(inplace=True)
sales.dropna(inplace=True)

products.head()

products.duplicated().sum()
products.drop_duplicates(inplace=True)
products.dropna(inplace=True)
products.isna().sum()

sales_team.head()

sales_team.duplicated().sum()
sales_team.drop_duplicates(inplace=True)
sales_team.dropna(inplace=True)
sales_team.isna().sum()

sales.head()

merged_data = pd.merge(sales,products, how='left', left_on='product', right_on='product')

merged_data.head()

data=pd.merge(merged_data,sales_team, how='left', left_on='sales_agent', right_on='sales_agent')
pd.set_option('display.max_columns', None)
data.head()

describe=data.describe()
describe



data.info()

"""**Most Product Sales**"""

product_counts=data['product'].value_counts()
plt.figure(figsize=(12,6))
sns.barplot(x=product_counts.index, y=product_counts.values, palette='viridis')

plt.title('Number of opportunities for each product', fontsize=16)
plt.xlabel('product', fontsize=14)
plt.ylabel('number of opportunity', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

product_deal_counts = data.groupby(['product', 'deal_stage']).size().reset_index(name='count')


plt.figure(figsize=(14,8))
sns.barplot(
    data=product_deal_counts,
    x='product',
    y='count',
    hue='deal_stage',
    palette='Set2'
)

plt.title('deal statue of each product', fontsize=16)
plt.xlabel('product', fontsize=14)
plt.ylabel('number of opportunity', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='deal statue')
plt.grid(axis='y')
plt.show()

sales_agent=data['sales_agent'].value_counts()
sales_agent=sales_agent.head(5)
plt.figure(figsize=(12,6))
sns.barplot(x=sales_agent.index, y=sales_agent, palette='viridis')

plt.title('Number of opportunities for each sales agent', fontsize=16)
plt

data['deal_stage'].value_counts()
plt.figure(figsize=(12,6))
sns.countplot(data=data, x='deal_stage', palette='viridis')

plt.title('Number of opportunities for each deal stage', fontsize=16)

plt.subplot(2, 3, 4)
data['engage_date'] = pd.to_datetime(data['engage_date'])
data['close_date'] = pd.to_datetime(data['close_date'])
data['close_duration'] = (data['close_date'] - data['engage_date']).dt.days
sns.histplot(data['close_duration'], bins=20, kde=True, color='teal')
plt.title('Closing time of deals (days)')

most_profitable_sales=data.groupby('sales_agent')['close_value'].sum().sort_values(ascending=False).head(5)
plt.figure(figsize=(12,6))
sns.barplot(x=most_profitable_sales.index, y=most_profitable_sales, palette='viridis')

plt.title('Most profitable sales agent', fontsize=16)
plt.xlabel('sales agent', fontsize=14)
plt.ylabel('close value', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

series_total = data.groupby('series')['close_value'].sum()
plt.figure(figsize=(12,6))
sns.barplot(x=series_total.index, y=series_total, palette='viridis')

plt

# Theme وألوان
sns.set_style('whitegrid')
custom_palette = sns.color_palette("coolwarm", as_cmap=True)



# KPIs حساب
total_deals = data.shape[0]
win_rate = (data['deal_stage'] == 'won').sum() / total_deals * 100
avg_close_duration = data['close_duration'].mean()
total_revenue = data['close_value'].sum()

# تحضير الفيجور الأساسي
fig = plt.figure(figsize=(24, 18), facecolor='#f7f7f7')

# Fonts
title_font = {'fontsize': 16, 'fontweight': 'bold', 'color': '#333'}
kpi_font = {'fontsize': 20, 'fontweight': 'bold', 'color': '#2c3e50'}

# --- KPIs Section ---

# Total Deals
ax_kpi1 = plt.subplot2grid((4, 3), (0, 0))
ax_kpi1.axis('off')
ax_kpi1.text(0.5, 0.6, '🧾 Total Deals', ha='center', **title_font)
ax_kpi1.text(0.5, 0.3, f"{total_deals:,}", ha='center', **kpi_font)

# Win Rate
ax_kpi2 = plt.subplot2grid((4, 3), (0, 1))
ax_kpi2.axis('off')
ax_kpi2.text(0.5, 0.6, '🏆 Win Rate', ha='center', **title_font)
ax_kpi2.text(0.5, 0.3, f"{win_rate:.1f}%", ha='center', **kpi_font)

# Average Close Duration
ax_kpi3 = plt.subplot2grid((4, 3), (0, 2))
ax_kpi3.axis('off')
ax_kpi3.text(0.5, 0.6, '⏳ Avg. Close Duration', ha='center', **title_font)
ax_kpi3.text(0.5, 0.3, f"{avg_close_duration:.1f} Days", ha='center', **kpi_font)

# --- Graphs Section ---

# 1- Deals per Product
ax1 = plt.subplot2grid((4, 3), (1, 0), rowspan=2)
sns.countplot(data=data, x='product', order=data['product'].value_counts().index, palette='cool')
ax1.set_title('Deals per Product', **title_font)
ax1.set_xlabel('')
ax1.set_ylabel('Number of Deals')
plt.setp(ax1.get_xticklabels(), rotation=45)

# 2- Win vs Lost per Product
ax2 = plt.subplot2grid((4, 3), (1, 1), rowspan=2)
cross = pd.crosstab(data['product'], data['deal_stage'], normalize='index')
cross.plot(kind='bar', stacked=True, ax=ax2, colormap='coolwarm', edgecolor='black')
ax2.set_title(' Win vs Lost Deals per Product', **title_font)
ax2.set_ylabel('Percentage')
plt.setp(ax2.get_xticklabels(), rotation=45)

# 3- Close Duration Distribution
ax3 = plt.subplot2grid((4, 3), (1, 2), rowspan=2)
sns.histplot(data['close_duration'], bins=20, kde=True, color='#007acc', edgecolor='black')
ax3.set_title(' Close Duration Distribution', **title_font)
ax3.set_xlabel('Duration (Days)')
ax3.set_ylabel('Number of Deals')

# 4- Revenue Share by Series
ax4 = plt.subplot2grid((4, 3), (3, 1))
series_total = data.groupby('series')['close_value'].sum()
series_total.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='Set3', ax=ax4, wedgeprops=dict(edgecolor='black'))
ax4.set_title('🎯 Revenue Share by Series', **title_font)
ax4.set_ylabel('')

plt.tight_layout(pad=2.0)
plt.show()