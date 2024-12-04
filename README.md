# Lab 1 : Data Pipelines with SQL and NoSQL Integration

This lab will guide you through creating a data pipeline for a Data Lake by integrating SQL and NoSQL databases into the Staging and Curated zones. 

---

## 1. **Data Importation**

Logs indicate the creation of CSV files from Arrow format:

```
Creating CSV from Arrow format: 100%|████████████████████████████████████████████████████████████████████████████| 37/37 [00:00<00:00, 143.30ba/s]
Creating CSV from Arrow format: 100%|██████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 155.56ba/s]
Creating CSV from Arrow format: 100%|██████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 133.11ba/s]
```

---

## 2. **Data to Raw Layer**

### Process:
- The combined data is saved in the `raw` layer as `combined.csv`.
- Logs:
  ```
  Combined file saved: data/raw/combined.csv
  File uploaded to raw with the name combined.csv
  ```

---

## 3. **Prepare Staging Layer**

### Process:
- The combined file is downloaded from S3.
- Data cleaning removes invalid rows.
- The cleaned data is inserted into a MySQL database (`staging`) in the `texts` table.

### Logs:
```
File downloaded from S3: combined.csv -> ./combined_cleaned.csv
Available columns: Index(['text', 'split'], dtype='object')
Cleaned data: 17970 rows removed.
Connection established with MySQL database: staging
Table 'texts' successfully verified/created.
26866 rows inserted into the 'texts' table.
Total number of rows in the 'texts' table: 53732
Number of rows where 'content' is not NULL: 53732
Number of rows retrieved: 53732
Example retrieved data: [{'id': 1, 'content': ' = Valkyria Chronicles III = \n'}, ...]
MySQL connection closed.
```

---

## 4. **Staging Layer to Curated Layer**

### Process:
- Data from the staging layer is tokenized.
- The tokenized data is stored in MongoDB for further use.

