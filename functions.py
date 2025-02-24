
import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
import re
    #from google.cloud import storage
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import requests

import time  
import webbrowser
import stripe

import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account


def popup_message(message):

    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        ">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_options():
    check_list=['money','car']
    # Display form for name, address, and number input
    quantities={}
    for sub_option in check_list:
            quantity_su = st.number_input(f'Quantity for {sub_option}:', min_value=0, value=0, step=1)
            if quantity_su > 0:
                    quantities[f'{sub_option}'] = quantity_su
    
    return quantities

def data_overview(data, title):
    overview_analysis = {f'{title}':[data.shape[1], data.shape[0], 
                                     data.isnull().any(axis=1).sum(), 
                                     data.isnull().any(axis=1).sum()/len(data)*100,
                                     data.duplicated().sum(),
                                    data.duplicated().sum()/len(data)*100, 
                                     sum((data.dtypes == 'object') & (data.nunique() > 2)),
                                     sum((data.dtypes == 'object') & (data.nunique() < 3)),
                                     data.select_dtypes(include=['int64', 'float64']).shape[1]
                                    ]}
    overview_analysis=pd.DataFrame(overview_analysis, index=['Columns','Rows','Missing_Values','Missing_Values %',
                                                             'Duplicates', 'Duplicates %','Categorical_variables','Boolean_variables','Numerical_variables']).round(2)
    return overview_analysis

def has_digits(row):
    return any(char.isdigit() for char in str(row))


def variables_overview(data):
    variable_details = {
        'unique': data.nunique(),
        'dtype': data.dtypes,
        'null': data.isna().sum(),
        'null %': data.isna().sum() / len(data) * 100,
    }
    variable_details = pd.DataFrame(variable_details)


    # Add a new column 'has_non_alphanumeric' to indicate if there are non-alphanumeric characters
    
    variable_details['has_non_alphanumeric'] = data.apply(lambda col: any(col.apply(lambda x: not str(x).replace(" ", "").isalnum())))
    #variable_details['has_non_alphanumeric'] = data.apply(lambda col: any(col.apply(lambda x: not str(x).isalnum())))

    # Add a new column 'has_digits' to indicate if there are rows containing digits in each column
    variable_details['has_digits'] = data.apply(lambda col: any(col.apply(has_digits)))

    
    return variable_details




def display_options2():
    check_list=['money','car']
    # Display form for name, address, and number input
    quantities={}
    for sub_option in check_list:
            quantity_su = st.number_input(f'Quantity for {sub_option}:', min_value=0, value=0, step=1)
            if quantity_su > 0:
                    quantities[f'{sub_option}'] = quantity_su
    
    return quantities
