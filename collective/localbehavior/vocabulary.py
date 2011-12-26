from zope.interface import directlyProvides
from zope.component import getUtilitiesFor, getUtility

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from plone.dexterity.interfaces import IDexterityFTI

from plone.behavior.interfaces import IBehavior

def LocalBehaviorsVocabularyFactory(context):
    behaviors = getUtilitiesFor(IBehavior)
    fti = getUtility(IDexterityFTI, name=context.portal_type)
    items = [
        (reg.title, reg.interface.__identifier__) for (
        title, reg) in behaviors if (
        reg.interface.__identifier__ not in fti.behaviors)
    ]
    return SimpleVocabulary.fromItems(items)
directlyProvides(LocalBehaviorsVocabularyFactory, IVocabularyFactory)