### Logs:
```
None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
Connexion MySQL établie.
53732 lignes récupérées depuis MySQL.
53732 textes tokenisés.
Connexion MongoDB établie.
53732 documents insérés dans MongoDB.
Échantillon de données depuis MongoDB (5 documents) :
{'_id': ObjectId('67507be71c4fb82f4de52e45'), 'id': 1, 'text': ' = Valkyria Chronicles III = \n', 'tokens': [101, 1027, 11748, 4801, 4360, 11906, 3523, 1027, 102], 'metadata': {'source': 'mysql', 'processed_at': '2024-12-04T15:57:17.700756Z'}}
{'_id': ObjectId('67507be71c4fb82f4de52e46'), 'id': 2, 'text': ' Senjō no Valkyria 3 : Unrecorded Chronicles ( Japanese : 戦場のヴァルキュリア3 , lit . Valkyria of the Battlefield 3 ) , commonly referred to as Valkyria Chronicles III outside Japan , is a tactical role @-@ playing video game developed by Sega and Media.Vision for the PlayStation Portable . Released in January 2011 in Japan , it is the third game in the Valkyria series . Employing the same fusion of tactical and real @-@ time gameplay as its predecessors , the story runs parallel to the first game and follows the " Nameless " , a penal military unit serving the nation of Gallia during the Second Europan War who perform secret black operations and are pitted against the Imperial unit " Calamaty Raven " . \n', 'tokens': [101, 12411, 5558, 2053, 11748, 4801, 4360, 1017, 1024, 4895, 2890, 27108, 5732, 11906, 1006, 2887, 1024, 1856, 1806, 1671, 30222, 30218, 30259, 30227, 30255, 30258, 30219, 2509, 1010, 5507, 1012, 11748, 4801, 4360, 1997, 1996, 11686, 1017, 1007, 1010, 4141, 3615, 2000, 2004, 11748, 4801, 4360, 11906, 3523, 2648, 2900, 1010, 2003, 1037, 8608, 2535, 1030, 1011, 1030, 2652, 2678, 2208, 2764, 2011, 16562, 1998, 2865, 1012, 4432, 2005, 1996, 9160, 12109, 1012, 2207, 1999, 2254, 2249, 1999, 2900, 1010, 2009, 2003, 1996, 2353, 2208, 1999, 1996, 11748, 4801, 4360, 2186, 1012, 15440, 1996, 2168, 10077, 1997, 8608, 1998, 2613, 1030, 1011, 1030, 2051, 11247, 2004, 2049, 16372, 1010, 1996, 2466, 3216, 5903, 2000, 1996, 2034, 2208, 1998, 4076, 1996, 1000, 2171, 3238, 1000, 1010, 1037, 18476, 2510, 3131, 3529, 1996, 3842, 1997, 26033, 2401, 2076, 1996, 2117, 12124, 2078, 2162, 2040, 4685, 3595, 2304, 3136, 1998, 2024, 25895, 2114, 1996, 4461, 3131, 1000, 10250, 8067, 3723, 10000, 1000, 1012, 102], 'metadata': {'source': 'mysql', 'processed_at': '2024-12-04T15:57:17.701660Z'}}
{'_id': ObjectId('67507be71c4fb82f4de52e47'), 'id': 3, 'text': " The game began development in 2010 , carrying over a large portion of the work done on Valkyria Chronicles II . While it retained the standard features of the series , it also underwent multiple adjustments , such as making the game more forgiving for series newcomers . Character designer Raita Honjou and composer Hitoshi Sakimoto both returned from previous entries , along with Valkyria Chronicles II director Takeshi Ozawa . A large team of writers handled the script . The game 's opening theme was sung by May 'n . \n", 'tokens': [101, 1996, 2208, 2211, 2458, 1999, 2230, 1010, 4755, 2058, 1037, 2312, 4664, 1997, 1996, 2147, 2589, 2006, 11748, 4801, 4360, 11906, 2462, 1012, 2096, 2009, 6025, 1996, 3115, 2838, 1997, 1996, 2186, 1010, 2009, 2036, 9601, 3674, 24081, 1010, 2107, 2004, 2437, 1996, 2208, 2062, 2005, 23795, 2005, 2186, 24159, 1012, 2839, 5859, 15547, 2696, 10189, 23099, 1998, 4543, 2718, 24303, 7842, 21138, 11439, 2119, 2513, 2013, 3025, 10445, 1010, 2247, 2007, 11748, 4801, 4360, 11906, 2462, 2472, 3138, 4048, 11472, 10830, 1012, 1037, 2312, 2136, 1997, 4898, 8971, 1996, 5896, 1012, 1996, 2208, 1005, 1055, 3098, 4323, 2001, 7042, 2011, 2089, 1005, 1050, 1012, 102], 'metadata': {'source': 'mysql', 'processed_at': '2024-12-04T15:57:17.702031Z'}}
{'_id': ObjectId('67507be71c4fb82f4de52e48'), 'id': 4, 'text': " It met with positive sales in Japan , and was praised by both Japanese and western critics . After release , it received downloadable content , along with an expanded edition in November of that year . It was also adapted into manga and an original video animation series . Due to low sales of Valkyria Chronicles II , Valkyria Chronicles III was not localized , but a fan translation compatible with the game 's expanded edition was released in 2014 . Media.Vision would return to the franchise with the development of Valkyria : Azure Revolution for the PlayStation 4 . \n", 'tokens': [101, 2009, 2777, 2007, 3893, 4341, 1999, 2900, 1010, 1998, 2001, 5868, 2011, 2119, 2887, 1998, 2530, 4401, 1012, 2044, 2713, 1010, 2009, 2363, 26720, 4180, 1010, 2247, 2007, 2019, 4423, 3179, 1999, 2281, 1997, 2008, 2095, 1012, 2009, 2001, 2036, 5967, 2046, 8952, 1998, 2019, 2434, 2678, 7284, 2186, 1012, 2349, 2000, 2659, 4341, 1997, 11748, 4801, 4360, 11906, 2462, 1010, 11748, 4801, 4360, 11906, 3523, 2001, 2025, 22574, 1010, 2021, 1037, 5470, 5449, 11892, 2007, 1996, 2208, 1005, 1055, 4423, 3179, 2001, 2207, 1999, 2297, 1012, 2865, 1012, 4432, 2052, 2709, 2000, 1996, 6329, 2007, 1996, 2458, 1997, 11748, 4801, 4360, 1024, 24296, 4329, 2005, 1996, 9160, 1018, 1012, 102], 'metadata': {'source': 'mysql', 'processed_at': '2024-12-04T15:57:17.702423Z'}}
{'_id': ObjectId('67507be71c4fb82f4de52e49'), 'id': 5, 'text': ' = = Gameplay = = \n', 'tokens': [101, 1027, 1027, 11247, 1027, 1027, 102], 'metadata': {'source': 'mysql', 'processed_at': '2024-12-04T15:57:17.702484Z'}}
```

