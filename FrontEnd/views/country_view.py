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

    # def _convert_sql_data_to_front_end_data(self, data: List[Tuple]) -> List[dict]:
    #     fe_response = []
    #     for country in data:
    #         fe_response.append({
    #             "country": country[1].strip(),
    #             "iso": country[2].strip(),
    #         })
    #     return fe_response

    def get(self):
        """Get either all countries or country which contains searched iso."""
        iso = request.args.get(Country.ISO.value)

        if iso is not None: # user added "iso" search to the request
            # query = f"""
            #     SELECT *
            #     FROM country_detail
            #     WHERE iso LIKE '%{iso}%';
            # """
            # ORM approach > 
            filtr_countries = (
                session.query(CountryDetail)
                .filter(CountryDetail.iso.like(f"%{iso}%"))
            )
            filtered_countries = [country.to_dict() for country in filtr_countries]

            # cursor.execute(query)
            # countries = self._convert_sql_data_to_front_end_data(cursor.fetchall())
            return jsonify(success=True, filtered_countries = filtered_countries)
        else: 
            all_countries = session.query(CountryDetail).all()
            countries = [country.to_dict() for country in all_countries]
             
            # query = "SELECT * FROM country_detail"
            # cursor.execute(query)
            # all_countries = self._convert_sql_data_to_front_end_data(cursor.fetchall())
            return render_template("country_overview.html", available_countries=countries)
    
    def delete(self):
        """Delete country based on iso and country name"""
        payload = request.get_json()

        # query = f"""
        #     DELETE FROM country_detail
        #     WHERE iso = '{payload[Country.ISO.value]}' AND country = '{payload[Country.COUNTRY.value]}';
        # """
        # cursor.execute(query)
        # connection.commit()
        # return jsonify(success=cursor.rowcount > 0)

        is_deleted = (
            session.query(CountryDetail)
            .filter(CountryDetail.iso == payload[Country.ISO.value], 
                    CountryDetail.country == payload[Country.COUNTRY.value])
            .delete()
        )
        session.commit()
        return jsonify(success=is_deleted)
    
    def post(self):
        """Create new country"""
        payload = request.get_json()

        try:
            # query = f"""
            #     SELECT *
            #     FROM country_detail
            #     WHERE country = '{payload[Country.COUNTRY.value]}' AND iso = '{payload[Country.ISO.value]}';
            # """
            # cursor.execute(query)
            # existing_record = cursor.fetchone()

            # if existing_record is not None:
            #     return jsonify(success=False)

            # insert_query = f"""
            #     INSERT INTO country_detail (Country, Iso)
            #     VALUES ('{payload[Country.COUNTRY.value]}', '{payload[Country.ISO.value]}')
            # """
            
            # cursor.execute(insert_query)
            existing_record = session.query(CountryDetail).filter(
                CountryDetail.country == payload[Country.COUNTRY.value],
                CountryDetail.iso == payload[Country.ISO.value]
            ).first()

            if existing_record is None:
                new_country = CountryDetail(**payload)
                session.add(new_country)
                session.commit()
                return jsonify(success=True)

            return jsonify(success=False)
        except Exception as e:
            return jsonify(success=False)
