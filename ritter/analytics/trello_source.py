import re
import json
import os

import requests

from ..dataprocessors.artifact_extractor import ArtifactExtractor


class TrelloSource:

    def refresh_source(project, artifacts):

        api_key = os.getenv('RITTER_TRELLO_KEY')
        user_key = project.get('trello_user_key')
        organization_id = project.get('trello_org_id')
        if not (api_key and user_key and organization_id):
            return

        cards = TrelloSource._get_all_cards(api_key, user_key, organization_id)
        if cards == False:
            return {'artifact_cards': []}

        artifact_cards = TrelloSource._match_with_artifacts(cards, artifacts)
        return {
            'artifact_cards': artifact_cards
        }

    def _get_all_cards(ak, uk, organization_id):

        boards = TrelloSource._fetch_organization_boards(ak, uk,
                                                         organization_id)
        if not boards:
            return False

        cards = []
        for b in boards:
            cards.extend(TrelloSource._fetch_all_cards(ak, uk, b))
        return cards

    def _match_with_artifacts(cards, artifacts):
        artifact_cards = {}
        for artifact in artifacts:
            reg = ArtifactExtractor._paragraph_reg(artifact['tokens'])
            matches = [c for c in cards if (reg.search(c['name']) or
                                            reg.search(c['desc']))]
            artifact_cards[artifact['_id']] = matches
        return artifact_cards

    def _fetch_organization_boards(ak, uk, organization_id):
        url = 'https://api.trello.com/1/organizations/%s/boards' % (
            organization_id)
        params = {
            'key': ak,
            'token': uk,
            'lists': 'all'
        }
        r = requests.get(url, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            return False

    def _fetch_all_cards(ak, uk, board):
        cards = []
        for lst in board['lists']:
            url = 'https://api.trello.com/1/lists/%s/cards' % (
                lst['id'])
            params = {
                'key': ak,
                'token': uk,
                'limit': 1000,
                'fields': 'name,desc,dateLastActivity,id,idList,labels,shortUrl,shortLink,pos,url',
                'attachments': 'true'
            }
            r = requests.get(url, params=params)
            if r.status_code == 200:
                for c in r.json():
                    c['listName'] = lst['name']
                    cards.append(c)
        return cards
