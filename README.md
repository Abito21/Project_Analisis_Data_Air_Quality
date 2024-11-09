# Submission Dicoding "Belajar Data Analytic dengan Python" : Air Quality Dashboard ✨

Repository ini berisikan projek analisis data menggunakan dataset kualitas udara dari https://github.com/marceloreis/HTI/tree/master. Sumber bacaan sudah disertakan juga pada link github tersebut yang terdiri dari parameter cuaca dan parameter material kadar kualitas udara yang berdasarkan hari, bulan, tahun dan stasiun cuaca. Deployment dashboard dapat diakses pada link berikut https://airqualityanalyzeabid.streamlit.app/.

## Instalasi

1. Clone repository ke komputer lokal menggunakan perintah dibawah ini:

   ```shell
   git clone https://github.com/Abito21/Project_Analisis_Data_Air_Quality.git
   ```

2. Pastikan memiliki environment Python yang sesuai dan library yang diperlukan. Perintah dibawah dapat digunakan untuk melakukan instalasi library yang dibutuhkan :

   ```shell
   pip install streamlit
   pip install -r dashboard/requirements.txt
   ```

## Setup Environment - Python
```
python -m venv main-ds
main-ds\Scripts\activate
pip install -r requirements.txt

Notebook dikerjakan di Google Collaboratory
a. numpy==1.26.4
b. pandas==2.2.2
c. matplotlib==3.8.0
d. seaborn==0.13.2

Dashboard dikerjakan di Visual Studio Code dengan environment python 3.12.1
a. numpy==2.1.3
b. pandas==2.2.3
c. matplotlib==3.9.2
d. seaborn==0.13.2
e. streamlit==1.40.0
```

## Setup Environment - Shell/Terminal
```
mkdir Project_Analisis_Data_Air_Quality
cd Project_Analisis_Data_Air_Quality
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Struktur Direktori

- **/data**: Direktori yang digunakan untuk menampung dataset dalam format .csv.
- **/dashboard**: Direktori berisi dashboard.py yang digunakan untuk membuat dashboard hasil analisis data air quality.
- **Proyek_Analisis_Data_E_Commerce.ipynb**: File yang digunakan untuk melakukan olah dan analisis data.

## Run steamlit app
```
streamlit run dashboard.py
```
