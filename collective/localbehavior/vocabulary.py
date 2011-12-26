from zope.interface import directlyProvides
from zope.component import getUtilitiesFor, getUtility, queryUtility

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from plone.dexterity.interfaces import IDexterityFTI

from plone.behavior.interfaces import IBehavior
from zope.globalrequest import getRequest

def LocalBehaviorsVocabularyFactory(context):
    behaviors = getUtilitiesFor(IBehavior)
    fti = queryUtility(IDexterityFTI, name=context.portal_type)
    if fti is None:
        # hack to get fti when adding content
        req = getRequest()
        path = req.physicalPathFromURL(req.getURL())
        if not '++add++' in path[-1]:
            return SimpleVocabulary.fromItems([])
        ft = path[-1].replace('++add++', '')
        fti = getattr(context.portal_types, ft, None)
        if fti is None:
            return SimpleVocabulary.fromItems([])

    # query behaviors, exclude the content-level behaviors
    items = [
        (reg.title, reg.interface.__identifier__) for (
        title, reg) in behaviors if (
        reg.interface.__identifier__ not in fti.behaviors)
    ]
    return SimpleVocabulary.fromItems(items)
directlyProvides(LocalBehaviorsVocabularyFactory, IVocabularyFactory)
