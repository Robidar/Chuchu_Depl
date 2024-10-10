# Artificial intelligence has the potential to revolutionise cardiovascular health

 The dataset for this study is not publicly available, but it can be accessed by requesting it through https://ams.aspree.org/application/home.aspx
 
 [paper link to be provided]

## Atherosclerotic cardiovascular disease (ASCVD) risk prediction 

The codes utilised for model development are available on this GitHub repository. Additionally, the repository contains the saved model in *.pkl* format, along with the *app.py* and *requirements.txt* files. The figure below (at the end) shows the survival probabilities of five patients as an example, at 3-year, 5-year, and 10-year intervals.

The survival probabilities were generated using our best-performing model (DeepSurv) via "streamlit run app.py" in the terminal to open the web application locally.

To open the web app (app.py) and check the survival probability on a local computer, visit [Streamlit](https://streamlit.io/cloud) and [GitHub codespaces](https://github.blog/developer-skills/github/a-beginners-guide-to-learning-to-code-with-github-codespaces/)


**In brief, follow the following steps to run the web app:**

- Download or clone the project
  
  *The .pkl file, the app.py, and the requirements.text should be downloaded and put in the same folder.*

  Or clone the project as follows

  ```
  git clone https://github.com/Robidar/Chuchu_Depl.git
  cd Chuchu_Depl 
  ```
  
- Create a virtual environment
  
  ```
  python -m venv name python==3.7.10
  ```
- Install dependencies using

  ```
  pip install -r requirements.text
  ```
- Execute the app.py file

 ```
streamlit run app.py
 ```

**Now, you should go to the first page of the web app to start entering values**

![pointing-down (1)](https://github.com/user-attachments/assets/a716b9ba-8ebc-4d84-97f8-950328a8c4dd)






![Screenshot 2024-10-10 220554_1st](https://github.com/user-attachments/assets/ae9c0850-b112-4e79-8665-329932b92ceb)




**For example, the screenshot below represents the survival probabilities using the five patient profiles**

![pointing-down (1)](https://github.com/user-attachments/assets/c52d344c-ebb4-47f1-bfa5-c42fa6968238)




![Screenshot 2024-10-10 220854_2nd](https://github.com/user-attachments/assets/4c444390-d858-42cf-bdd2-20671320eab9)

