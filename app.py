import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import pickle
import matplotlib.pyplot as plt

# Define multiple mapping dictionaries
# Define multiple mapping dictionaries
Gender_map = {0: 'Men', 1: 'Women'}
Smoking_map = {0: 'None smoker', 1: 'Current smoker'}
Diabetes_map = {0: 'No', 1: 'Yes'}
Antihypertensive_medication_use_map = {0: 'No', 1: 'Yes'}
def map_variable(value, mapping):
    return mapping.get(value, 'Unknown')

st.set_page_config(layout="wide")

@st.cache_data
def load_setting():
    settings = {
        'Age': {'values': [70, 100], 'type': 'slider', 'init_value': 70, 'add_after': ' (year)'},
        'Gender': {'values': ["Men", "Women"], 'type': 'selectbox', 'init_value': 0, 'add_after': ''},
        'Smoking': {'values': ["Non smoker", "Smoker"], 'type': 'selectbox', 'init_value': 0, 'add_after': ''},
        'Diabetes': {'values': ["No", "Yes"], 'type': 'selectbox', 'init_value': 0, 'add_after': ''},
        'Antihypertensive_medication_use': {'values': ["No", "Yes"], 'type': 'selectbox', 'init_value': 0, 'add_after': ''},
        'Non_HDL_Cholesterol': {'values': [0.0, 12.0], 'type': 'slider', 'init_value': 0.0, 'add_after': ' (mmol/L)'},
        'HDL_Cholesterol': {'values': [0.0, 6.0], 'type': 'slider', 'init_value': 0.0, 'add_after': ' (mmol/L)'},
        'Serum creatinine': {'values': [0.0, 20.0], 'type': 'slider', 'init_value': 0.0, 'add_after': ' (mg/dl)'},
        'Systolic blood pressure': {'values': [70, 200], 'type': 'slider', 'init_value': 0, 'add_after': ' (mmHg)'}
    }
    input_keys = list(settings.keys())
    return settings, input_keys

settings, input_keys = load_setting()

@st.cache_resource
def get_model(model_name='DeepSurv_Jo'):
    try:
        # Construct the full path to the model file
        model_path = os.path.join(f"{model_name}.pkl")
        
        # Check if the file exists
        if not os.path.exists(model_path):
            st.error(f"Model file not found: {model_path}")
            return None
        
        # Load the model using joblib
        model = joblib.load(model_path)
        st.success(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None    

def get_code():
    sidebar_code = []
    for key in settings:
        if settings[key]['type'] == 'slider':
            sidebar_code.append(
                "{} = st.slider('{}',{},{},key='{}')".format(
                    key.replace(' ', '____'),
                    key + settings[key]['add_after'],
                    # settings[key]['values'][0],
                    ','.join(['{}'.format(value) for value in settings[key]['values']]),
                    settings[key]['init_value'],
                    key
                )
            )
        if settings[key]['type'] == 'selectbox':
            sidebar_code.append('{} = st.selectbox("{}",({}),{},key="{}")'.format(
                key.replace(' ', '____'),
                key + settings[key]['add_after'],
                ','.join('"{}"'.format(value) for value in settings[key]['values']),
                settings[key]['init_value'],
                key
            )
            )
    return sidebar_code

# print('\n'.join(sidebar_code))
if 'patients' not in st.session_state:
    st.session_state['patients'] = []
if 'How many patients would you like to make predictions for?' not in st.session_state:
    st.session_state['How many patients would you like to make predictions for?'] = 1
if 'model' not in st.session_state:
    st.session_state['model'] = 'DeepSurv_Jo'

deepsurv_model = get_model(st.session_state['model'])

if deepsurv_model is None:
    st.stop()  # Stop execution if the model couldn't be loaded
else:
    st.success("Model loaded and ready for use!")
    # Function to generate sidebar code
def get_code():
    sidebar_code = []
    for key in settings:
        if settings[key]['type'] == 'slider':
            sidebar_code.append(
                "{} = st.slider('{}', {}, {}, key='{}')".format(
                    key.replace(' ', '____'),
                    key + settings[key]['add_after'],
                    settings[key]['values'][0],
                    settings[key]['values'][1],
                    key
                )
            )
        if settings[key]['type'] == 'selectbox':
            sidebar_code.append('{} = st.selectbox("{}", ({}) ,{}, key="{}")'.format(
                key.replace(' ', '____'),
                key + settings[key]['add_after'],
                ','.join(f'"{value}"' for value in settings[key]['values']),
                settings[key]['init_value'],
                key
            ))
    return sidebar_code
sidebar_code = get_code()
def plot_survival():
    pd_data = pd.concat(
        [
            pd.DataFrame(
                {
                    'Survival': item['survival'],
                    'Time': item['times'],
                    'Patients': [f"Patient {item['No']}" for _ in item['times']]
                }
            ) for item in st.session_state['patients']
        ]
    )
    
    if st.session_state['How many patients would you like to make predictions for?']:
        fig = px.line(pd_data, x="Time", y="Survival", color='Patients', range_y=[0, 1])
    else:
        fig = px.line(pd_data.loc[pd_data['Patients'] == pd_data['Patients'].to_list()[-1], :], x="Time", y="Survival",
                      range_y=[0, 1])
    
    fig.update_layout(template='simple_white',
                      title={
                          'text': 'Estimated Survival Probability',
                          'y': 0.9,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top',
                          'font': dict(size=25)
                      },
                      plot_bgcolor="white",
                      xaxis_title="Time (Years)",
                      yaxis_title="Survival probability",
                      )
    
    fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)  # Set ticks every 1 year, starting from 1
    
    st.plotly_chart(fig, use_container_width=True)


