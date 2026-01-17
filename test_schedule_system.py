from schedule_manager import get_all_schedules, get_student

print('=== SCHEDULES TODAY ===')
for s in get_all_schedules():
    print(f'  {s.id}: {s.course} at {s.start_time}-{s.end_time}')

print('\n=== STUDENT 12345 ===')
student = get_student('12345')
print(f'Name: {student["name"]}')
print(f'Enrolled: {student["enrolled_courses"]}')
print(f'Registered:')
for sched in student['registered_schedules']:
    print(f'  - {sched["course"]} at {sched["time"]}')

print('\n=== STUDENT 67890 ===')
student2 = get_student('67890')
print(f'Name: {student2["name"]}')
print(f'Enrolled: {student2["enrolled_courses"]}')
print(f'Registered:')
for sched in student2['registered_schedules']:
    print(f'  - {sched["course"]} at {sched["time"]}')
