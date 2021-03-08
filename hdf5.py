# Pandas has a built-in solution for this which uses HDF5 - a high-performance storage format 
# designed specifically for storing tabular arrays of data. 
# Pandas’ HDFStore class allows you to store your DataFrame in an HDF5 file so that it can be 
# accessed efficiently, while still retaining column types and other metadata.


# ===== SAVING pre-processed df =====

# Create storage object with filename `processed_data`
data_store = pd.HDFStore('processed_data.h5')

# Put DataFrame into the object setting the key as 'preprocessed_df'
data_store['preprocessed_df'] = df
data_store.close()


# ===== LOADING pre-processed df =====

# Access data store
data_store = pd.HDFStore('processed_data.h5')

# Retrieve data using key
preprocessed_df = data_store['preprocessed_df']
data_store.close()


# A data store can house multiple tables, with the name of each as a key.

# Just a note about using the HDFStore in Pandas: you will need to have PyTables >= 3.0.0 installed. 
# So after you have installed Pandas, make sure to update PyTables like this: 
# pip install --upgrade tables