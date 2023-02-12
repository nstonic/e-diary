from random import choice

from datacenter.models import Commendation, Lesson, Schoolkid, Chastisement, Mark

COMMENDATION_TEXTS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def get_schoolkid(schoolkid_name: str) -> Schoolkid | None:
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print('Ученик не найден. Проверьте ФИО.')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников. Уточните ФИО.')


def fix_marks(schoolkid_name: str):
    """Функция для исправления плохих оценок.
    Плохими считаются оценки 1, 2 и 3. Они исправляются случайно на 4 или 5.
    @param schoolkid_name: ФИО ученика. Можно указывать не полностью.
    """
    if schoolkid := get_schoolkid(schoolkid_name):
        Mark.objects.filter(schoolkid=schoolkid, points__lte=3).update(points=choice([4, 5]))
        print('Готово!')


def remove_chastisements(schoolkid_name: str):
    """Функция для исправления плохих оценок.
    Плохими считаются оценки 1, 2 и 3. Они исправляются случайно на 4 или 5.
    @param schoolkid_name: ФИО ученика. Можно указывать не полностью.
    """
    if schoolkid := get_schoolkid(schoolkid_name):
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        chastisements.delete()
        print('Готово!')


def create_commendation(schoolkid_name: str, subject: str):
    """Функция для добавления похвалы от учителя по заданному предмету.
    Добавляет похвалу в последний урок, в котором еще нет похвалы.
    @param schoolkid_name: ФИО ученика. Можно указывать не полностью.
    @param subject: Предмет
    """

    if schoolkid := get_schoolkid(schoolkid_name):
        if lesson := Lesson.objects.filter(
                year_of_study=schoolkid.year_of_study,
                group_letter=schoolkid.group_letter,
                subject__title=subject.capitalize()
        ).order_by('?').first():
            Commendation.objects.create(
                text=choice(COMMENDATION_TEXTS),
                created=lesson.date,
                schoolkid=schoolkid,
                subject=lesson.subject,
                teacher=lesson.teacher
            )
            print('Готово!')
        else:
            print('Предмет не найден.')
