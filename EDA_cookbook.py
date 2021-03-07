# Describe
df.describe()
df.describe(include='object')


# Plot categorical features counts
for column in df.select_dtypes(include='object'):
    if df[column].nunique() < 10:
        sns.countplot(y=column, data=df)
        plt.show()


# Boxplots for each level of categorical feature vs target
for column in df.select_dtypes(include=’object’):
 if df[column].nunique() < 10:
     sns.boxplot(y=column, x=’Price’, data=df)
     plt.show()


# Aggregating numeric features for each categorical feature
 for column in df.select_dtypes(include='object'):
     if df[column].nunique() < 10:
         display(df.groupby(column).mean())


# Numerical features correlations
corrs = df.corr()
plt.figure(figsize=(7,7))
sns.heatmap(corrs, cmap='RdBu_r', annot=True)
plt.show()