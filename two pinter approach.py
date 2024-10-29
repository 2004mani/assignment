#!/usr/bin/env python
# coding: utf-8

# In[1]:


# finding two elements sum is 23 in the given list
l=[1,2,3,6,17,20,25]
s=23
f=False
for i in range(len(l)-1):
    for j in range(i+1,len(l)):
        if s==(l[i]+l[j]):
            print(l[i],l[j],end=" ")
    print()
print()
            


# In[ ]:




