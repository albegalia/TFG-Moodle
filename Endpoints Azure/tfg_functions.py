def create_student_html(student_info: list):

    logins = student_info[0]['logins']
    n_logins = logins[0]['n_logins']
    last_login_day = logins[0]['last_login_day']
    studentname = student_info[0]['firstname']

    html = f'<p>¡Bienvenido de nuevo {studentname}!</p>'
    html += f'<p>Tu último inicio de sesión fue el {last_login_day}, lo cual significa '
    html += f'que llevas {n_logins} inicios de sesión desde que entraste en la UPCT 😎</p><br>'
    html += f'<p>¡Sigue así que vas muy bien! 💪</p>'

    return html

def create_course_html(course_info: list):

    html = '<p>¡Bienvenido de nuevo profesor!</p>'
    html += '<p>Los alumnos matriculados en la asignatura sin iniciar sesión '
    html += 'desde hace más de una semana son:</p>'
    for alumno in course_info:
        for login in alumno['students_not_logged_week']:
            nombre = login['firstname']
            apellido = login['lastname']
            email = login['email']
            html += f'<ul><li>{nombre} {apellido} | {email}</li></ul>'
    html += '<p>Ahí tiene sus correos por si necesita contactarles y preguntar qué sucede. 😉</p>'
    
    return html
