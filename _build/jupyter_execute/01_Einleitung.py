#!/usr/bin/env python
# coding: utf-8

# # Einleitung
# Hier steht die Einleitung.
# 
# ## Voraussetzungen
# Python installieren

# In[1]:


import numpy as np
import seaborn as sns
import plotly.express as px


# ## Ein erstes Python Beispiel

# In[2]:


x = np.linspace(0,1,50)
y = 2*x/(x+3)

sns.lineplot(x=x,y=y)
#px.line(x=x,y=y)


# ## Mathematik
# ```{prf:theorem} Mein erstes Theorem
# :label: my-theorem
# 
# 
# $f(x)=x^2$
# 
# $$
# f(x)=x^2
# $$ (mylabel)
# 
# $$
# f(x)=\vec{x}
# $$ (mylabel2)
# 
# \begin{align*}
# \bar{x}=\sum_{i=1}^m x_i\cdot P(X=x_i)\\\label{eq:1}
# \bmat{cc} 1 & 2 \\ 0 & 1 \emat{}\in \N \\
# \derv{f}{x}\\
# \dervquad{f}{x}\\
# \dervzwei{f}{x}{y}\\
# \mat{A}=
# \end{align*}
# 
# 
# Was geht ab
# ````

# Schau dir Gleichung {eq}`mylabel2` oder {eq}`mylabel` an

# In[ ]:




