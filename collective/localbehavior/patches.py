
def patch_fti_localbehavior():
    from plone.dexterity.content import FTIAwareSpecification

    if getattr(FTIAwareSpecification, '__localbehavior_patched', False):
        return

    from plone.behavior.interfaces import IBehaviorAssignable
    from plone.behavior.interfaces import IBehavior
    from zope.component import queryUtility

    _orig_get = FTIAwareSpecification.__get__

    def __get__(self, inst, cls=None):
        spec = _orig_get(self, inst, cls)
        bases = list(spec.__bases__)
        for name in getattr(inst, 'local_behaviors', []):
            behavior = queryUtility(IBehavior, name=name)
            if behavior.marker is not None:
                bases.append(behavior.marker)
        spec.__bases__ = tuple(bases)
        return spec

    FTIAwareSpecification.__get__ = __get__
    FTIAwareSpecification.__localbehavior_patched = True

patch_fti_localbehavior()
