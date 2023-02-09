from random import choice

from datacenter import models


def fix_marks(schoolkid_name: str):
    """Функция для исправления плохих оценок.
    Плохими считаются оценки 1, 2 и 3. Они исправляются случайно на 4 или 5.
    @param schoolkid_name: ФИО ученика. Можно указывать не полностью,
    но тогда в случае ошибки MultipleObjectsReturned уточните ФИО.
    Возможно были найдены несколько учеников.
    """
    schoolkid = models.Schoolkid.objects.get(full_name__contains=schoolkid_name)
    for mark in models.Mark.objects.filter(schoolkid=schoolkid, points__le=3):
        mark.points = choice([4, 5])
        mark.save()


def remove_chastisements(schoolkid_name: str):
    """Функция для удаления замечаний учителей.
    @param schoolkid_name: ФИО ученика. Можно указывать не полностью,
    но тогда в случае ошибки MultipleObjectsReturned уточните ФИО.
    Возможно были найдены несколько учеников.
    """
    schoolkid = models.Schoolkid.objects.get(full_name__contains=schoolkid_name)
    chastisements = models.Chastisement.objects.filter(schoolkid=schoolkid.full_name)
    for chastisement in chastisements:
        chastisement.delete()


def create_commendation(schoolkid_name: str, subject: str):
    """Функция для добавления похвалы от учителя по заданному предмету.
    Добавляет похвалу в последний урок, в котором еще нет похвалы.
    @param schoolkid_name: ФИО ученика. Можно указывать не полностью,
    но тогда в случае ошибки MultipleObjectsReturned уточните ФИО.
    Возможно были найдены несколько учеников.
    @param subject: Предмет
    """
    commendation_texts = [
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
    schoolkid = models.Schoolkid.objects.get(full_name__contains=schoolkid_name)
    lessons = models.Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('-date')
    for lesson in lessons:
        if not models.Commendation.objects.filter(
                schoolkid=schoolkid,
                created=lesson.date,
                subject=lesson.subject
        ):
            models.Commendation.objects.create(
                text=choice(commendation_texts),
                created=lesson.date,
                schoolkid=schoolkid,
                subject=lesson.subject,
                teacher=lesson.teacher
            )
            return
