import logging
import os

from django.core.management.base import BaseCommand, CommandError
from yatube.posts.parsers import xlsx_group_parser
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            raise CommandError(f'file "{file_path}" does not exists')

        logger.info('Loading applications from file %s', file_path)

        groups = xlsx_group_parser.xlsx_group_parser(file_path)

        for group in tqdm(groups):
            group.save()
