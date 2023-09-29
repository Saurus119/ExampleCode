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
        filtered_countries = (
            session.query(CountryDetail)
            .filter(
                CountryDetail.iso == payload[Country.ISO.value],
                CountryDetail.country.in_(payload[self.PAYLOAD_COUNTRIES])
                )
            .all()
            )

        response = {
            Country.ISO.value: payload[Country.ISO.value],
            self.RESPONSE_COUNT: 0,
            self.RESPONSE_MATCH: []
        }

        for country in filtered_countries:
            response[self.RESPONSE_COUNT] += 1
            response[self.RESPONSE_MATCH].append(country.country)

        if cached_val := self.cache.get("mykey"):
            response["cached"] = cached_val

        return jsonify(response)
    

