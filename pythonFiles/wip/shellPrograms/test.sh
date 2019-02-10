echo "Setting up tables and databases"
echo $?
python3 setup.py
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "New registration"
python3	database.py '{"table_name":"1","request_type":"insert","data":{"rail_id":"RSK17CS023","student_name":"PRAJWAL H D","gender":"M","date_of_birth":"1999-05-03","time_of_joining_rail":"2018-10-18 14:34:23","phone_number":"8951041906","email":"hdprajwalgowda@gmail.com","associated_team":"B","projects_done":"0","branch":"CS","login_status":"NO","component_status":"NO","usn":"1SK17CS023","time_in_rail":"09:06:54","current_highest_role":"member"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "New registration"
python3	database.py '{"table_name":"1","request_type":"insert","data":{"rail_id":"RSK17CS024","student_name":"PRATHIK S","gender":"M","date_of_birth":"1999-04-01","time_of_joining_rail":"2018-10-18 14:34:23","phone_number":"9148021668","email":"prathikrebellion@gmail.com","associated_team":"A","projects_done":"0","branch":"CS","login_status":"NO","component_status":"NO","usn":"1SK17CS024","time_in_rail":"08:56:54","current_highest_role":"member"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "New registration"
python3	database.py '{"table_name":"1","request_type":"insert","data":{"rail_id":"RSK17CS036","student_name":"TARUN GOPALKRISHNA A","gender":"M","date_of_birth":"1999-05-01","time_of_joining_rail":"2018-10-18 14:34:23","phone_number":"8296177426","email":"tarungopalkrishna@gmail.com","associated_team":"B","projects_done":"0","branch":"CS","login_status":"NO","component_status":"NO","usn":"1SK17CS036","time_in_rail":"09:06:54","current_highest_role":"member"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Attendence login"
python3	database.py '{"table_name":"2","request_type":"login","data":{"rail_id":"RSK17CS023","current_team":"B","time_in":"2019-01-29 09:00:45","purpose":"RnD"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Attendence login"
python3	database.py '{"table_name":"2","request_type":"login","data":{"rail_id":"RSK17CS024","current_team":"A","time_in":"2019-01-29 09:00:45","purpose":"RnD"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Attendence login"
python3	database.py '{"table_name":"2","request_type":"login","data":{"rail_id":"RSK17CS036","current_team":"B","time_in":"2019-01-29 09:00:45","purpose":"RnD"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Reading data"
python3	database.py '{"table_name":"1","request_type":"read"}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Reading each data"
python3	database.py '{"table_name":"1","request_type":"readeach","data":{"rail_id":"RSK17CS036"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Attendence logout"
python3	database.py '{"table_name":"2","request_type":"logout","data":{"rail_id":"RSK17CS036","time_out":"2019-01-29 18:00:45"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Attendence logout"
python3	database.py '{"table_name":"2","request_type":"logout","data":{"rail_id":"RSK17CS024","time_out":"2019-01-29 18:00:45"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Attendence logout"
python3	database.py '{"table_name":"2","request_type":"logout","data":{"rail_id":"RSK17CS023","time_out":"2019-01-29 18:00:45"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Reading data"
python3	database.py '{"table_name":"1","request_type":"read"}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
echo "Reading each data"
python3	database.py '{"table_name":"1","request_type":"readeach","data":{"rail_id":"RSK17CS036"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"2","request_type":"read"}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"5","request_type":"insert","data":{"project_name":"test_proj","associated_team":"A","project_description":"just_testing_this_code","number_of_members":"4","mentor":"test_person","team_lead":"test_leader","guide":"test_guide","idea_by":"test_idea_name","type_of_project":"software","expected_duration":"5months","date_start":"2018-10-10 01:01:01","date_end":"2019-02-10 01:01:01","status":"test_status","priority":"test_prio","technology_stack":"test_stack"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"5","request_type":"read","data":{"associated_team":"A,B"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"5","request_type":"readeach","data":{"associated_team":"A,B"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"5","request_type":"update","data":{"associated_team":"RSK17CS036"}}'
echo $?
#echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
#python3	database.py '{"table_name":"5","request_type":"delete","data":{"associated_team":"RSK17CS036"}}'
#echo $?
#echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
#python3	database.py '{"table_name":"5","request_type":"delete","data":{"associated_team":"RSK17CS036"}}'
#echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"6","request_type":"insert","data":{"team_name":"A","associated_projects":"test_project","number_of_members":"4","team_members":"RSK17CS036,RSK17CS023,RSK17CS024,RSK17CS099","date_of_team_creation":"2018-02-02 11:17:00"}}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"6","request_type":"read"}'
echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"6","request_type":"readeach","data":{"team_name":"A"}}'
echo $?
#echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
#python3	database.py '{"table_name":"6","request_type":"delete","data":{"team_name":"A"}}'
#echo $?
echo "---------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------"
python3	database.py '{"table_name":"6","request_type":"update","data":{"team_name":"A","associated_projects":"test_project","number_of_members":"4","team_members":"RSK17CS036,RSK17CS023,RSK17CS024,RSK17CS099","date_of_team_creation":"2018-02-02 11:17:00"}}'
echo $?
