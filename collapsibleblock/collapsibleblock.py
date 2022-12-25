"""TO-DO: Write a description of what this XBlock is."""
import sqlite3

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String


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


