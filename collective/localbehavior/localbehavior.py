from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from collective.localbehavior import MessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget

class ILocalBehaviorSupport(form.Schema):

    form.fieldset(
        'local_behavior',
        label=_(u'Local Behaviors'),
        fields=['local_behaviors']
    )

    form.widget(local_behaviors=CheckBoxFieldWidget)
    local_behaviors = schema.List(
        title=u'Behaviors',
        description=(u'Select local behaviors for this content,' +
                     ' behavior changes will be applied after saving'),
        required=False,
        value_type=schema.Choice(
            title=u'Behavior',
            vocabulary="LocalBehaviors"
        )
    )

alsoProvides(ILocalBehaviorSupport,IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class LocalBehaviorSupport(object):

    implements(ILocalBehaviorSupport)
    adapts(IDexterityContent)

    local_behaviors = context_property('local_behaviors')

    def __init__(self,context):
        self.context = context

