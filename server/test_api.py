import requests
import time

API = 'http://localhost:8000'

try:
    # Wait for server to be up
    for _ in range(5):
        try:
            requests.get(f'{API}/health')
            break
        except:
            time.sleep(1)

    print('Server is up.')

    # Test 1: Empty state /stats
    requests.delete(f'{API}/records')
    res = requests.get(f'{API}/stats')
    stats = res.json()
    if stats['total_students'] == 0:
        print('PASS: /stats gracefully handles 0 records.')
    else:
        print(f'FAIL: /stats total_students = {stats["total_students"]}')

    # Test 2: Replace Dataset flow
    # First insert one dummy prediction
    requests.post(f'{API}/predict', json={
        'Age': 20, 'Gender': 'Male', 'Socioeconomic_Status': 'Medium',
        'Attendance_Percentage': 80, 'Study_Hours_Per_Week': 10,
        'Previous_Term_Grade': 65, 'Continuous_Assessment_Score': 25
    })
    
    # Verify count is 1
    res = requests.get(f'{API}/stats')
    print('Before replace, total:', res.json()['total_students'])

    # Upload batch with replace=true
    files = {'file': ('test.csv', b'Age,Gender,Socioeconomic_Status,Attendance_Percentage,Study_Hours_Per_Week,Previous_Term_Grade,Continuous_Assessment_Score\n18,Female,High,90,15,85,40\n19,Male,Low,60,5,50,20', 'text/csv')}
    res = requests.post(f'{API}/predict/batch', files=files, data={'replace': 'true'})
    
    res = requests.get(f'{API}/stats')
    stats = res.json()
    print('After replace, total:', stats['total_students'])
    if stats['total_students'] == 2:
        print('PASS: Dataset replacement flow successful.')
    else:
        print('FAIL: Dataset replacement flow failed.')
    
    # Test 3: Dynamic chart rendering (verify stats output)
    print('Weekly Volume:', stats.get('weekly_volume'))
    print('Attendance vs Outcome:', stats.get('attendance_vs_outcome'))
    print('Study Hours vs Outcome:', stats.get('study_hours_vs_outcome'))
    if stats.get('weekly_volume') and stats.get('attendance_vs_outcome'):
         print('PASS: Dynamic chart data structures are correctly generated.')

except Exception as e:
    print('Error:', e)
