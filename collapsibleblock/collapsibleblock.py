"""TO-DO: Write a description of what this XBlock is."""
import itertools

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from django.core import serializers

import json
import os
from os import path


class Header:

    id_head = itertools.count(1)
    # id_sub_head = itertools.count(1)

    def __init__(self, header_name, *argv):
        self.id_header = next(Header.id_head)
        # self.id_sub_header = f"{self.id_header}.{next(Header.id_sub_head)}"
        # self.header_id = self.id_header or self.new_header_id()
        self.header_name = header_name
        self.sub_header_name = [sub_header for sub_header in argv]
        self.folder_to_create = "json_files/"
        self.json_file_template = f"episode_{self.id_header}"

    def check_header_id(self):
        dir_files = os.listdir("json_files")
        file = self.json_file_template
        # print(f"file: {file}")
        # print(f"dir_files: {dir_files}")
        for f in dir_files:
            # print(f"f: {f}")
            if f == file:
                file = f"episode_{self.id_header+1}"
            return file

        else:
            raise ValueError("Error with naming of the file")

    def new_header_id(self):
        self.check_header_id()

        dictionary = {
            "header_name": self.header_name,
            "header_id": self.id_header,
            "sub_header_name": self.sub_header_name,
            # "sub_header_id": self.id_sub_header
        }
        # print(dictionary)
        json_object = json.dumps(dictionary, indent=4)

        with open(f"{self.folder_to_create}{self.json_file_template}", "w") as file:
            file.write(json_object)
        return json_object

    def edit_header(self, id_header, header_name):
        if id_header != self.id_header:
            return "No such id"
        else:
            self.header_name = header_name
            return self.new_header_id()

    def edit_sub_header(self, id_header, sub_header_old_name, sub_header_new_name):
        if id_header != self.id_header:
            return "No such id"
        else:
            for sub_header in self.sub_header_name:
                if sub_header_old_name == sub_header:
                    self.sub_header_name = list(map(lambda x: x.replace(sub_header, sub_header_new_name), self.sub_header_name))
                    return self.new_header_id()

    # @staticmethod
    # def from_json(file):
    #     pass
        # with open("header.json, "w") as file




# def create_csv():
#     with open("header.csv", "w") as file:
#         fieldnames = ["header_name", "header_id", "sub_header_name", "sub_header_id"]
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows("Episode_1", 1, "Subepisode_1", 1.1)
#         writer.writerows("Episode_2", 1, "Subepisode_1", 2.1)
#
# create_csv()


class CollapsibleXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    # count = Integer(default=0, scope=Scope.user_state, help="A simple counter, to show something happening",)
    # header = String(default="Episode", scope=Scope.user_state_summary, help="The header of the collapsible block",)
    header = String(default="Default episode", scope=Scope.user_state_summary, help="The header of the collapsible block")
    sub_header = String(default="Default subheader", scope=Scope.user_state_summary, help=(f"The subheader of the {header}"))
    # db_extract = String(default="No records from DB", scope=Scope.user_state_summary, help=(f"Brace yourself!"))

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the CollapsibleXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/collapsibleblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/collapsibleblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/collapsibleblock.js"))
        frag.initialize_js('CollapsibleXBlock')
        return frag

    # todo - replace this method please
    # @XBlock.json_handler
    # def blocks_all(self):
    #     db_clt = ShittyDBClient()
    #     db_clt.connect_to_db()
    #     return db_clt.get_all_blocks()


    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        # assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CollapsibleXBlock",
             """<collapsibleblock/>
             """),
            ("Multiple CollapsibleXBlock",
             """<vertical_demo>
                <collapsibleblock/>
                <collapsibleblock/>
                <collapsibleblock/>
                </vertical_demo>
             """),
        ]

if __name__ == '__main__':
    h1 = Header("Episode_1", "Sub_episode_1")
    h1.new_header_id()
    h1.edit_header(1, "Episode_1")

    h2 = Header("Episode_2", "Sub_episode_1")
    h2.new_header_id()
    # h2.edit_sub_header(2, "Sub_episode_10")

    h3 = Header("Episode_3", "Sub_episode_1", "Sub_episode_2", "Sub_episode_3")
    h3.new_header_id()
    h3.edit_sub_header(3, "Sub_episode_3", "Sub_episode_bla")

    h4 = Header("Episode_3", ["Sub_episode_1", "Sub_episode_2"])
    h4.new_header_id()




# class ShittyDBClient:
#     def __init__(self):
#         self._db_path = 'sqlite:///Users/eleonoramatviiv/study/XBlock_for_Open_edX/xblock_development/var/workbench.db'
#         self._conn = None
#         self._query_template = "select %s from workbench_xblockstate"
#
#     def connect_to_db(self):
#         if not self._conn:
#             self._conn = sqlite3.connect(self._db_path)
#
#     def read_from_db(self, q):
#         cursor = self._conn.cursor()
#         cursor.execute(q)
#         return cursor.fetchall()
#
#     def get_block_by_id(self, id_, filtering=None):
#         q = self._query_template % '*'
#         q_filter = f'where id = {id_}'
#         if filtering:
#             q_filter += f'AND ({filtering})'
#         q += '\n' + q_filter
#         q += '\n' + 'limit 1'
#         return self.read_from_db(q)
#
#     def get_all_blocks(self):
#         blocks = self.read_from_db(self._query_template % '*')
#         keys = ['id', 'scope', 'scope_id','user_id', 'scenariro', 'tag', 'created', 'state']
#         return [dict(zip(keys, block)) for block in blocks]
#
#     def __del__(self):
#         self._conn.close()


