# Установка
Для того, чтобы установить PyCharm надо скачать из http://qoo.by/H8h <br/>
В компьютере должен быть установлен Python 3.4 <br/>
Надо  установить Postgresql версию 9.4.10 http://qoo.by/H8i при установке надо поставить галочку pgAdmin III <br/>
Для того чтобы установить в себе виртуальную среду (virtual env) надо в командной строке написать (командная строка должна быть в папке ReservationSystem) С:/Python34/python.exe -m venv myenv <br/>
Потом по командной строке переходим в папку myenv\Script\ и запускаем activate.bat <br/>
После этого устанавливаем пакеты: <br/>
#pip команды
myenv\Script\pip install flask <br/> 
myenv\Script\pip install flask_sqlalchemy <br/> 
myenv\Script\pip install psycopg2 <br/>
myenv\Script\pip install flask-migrate <br/>

#Литература
Flask - документация http://qoo.by/H8k, вики http://qoo.by/H8v <br/>
SQlAlchemy - http://qoo.by/H8j русский перевод - http://qoo.by/H8g <br/>
Учебник по Flask - http://qoo.by/H8l<br/>
