from embed_video.fields import EmbedVideoField

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
from users.utils.thumbs import ImageWithThumbsField


class Basic(models.Model):
    '''
    Basic model to handle shared properties for all models
    '''
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
    creator = models.ForeignKey(User)

    class Meta:
        abstract = True


class Titled(models.Model):
    '''
    add title field
    '''
    title = models.CharField(_('Title'), max_length=100)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True



class Course(Basic, Titled):
    slug = models.SlugField(_('Slug'), max_length=100)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __unicode__(self):
        return self.title

    def activate(self):
        for lesson in self.lessons.all():
            lesson.activate()
        self.is_active = True
        self.save()


class Lesson(Basic, Titled):
    slug = models.SlugField(_('Slug', editable=False), max_length=100)
    course = models.ForeignKey(
        Course,
        verbose_name=_('Course'),
        related_name='lessons',
    )
    notes = models.FileField(
        _('Lesson notes'),
        upload_to='lesson_notes/',
        null=True, blank=True
    )

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __unicode__(self):
        return self.title

    def user_passed(self, user):
        '''
        Detects whether User pased all units of current lesson.
        Args:
            user: User instance
        Returns:
            (True, int(100)): if user passed this lesson
            (False, int): if user did not pass this lesson.
                          Adds percentage of passed units.
        '''
        right = self.progress.get(user=user)
        answered_right = len(right.units_get())
        all_units = self.units.count()  # TODO: add counter field
        if answered_right == all_units:
            return (True, 100)
        else:
            percentage = (answered_right / all_units) * 100
            return (False, percentage)

    def activate(self):
        for unit in self.units.all():
            unit.activate()
        self.is_active = True
        self.save()


class Unit(Basic, Titled):
    """
    Container to store video + explanation + link to question
    """
    # Data fields.
    explanation = models.TextField(_('Explanation'), null=True, blank=True)
    video = EmbedVideoField()
    position = models.IntegerField(_('Position'))  # position in a lesson
    # Technical fields.
    lesson = models.ForeignKey(
        Lesson,
        verbose_name=_('Lesson'),
        related_name='units',
    )

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.position:
            n = Unit.objects.filter(lesson=self.lesson).count()
            self.position = n + 1
        super(Unit, self).save(*args,**kwargs)

    def activate(self):
        for question in self.questions.all():
            question.activate()
        self.is_active = True
        self.save()


class Question(Basic, Titled):
    """
    Question to ask students
    """
    # Data fields
    picture = ImageWithThumbsField(
        _('Question picture'),
        upload_to='question_images/',
        sizes=settings.QUESTIONPIC_SIZES,
        null=True, blank=True
    )
    text = models.CharField(max_length=255)
    # Technical fields
    unit = models.ForeignKey(
        Unit,
        verbose_name=_('Unit'),
        related_name='questions',
    )

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __unicode__(self):
        return self.pk

    def activate(self):
        if self.answers.count() < 2:
            raise ValidationError(
                _('Too little answers or question: %(pk)s'),
                code='question_number',
                params={'pk': self.pk},
            )
        if not self.answers.filter(is_right=True).exists():
            raise ValidationError(
                _('No right answer provided for question: %(pk)s'),
                code='question_answer',
                params={'pk': self.pk},
            )
        self.is_active = True
        self.save()


class Answer(Basic):
    is_right = models.BooleanField(_('is_right'), default=False)
    text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question,
        verbose_name=_('Question'),
        related_name='answers',
    )

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __unicode__(self):
        return self.text

    def commit(self, user):
        """
        Add data to user progress
        Returns:
            True/False dependent on rightfullness of Answer
        """
        if self.is_right:
            progress = UserLessonProgress.objects.get(
                user=user,
                lesson=self.lesson
            )
            progress.units_add(self.unit.pk)
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        """
        Populate additional fields for Answer
        """
        self.lesson = self.question.unit.lesson
        self.unit = self.question.unit
        super(Answer, self).save(*args,**kwargs)


class UserLessonProgress(models.Model):
    '''
    Put ids of succesfuly answered units here
    '''
    user = models.ForeignKey(
        User,
        related_name='progress',
        )
    lesson = models.ForeignKey(
        Lesson,
        related_name='progress',
        )
    units = models.CommaSeparatedIntegerField(max_length=255)

    class Meta(object):
        unique_together = ('user', 'lesson')

    def units_get(self):
        if self.units:
            return set([int(unit_id) for unit_id in self.units.split(',')])
        else:
            return set([])

    def units_add(self, unit):
        self.units = self.units_get()
        self.units.add(unit.pk)
        self.save()
