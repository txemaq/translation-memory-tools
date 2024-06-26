# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os

from .crawler import Crawler
from .downloadfile import DownloadFile
from .compressedfileset import CompressedFileSet
from .fileset import FileSet


class CrawlFileSet(FileSet):
    def _download_links(self, links, directory):
        for link in links:
            if self.is_retrieval_pattern(link):
                filename = os.path.join(directory, link.split("/")[-1])

                download = DownloadFile()
                download.get_file(link, filename)
                CompressedFileSet.uncompress(filename, False, self.temp_dir)

    def do(self):
        crawler = Crawler(self.url)
        crawler.run()
        links = crawler.get_all_links()
        self._download_links(links, self.temp_dir)

        self.build()
