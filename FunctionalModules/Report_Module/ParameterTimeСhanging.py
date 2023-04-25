from Models.Patient import Patient
from Models.Analysis import Analysis
from statistics import mean

class ParameterTimeLine:
    def __init__(self, patient: Patient, analysis: Analysis):
        self.patient = patient
        self.analysis = analysis
        pass

    def get(self, parameter_index, season, include_zeroes = False):
        analysis = self.patient.select_analysis_by_season(season)
        analysis = self._get_analysys_before( analysis)
        parameters_line = self._get_parameters_in_time(analysis, parameter_index, include_zeroes)


        if len(parameters_line) ==1 :
            avg = 0
        elif len(parameters_line) ==2 :
            avg = parameters_line[0].value
        elif len(parameters_line) == 0:
            return [0,0,0]
        else:
            avg = round( self._calculate_average(parameters_line[:-1]),2)

        last = round(parameters_line[-1].value,2)
        divation = round(last-avg,2)

        return [avg, last, divation]


    def _get_parameters_in_time(self, analysis_list: list, parameter_index, include_zeroes=False):
        result = []

        for index, anal in enumerate(analysis_list):
            parameter = anal.parameters[parameter_index]
            if not include_zeroes and parameter.value == 0:
                continue
            result.append(parameter)

        return result

    def _calculate_average(self, params:list):
        l = [param.value for param in params]
        avg = mean(l)

        return avg

    def _get_analysys_before(self, analysis_list:list):
        res = []
        for anal in analysis_list:
            res.append(anal)
            if anal.analysis_date == self.analysis.analysis_date:
                break
        return res

'''
pat = CreateFullPatientFromDB(5)
s = pat.select_analysis_by_season('1')
ptl = ParameterTimeLine(pat)
avg = ptl.get(1, season='1', include_zeroes=False)
print(avg)'''


