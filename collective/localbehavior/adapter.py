from zope.interface import implements
from zope.component import adapts, getUtility, queryUtility

from plone.dexterity.behavior import DexterityBehaviorAssignable
from plone.behavior.interfaces import IBehavior
import itertools

from collective.localbehavior.localbehavior import ILocalBehaviorSupport


class DexterityLocalBehaviorAssignable(DexterityBehaviorAssignable):
    adapts(ILocalBehaviorSupport)

    def __init__(self, context):
        super(DexterityLocalBehaviorAssignable, self).__init__(context)
        self.context = context

    def enumerateBehaviors(self):
        local_behaviors = getattr(self.context, 'local_behaviors', [])
        for name in itertools.chain(self.fti.behaviors, local_behaviors):
            behavior = queryUtility(IBehavior, name=name)
            if behavior is not None:
                yield behavior
