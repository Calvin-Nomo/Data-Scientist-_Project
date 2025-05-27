#python -m streamlit run disease_app.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
st.title("Disease  prediction App")
diabetes=joblib.load('model/Diabetes_result.pkl')
heart_disease=joblib.load('model/Heart_disease_Prediction.pkl')
fever=joblib.load('model/fever_disease_Prediction.pkl')
# Ask the user to choose a method
tab1,tab2,tab3,tab4=st.tabs(['Diabetes_prediction','Heart_disease Prediction','alzheimers_disease','Fever_disease'])
with tab1:
    method = st.radio("Choose input method:", ["Load Dataset", "Fill Parameters"],key='display_choice')
    if method == "Load Dataset":
        fichier = st.file_uploader("Upload your CSV file", type=["csv"])
        
        if fichier:
            data_set=pd.read_csv(fichier,usecols=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age'])
            st.success("Dataset loaded successfully!")
            st.dataframe(data_set)
            if st.button('Predict'):
                st.write('**********Prediction**********')
                label={0:'Not_Diabetic',1:'Diabetic'}
                st.write(label)
                input_data=data_set
                prediction=diabetes.predict(input_data)
                data_set['Predictions']=prediction
                st.dataframe(data_set)
                # Optionally download the result
                csv = data_set.to_csv(index=False).encode('utf-8')
                st.download_button("Download Results CSV", csv, " diabetes_predictions.csv", "text/csv",key='download_key')
        else:
            st.info("Please upload a CSV file.")

    elif method == "Fill Parameters":
        with st.form(key='User_info_form'):
            st.subheader("Enter Your Health Parameters")
            pregnancies= st.number_input('What is thre total number of pregnancies',min_value=1,max_value=18)
            Glucose=st.number_input('What is your Glucose Level')
            BloodPressure=st.number_input('What is your BloodPressure')
            SkinThickness=st.number_input('What is your SkinThickness')
            Insulin=st.number_input('What is your Insulin Level')
            BMI=st.number_input('What is your BMI')
            DiabetesPedigreeFunction=st.number_input('What is your DiabetesPedigreeFunction Level')
            Age=st.number_input('What is Your Age',max_value=80,min_value=1)
            submit_button=st.form_submit_button(label='Prediction')
            if submit_button:
                data=np.array([pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]).reshape(1,-1)
                prediction=diabetes.predict(data)
                if prediction==0:
                    st.success("You don't have diabetes")
                elif prediction==1:
                    st.write(" You have diabetes")
with tab2:

    # Input method selection
    meth = st.radio("Choose input method:", ["Load Dataset", "Fill Parameters"],key="input_method_radio")

    # ----------------- LOAD DATASET --------------------
    if meth == "Load Dataset":
        st.subheader("Upload Your Dataset")
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"] )
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df=df.drop(columns=['Family Heart Disease','High Blood Pressure','Heart Disease Status'],axis=1)
            df=df.dropna()
            st.write("Raw uploaded data:")
            
            st.dataframe(df)

            # Encode all categorical columns with LabelEncoder
            cat_cols = df.select_dtypes(include='object').columns
            encoders = {}

            for col in cat_cols:
                encoder = LabelEncoder()
                df[col] = encoder.fit_transform(df[col])
                encoders[col] = encoder  # Store if needed later

            st.success("Categorical columns encoded successfully!")

            # Make predictions
            predictions = heart_disease.predict(df)
            df["Prediction"] = predictions

            # Show results
            st.subheader("Prediction Results")
            st.dataframe(df)

            # Optionally download the result
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Results CSV", csv,"heart disease_predictions.csv", "text/csv")
        else:
                  st.info("Please upload a CSV file.")

    # ----------------- FILL PARAMETERS --------------------
    elif meth == "Fill Parameters":
        
        st.subheader("Enter Your Health Parameters")
        with st.form("prediction_form"):
            Age = st.number_input('What is your Age', min_value=1, max_value=120)
            gender = st.selectbox("What's your gender", ['Choose an option','Male', 'Female'])
            BloodPressure = st.number_input('What is your Blood Pressure')
            Cholesterol_Level = st.number_input("What's your Cholesterol Level")
            Exercise_Habits = st.selectbox("What's your exercise habits level", ['Choose an option','High', 'Meduim', 'Low'])
            smoking = st.selectbox('Do you smoke ?', ['Choose an option','Yes', 'No'])
            diabetes = st.selectbox('Are you suffering from diabetes?', ['Choose an option','Yes', 'No'])
            BMI = st.number_input("What's your BMI Level")
            Low_HDL_Cholesterol = st.selectbox("Do you have Low HDL Cholesterol level?", ['Choose an option','Yes', 'No'])
            High_LDL_Cholesterol = st.selectbox("Do you have High LDL Cholesterol level?", ['Choose an option','Yes', 'No'])
            Alcohol_Consumption = st.selectbox("What's your Alcohol Consumption Level?", ['Choose an option','High', 'Medium', 'Low'])
            stress_level = st.selectbox("What's your stress level?", ['Choose an option','High', 'Medium', 'Low'])
            sleep_hour = st.slider("What's the number of hours you sleep?", 1, 8, 1)
            sugar_Consumption = st.selectbox("What's your sugar Consumption Level?", ['Choose an option','High', 'Medium', 'Low'])
            Triglyceride_Level = st.number_input("What's your Triglyceride Level?")
            Fasting_Blood_Sugar = st.number_input("What's your Fasting Blood Sugar?")
            CRP_Level = st.number_input("What's your CRP Level?")
            Homocysteine_Level = st.number_input("What's your Homocysteine Level?")
            
            submit_button = st.form_submit_button(label='Prediction')

        if submit_button:
            # Prepare data as a single-row DataFrame
            data = pd.DataFrame({
                'Age': [Age],
                'Gender': [gender],
                'BloodPressure': [BloodPressure],
                'Cholesterol_Level': [Cholesterol_Level],
                'Exercise_Habits': [Exercise_Habits],
                'Smoking': [smoking],
                'Diabetes': [diabetes],
                'BMI': [BMI],
                'Low_HDL_Cholesterol': [Low_HDL_Cholesterol],
                'High_LDL_Cholesterol': [High_LDL_Cholesterol],
                'Alcohol_Consumption': [Alcohol_Consumption],
                'Stress_Level': [stress_level],
                'Sleep_Hour': [sleep_hour],
                'Sugar_Consumption': [sugar_Consumption],
                'Triglyceride_Level': [Triglyceride_Level],
                'Fasting_Blood_Sugar': [Fasting_Blood_Sugar],
                'CRP_Level': [CRP_Level],
                'Homocysteine_Level': [Homocysteine_Level]
            })

            # Encode categorical columns using LabelEncoder
            cat_columns = [
                'Gender', 'Exercise_Habits', 'Smoking', 'Diabetes', 'Low_HDL_Cholesterol',
                'High_LDL_Cholesterol', 'Alcohol_Consumption', 'Stress_Level', 'Sugar_Consumption'
            ]

            for col in cat_columns:
                encoder = LabelEncoder()
                data[col] = encoder.fit_transform(data[col])

            # Convert DataFrame to numpy array
            input_data = data.values

            # Use your trained model to predict
            prediction = heart_disease.predict(input_data)
            if prediction[0] == 0:
                st.success("You don't have heart disease.")
            else:
                st.warning("You may have heart disease.")
with tab3:
    st.write('Pass')
with tab4:
    # Input method selection
    example = st.radio("Choose input method:", ["Load Dataset", "Fill Parameters"],key="fever_input")

    # ----------------- LOAD DATASET --------------------
    if example == "Load Dataset":
        st.subheader("Upload Your Dataset")
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"],key='Load_fever_dataset' )
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df=df.drop(columns=['Previous_Medication','Recommended_Medication','Fever_Severity'],axis=1)
            df=df.dropna()
            st.write("Raw uploaded data:")
            
            st.dataframe(df)

            # Encode all categorical columns with LabelEncoder
            cat_cols = df.select_dtypes(include='object').columns
            encoders = {}

            for col in cat_cols:
                encoder = LabelEncoder()
                df[col] = encoder.fit_transform(df[col])
                encoders[col] = encoder  # Store if needed later

            st.success("Categorical columns encoded successfully!")

            # Make predictions
            predictions = fever.predict(df)
            df["Prediction"] = predictions

            # Show results
            st.subheader("Prediction Results")
            st.dataframe(df)

            # Optionally download the result
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Results CSV", csv,"heart disease_predictions.csv", "text/csv",key='result')
        else:
                  st.info("Please upload a CSV file.")

    # ----------------- FILL PARAMETERS --------------------
    elif example == "Fill Parameters":
        
        st.subheader("Enter Your Health Parameters")
        with st.form("prediction_form"):
            Temp = st.number_input("What's your Temperature in Celsuis")
            Age = st.number_input('What is your Age ?', min_value=1, max_value=120)
            gender = st.selectbox("What's your gender ?", ['Choose an option','Male', 'Female'])
            BMI = st.number_input("What's your BMI ")
            Head_ache= st.selectbox("Do you have Headache ?", ['Choose an option','Yes', 'No'])
            Body_ache = st.selectbox("Do you have Bodyache ?", ['Choose an option','Yes', 'No'])
            fatigue = st.selectbox("Do you Feel fatigue ?", ['Choose an option','Yes', 'No',])
            chronic_Condition = st.selectbox("Do you have chronic_Condition ?", ['Choose an option','Yes', 'No'])
            Allergies = st.selectbox('Do you have Allergies ?', ['Choose an option','Yes', 'No'])
            smoking = st.selectbox('Do you smoke ?', ['Choose an option','Yes', 'No'])
            Alcohol_Consumption = st.selectbox("What's your Alcohol Consumption Level?", ['Choose an option','Yes', 'No'])
            humidity = st.number_input("What's the humidity Level ?")
            AQI_Level = st.number_input("What's your AQI Level ?")
            physical_activity= st.selectbox(" Do your practice physical_activity ?", ['Choose an option','Active', 'Moderate', 'Sendetary'])
            Diet_type = st.selectbox("What's your Diet type ?", ['Choose an option','Vegan', 'Vegitarian', 'Non-Vegiterian'])
            Heart_rate = st.number_input("What's your Heart-Rate ?")
            Blood_pressure = st.selectbox("What's your Blood_pressure  Level ?", ['Choose an option','High', 'Normal', 'Low'])
            
            submit_button = st.form_submit_button(label='Prediction')

        if submit_button:
            # Prepare data as a single-row DataFrame
            data_values = pd.DataFrame({
                'Temperature': [Temp],
                'Age':[Age],
                'Gender': [gender],
                'BMI': [BMI],
                'Headache': [Head_ache],
                'Body_Ache': [Body_ache],
                'Fatigue': [fatigue],
                'Chronic_Conditions':[chronic_Condition],
                'Allergies': [Allergies],
                'Smoking': [smoking],
                'Alcohol_Consumption': [Alcohol_Consumption],
                'humidity': [humidity],
                'AQI_Level': [AQI_Level],
                'Heart-Rate': [Heart_rate],
                'Physical_Activity': [physical_activity],
                'Diet_Type': [Diet_type],
                'Blood-Pressure': [Blood_pressure]
                
                
            })
            st.success('The Health Parameters loaded successfully')
            #display me dataframe
            st.dataframe(data_values)
            # Encode categorical columns using LabelEncoder
            cat_columns = [
                'Headache', 'Chronic_Conditions', 'Smoking', 'Alcohol_Consumption', 'Physical_Activity',
                'Blood-Pressure', 'Diet_Type', 'Body_Ache', 'Fatigue','Allergies','Gender'
            ]
            for col in cat_columns:
                encoder = LabelEncoder()
                data_values[col] = encoder.fit_transform(data_values[col])

            # Convert DataFrame to numpy array
            input_data = data_values.values
            
            st.status('Predicted Result')
            # Use your trained model to predict
            prediction = fever.predict(input_data)
            if prediction[0] == 0:
                st.warning("You  have High Fever.")
            elif prediction[0] == 1:
                st.warning("You have Mild Fever")
            else:
                st.success(" Your don't have Fever")