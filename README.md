# 🧵 Stitching Unit Defect Prediction

This project develops a machine learning pipeline to predict garment defects per shift in a textile manufacturing setting. By integrating and engineering features from production schedules, machine assignments, quality records, and employee data, the model aims to proactively identify high-risk shifts, enabling targeted interventions to maintain high-quality standards.

## 📊 Data Sources

- **Production Schedule Data**: Details of each shift, including garment type, target units, and assigned employees.
- **Machine Assignment Data**: Information on each machine's make, model, and assignment status per shift.
- **Quality Data**: Recorded defect counts for each shift.
- **Employee Data**: Employee demographics, experience, education, and training status.

## 🛠️ Project Workflow

1. **Data Preprocessing**: Standardized formats and handled missing values across datasets.
2. **Data Integration**: Merged datasets on common fields (date and shift) to create a comprehensive dataset.
3. **Feature Engineering**: Generated shift-level features such as average employee experience, training level distribution, and machine make/model frequencies.
4. **Model Training**: Trained a supervised learning model to predict defects per shift.

## 📈 Outcome

The predictive model identifies shifts with a higher likelihood of defects, allowing the company to make proactive adjustments in staffing, machine usage, or training to minimize defects.

## 🧰 Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook

## 📁 Repository Structure

- `pro.py`: Main Python script containing the data processing and modeling pipeline.
- `Employees.csv`, `Machines.csv`, `Production Schedule.csv`, `Quality.csv`: Raw datasets.
- `merged_data_*.csv`: Intermediate datasets after merging and preprocessing.
- `machine_counts.csv`, `marge_pq_mac_counts.csv`: Feature-engineered datasets.
- `T1.docx`: Project documentation.

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/DevMoazAI/Revise_First_ML_Project.git
