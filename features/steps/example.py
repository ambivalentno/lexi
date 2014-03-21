#-*- coding=utf-8 -*-
from behave import given, when, then

@given('we have behave installed')
def step(context):
    pass

@when(u'we implement a тест')
def step(context):
    assert True is not False

@then('behave will test it for us!')
def step(context):
    assert context.failed is False
