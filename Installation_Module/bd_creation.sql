create table patients
(
	patient_id SERIAL PRIMARY KEY,
	name varchar(20),
	surname varchar(20),
	patronymic varchar(20),
	birthday date,
	main_diagnosis varchar(100),
	concomitant_diagnosis varchar(100),
	genes varchar(100), /*скорее всего изменится*/
	gender varchar(10)
	
);


create table Analysis
(
	analysis_id serial primary key,
	owner_id int,
	analysis_date date,
	
	foreign key (owner_id) references patients(patient_id)  ON DELETE CASCADE
);

create table parameter_catalog
(
	parameter_id serial primary key,
	name varchar(100),
	unit varchar(10) DEFAULT '10E9/л',
	interval_start float,
	interval_end float
);

create table parameter_results
(
	result_id serial primary key,
	parameter_id int,
	foreign key (parameter_id) references parameter_catalog(parameter_id),
	
	value float,
	analysis_id int,
	foreign key (analysis_id) references Analysis(analysis_id)  ON DELETE cascade,
	
	deviation varchar(10)
);

create table calculator_rules
(
    rule_id serial primary key,
    expr text,
    cause text,
    recommendation text,
    variable text,
    value text,
    for_sping bool,
    for_autumn bool
);

insert into parameter_catalog(name, interval_start, interval_end, unit) 
values
('Лейкоциты (WBC)'     										,4.60, 	7.10,	'10E9/л'),
('Лимфоциты (LYMF)'    										,1.60, 	2.40, 	'10E9/л'),
('Моноциты (MON)'      										,0.00, 	0.80, 	'10E9/л'),
('Нейтрофилы (NEU)'    										,2.00, 	5.50, 	'10E9/л'),
('Эозинофилы (EOS)'											,0.00, 	0.70, 	'10E9/л'),
('Базофилы (BAS)'											,0.00, 	0.20, 	'10E9/л'),
('Гемоглобин (HGB)'											,110.00,160.00,	'г/л'	),
('Тромбоциты (PLT)'											,180.00,320.00,	'10E9/л'),
('Общие T-лимфоциты (CD45+CD3+)'							,0.80,	2.20,	'10E9/л'),
('Общие В-лимфоциты (CD45+CD19+)'							,0.1,	0.5,	'10E9/л'),
('Т-хелперы (CD45+CD3+CD4+)'								,0.70,	1.10,	'10E9/л'),
('Соотношение CD3+CD4+/CD3+CD8+'							,1.00,	2.50,	' '),
('Т-цитотоксические лимфоциты (CD45+CD3+СD8+)'				,0.5,	0.9,	'10E9/л'),
('Общие NK-клетки (CD45+CD3-CD16+56+)'						,0.15,	0.50,	'10E9/л'),
('NK-клетки цитокинпродуцирующие (CD45+CD3-CD16brightCD56dim)',93.75, 97.50,'%'),
('Циркулирующие иммунные комплексы'							,40.00,	70.00,	'ед.'),
('НСТ-тест (спонтанный)'									,6.00,	12.00,	'%'),
('НСТ-тест (стимулированный)'								,24.00,	80.00,	'%'),
('CD3+IFNy+(стимулированный)'								,0.185,	0.377,	'10E9/л'),
('CD3+IFNy+(спонтанный)'									,0.000,	0.500,	'10E9/л'),
('Индекс {CD3+IFNy+(стимулированный)/CD3+IFNy+(спонтанный)}',0,0,			' '),
('CD3+TNFa+(стимулированный)'								,0.521,	0.942,	'10E9/л'),
('CD3+TNFa+(спонтанный)'									,0.000,	0.900,	'10E9/л'),
('Индекс {CD3+TNFa+(стимулированный)/CD3+TNFa+(спонтанный)}',0,0,' '),
('CD3+IL2+(стимулированный)'								,0.328,	0.651,	'10E9/л'),
('CD3+IL2+(спонтанный)'										,0.000,	0.100,	'10E9/л'),
('Индекс {CD3+IL2+(стимулированный)/CD3+IL2+(спонтанный)}'	,0, 0,			' '),
('ФНО фактор некроза опухоли'								,0, 0,			'10E9/л')
