class AnalyzerBase:

    def ritter_id(self):
        return '%s_%s' % (self.ritter_type, self.id)

    def _get_doc(self, collection, _id):
        coll = self.db[collection]
        return coll.find_one({'_id': _id})

    def _save_analytics(self, collection, data, project):
        coll = self.db['ritterData']
        coll.remove({'id': self.ritter_id()})
        doc = {
            'id': self.ritter_id(),
            'type': self.ritter_type,
            'data': data,
            'project': project
        }
        self._remove_old_analytics(collection)
        return coll.insert_one(doc)

    def _remove_old_analytics(self, collection):
        coll = self.db[collection]
        return coll.delete_many({'id': self.ritter_id()})
