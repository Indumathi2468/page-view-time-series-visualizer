import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data by removing top 2.5% and bottom 2.5% of page views
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

# Function to draw line plot
def draw_line_plot():
    # Copy dataframe for safety
    df_line = df.copy()
    
    plt.figure(figsize=(15,5))
    plt.plot(df_line.index, df_line['value'], color='red')
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    
    # Save figure
    plt.savefig("line_plot.png")
    return plt.gcf()

# Function to draw bar plot
def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # Group by year and month and take mean
    df_bar_grouped = df_bar.groupby(['year','month'])['value'].mean().unstack()
    
    # Plot
    df_bar_grouped.plot(kind='bar', figsize=(15,7))
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=[
        'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
    ])
    
    # Save figure
    plt.savefig("bar_plot.png")
    return plt.gcf()

# Function to draw box plot
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    
    # Sort months for proper order
    df_box = df_box.sort_values('month_num')
    
    fig, axes = plt.subplots(1, 2, figsize=(20,7))
    
    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    
    plt.savefig("box_plot.png")
    return fig
