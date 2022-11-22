from DB_Module.db_module import *
import json
import psycopg2

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

def execute_sql(filename):
    with open(filename) as f:
        sql = f.read()

    con = MainDBController._create_connection_to_DB()
    with con.cursor() as cur:
        cur.execute(sql)
        con.commit()


def patient_to_dct(id:int):
    '''Функция готовит запись о пациенте к формату для передачи'''
    res = {}
    res['DATA'] = list(MainDBController.GetPatientByID(id)[0][1:-1])    #пациент без ИД и возраста
    res['DATA'][3] = str(res['DATA'][3])                                #date перевести в строку
    analysis = MainDBController.GetAllAnalysisByPatientID(id)
    res['ANALYSIS'] = {}
    for anal in analysis:
        anal_params = MainDBController.GetAllParametersByAnalysisID(anal[0])
        res['ANALYSIS'][str(anal[2])] = [[param[1], param[2], param[4]] for param in anal_params]

    return res

def dump_patient_to_json(patients_ids: list, filename='db.json'):
    data = []
    for id in patients_ids:
        data.append(patient_to_dct(id))

    json_data =  json.dumps(data, indent=4)
    with open (filename, 'w', encoding='utf-8') as file:
        file.write(json_data)


def load_data_from_json(filename='db.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        data =  json.loads(file.read())
    con = MainDBController._create_connection_to_DB()
    for patient in data:
        patient_info = patient['DATA']
        with con.cursor() as cur:
            sql=' '.join([f"insert into patients(surname, name,patronymic,birthday,main_diagnosis,concomitant_diagnosis,genes, gender)",
                f"values('{patient_info[1]}','{patient_info[0]}','{patient_info[2]}','{patient_info[3]}', '{patient_info[4]}', '{patient_info[5]}', '{patient_info[6]}', '{patient_info[7]}')",
                f"returning patient_id"])
            cur.execute(sql)
            patient_id = cur.fetchone()[0]
            con.commit()

        for anal_date in patient['ANALYSIS']:
            with con.cursor() as cur:
                sql = ' '.join([f"insert into Analysis(owner_id,analysis_date)",
                            f"values({patient_id},'{anal_date}')",
                            f"returning analysis_id"])
                cur.execute(sql)
                analysis_id = cur.fetchone()[0]
                con.commit()
            MainDBController.InsertListOfParametersByAnalysisId(analysis_id, patient['ANALYSIS'][anal_date])


def dump_all_patients_to_json():
    patients = MainDBController.GetAllPatients()
    patients_ids = [patient[0] for patient in patients]
    dump_patient_to_json(patients_ids, filename='aa.json')


#dump_all_patients_to_json()

#dump_patient_to_json([5])
#load_data_from_json()



#all_patients_to_sql("patients_backup.sql")
#all_analysis_to_sql("analysis_backup.sql")
#all_parameters_to_sql("parameter_res_backup.sql")