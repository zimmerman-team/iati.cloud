from django.db import connection
from django.http import HttpResponse

from iati.models import Activity
from tastypie.resources import ModelResource
import ujson


class ActivityAggregateResource(ModelResource):

    class Meta:
        queryset = Activity.objects.none()
        resource_name = 'aggregate'
        include_resource_uri = True
        allowed_methods = ['get']

    def make_where_query(self, values, name):
        query = ''
        if values:
            if not values[0]:
                return None

            for v in values:
                query = '{query} {name} = "{v}" OR'.format(
                    query=query, name=name, v=v)
            query = query[:-2]
        return query

    def get_and_query(self, request, parameter, queryparameter):

        filters = request.GET.get(parameter, '')
        if filters:
            query = self.make_where_query(
                values=filters.split(','),
                name=queryparameter)
            query = '{query}'.format(query=query)
        else:
            query = ''
        return query

    def get_filter_string(self, request, join_list):

        filter_list = []
        filters = [
            {
                'parameter_name': 'reporting_organisation__in',
                'filter_name': 'a.reporting_organisation_id',
                'from_addition': []},
            {
                'parameter_name': 'countries__in',
                'filter_name': 'rc.country_id',
                'from_addition': ['countries']},
            {
                'parameter_name': 'regions__in',
                'filter_name': 'rr.region_id',
                'from_addition': ['regions']},
            {
                'parameter_name': 'total_budget__in',
                'filter_name': 'a.total_budget',
                'from_addition': ['countries']},
            {
                'parameter_name': 'sectors__in',
                'filter_name': 'acts.sector_id',
                'from_addition': ['sectors']},
            {
                'parameter_name': 'activity_status__in',
                'filter_name': 'acs.code',
                'from_addition': ['activity-status']},
            {
                'parameter_name': 'participating_organisation__in',
                'filter_name': 'po.organisation_id',
                'from_addition': ['participating-org']},
            {
                'parameter_name': 'participating_organisations__organisation__code__in',
                'filter_name': 'po.organisation_id',
                'from_addition': ['participating-org']},
            {
                'parameter_name': 'transaction__receiver_organisation__in',
                'filter_name': 't.receiver_organisation_id',
                'from_addition': ['transaction']},
            {
                'parameter_name': 'start_planned_year',
                'filter_name': 'YEAR(start_planned)',
                'from_addition': []},
            {
                'parameter_name': 'start_actual_year',
                'filter_name': 'YEAR(start_actual)',
                'from_addition': []},
            {
                'parameter_name': 'end_planned_year',
                'filter_name': 'YEAR(end_planned)',
                'from_addition': []},
            {
                'parameter_name': 'end_actual_year',
                'filter_name': 'YEAR(end_actual)',
                'from_addition': []},
            {
                'parameter_name': 'total_budget__lt',
                'filter_name': 'a.total_budget',
                'type': '<',
                'from_addition': []},
            {
                'parameter_name': 'total_budget__gt',
                'filter_name': 'a.total_budget',
                'type': '>',
                'from_addition': []},
            {
                'parameter_name': 'policy_marker__in',
                'filter_name': 'pm.policy_marker_id',
                'from_addition': ['policy-marker']},
            {
                'parameter_name': 'document_link__gt',
                'filter_name': 'dl.id',
                'from_addition': ['document-link'],
                'type': '>'},
            {
                'parameter_name': 'result__gt',
                'filter_name': 'r.id',
                'from_addition': ['result'],
                'type': '>'},
            {
                'parameter_name': 'budget__period_start',
                'filter_name': 'bud.period_start',
                'from_addition': ['result'],
                'type': '>'},
            {
                'parameter_name': 'budget__period_end',
                'filter_name': 'bud.period_end',
                'from_addition': ['result'],
                'type': '>'},
            {
                'parameter_name': 'location__adm_country_iso_id__in',
                'filter_name': 'l.adm_country_iso_id',
                'from_addition': ['location'],
                'type': '='},
            {
                'parameter_name': 'not_in_locations',
                'static': ' a.id not in (select activity_id from iati_location) ',
                'from_addition': []},
            {
                'parameter_name': 'activity_status__in',
                'filter_name': 'a.activity_status_id',
                'from_addition': []},
            {
                'parameter_name': 'transaction_date__year__in',
                'filter_name': 'YEAR(t.transaction_date)',
                'from_addition': ['transaction']},
            {
                'parameter_name': 'transactions__transaction_date__gte',
                'filter_name': 't.transaction_date',
                'from_addition': ['transaction'],
                'type': '>='},
            {
                'parameter_name': 'transactions__transaction_date__lte',
                'filter_name': 't.transaction_date',
                'from_addition': ['transaction'],
                'type': '<='},
        ]


        for filter_item in filters:

            if 'static' in filter_item:
                parameter = request.GET.get(filter_item['parameter_name'], '')
                if parameter != '':
                    filter_list.append(filter_item['static'])
                    join_list.extend(filter_item['from_addition'])
                continue

            filter_list_item = self.get_and_query(
                request,
                filter_item['parameter_name'],
                filter_item['filter_name'])
            if filter_list_item != '':

                if 'type' in filter_item:
                    filter_list_item = filter_list_item.replace("=", filter_item['type'], 1)

                filter_list.append(filter_list_item)
                join_list.extend(filter_item['from_addition'])

        #search
        q = request.GET.get('query', '')
        if q:
            q_string = ''.join([
                "(MATCH (asd.`search_title`) AGAINST ('+",
                q,
                "*' IN BOOLEAN MODE) ",
                "OR MATCH (asd.`search_description`) AGAINST ('+",
                q,
                "*' IN BOOLEAN MODE) ",
                "OR asd.`search_identifier` = '",
                q,
                "') ",
            ])

            filter_list.append(q_string)
            join_list.extend(['activity-search-data'])


        filter_string = ') AND ('.join(filter_list)
        if filter_string:
            filter_string = 'AND (' + filter_string + ')'

        return [filter_string, join_list]

    def format_results(self, cursor):
        desc = cursor.description
        results = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return results

    def create_join_string(self, join_list):

        def remove_duplicates(seq):
            seen = set()
            seen_add = seen.add
            return [ x for x in seq if not (x in seen or seen_add(x))]

        join_list = remove_duplicates(join_list)

        join_map = {
            'title': 'JOIN iati_title as t on a.id = t.activity_id',
            'location': 'JOIN iati_location as l on a.id = l.activity_id',
            'description': 'JOIN iati_description as d on a.id = d.activity_id',
            'policy-marker': 'JOIN iati_activitypolicymarker as pm on a.id = pm.activity_id',
            'policy-marker-significance': 'JOIN iati_policysignificance as pms on pm.policy_significance_id = pms.code',
            'transaction': 'JOIN iati_transaction as t on a.id = t.activity_id',
            'regions': 'JOIN iati_activityrecipientregion as rr on a.id = rr.activity_id JOIN geodata_region as r on rr.region_id = r.code',
            'sectors': 'JOIN iati_activitysector as acts on a.id = acts.activity_id JOIN iati_sector as s on acts.sector_id = s.code',
            'result': 'JOIN iati_result as r on a.id = r.activity_id',
            'countries': 'JOIN iati_activityrecipientcountry as rc on a.id = rc.activity_id JOIN geodata_country as c on rc.country_id = c.code',
            'participating-org': 'JOIN iati_activityparticipatingorganisation as po on a.id = po.activity_id JOIN iati_organisation as o on po.organisation_id = o.code',
            'receiver-org': 'JOIN iati_organisation as rpo on t.receiver_organisation_id = rpo.code',
            'activity-status': 'JOIN iati_activitystatus as acs on a.activity_status_id = acs.code',
            'activity-search-data': 'JOIN iati_activitysearchdata as asd on a.id = asd.activity_id',
            'document-link': 'JOIN iati_documentlink as dl on a.id = dl.activity_id',
            'budget': 'JOIN iati_budget as bud on a.id = bud.activity_id',
            'location__countries': 'JOIN geodata_country as lc on l.adm_country_iso_id = lc.code'
        }

        joins = []

        for join in join_list:
            if join in join_map:
                joins.append(join_map[join])

        join_string = ''.join([
            'FROM iati_activity as a ',
            ' '.join(joins)])

        return join_string

    def get_list(self, request, **kwargs):

        # get group by and aggregation pars
        group_by_arr = request.GET.get('group_by', 'invalid_key').split(',')
        aggregation_key = request.GET.get('aggregation_key', 'invalid_key')
        result_query = request.GET.get('result_query', '')
        name_query = request.GET.get('name_query', '')
        order_by = request.GET.get('order_by', '')
        limit = request.GET.get('limit', '')
        offset = request.GET.get('offset', '')
        extra_select = request.GET.get('extra_select', '')

        select_list = []
        join_list = []
        where_list = []
        group_by_list = []

        extra_select_dict = {
            'activity_count': 'count(distinct a.id) as activity_count',
            'country_region_id': 'c.region_id'
        }

        if extra_select in extra_select_dict:
            select_list.append(extra_select_dict[extra_select])

        aggregation_dict = {
            'iati-identifier': {
                'select': 'count(a.id) as activity_count'},
            'reporting-org': {
                'select': 'count(a.reporting_organisation_id) as organisation_count'},
            'title': {
                'select': 'count(t.title)  as title_count',
                'from_addition': ['title']},
            'description': {
                'select': 'count(d.description)  as description_count',
                'from_addition': ['description']},
            'commitment': {
                'select': 'sum(t.value) as total_commitments',
                'from_addition': ['transaction'],
                'where_addition': 'AND t.transaction_type_id = "C" '},
            'disbursement': {
                'select': 'sum(t.value) as total_disbursements',
                'from_addition': ['transaction'],
                'where_addition': 'AND t.transaction_type_id = "D" '},
            'expenditure': {
                'select': 'sum(t.value) as total_expenditure',
                'from_addition': ['transaction'],
                'where_addition': 'AND t.transaction_type_id = "E" '},
            'incoming-fund': {
                'select': 'sum(t.value) as total_incoming_funds',
                'from_addition': ['transaction'],
                'where_addition': 'AND t.transaction_type_id = "IF" '},
            'location': {
                'select': 'count(l.activity_id) as location_count',
                'from_addition': ['location']},
            'policy-marker': {
                'select': 'count(pm.policy_marker_id) as policy_marker_count'},
            'total-budget': {
                'select': 'sum(a.total_budget) as total_budget'},
            'budget__value': {
                'select': 'sum(bud.value) as budget__value',
                'from_addition': ['budget']},
            'location_commitment': {
                'select': '(sum(t.value)/count(distinct l.adm_country_iso_id)) as value_by_country',
                'from_addition': ['transaction'],
                'where_addition': 'AND t.transaction_type_id = "C" '},
            'location_disbursement': {
                'select': '(sum(t.value)/count(distinct l.adm_country_iso_id)) as value_by_country',
                'from_addition': ['transaction'],
                'where_addition': 'AND t.transaction_type_id = "D" '},
        }

        if aggregation_key in aggregation_dict:

            select_list.append(aggregation_dict[aggregation_key]['select'])

            if "from_addition" in aggregation_dict[aggregation_key]:
                join_list.extend(aggregation_dict[aggregation_key]['from_addition'])

            if "where_addition" in aggregation_dict[aggregation_key]:
                where_list.append(aggregation_dict[aggregation_key]["where_addition"])
        else:
            return HttpResponse(ujson.dumps({
                "error": "Invalid aggregation key, see included list for viable keys.",
                "valid_aggregation_keys": list(aggregation_dict.keys())}),
                content_type='application/json')

        group_by_dict = {
            'recipient-country': {
                'select': 'rc.country_id, c.name, AsText(c.center_longlat) as location',
                'from_addition': ['countries'],
                'group_by': 'rc.country_id',
                'where_search_addition': 'AND c.name like %(name_query)s OR c.code like %(name_query)s '},
            'recipient-region': {
                'select': 'r.name, rr.region_id, AsText(r.center_longlat) as location',
                'from_addition': ['regions'],
                'group_by': 'rr.region_id',
                'where_search_addition': 'AND r.name like %(name_query)s OR r.code like %(name_query)s '},
            'activity-date__start_planned': {
                'select': 'YEAR(start_planned) as start_planned_year',
                'group_by': 'YEAR(start_planned)'},
            'activity-date__start_actual': {
                'select': 'YEAR(start_actual) as start_actual_year',
                'group_by': 'YEAR(start_actual)'},
            'activity-date__end-planned': {
                'select': 'YEAR(end_planned) as end_planned_year',
                'group_by': 'YEAR(end_planned)'},
            'activity-date__end-actual': {
                'select': 'YEAR(end_actual) as end_actual_year',
                'group_by': 'YEAR(end_actual)'},
            'sector': {
                'select': 'acts.sector_id, s.name',
                'from_addition': ['sectors'],
                'where_search_addition': 'AND s.name like %(name_query)s OR s.code like %(name_query)s '},
            'reporting-org': {
                'select': 'a.reporting_organisation_id'},
            'participating-org': {
                'select': 'po.organisation_id, o.name',
                'from_addition': ['participating-org'],
                'where_search_addition': 'AND o.name like %(name_query)s OR o.code like %(name_query)s '},
            'policy-marker': {
                'select': 'pm.policy_marker_id',
                'from_addition': ['policy-marker']},
            'result__title': {
                'select': 'r.title',
                'from_addition': ['result'],
                'where_addition': ' AND r.title = %(result_query)s '},
            'transaction__transaction-date_year': {
                'select': 'YEAR(t.transaction_date) as transaction_date_year',
                'from_addition': ['transaction'],
                'group_by': 'YEAR(t.transaction_date)'
            },
            'activity-status': {
                'select': 'acs.code, acs.name',
                'from_addition': ['activity-status'],
                'group_by': 'a.activity_status_id'
            },
            'transaction__receiver-org': {
                'select': 't.receiver_organisation_id, rpo.name',
                'from_addition': ['transaction', 'receiver-org'],
                'group_by': 't.receiver_organisation_id',
                'where_search_addition': 'AND rpo.name like %(name_query)s '
            },
            'policy_marker__significance': {
                'select': 'pm.policy_marker_id, pm.policy_significance_id',
                'from_addition': ['policy-marker'],
                'group_by': 'pm.policy_marker_id, pm.policy_significance_id'
            },
            'budget__period_start_year': {
                'select': 'YEAR(bud.period_start) as budget__period_start_year',
                'from_addition': ['budget'],
                'group_by': 'YEAR(bud.period_start)'
            },
            'location__administrative__code': {
                'select': 'l.adm_country_iso_id',
                'from_addition': ['location'],
            },
            'location_countries': {
                'select': 'a.id, l.adm_country_iso_id as loc_country_id, lc.name as country_name, lc.region_id',
                'from_addition': ['location', 'location__countries'],
                'group_by': 'a.id, l.adm_country_iso_id',
            }
        }

        for group_by_key in group_by_arr:
            if group_by_key in group_by_dict:

                select_list.append(group_by_dict[group_by_key]['select'])

                if 'group_by' in group_by_dict[group_by_key]:
                    group_by_list.append(group_by_dict[group_by_key]['group_by'])
                else:
                    group_by_list.append(group_by_dict[group_by_key]['select'])

                if "from_addition" in group_by_dict[group_by_key]:
                    join_list.extend(group_by_dict[group_by_key]['from_addition'])

                if 'where_addition' in group_by_dict[group_by_key] and query:
                    where_list.append(group_by_dict[group_by_key]['where_addition'])

                if 'where_search_addition' in group_by_dict[group_by_key] and name_query:
                    where_list.append(group_by_dict[group_by_key]['where_search_addition'])
            else:
                return HttpResponse(ujson.dumps({
                    "error": "Invalid group by key, see included list for viable keys.",
                    "valid_group_by_keys": list(group_by_dict.keys())}),
                    content_type='application/json')


        query_where = 'WHERE 1 ' + ' '.join(where_list)
        extra_where_and_join = self.get_filter_string(request, join_list)
        query_where += extra_where_and_join[0] + ' '

        query_select = 'SELECT SQL_CALC_FOUND_ROWS ' + ', '.join(select_list) + ' '

        query_from = self.create_join_string(join_list) + ' '

        query_group_by = ''.join([
            'GROUP BY ',
            ','.join(group_by_list),
            ' '])

        # to do, sec it
        if order_by:
            if order_by[:1] == '-':
                order_by = 'ORDER BY ' + order_by[1:] + ' DESC '
            else:
                order_by = 'ORDER BY ' + order_by + ' ASC '

        if limit:
            limit = 'LIMIT ' + str(limit)

        if offset:
            offset = ' OFFSET ' + str(offset)

        full_query = query_select + query_from + query_where + query_group_by + order_by + limit + offset

        # weird edge case for value by location country
        if 'location_countries' in group_by_arr:
            full_query = full_query.replace('SQL_CALC_FOUND_ROWS ', '')
            full_query = ''.join([
                'select SQL_CALC_FOUND_ROWS loc_country_id, sum(value_by_country) as total_value, region_id, country_name from (',
                full_query,
                ') as per_activity group by per_activity.loc_country_id'
            ])

        cursor = connection.cursor()
        cursor.execute(full_query,
                       {"result_query": result_query, "name_query": '%' + name_query + '%'})
        results = self.format_results(cursor=cursor)

        cursor.execute('SELECT FOUND_ROWS();')
        count = self.format_results(cursor=cursor)

        return HttpResponse(ujson.dumps({
            'count': count[0]['FOUND_ROWS()'],
            'results': results
        }), content_type='application/json')

