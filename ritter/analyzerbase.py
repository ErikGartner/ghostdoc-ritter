class AnalyzerBase:

    def ritter_id(self):
        return '%s_%s' % (self.ritter_type, self.id)

    def _get_doc(self, collection, _id):
        coll = self.db[collection]
        return coll.find_one({'_id': _id})

    def _save_analytics(self, collection, data, project):
        coll = self.db['ritterData']
        doc = {
            'id': self.ritter_id(),
            'type': self.ritter_type,
            'data': data,
            'project': project
        }
        return coll.replace_one({'id': self.ritter_id()}, doc, True)
