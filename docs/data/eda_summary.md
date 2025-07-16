# EDA Summary

## Data Shape
Rows: 32593, Columns: 15

## Numeric Columns
['id_student', 'num_of_prev_attempts', 'studied_credits', 'date_registration', 'date_unregistration', 'module_presentation_length']

## Categorical Columns
['gender', 'final_result', 'age_band', 'highest_education', 'region', 'disability']

## Outlier Report
- id_student: 6460 outliers (19.82%), bounds=(304753.00, 848273.00)
- num_of_prev_attempts: 4172 outliers (12.80%), bounds=(0.00, 0.00)
- studied_credits: 350 outliers (1.07%), bounds=(-30.00, 210.00)
- date_registration: 339 outliers (1.04%), bounds=(-206.50, 77.50)
- date_unregistration: 41 outliers (0.13%), bounds=(-168.50, 275.50)
- module_presentation_length: 0 outliers (0.00%), bounds=(200.50, 308.50)

## Plots
- ![Distribution of gender](eda_plots/gender_countplot.png)
- ![Distribution of final_result](eda_plots/final_result_countplot.png)
- ![Distribution of age_band](eda_plots/age_band_countplot.png)
- ![Distribution of highest_education](eda_plots/highest_education_countplot.png)
- ![Distribution of region](eda_plots/region_countplot.png)
- ![Distribution of disability](eda_plots/disability_countplot.png)
- ![Distribution of id_student](eda_plots/id_student_hist.png)
- ![Distribution of num_of_prev_attempts](eda_plots/num_of_prev_attempts_hist.png)
- ![Distribution of studied_credits](eda_plots/studied_credits_hist.png)
- ![Distribution of date_registration](eda_plots/date_registration_hist.png)
- ![Distribution of date_unregistration](eda_plots/date_unregistration_hist.png)
- ![Distribution of module_presentation_length](eda_plots/module_presentation_length_hist.png)
- ![Correlation Heatmap](eda_plots/correlation_heatmap.png)
