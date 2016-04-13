class AnalyzerBase:

    def ritter_id(self):
        return '%s_%s' % (self.ritter_type, self.id)

    def _get_doc(self, collection, _id):
        collection = self.db[collection]
        return collection.find_one({'_id': _id})

    def _save_analytics(self, collection, data, project):
        collection = self.db['ritterData']
        collection.remove({'id': self.ritter_id()})
        doc = {
            'id': self.ritter_id(),
            'type': self.ritter_type,
            'data': data,
            'project': project
        }
        return collection.insert_one(doc)
