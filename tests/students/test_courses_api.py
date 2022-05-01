import pytest
from rest_framework.test import APIClient
from students.models import Student, Course
from model_bakery import baker
from random import choice


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# @pytest.fixture
# def course():
#     return Course.objects.create(name='1 курс')


@pytest.mark.django_db
def test_get_one_course(client, course_factory, student_factory):
    students = student_factory(_quantity=20)
    courses = course_factory(_quantity=1, name='1 курс', students=students)
    for course in courses:
        course_id = course.id

    response = client.get(f'/api/v1/courses/{course_id}/')

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data['name'] == '1 курс'


@pytest.mark.django_db
def test_list_courses(client, course_factory, student_factory):
    students = student_factory(_quantity=20)
    course = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10


@pytest.mark.django_db
def test_filter_list_courses_by_id(client, course_factory, student_factory):
    students = student_factory(_quantity=20)
    courses = course_factory(_quantity=20)
    course_ids = []
    for course in courses:
        course_ids.append(course.id)
    course_id = choice(course_ids)

    response = client.get(f'/api/v1/courses/?id={course_id}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_filter_list_courses_by_name(client, course_factory, student_factory):
    students = student_factory(_quantity=20)
    courses = course_factory(_quantity=20)
    course_names = []
    for course in courses:
        course_names.append(course.name)
    course_name = choice(course_names)

    response = client.get(f'/api/v1/courses/?name={course_name}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == course_name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    response = client.post('/api/v1/courses/', data={'name': 'test'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    students = student_factory(_quantity=20)
    courses = course_factory(_quantity=1)
    for course in courses:
        course_id = course.id

    response = client.patch(f'/api/v1/courses/{course_id}/', data={'name': 'test_name'})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data['name'] == 'test_name'


@pytest.mark.django_db
def test_delete_course(client, course_factory, student_factory):
    students = student_factory(_quantity=20)
    courses = course_factory(_quantity=1)
    count = Course.objects.count()
    for course in courses:
        course_id = course.id

    response = client.delete(f'/api/v1/courses/{course_id}/')

    assert response.status_code == 204
    assert Course.objects.count() == count - 1
