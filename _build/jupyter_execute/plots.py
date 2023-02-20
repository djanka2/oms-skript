#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.graph_objects as go
import numpy as np

x = np.linspace(-4,4,100)
y = np.linspace(-2,2,100)
X,Y = np.meshgrid(x,y)
z = X + 2*Y

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues"))
fig.update_layout( autosize=True, height=250,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))


# In[2]:


import plotly.graph_objects as go
import numpy as np

x = np.linspace(0.1,3,100)
y = np.linspace(0.1,3,100)
X,Y = np.meshgrid(x,y)
z = 0.5*np.sin(3*X*Y) + np.log(X) - np.sqrt(Y)

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues"))
fig.update_layout(height=250, autosize=True,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))


# In[3]:


import plotly.graph_objects as go
import numpy as np

x = np.linspace(-2,2,100)
y = np.linspace(-4,4,100)
X,Y = np.meshgrid(x,y)
z = 3*X**2 + Y**2

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Portland"))
fig.update_layout( autosize=True, height=250,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))


# In[4]:


import plotly.graph_objects as go
import numpy as np

x = np.linspace(-2,2,100)
y = np.linspace(-2,2,100)
X,Y = np.meshgrid(x,y)
z = X + 2*Y

fig = go.Figure(go.Contour(x=x,y=y,z=z, colorscale="Blues", contours_coloring='heatmap'))
fig.update_layout( autosize=True, height=250,
                  margin=go.layout.Margin(l=150, r=150, b=0, t=0))


# In[5]:


import seaborn as sns
import numpy as np
sns.set(rc={'figure.figsize':(6,5)})
sns.set_style("whitegrid")

x = np.array([1,5])
y = np.array([1,4])

p = sns.scatterplot(x=x,y=y, s=150, color="black")
p.xaxis.set_ticks([0,1,2,3,4,5,6])
p.yaxis.set_ticks([0,1,2,3,4,5])


# In[6]:


import seaborn as sns
import numpy as np
sns.set(rc={'figure.figsize':(6,4.5)})
sns.set_style("whitegrid")

x = np.array([0])
y = np.array([0])

p = sns.scatterplot(x=x,y=y, s=0, color="black")
p.xaxis.set_ticks([-2,-1.5,-1,-0.5,0,0.5,1,1.5,2])
p.yaxis.set_ticks([-1.5,-1,-0.5,0,0.5,1,1.5])


# In[7]:


import plotly.graph_objects as go
import numpy as np

x = np.linspace(-3,3,100)
y = np.linspace(-3,3,100)
X,Y = np.meshgrid(x,y)
z = X*Y/(X**2 + Y**2)

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues"))
fig.update_layout( autosize=True, height=500,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))


# In[8]:


import plotly.express as px
import numpy as np

x = np.array([-1,-1e-16,1e-16,1])
y = (x>=0).astype("float")
px.line(x=x,y=y, color_discrete_sequence=list(reversed(px.colors.sequential.Blues)), height=250)


# In[9]:


import plotly.express as px
import numpy as np

x = np.linspace(-0.1,0.1,10000)
y = np.sin(1/x)
px.line(x=x,y=y, color_discrete_sequence=list(reversed(px.colors.sequential.Blues)), height=250)


# In[10]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(12,9)})
sns.set_style("whitegrid")

x = np.linspace(-5,5,1000)
y = np.linspace(-5,5,1000)

X,Y = np.meshgrid(x,y)

z = 50 - X**2 - Y**2
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, z, linewidth=0, antialiased=False)
plt.show()


# In[11]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(6,4.5)})
sns.set_style("whitegrid")

x = np.linspace(-5,5,1000)
p = sns.lineplot(x=x, y=50 - x**2)
p.yaxis.set_ticks(np.linspace(25,75,11))
#p.yaxis.set_ticks([0,1,2,3,4,5])


# In[12]:


import plotly.graph_objects as go
import numpy as np

a = 1
b = 1

x = np.linspace(-1.5,1.5,100)
y = np.linspace(-0.5,2.5,100)
X,Y = np.meshgrid(x,y)

z = (a-X)**2 + b*(Y-X**2)**2

fig = go.Figure(go.Contour(x=x,y=y,z=z, colorscale="Blues",
                           contours=dict(start=0,
                                        end=8,
                                        size=0.5,
        ),))
fig.update_layout( autosize=True,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))


# In[13]:


import plotly.graph_objects as go
import numpy as np

# Die Funktion f als Surface Plot
x = np.linspace(-1.5,1.5,100)
y = np.linspace(-0.5,2.5,100)
X,Y = np.meshgrid(x,y)
z = (1-X)**2 + (Y-X**2)**2

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues",))

# Richtungsvektor a=(2,1)
a1 = 2
a2 = 1
# Argument t der Kurve läuft von -0.5 bis 0.75
t = np.linspace(-0.5,0.75,100)
x = t*a1
y = t*a2
z = (1-x)**2 + (y-x**2)**2

# x,y,z enthält jetzt die Koordinaten der Kurve f(0+t*a). 
fig.add_trace(go.Scatter3d(x=x,y=y,z=z, mode="lines", line=dict(width=5)))
fig.update_layout( autosize=True,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))


# In[ ]:




