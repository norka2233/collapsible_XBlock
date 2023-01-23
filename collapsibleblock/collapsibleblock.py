"""TO-DO: Write a description of what this XBlock is."""
import itertools
import logging

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, Integer, Scope, String

import json
import os

log = logging.getLogger(__name__)


class CollapsibleXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """
    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(default=0, scope=Scope.user_state,help="A simple counter, to show something happening")
    upvotes = Integer(help="Number of up votes", default=0, scope=Scope.user_state_summary)
    downvotes = Integer(help="Number of down votes", default=0, scope=Scope.user_state_summary)
    voted = Boolean(help="Has this student voted?", default=False, scope=Scope.user_state)
    # header = String(default="Episode", scope=Scope.user_state_summary, help="The header of the collapsible block",)
    # sub_header = String(default="Default subheader", scope=Scope.user_state_summary, help=(f"The subheader of the {header}"))
    # db_extract = String(default="No records from DB", scope=Scope.user_state_summary, help=(f"Brace yourself!"))

    id_header = Integer(default=0, scope=Scope.user_state_summary, help="header ID ")
    header_name = String(default="Default header", scope=Scope.user_state_summary, help=("header name"))
    sub_header_name = String(default="Default sub_header_name", scope=Scope.user_state_summary, help=("sub_header_name"))

    def block(self, header_name, *args):
        self.id_header = next(CollapsibleXBlock.id_head)
        self.header_name = header_name
        self.sub_header_name = [sub_header for sub_header in args]
        self.folder_to_create = "json_files/"
        self.json_file_template = f"episode_{self.id_header}"

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the MyXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/collapsibleblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/collapsibleblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/collapsibleblock.js"))
        frag.initialize_js('CollapsibleXBlock')
        return frag

    @XBlock.json_handler
    def vote(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Update the vote count in response to a user action.
        """
        # Here is where we would prevent a student from voting twice, but then
        # we couldn't click more than once in the demo!
        #
        #     if self.voted:
        #         log.error("cheater!")
        #         return

        if data['voteType'] not in ('up', 'down'):
            log.error('error!')
            return None

        if data['voteType'] == 'up':
            self.upvotes += 1
        else:
            self.downvotes += 1

        self.voted = True

        return {'up': self.upvotes, 'down': self.downvotes}

    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

        # html = self.resource_string("static/html/collapsibleblock.html")
        # frag = Fragment(html.format(self=self))
        # frag.add_css(self.resource_string("static/css/collapsibleblock.css"))
        # frag.add_javascript(self.resource_string("static/js/src/collapsibleblock.js"))
        # frag.initialize_js('CollapsibleXBlock')
        # return frag
    problem_view = student_view

    @XBlock.json_handler
    def check_header_id(self):
        dir_files = os.listdir("json_files")
        file = self.json_file_template

        for f in dir_files:
            if f == file:
                file = f"episode_{self.id_header+1}"
            return file
        else:
            raise ValueError("Error with naming of the file")

    @XBlock.json_handler
    def new_header_id(self):
        self.check_header_id()

        dictionary = {
            "header_name": self.header_name,
            "header_id": self.id_header,
            "sub_header_name": self.sub_header_name,
        }
        json_object = json.dumps(dictionary, indent=4)

        with open(f"{self.folder_to_create}{self.json_file_template}", "w") as file:
            file.write(json_object)
        return json_object

    # @XBlock.json_handler
    # def new_sub_header_id(self, header_id, header_name, added_sub_header_name):
    #     if self.id_header == header_id and self.header_name == header_name:
    #         self.sub_header_name.append(added_sub_header_name)
    #     return self.new_header_id()

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    # @XBlock.json_handler
    # def increment_count(self, data, suffix=''):
    #     """
    #     An example handler, which increments the data.
    #     """
    #     # Just to show data coming in...
    #     # assert data['hello'] == 'world'
    #
    #     self.count += 1
    #     return {"count": self.count}

    @XBlock.json_handler
    def edit_header(self, new_header_name):
        new_header_name = input()
        self.header_name == new_header_name

        dictionary = {
            "header_name": self.header_name,
            "header_id": self.id_header,
            "sub_header_name": self.sub_header_name,
        }
        json_object = json.dumps(dictionary, indent=4)

        with open(f"{self.folder_to_create}{self.json_file_template}", "w") as file:
            file.write(json_object)
        return json_object


        # id_header = new_header_name.get('id_header')
        # header_name = new_header_name.get('header_name')
        # if id_header != self.id_header:
        #     return "No such id"
        # else:
        #     self.header_name = header_name

    @XBlock.json_handler
    def edit_sub_header(self, id_header, sub_header_old_name, sub_header_new_name):
        if id_header != self.id_header:
            return "No such id"
        else:
            for sub_header in self.sub_header_name:
                if sub_header_old_name == sub_header:
                    self.sub_header_name = list(map(lambda x: x.replace(sub_header, sub_header_new_name), self.sub_header_name))
                    return self.new_header_id()

    @XBlock.json_handler
    def delete_file_by_header(self, header_id, header_name):
        if header_id == self.id_header and header_name == self.header_name:
            return os.remove(f"{self.folder_to_create}{self.json_file_template}")

    @XBlock.json_handler
    def delete_sub_header(self, header_id, header_name, sub_header_name_to_delete):
        if header_id == self.id_header and header_name == self.header_name:
            for sub_header in self.sub_header_name:
                if sub_header_name_to_delete == sub_header:
                    self.sub_header_name.remove(sub_header_name_to_delete)

            dictionary = {
                "header_name": self.header_name,
                "header_id": self.id_header,
                "sub_header_name": self.sub_header_name,
            }

            json_object = json.dumps(dictionary, indent=4)

            with open(f"{self.folder_to_create}{self.json_file_template}", "w") as file:
                file.write(json_object)
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
#
# if __name__ == '__main__':
#     h1 = Header("Episode_1", "Sub_episode_1")
#     h1.new_header_id()
#     h1.edit_header(1, "Episode_1")
#     # h1.delete_file_by_header(1,"Episode_1")
#
#     h2 = Header("Episode_2", "Sub_episode_1")
#     h2.new_header_id()
#     # h2.edit_sub_header(2, "Sub_episode_10")
#
#     h3 = Header("Episode_3", "Sub_episode_1", "Sub_episode_2", "Sub_episode_3")
#     h3.new_header_id()
#     h3.edit_header(3, "Episode_pes")
#     h3.edit_sub_header(3, "Sub_episode_3", "Sub_episode_cho")
#     h3.new_sub_header_id(3, "Episode_pes", "Sub_episode_add_test")
#     # h3.delete_sub_header(3, "Episode_pes", "Sub_episode_cho")
#
#     h4 = Header("Episode_3", "Sub_episode_1", "Sub_episode_2")
#     h4.new_header_id()
#     h4.new_sub_header_id(4, "Episode_3", "Sub_episode_4")
#     # h4.delete_sub_header(4, "Episode_3", "Sub_episode_1")
#     h4.delete_sub_header(4, "Episode_3", "Sub_episode_2")
#     h4.delete_sub_header(4, "Episode_3", "Sub_episode_4")
