# refer to https://github.com/samisaf/preceptorials-tracker-directus/blob/main/data_wrangle/calculate_average_score.ipynb

queries_calculate_averages = """
ALTER TABLE a ADD COLUMN a_average REAL;


UPDATE a SET a_average = (COALESCE(OhmsLaw, 0) + COALESCE(EquationOfMotion, 0) + COALESCE(Resistance, 0) + COALESCE(Compliance, 0) + COALESCE(NormalPressureControlWaveforms, 0) + COALESCE(PalvTimeCurve, 0) + COALESCE(Waveforms_with_changing_R_C_and_IT, 0) + COALESCE(InspiratoryTimeConstant, 0) + COALESCE(Effect_of_Flow_Asynchrony_on_Pressure_Breaths, 0) + COALESCE(Chapter_A_Cases, 0) + COALESCE(Plateau_Pressure, 0) + COALESCE(PVLoops_in_Pressure_Breaths, 0)) / 12;


ALTER TABLE b ADD COLUMN b_average REAL;


UPDATE b SET b_average = (COALESCE(Measuring_Resistance_and_Compliance, 0) + COALESCE(Inspiratory_Time_Constant, 0) + COALESCE(PV_Loops_in_Volume_Breaths, 0) + COALESCE(Chapter_B_Cases, 0) + COALESCE(Waveforms_with_changing_R_C_and_IT, 0) + COALESCE(Effect_of_Flow_Asynchrony_on_Volume_Breaths, 0) + COALESCE(Inflection_Points_and_Stress_Index, 0) + COALESCE(PEEP_versus_Ppl_Curve, 0)) / 8;


ALTER TABLE c ADD COLUMN c_average REAL;


UPDATE c SET c_average = (COALESCE(Paw_and_Palv_Time_Curves_in_Expiration, 0) + COALESCE(Flow_and_Volume_Time_Curves_in_Expiration, 0) + COALESCE(Adverse_Effects_of_AutoPEEP, 0) + COALESCE(Signs_of_AutoPEEP, 0) + COALESCE(Chapter_C_Cases, 0) + COALESCE(Natural_Decay_Equation, 0) + COALESCE(Expiratory_Time_Constant, 0) + COALESCE(Waveforms_with_changing_R_C_and_IT, 0) + COALESCE(Effect_of_Cycling_Asynchrony_During_Expiration, 0)) / 9;


ALTER TABLE d ADD COLUMN d_average REAL;


UPDATE d SET d_average = (COALESCE(Waveforms_with_Changing_R_C, 0) + COALESCE(Waveforms_with_Patient_Effort, 0) + COALESCE(Effect_of_Changing_IT_for_Pressure_and_Volume_Cycled_Breaths, 0) + COALESCE(Chapter_D_Cases, 0) + COALESCE(Effect_of_AutoPEEP_on_PV_Cruve_in_P_and_V_Breaths, 0) + COALESCE(Physiologic_Determinants_of_PCO2, 0)) / 6;


ALTER TABLE e ADD COLUMN e_average REAL;


UPDATE e SET e_average = (COALESCE(Triggering_Sensitivity, 0) + COALESCE(Ineffective_Triggering, 0) + COALESCE(Auto_Triggering, 0)) / 3;


ALTER TABLE f ADD COLUMN f_average REAL;


UPDATE f SET f_average = (COALESCE(Chapter_F_Cases, 0) + COALESCE(Termination_of_Inspiration_for_Various_Breath_Types, 0) + COALESCE(Premature_Cycling, 0) + COALESCE(Delayed_Cycling, 0)) / 4;


ALTER TABLE g ADD COLUMN g_average REAL;


UPDATE g SET g_average = (COALESCE(Work_of_Breathing_and_the_Campbell_Diagram, 0) + COALESCE(Diaphragmatic_Atrophy_and_Fatigue, 0) + COALESCE(Ventilator_Induced_Diaphragmatic_Dysfunction, 0) + COALESCE(Chapter_G_Cases, 0)) / 4;


ALTER TABLE h ADD COLUMN h_average REAL;


UPDATE h SET h_average = (COALESCE(Patient_Work_of_Breathing_During_AC_SIMV_and_PS, 0) + COALESCE(Estimating_Pmus, 0) + COALESCE(Physiology_of_Proportional_Assist_Ventilation, 0) + COALESCE(Neurally_Adjusted_Ventilatory_Assistance, 0)) / 4;
""".split('\n')

query_create_join_learners = """
CREATE TABLE IF NOT EXISTS learners AS

WITH
    a_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_a,
            date_created AS date_created_a,
            a_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                a_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY a_average DESC) AS rnk
            FROM a
        ) AS ranked
        WHERE rnk = 1
    ),b_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_b,
            date_created AS date_created_b,
            b_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                b_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY b_average DESC) AS rnk
            FROM b
        ) AS ranked
        WHERE rnk = 1
    ),c_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_c,
            date_created AS date_created_c,
            c_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                c_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY c_average DESC) AS rnk
            FROM c
        ) AS ranked
        WHERE rnk = 1
    ),d_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_d,
            date_created AS date_created_d,
            d_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                d_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY d_average DESC) AS rnk
            FROM d
        ) AS ranked
        WHERE rnk = 1
    ),e_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_e,
            date_created AS date_created_e,
            e_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                e_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY e_average DESC) AS rnk
            FROM e
        ) AS ranked
        WHERE rnk = 1
    ),f_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_f,
            date_created AS date_created_f,
            f_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                f_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY f_average DESC) AS rnk
            FROM f
        ) AS ranked
        WHERE rnk = 1
    ),g_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_g,
            date_created AS date_created_g,
            g_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                g_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY g_average DESC) AS rnk
            FROM g
        ) AS ranked
        WHERE rnk = 1
    ),h_aggregated AS (
        SELECT 
            student,
            user_created AS user_created_h,
            date_created AS date_created_h,
            h_average
        FROM (
            SELECT 
                student, 
                user_created, 
                date_created, 
                h_average,
                ROW_NUMBER() OVER (PARTITION BY student ORDER BY h_average DESC) AS rnk
            FROM h
        ) AS ranked
        WHERE rnk = 1
    )
SELECT 
    s.id AS student_id, s.email, s.first_name, s.last_name, 
    s.institution, s.specialty,
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
    LEFT JOIN h_aggregated AS h ON s.id = h.student;
"""

# this query is not accurate as it doesn't adjust the denominator 
queries_insert_total_score = """
ALTER TABLE learners ADD COLUMN total_score REAL

UPDATE learners SET total_score = ( COALESCE(a_average, 0) + COALESCE(b_average, 0) + COALESCE(c_average, 0) + COALESCE(d_average, 0) + COALESCE(e_average, 0) + COALESCE(f_average, 0) + COALESCE(g_average, 0) + COALESCE(h_average, 0)) / 8.0
""".split('\n')