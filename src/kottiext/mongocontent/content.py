import kotti.resources#
import kotti.views.edit
import zope.interface

from pyramid.security import ALL_PERMISSIONS
from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index, DocumentField
from mongoalchemy.fields import *

class MongoRoot(object):
    __name__ = '' # root is required to have an empty name!
    __parent__ = None
    __acl__ = [('Allow', 'role:admin', ALL_PERMISSIONS)]

    def __setitem__(self, key, node):
        #XXX already done by MD.__init__?!?
        pass

    def __delitem__(self, key):
        #XXX
        #del mongo_fake[unicode(key)]
        pass

    def keys(self):
        return [str(d.mongo_id) for d in self.values()]

    def values(self):
        with Session.connect('mongoalchemy') as s:
            return s.query(MongoDocument)

    def __getitem__(self, path):
        if path == 'description':
            return
        with Session.connect('mongoalchemy') as s:
            return s.query(MongoDocument).filter(MongoDocument.mongo_id == path).one()


def get_mongo_root(request=None):
    return MongoRoot()


class MongoDocument(Document):
    __name__ = ''
    __parent__ = MongoRoot()
    #make getattr in kotti!
    default_view = ''
    id = ''
    in_navigation = False

    title = StringField()
    description = StringField()
    body = StringField()
    zope.interface.implements(kotti.resources.IContent)

    type_info = kotti.resources.Document.type_info.copy(
    name=u'MongoDocument',
    add_view=u'add_mongodocument',
    addable_to=[],
    )

    def values(self):
        return []

    def __getitem__(self, key):
        return getattr(self, key)


    def __init__(self, *args, **kw):
        super(MongoDocument, self).__init__(*args, **kw)
        if hasattr(self, 'mongo_id'):
            self.__name__ = self.id = self.name = str(self.mongo_id)


def mongo_doc_factory(*args, **kw):
    with Session.connect('mongoalchemy') as s:
        doc = MongoDocument(*args, **kw)
        s.insert(doc)
        doc.__name__ = doc.id = doc.name = str(doc.mongo_id)
        return doc


class MongodocEditFormView(kotti.views.util.EditFormView):

    def before(self, form):
        form.appstruct = self.context._field_values.copy()

    def save_success(self, appstruct):
        result = super(MongodocEditFormView, self).save_success(appstruct)
        with Session.connect('mongoalchemy') as s:
            for fieldname in appstruct.keys():
                up = s.query(MongoDocument).filter(
                    MongoDocument.mongo_id == self.context.mongo_id).set(
                        getattr(MongoDocument, fieldname), appstruct[fieldname])
                up.execute()
        return result


def mongodoc_edit(context, request, schema, **kwargs):
    return MongodocEditFormView(
        context,
        request,
        schema=schema,
        **kwargs
        )()

def mongodoc_edit_factory(schema, **kwargs):
    @kotti.views.util.ensure_view_selector
    def view(context, request):
        return mongodoc_edit(context, request, schema, **kwargs)
    return view


def includeme(config):
    config.add_view(
        mongodoc_edit_factory(kotti.views.edit.DocumentSchema()),
        context=MongoDocument,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )
    config.add_view(
        kotti.views.edit.make_generic_add(kotti.views.edit.DocumentSchema(), mongo_doc_factory, u'mongodocument'),
        name=MongoDocument.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )
    config.add_view(
        context=MongoDocument,
        name='view',
        permission='view',
        renderer='kotti:templates/view/document.pt',
        )
