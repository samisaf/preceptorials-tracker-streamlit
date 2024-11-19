import pandas as pd
from io import StringIO
import streamlit as st

students_locations = """
name,latitude,longitude
University of Maryland,39.287557,-76.623834      
Washington Hospital Center,38.9287492,-77.014769282973
University of Virginia,38.0410576,-78.505508412148
Johns Hopkins University,39.33020225,-76.621853578583
Penn State University,40.8025835,-77.855938331846
University of Pittsburgh,40.44415295,-79.962460951445
University of Alabama at Birmingham,33.5016153,-86.806047560765
University of California San Francisco,37.7627257,-122.45825681806
Jordan Ministry of Health,31.9554289,35.9260816      
Kijabe Hospital,-1.2667439,36.7964808      
University of Southern California,34.02186895,-118.28585792313
Mayo Clinic Rochester,44.0225389,-92.466607460917
National Institutes of Health,39.00001425,-77.104003945236
Christiana Care,39.4550864,-75.683144325081
Georgetown University,38.90893925,-77.074579620608
University of Minnesota,44.9863392,-93.179455802185
Yale University,41.25713055,-72.989669601522
Emory University,33.80045465,-84.317237804663
University of Washington,47.6554303,-122.30016924821
New York University,40.7292053,-73.99501481291 
Case Western Reserve,41.50138695,-81.600702166005
University of Michigan,42.2942142,-83.710038935096
Allegheny General Hospital,40.45697185,-80.003306882476
Akron Children's Hospital,41.0792309,-81.525795801765
"""

@st.cache_data
def get_student_locations():
    df = pd.read_csv(StringIO(students_locations))
    return df.to_dict(orient='records')
