import json

from flask import jsonify, request
from flask.views import MethodView

from Shared.Enums.models.table_columns import Country
from Shared.DataAccess.models.country_detail_model import CountryDetail
from Shared.DataAccess.config.config import session
from Shared.Cache import redis_cache

class CountryAPI(MethodView):
    PAYLOAD_COUNTRIES = "countries"
    RESPONSE_COUNT = "match_count"
    RESPONSE_MATCH = "matches"
    init_every_request = False

    def __init__(self) -> None:
        self.cache = redis_cache

    def post(self):
        payload = request.get_json()

        response = {
            Country.ISO.value: payload[Country.ISO.value],
            self.RESPONSE_COUNT: 0,
            self.RESPONSE_MATCH: []
        }

        # caching
        if cached_countries := self.cache.lrange(payload[Country.ISO.value], 0, -1):
            cached_countries = [country.decode("utf-8") if (isinstance(country, bytes)) else country for country in cached_countries]
            for cached_country in cached_countries:
                # return only those countries from cache that was used in the request payload.
                if cached_country in payload[self.PAYLOAD_COUNTRIES]:
                    response[self.RESPONSE_COUNT] += 1
                    response[self.RESPONSE_MATCH].append(cached_country)
                
            return jsonify(response)

        filtered_countries = (
            session.query(CountryDetail)
            .filter(
                CountryDetail.iso == payload[Country.ISO.value],
                CountryDetail.country.in_(payload[self.PAYLOAD_COUNTRIES])
                )
            .all()
            )

        for country in filtered_countries:
            response[self.RESPONSE_COUNT] += 1
            response[self.RESPONSE_MATCH].append(country.country)

        if len(response[self.RESPONSE_MATCH]):
            self.cache.rpush(payload[Country.ISO.value],  json.dumps(response[self.RESPONSE_MATCH]))     

        return jsonify(response)