def plot_patients():
    patients = pd.concat(
        [
            pd.DataFrame(
                dict(
                    {
                        'Patients': [item['No']],
                        '3-year': ["{:.2f}%".format(item['3-year'] * 100)],
                        '5-year': ["{:.2f}%".format(item['5-year'] * 100)],
                        '10-year': ["{:.2f}%".format(item['10-year'] * 100)]
                    },
                    **item['arg']
                )
            ) for item in st.session_state['patients']
        ]
    ).reset_index(drop=True)
    st.dataframe(patients)

# @st.cache(show_spinner=True)
def predict():
    print('update patients. ##########')
    print(st.session_state)
    input = []
    for key in input_keys:
        value = st.session_state[key]
        if isinstance(value, (int, float)):
            input.append(value)
        if isinstance(value, str):
            input.append(settings[key]['values'].index(value))
    survival = deepsurv_model.predict_survival(np.array(input), t=None)
    max_years = 11.8
    time_points = np.linspace(0, max_years, len(survival.flatten()))
    data = {
        'survival': survival.flatten(),
        'times': time_points.tolist(),
        'No': len(st.session_state['patients']) + 1,
        'arg': {key: st.session_state[key] for key in input_keys},
        '3-year': survival[0, np.argmin(np.abs(time_points - 3))],
        '5-year': survival[0, np.argmin(np.abs(time_points - 5))],
        '10-year': survival[0, np.argmin(np.abs(time_points - 10))]
    }
    st.session_state['patients'].append(
        data
    )
    print('update patients ... ##########')

def plot_below_header():
    col1, col2 = st.columns([1, 9])
    col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2])
    with col1:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        # st.session_state['display'] = ['Single', 'Multiple'].index(
        #     st.radio("Display", ('Single', 'Multiple'), st.session_state['display']))
        st.session_state['How many patients would you like to make predictions for?'] = ['Single patient', 'Multiple patients'].index(
            st.radio("How many patients would you like to make predictions for?", ('Single patient', 'Multiple patients'), st.session_state['How many patients would you like to make predictions for?']))
    with col2:
        plot_survival()
    with col4:
        st.metric(
            label='3-year survival probability',
            value="{:.2f}%".format(st.session_state['patients'][-1]['3-year'] * 100)
        )
    with col5:
        st.metric(
            label='5-year survival probability',
            value="{:.2f}%".format(st.session_state['patients'][-1]['5-year'] * 100)
        )
    with col6:
        st.metric(
            label='10-year survival probability',
            value="{:.2f}%".format(st.session_state['patients'][-1]['10-year'] * 100)
        )
    st.write('')
    st.write('')
    st.write('')
    plot_patients()
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')

st.header('Predicting risk of ASCVD among relatively healthy community-dwelling older adults', anchor='Risk of ASCVD')
if st.session_state['patients']:
    plot_below_header()
st.subheader("Instructions:")
st.write("1. Fill Patients' information in the calculator\n2. Click the predict button\n3. Click the Predict button-->the page showing 3 year, 5 year, and 10 year survival probabilities should be displayed now")
st.write('***Note: this model is not validated, the accuracy of the model cannot be guaranteed!***')
st.write("***The analysis is to purely boost the quality of diagnosis and is not meant as a substitute to professional diagnosis***")

st.write( '******Thank you******')
with st.sidebar:
    with st.form("my_form",clear_on_submit = False):
        for code in sidebar_code:
            exec(code)
        col8, col9, col10 = st.columns([3, 4, 3])
        with col9:
            prediction = st.form_submit_button(
                'Predict',
                on_click=predict,
                # args=[{key: eval(key.replace(' ', '____')) for key in input_keys}]
            )
