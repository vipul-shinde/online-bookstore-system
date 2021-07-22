from bookstore.models import Book
import pandas as pd
import numpy as np

rating = np.random.choice(5, size=90) + 1
df = pd.read_csv('~/Desktop/Temp/database/database.csv')
df['rating'] = rating

for i,r in df.iterrows():
    q = Book(isbn=r['isbn'],
             category=r['category'],
             title=r['title'],
             description=r['description'],
             image_path=r['image_path'],
             edition=r['edition'],
             publisher=r['publisher'],
             publication_year=r['publication_year'],
             author=r['author'],
             stock=r['stock'],
             cost=r['cost'],
             rating=r['rating'])
    q.save()
