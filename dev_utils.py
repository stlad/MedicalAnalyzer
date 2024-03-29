from FunctionalModules.DB_Module.db_module import *


# пациент [ID, имя, фамилия, отчество, дата рождения, диаг, диаг2, гены, пол, возраст]
# анализ [ID, ID_пациента, дата]
# каталог [ID, название, ед, от, до]
# параметр [ID, ID_по_каталогу, значение, ID_анализа, отклонение]


def all_patients_to_sql(filename):
    patients = MainDBController.GetAllPatients()
    ressql = "insert into patients(patient_id,surname, name,patronymic,birthday,main_diagnosis,concomitant_diagnosis,genes, gender)\nvalues\n"

    lines = []
    for pat in patients:
        lines.append(f"({pat[0]}, '{pat[2]}','{pat[1]}','{pat[3]}','{pat[4]}','{pat[5]}','{pat[6]}','{pat[7]}','{pat[8]}')")
    lines =ressql +  ',\n'.join(lines)
    with open(filename, 'w') as file:
        file.write(lines)



def all_analysis_to_sql(filename):
    con = MainDBController._create_connection_to_DB()
    with con.cursor() as cur:
        sql = f"select * from analysis"
        cur.execute(sql)
        rows = cur.fetchall()
    ressql = "insert into Analysis(analysis_id, owner_id,analysis_date)\nvalues\n"
    lines = []
    for anal in rows:
        lines.append(f"({anal[0]}, {anal[1]}, '{str(anal[2])}')")
    lines = ressql + ',\n'.join(lines)
    with open(filename, 'w') as file:
        file.write(lines)

def all_parameters_to_sql(filename):
    con = MainDBController._create_connection_to_DB()
    with con.cursor() as cur:
        sql = f"select * from parameter_results"
        cur.execute(sql)
        rows = cur.fetchall()
    ressql = "insert into parameter_results(result_id, analysis_id, parameter_id, value, deviation)\nvalues\n"
    lines = []
    for res in rows:
        lines.append(f"({res[0]}, {res[3]},{res[1]}, {res[2]}, '{res[4]}')")
    lines = ressql + ',\n'.join(lines)
    with open(filename, 'w') as file:
        file.write(lines)






#dump_all_patients_to_json()

#dump_patient_to_json([5])
#load_data_from_json()



#all_patients_to_sql("patients_backup.sql")
#all_analysis_to_sql("analysis_backup.sql")
#all_parameters_to_sql("parameter_res_backup.sql")