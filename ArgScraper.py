import numpy as np
import pandas as pd
import requests
import bs4
import lxml.etree as xml
import csv
import json
import re


def get_children_dicts(arg):
    children_dicts = []
    for child in arg.children_objs:
        grand_child_dicts = get_children_dicts(child)
        if child.topic != ' ':
            description = child.text.replace(child.topic, '').strip()
        else:
            description = child.text.strip()
        child_dict = {
            'type': child.type,
            'name': child.topic,
            'description': description,
            'children': grand_child_dicts
        }
        children_dicts.append(child_dict)

    return children_dicts


def map_to_json(map, file_name):
    arg = map.post_list[0]
    map_dict = {
        'type': arg.type,
        'name': arg.topic,
        'description': arg.text.replace(arg.topic, '').strip(),
        'children': get_children_dicts(arg)
    }
    with open(file_name + '.json', 'w') as outfile:
        json.dump(map_dict, outfile)


class Post:
    def __init__(self, entity, type, name, text, children):
        self.entity = entity
        self.type = type
        self.topic = name
        if str(text) != "nan" and name is not None:
            text = re.sub(r'http\S+', '', text)
            self.text = name.strip() + " " + text.strip()
        elif name is None:
            self.text = text.strip()
        else:
            self.text = name.strip()
        child_list = []
        if children is not None:
            children = str(children).strip(')')
            children = str(children).strip('(')
            child_list = children.split(' ')
        self.children_entities = child_list
        self.parent = None
        self.children_objs = []

    def initialize_parent(self, parent):
        self.parent = parent

    def initialize_children(self, children):
        self.children_objs = children


class Map:
    def __init__(self, map_name):
        self.post_list = []
        self.new_training_data = []
        self.max_traverse_steps = 0
        list_of_map_names = []

        test_df_dc = pd.read_csv(map_name, delimiter=None, header=0, engine='python')
        entities = test_df_dc.Entity.values
        types = test_df_dc.Type.values
        names = test_df_dc.Name.values
        descriptions = test_df_dc.Description.values
        children = test_df_dc.Children.values

        for entity, type, name, description, childs in zip(entities, types, names, descriptions, children):
            entity = str(entity).strip('(')
            entity = str(entity).strip(')')
            self.post_list.append(Post(entity, type, name, description, childs))
        for i in range(len(self.post_list)):
            children_objs = []
            parent = None
            for arg in self.post_list:
                if arg.entity in self.post_list[i].children_entities:
                    children_objs.append(arg)
                if self.post_list[i].entity in arg.children_entities:
                    parent = arg
                self.post_list[i].initialize_children(children_objs)
                self.post_list[i].initialize_parent(parent)


def get_arguments(debate_topic_links):
    for subpage in debate_topic_links:
        entity = 0
        all_args = []
        web_page = bs4.BeautifulSoup(requests.get(subpage, {}).text, "lxml")
        all_texts = web_page.find_all(["a", "ul"])
        titles = web_page.find_all('b')

        arg_titles = []
        for title in titles:
            arg_titles.append(title.get_text())

        first_index_children = ''
        new_idea_tracker = -1

        for arg in all_texts:
            title = arg.get('title')

            if title is not None:
                if "Edit section: " in title:
                    if '?' in title:
                        con = 0
                        if new_idea_tracker == -1:
                            all_args.append([[str(entity), 'ISSUE', title, '']])
                        else:
                            first_index_children += (str(entity) + ' ')
                            all_args.append([[str(entity), 'IDEA', title, '']])
                        entity += 1
                        new_idea_tracker += 1
                if "Edit section: No" in title:
                    con = 1

            arg_text = arg.get_text()
            tex = arg_text.split('\n')[0]

            if len(tex.split(' ')) > 30:
                if new_idea_tracker != -1:
                    for arg in arg_titles:
                        arg = arg.split('\n')[0]
                        if arg in tex:
                            title = arg
                            if not title.isspace():
                                tex = tex.replace(title, '')
                    if title is not None:
                        if con == 1:
                            all_args[new_idea_tracker].append([str(entity), 'CON', title, tex, ''])
                            entity += 1
                        else:

                            all_args[new_idea_tracker].append([str(entity), "PRO", title, tex, ''])
                            entity += 1

        if len(all_args) > 0:
            all_args[0][0].append(first_index_children.strip())

        file_name = subpage.replace('http://www.debatepedia.org/en/index.php/Debate:_', '')

        with open(file_name + '.csv', 'w', newline='') as f:
            con = 0
            writer = csv.writer(f)
            writer.writerow(['Entity', 'Type', 'Name', 'Description', 'Children'])
            for idea in all_args:

                if idea[0][1] == 'IDEA':
                    a = 0
                    children = ''
                    for argument in idea:
                        a += 1
                        if a > 1:
                            children += (str(argument[0]) + ' ')

                    idea[0].append(children)

                for argument in idea:
                    if '1.' not in argument[3]:
                        argument[2] = argument[2].replace('Edit section: ', '')
                        writer.writerow(argument)

        map = Map(file_name + '.csv')
        map_to_json(map, file_name)