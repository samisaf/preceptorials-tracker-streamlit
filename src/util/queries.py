# refer to https://github.com/samisaf/preceptorials-tracker-directus/blob/main/data_wrangle/calculate_average_score.ipynb

queries_calculate_averages = """ALTER TABLE a ADD COLUMN a_average REAL;


UPDATE a SET a_average = (OhmsLaw + EquationOfMotion + Resistance + Compliance + NormalPressureControlWaveforms + PalvTimeCurve + Waveforms_with_changing_R_C_and_IT + InspiratoryTimeConstant + Effect_of_Flow_Asynchrony_on_Pressure_Breaths + Chapter_A_Cases + Plateau_Pressure + PVLoops_in_Pressure_Breaths) / 12;


ALTER TABLE b ADD COLUMN b_average REAL;


UPDATE b SET b_average = (Measuring_Resistance_and_Compliance + Inspiratory_Time_Constant + PV_Loops_in_Volume_Breaths + Chapter_B_Cases + Waveforms_with_changing_R_C_and_IT + Effect_of_Flow_Asynchrony_on_Volume_Breaths + Inflection_Points_and_Stress_Index + PEEP_versus_Ppl_Curve) / 8;


ALTER TABLE c ADD COLUMN c_average REAL;


UPDATE c SET c_average = (Paw_and_Palv_Time_Curves_in_Expiration + Flow_and_Volume_Time_Curves_in_Expiration + Adverse_Effects_of_AutoPEEP + Signs_of_AutoPEEP + Chapter_C_Cases + Natural_Decay_Equation + Expiratory_Time_Constant + Waveforms_with_changing_R_C_and_IT + Effect_of_Cycling_Asynchrony_During_Expiration) / 9;


ALTER TABLE d ADD COLUMN d_average REAL;


UPDATE d SET d_average = (Waveforms_with_Changing_R_C + Waveforms_with_Patient_Effort + Effect_of_Changing_IT_for_Pressure_and_Volume_Cycled_Breaths + Chapter_D_Cases + Effect_of_AutoPEEP_on_PV_Cruve_in_P_and_V_Breaths + Physiologic_Determinants_of_PCO2) / 6;


ALTER TABLE e ADD COLUMN e_average REAL;


UPDATE e SET e_average = (Triggering_Sensitivity + Ineffective_Triggering + Auto_Triggering) / 3;


ALTER TABLE f ADD COLUMN f_average REAL;


UPDATE f SET f_average = (Chapter_F_Cases + Termination_of_Inspiration_for_Various_Breath_Types + Premature_Cycling + Delayed_Cycling) / 4;


ALTER TABLE g ADD COLUMN g_average REAL;


UPDATE g SET g_average = (Work_of_Breathing_and_the_Campbell_Diagram + Diaphragmatic_Atrophy_and_Fatigue + Ventilator_Induced_Diaphragmatic_Dysfunction + Chapter_G_Cases) / 4;


ALTER TABLE h ADD COLUMN h_average REAL;


UPDATE h SET h_average = (Patient_Work_of_Breathing_During_AC_SIMV_and_PS + Estimating_Pmus + Physiology_of_Proportional_Assist_Ventilation + Neurally_Adjusted_Ventilatory_Assistance) / 4;""".split('\n')

query_create_join_learners = """
CREATE TABLE IF NOT EXISTS learners AS

WITH
    
a_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_a, 
        MAX(date_created) AS date_created_a,
        MAX(a_average) AS a_average
    FROM a
    GROUP BY student
),
    
b_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_b, 
        MAX(date_created) AS date_created_b,
        MAX(b_average) AS b_average
    FROM b
    GROUP BY student
),
    
c_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_c, 
        MAX(date_created) AS date_created_c,
        MAX(c_average) AS c_average
    FROM c
    GROUP BY student
),
    
d_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_d, 
        MAX(date_created) AS date_created_d,
        MAX(d_average) AS d_average
    FROM d
    GROUP BY student
),
    
e_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_e, 
        MAX(date_created) AS date_created_e,
        MAX(e_average) AS e_average
    FROM e
    GROUP BY student
),
    
f_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_f, 
        MAX(date_created) AS date_created_f,
        MAX(f_average) AS f_average
    FROM f
    GROUP BY student
),
    
g_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_g, 
        MAX(date_created) AS date_created_g,
        MAX(g_average) AS g_average
    FROM g
    GROUP BY student
),
    
h_aggregated AS (
    SELECT 
        student,
        MAX(user_created) AS user_created_h, 
        MAX(date_created) AS date_created_h,
        MAX(h_average) AS h_average
    FROM h
    GROUP BY student
)
SELECT 
    s.id AS student_id, s.email, s.first_name, s.last_name, 
    s.institution, s.specialty, s.status,
    CAST(s.year AS INTEGER) AS year, -- Ensure year is an integer
    a.user_created_a, a.date_created_a, a.a_average,
    b.user_created_b, b.date_created_b, b.b_average,
    c.user_created_c, c.date_created_c, c.c_average,
    d.user_created_d, d.date_created_d, d.d_average,
    e.user_created_e, e.date_created_e, e.e_average,
    f.user_created_f, f.date_created_f, f.f_average,
    g.user_created_g, g.date_created_g, g.g_average,
    h.user_created_h, h.date_created_h, h.h_average
FROM 
    students AS s
LEFT JOIN a_aggregated AS a ON s.id = a.student
LEFT JOIN b_aggregated AS b ON s.id = b.student
LEFT JOIN c_aggregated AS c ON s.id = c.student
LEFT JOIN d_aggregated AS d ON s.id = d.student
LEFT JOIN e_aggregated AS e ON s.id = e.student
LEFT JOIN f_aggregated AS f ON s.id = f.student
LEFT JOIN g_aggregated AS g ON s.id = g.student
LEFT JOIN h_aggregated AS h ON s.id = h.student;"""

# this query is not accurate as it doesn't adjust the denominator 
queries_insert_total_score = """
ALTER TABLE learners ADD COLUMN total_score REAL

UPDATE learners SET total_score = ( COALESCE(a_average, 0) + COALESCE(b_average, 0) + COALESCE(c_average, 0) + COALESCE(d_average, 0) + COALESCE(e_average, 0) + COALESCE(f_average, 0) + COALESCE(g_average, 0) + COALESCE(h_average, 0)) / 8.0
""".split('\n')