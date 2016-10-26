import json
import models
import urllib2
import datetime

from django.db.models import Count


IATI_URL = 'https://iatiregistry.org/api/3/action/package_search?{options}'


class DatasetSyncer():

    def __init__(self):
        """
        Prefetch data, to minify amount of DB queries
        """
        source_url_tuples = models.Dataset.objects.values_list('id')
        self.source_urls = [url[0] for url in source_url_tuples]

        publisher_id_tuples = models.Publisher.objects.values_list('id')
        self.publisher_ids = [pub_id[0] for pub_id in publisher_id_tuples]

        self.source_count = 10000

    def synchronize_with_iati_api(self):
        """
        Start looping through the datasets
        """
        url_options = ['rows=200']

        offset = 0
        while self.source_count >= offset:
            options = '&'.join(url_options + ['start={}'.format(offset)])
            page_url = IATI_URL.format(options=options)
            self.synchronize_with_iati_api_by_page(page_url)
            offset += 200

    def synchronize_with_iati_api_by_page(self, url):
        """
        Loop through the datasets by page
        """
        req = urllib2.Request(url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        json_objects = json.load(f)

        self.source_count = json_objects['count']

        for line in json_objects['results']:
            self.parse_package(line)

    def get_or_create_publisher(self, publisher_iati_id, abbreviation, name):

        if publisher_iati_id in self.publisher_ids:
            return models.Publisher.objects.get(publisher_iati_id=publisher_iati_id)

        current_publisher = models.Publisher(
        publisher_iati_id=publisher_iati_id,
        display_name=abbreviation,
        name=name)
        current_publisher.save()
        self.publisher_ids.append(publisher_iati_id)

        return current_publisher

    def add_iati_xml_source_to_db(
            self,
            url,
            title,
            name,
            current_publisher,
            cur_type,
            iati_version):

        if cur_type == 'organisation':
            cur_type = 2
        else:
            cur_type = 1

        new_source = models.Dataset(
            ref=name,
            title=title,
            publisher=current_publisher,
            source_url=url,
            type=cur_type,
            iati_standard_version=iati_version,
            last_found_in_registry=datetime.datetime.now())
        new_source.save(process=False, added_manually=False)

        return new_source

    def parse_package(self, line):
        """
        Parse line from IATI response
        """

        data_dict = json.loads(line.get('data_dict', ''))
        res_url = line.get('res_url')
        publisher_iati_id = line['extras'].get('publisher_iati_id', None)

        if not res_url or not publisher_iati_id:
            # no url / id given, dont save
            return False

        source_url = str(res_url[0]).replace(' ', '%20')
        source_name = line.get('name', '')
        source_title = line.get('title', '')
        filetype = line['extras'].get('filetype')
        iati_version = line['extras'].get('iati_version', '')

        self.remove_publisher_duplicates(publisher_iati_id)

        if source_url not in self.source_urls:

            # get publisher info
            if data_dict.get('organization') is None:
                publisher_abbreviation = ''
                publisher_name = 'Unnamed (on registry)'
            else:
                publisher_abbreviation = data_dict['organization'].get('name', '')
                publisher_name = data_dict['organization'].get('title', 'Unnamed (on registry)')


            # add or get publisher and save source
            current_publisher = self.get_or_create_publisher(
                publisher_iati_id,
                publisher_abbreviation,
                publisher_name)

            # add iati source
            self.add_iati_xml_source_to_db(
                source_url,
                source_title,
                source_name,
                current_publisher,
                filetype,
                iati_version)

            self.source_urls.append(source_url)

        else:
            # update iati source last found
            source = models.Dataset.objects.get(source_url=source_url)
            source.iati_standard_version = iati_version
            source.last_found_in_registry = datetime.datetime.now()
            source.save(process=False, added_manually=False)

