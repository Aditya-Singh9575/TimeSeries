#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install yfinance


# In[3]:


import yfinance as yf


# In[11]:


symbol = "EURINR=X"
start_date = "2023-01-01"
end_date = "2024-09-30"


# In[13]:


data = yf.download(symbol , start=start_date , end=end_date)


# In[15]:


data


# In[17]:


data.to_csv("EURINR_data.csv")


# In[ ]:




