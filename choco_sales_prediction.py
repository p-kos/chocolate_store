# Step 1: Load and Inspect the Data
import pandas as pd
from urllib.request import urlretrieve

# Load the CSV file
url = 'https://drive.google.com/file/d/1r0sSdVJX8tmZ-cjm2FEqkH8MXizWEsqH/view?usp=drive_link'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
filename = 'taboada_store.csv'
urlretrieve(url, filename)

data = pd.read_csv('taboada_store.csv') 

# Display the first few rows of the dataset
print(data.head())
print(data.info())
print(data.describe())

# Step 2: Data Cleaning

# Data Cleaning

# Handle missing values
data['ClientName'].fillna('Sin Nombre', inplace=True)

# Remove negative values in Quantity and Price
data = data[(data['Quantity'] > 0) & (data['Price'] > 0)]

# Convert InvoiceDate to datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Inspect cleaned data
print(data.info())
print(data.describe())

# Step 3: Exploratory Data Analysis (EDA)

import matplotlib.pyplot as plt
import seaborn as sns

# Distribution of PaidAmount
plt.figure(figsize=(10, 6))
sns.histplot(data['PaidAmount'], bins=50, kde=True)
plt.title('Distribution of PaidAmount')
plt.xlabel('PaidAmount')
plt.ylabel('Frequency')
plt.savefig('Figure_1.png')

# Distribution of Quantity
plt.figure(figsize=(10, 6))
sns.histplot(data['Quantity'], bins=50, kde=True)
plt.title('Distribution of Quantity')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.savefig('Figure_2.png')

# Distribution of Price
plt.figure(figsize=(10, 6))
sns.histplot(data['Price'], bins=50, kde=True)
plt.title('Distribution of Price')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.savefig('Figure_3.png')

# Sales Over Time
plt.figure(figsize=(14, 7))
data.set_index('InvoiceDate').resample('M')['PaidAmount'].sum().plot()
plt.title('Monthly Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total PaidAmount')
plt.savefig('Figure_4.png')


# Step 4: Data Transformation
# Feature Engineering: Extracting date-related features
data['Year'] = data['InvoiceDate'].dt.year
data['Month'] = data['InvoiceDate'].dt.month
data['Day'] = data['InvoiceDate'].dt.day
data['Weekday'] = data['InvoiceDate'].dt.weekday

# Encoding Categorical Variables
data = pd.get_dummies(data, columns=['WithInvoice', 'ProductCategory', 'ProductCode', 'ProductName', 'ClientName'], drop_first=True)

# Drop InvoiceDate and InvoiceNumber as they are not needed for modeling
data.drop(columns=['InvoiceDate', 'InvoiceNumber'], inplace=True)

# Define features and target variable
X = data.drop(columns=['PaidAmount'])
y = data['PaidAmount']

# Split data into training and test sets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.shape, X_test.shape, y_train.shape, y_test.shape

# Train Model

# Train the Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')