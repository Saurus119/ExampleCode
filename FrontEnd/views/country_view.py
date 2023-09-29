from typing import List, Tuple

from flask import render_template, jsonify, request
from flask.views import MethodView

from Shared.Enums.models.table_columns import Country
from Shared.Decorators.operation_restriction import restrict_by_auth_token
from Shared.DataAccess.config.config import session
from Shared.DataAccess.models.country_detail_model import CountryDetail
from Shared.Cache import redis_cache

class CountryView(MethodView):
    init_every_request = False
    
    decorators = [restrict_by_auth_token("DELETE")] # showcase of decorator functionality.

    def __init__(self) -> None:
        self.cache = redis_cache

    def _set_country_to_cache(self, iso: str, country: str)-> None:
        """We need to cache"""
        try:
            self.cache.rpush(iso, country)
        except Exception as e:
            print(str(e))

    def _delete_country_from_cache(self, iso, country) -> None:
        self.cache.lrem(iso.strip(), 0, country.strip())

    def get(self):
        """Get either all countries or country which contains searched iso."""
        # this endpoint for frontend doesnt include caching so you can verify API response through UI search.
        iso = request.args.get(Country.ISO.value)

        if iso is not None: # user added "iso" search to the request
            filtr_countries = (
                session.query(CountryDetail)
                .filter(CountryDetail.iso.like(f"%{iso}%"))
            )
            filtered_countries = [country.to_dict() for country in filtr_countries]

            return jsonify(success=True, filtered_countries = filtered_countries)
        else: 
            all_countries = session.query(CountryDetail).all()
            countries = [country.to_dict() for country in all_countries]
             
            return render_template("country_overview.html", available_countries=countries)
    
    def delete(self):
        """Delete country based on iso and country name"""
        payload = request.get_json()
        is_deleted = (
            session.query(CountryDetail)
            .filter(CountryDetail.iso == payload[Country.ISO.value], 
                    CountryDetail.country == payload[Country.COUNTRY.value])
            .delete()
        )
        session.commit()

        if is_deleted: 
            self._delete_country_from_cache(payload[Country.ISO.value], payload[Country.COUNTRY.value])

        return jsonify(success=is_deleted)
    
    def post(self):
        """Create new country"""
        payload = request.get_json()

        try:
            existing_record = session.query(CountryDetail).filter(
                CountryDetail.country == payload[Country.COUNTRY.value],
                CountryDetail.iso == payload[Country.ISO.value]
            ).first()

            if existing_record is None:
                new_country = CountryDetail(**payload)
                session.add(new_country)
                session.commit()
                
                self._set_country_to_cache(payload[Country.ISO.value], payload[Country.COUNTRY.value])
                return jsonify(success=True)

            return jsonify(success=False)
        except Exception as e:
            print(str(e))
            return jsonify(success=False)
