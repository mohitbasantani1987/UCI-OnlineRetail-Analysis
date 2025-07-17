import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class DataProcessor:
    def __init__(self, df):
        self.df = df

    def handle_level_1(self):
        """
        Perform Level-1 analysis: Basic data overview.
        """
        # description of the dataset
        desc = "This is a transactional data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers."

        columns_desc = {
        "InvoiceNo" : "A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'C', it indicates a cancellation.",
        "StockCode": "A 5-digit integral number uniquely assigned to each distinct product.", 
        "Description" : "Product (item) Name.",
        "Quantity" :"The quantities of each product(item) per transaction.",	
        "InvoiceDate" : "The day and time when a invoice was generated.", 
        "UnitPrice" : "Product price per unit.", 
        "CustomerID" : "A 5-digit integral number uniquely assigned to each customer.", 
        "Country" : "The name of the country where a customer resides."
        }

        data_types = {
        "InvoiceNo": "Text",
        "StockCode": "Text",
        "Description": "Text",
        "Quantity": "Numeric",
        "InvoiceDate": "Datetime",
        "UnitPrice": "Numeric",
        "CustomerID": "Numeric",
        "Country": "Text"
        }

        # Facts 
        total_transactions = self.df['Invoice'].nunique()
        total_countries = self.df['Country'].nunique()
        rows_count = self.df.shape[0]

        data = {
            "facts1" : f"There are {total_countries} unique countries in the dataset.",
            "facts2": f"This dataset has total {total_transactions} number of transactions.",
            "facts3" : f"The dataset contains {rows_count} records consolidated for two years after removing the null rows and irrelavant data.",      
        }

        return {
            "data_types": data_types,
            "description": desc,
            "columns_description": columns_desc,
            "facts": data
        }
    

    def handle_level_2(self):
        """
        Perform Level-2 analysis: Will Add the new feature and will create the plots based on the that.
        """
        self.df['Revenue'] = self.df['Quantity'] * self.df['Price'] # (feature engineering)
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        self.df['Month'] = self.df['InvoiceDate'].dt.to_period('M').astype(str) # (feature engineering)
        

        # Plot - 1 - Visualize the top 10 countries by total revenue
        top_countries = self.df.groupby('Country')['Revenue'].sum().nlargest(10).reset_index()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_countries['Country'], y=top_countries['Revenue'], hue=top_countries['Country'], legend=False, palette='magma')

        # Annotating each bar with value
        for i, value in enumerate(top_countries['Revenue']):
            plt.text(i, value + 1000, f'{value:,.0f}', ha='center', va='bottom', fontsize=10)

        plt.title("Top 10 Countries by Revenue (Annotated)")
        plt.ylabel("Total Revenue")
        plt.xticks(rotation=45)
        plt.savefig('assets/top_10_countries_revenue.png')
        plt.close()

        # Plot - 2 - Visualize Monthly Revenue Over Time
        monthly_rev = self.df.groupby('Month')['Revenue'].sum().sort_index()
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=monthly_rev.index, y=monthly_rev.values, marker='o')

        plt.title("Monthly Revenue Trend")
        plt.xticks(rotation=45)
        plt.ylim(0, monthly_rev.max() * 1.1)  # setting y-limit
        plt.ylabel("Total Revenue")
        plt.xlabel("Month")
        plt.tight_layout()
        plt.savefig("assets/monthly_revenue_trend.png")
        plt.close()

        # Plot - 3 - Visualize Top 10 Products by quantity sold
        top_products = self.df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_products.index, y=top_products['Quantity'],hue=top_products['Quantity'], legend=False, palette='viridis')
        plt.title("Top 10 Products by Quantity Sold")
        plt.ylabel("Total Quantity Sold")
        plt.tight_layout()
        plt.savefig("assets/top_10_products_quantity.png")
        plt.close()

        cummlative_plots = {
            'top_countries_revenue': 'assets/top_10_countries_revenue.png',
            'monthly_revenue_trend': 'assets/monthly_revenue_trend.png',
            'top_products_quantity': 'assets/top_10_products_quantity.png'
        }
        return cummlative_plots


    def handle_level_3(self):
        """
        Perform Level-3 analysis: Will create the plots with detailed analysis.
        """
        top_countries = self.df['Country'].value_counts().head(5).index.tolist()
        # Filter df to keep only those countries
        df_top = self.df[self.df['Country'].isin(top_countries)].copy()

        # Group by Country and Month, Sum the revenue
        grouped = df_top.groupby(['Country', 'Month'])['Revenue'].sum().reset_index()
        grouped['Month'] = pd.to_datetime(grouped['Month'])
        grouped = grouped.sort_values('Month')
        grouped['Month'] = grouped['Month'].dt.strftime('%Y-%m')
        pivot_df = grouped.pivot(index='Month', columns='Country', values='Revenue').fillna(0)


        # Plot - 1 - Monthly Revenue by Country (Stacked Bar Chart)
        plt.figure(figsize=(14, 6))
        bottom = None

        for country in pivot_df.columns:
            plt.bar(pivot_df.index, pivot_df[country], label=country, bottom=bottom)
            bottom = pivot_df[country] if bottom is None else bottom + pivot_df[country]

        plt.title('Monthly Revenue by Country (Stacked)')
        plt.ylabel('Revenue')
        plt.xlabel('Month')
        plt.xticks(rotation=45)
        plt.legend(title='Country')
        plt.tight_layout()
        plt.savefig(f"assets/monthly_revenue_by_country.png")
        plt.close()

        # Plot - 2 - KDE Curve for Quantity
        df_quantity = self.df[(self.df['Quantity'] > 0) & (self.df['Quantity'] < 100)]
        plt.figure(figsize=(12, 8))
        sns.kdeplot(df_quantity['Quantity'], fill=True, color='green')
        plt.title('Quantity KDE Curve')
        plt.xlabel('Quantity')
        plt.tight_layout()
        plt.savefig("assets/quantity_kde_curve.png")
        plt.close()

        # Plot - 3 - Visualize Top 10 Products by Quantity Sold using Plotly
        corr_matrix = self.df[['Quantity', 'Price', 'Revenue']].corr()

        plt.figure(figsize=(6, 4))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', linewidths=0.5)
        plt.title("Correlation Matrix")
        plt.tight_layout()
        plt.savefig("assets/correlation_matrix.png")
        plt.close()

        # Plot - 4 - Visualize Box Plot for Revenue by Country 
        sns.set_style("whitegrid")  # sets overall look

        plt.figure(figsize=(10, 5))
        sns.boxplot(data=self.df[self.df['Country'].isin(['Germany', 'France', 'United Kingdom'])],
                    x='Country', y='Revenue', hue='Country', legend=False, palette='Set1')
        sns.despine(left=False, bottom=False, top=False, right=False)  # removes top and right border

        plt.title("Revenue Distribution with Whitegrid Style")
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig("assets/revenue_boxplot.png")
        plt.close()

        cummlative_plots = {
            'monthly_revenue_by_country': 'assets/monthly_revenue_by_country.png',
            'quantity_kde_curve': 'assets/quantity_kde_curve.png',
            'correlation_matrix': 'assets/correlation_matrix.png',
            'revenue_boxplot': 'assets/revenue_boxplot.png'
        }
        return cummlative_plots


