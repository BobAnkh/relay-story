#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author       : BobAnkh
# @Github       : https://github.com/BobAnkh
# @Date         : 2021-02-25 22:13:02
# @LastEditTime : 2021-02-26 17:03:59
# @Description  : Main function to generate relay story

import argparse
import os
import re
import shutil
import sys
from operator import itemgetter


def get_meta_data(markdown_content, filename):
    '''
    Get meta data from content.

    Args:
        markdown_content (str): content of source markdown file
        filename (str): source markdown file name

    Returns:
        list: node, chapter_name, book_name, upstream, author
    '''
    node = os.path.splitext(filename)[0]
    chapter_name = ''
    chapter_regex = r'<!--\s*chapter\sname:\s*(.*?)-->'
    book_name = ''
    book_regex = r'<!--\s*book\sname:\s*(.*?)-->'
    upstream = ''
    upstream_regex = r'<!--\s*upstream:\s*(.*?)-->'
    author = ''
    author_regex = r'<!--\s*author:\s*(.*?)-->'
    lines = markdown_content.split('\n')
    for line in lines:
        if re.match(chapter_regex, line) and chapter_name == '':
            chapter_name = re.match(chapter_regex, line).group(1)
        if re.match(book_regex, line) and book_name == '':
            book_name = re.match(book_regex, line).group(1)
        if re.match(upstream_regex, line) and upstream == '':
            upstream = re.match(upstream_regex, line).group(1)
        if re.match(author_regex, line) and author == '':
            author = re.match(author_regex, line).group(1)
    return node, chapter_name, book_name, upstream, author


def content_process(markdown_content, chapter_name, author, node):
    '''
    Process markdown content.

    Args:
        markdown_content (str): content of source markdown file
        chapter_name (str): chapter name from meta data
        author (str): author name from meta data
        node (str): node from meta data

    Returns:
        str: processed content
    '''
    is_find = False
    lines = markdown_content.split('\n')
    for i, line in enumerate(lines):
        if re.match(r'#\s.*', line) and is_find == False:
            is_find = True
            lines[
                i] = f'# {chapter_name}' + '\n\n' + f'> Author: {author}\n>\n> Node: {node}'
        else:
            if re.match(r'#{1,6}\s.*', line):
                lines[i] = '#' + line
    result = ''
    for elem in lines:
        result += elem + '\n'
    if is_find == False:
        result = f'# {chapter_name}' + '\n\n' + f'> Author: {author}\n>\n> Node: {node}' + '\n\n' + result
    re.sub(r'^\n*', '', re.sub(r'\n*$', '', result))
    return result


def read_file(file_path, filename, content_process_func=content_process):
    '''
    Read source markdown file and process it.

    Args:
        file_path (str): source markdown file path
        filename (str): source markdown file name
        content_process_func (func, optional): function to process markdown content. Defaults to content_process.

    Returns:
        str, {chaptername, book_name, upstream, author, path, downstream, content}: processed file content
    '''
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    node, chapter_name, book_name, upstream, author = get_meta_data(
        markdown_content, filename)
    processed_content = content_process_func(markdown_content, chapter_name,
                                             author, node)
    return node, {
        'chapter_name': chapter_name,
        'book_name': book_name,
        'upstream': upstream,
        'author': author,
        'path': file_path,
        'downstream': [],
        'content': processed_content
    }


class RelayStory:
    def __init__(self, input, output, markdown, html, pdf):
        '''
        Init function of RelayStory

        Args:
            input (str): input folder path
            output (str): output folder path
            markdown (bool): whether to generate markdown story
            html (bool): whether to generate html story[Not implemented]
            pdf (bool): whether to generate pdf story[Not implemented]
        '''
        self._input_folder = input
        self._output_folder = output
        self._markdown = markdown
        self._html = html
        self._pdf = pdf
        self._head = {}
        self.roadmap = {}

    def read_raw_story(self):
        input_files = [
            x for x in os.listdir(self._input_folder) if x[-3:] == '.md'
        ]
        decorated = [(int(os.path.splitext(x)[0].split('.')[0]),
                      int(os.path.splitext(x)[0].split('.')[1]), x)
                     for x in input_files]
        decorated.sort(key=itemgetter(0, 1))
        input_files = [x for _, _, x in decorated]
        for file in input_files:
            if self._head == {} and self.roadmap == {}:
                node, meta_data = read_file(
                    os.path.join(self._input_folder, file), file)
                self._head = node
                self.roadmap[node] = meta_data
            else:
                node, meta_data = read_file(
                    os.path.join(self._input_folder, file), file)
                if meta_data['upstream'] in self.roadmap:
                    self.roadmap[meta_data['upstream']]['downstream'].append(
                        node)
                    self.roadmap[node] = meta_data
                else:
                    sys.exit('Middle node without an upstream is not allowed!')

    def _generate_markdown(self, node, content, streampath, author):
        if self.roadmap[node]['downstream'] == []:
            stream = '> RoadMap: '
            for elem in streampath:
                stream += elem + ' -> '
            stream += node
            authors = '> Authors: '
            for elem in set(author + [self.roadmap[node]['author']]):
                authors += elem + ', '
            authors = authors[:-2]
            book = f'# {self.roadmap[node]["book_name"]}' + '\n\n' + stream + '\n>\n' + authors + '\n\n' + content + '\n\n' + self.roadmap[
                node]['content'] + '\n\n'
            with open(os.path.join(
                    self._output_folder, 'markdown',
                    self.roadmap[node]['book_name'] + '(' + node + ')' +
                    '.md'),
                      'w',
                      encoding='utf-8') as f:
                f.write(book)
        else:
            for child_node in self.roadmap[node]['downstream']:
                if content == '':
                    self._generate_markdown(
                        child_node, self.roadmap[node]['content'],
                        streampath + [node],
                        author + [self.roadmap[node]['author']])
                else:
                    self._generate_markdown(
                        child_node,
                        content + '\n\n' + self.roadmap[node]['content'],
                        streampath + [node],
                        author + [self.roadmap[node]['author']])

    def markdown_story(self):
        if self._markdown:
            os.mkdir(os.path.join(self._output_folder, 'markdown'))
            self._generate_markdown(self._head, '', [], [])
        else:
            pass

    def html_story(self):
        if self._html:
            raise NotImplementedError
        else:
            pass

    def pdf_story(self):
        if self._pdf:
            raise NotImplementedError
        else:
            pass


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        help='directory contains the src markdown files. Default to story.',
        default='story')
    parser.add_argument(
        '-o',
        '--output',
        help=
        'directory to output all the generated stories. Default to output.',
        default='output')
    parser.add_argument(
        "-f",
        "--format",
        nargs='+',
        help=
        "select the output format. Options: all, markdown, html, pdf. Default to markdown.",
        default=['markdown'])
    args = parser.parse_args()
    return args


def main():
    args = argument_parser()
    if os.path.exists(args.input):
        pass
    else:
        sys.exit("Input directory does not exist!")
    if os.path.exists(args.output):
        shutil.rmtree(args.output)
        os.mkdir(args.output)
    else:
        os.mkdir(args.output)

    generate_markdown = False
    generate_html = False
    generate_pdf = False
    if 'all' in args.format:
        generate_markdown = True
        generate_html = True
        generate_pdf = True
    else:
        if 'markdown' in args.format:
            generate_markdown = True
        if 'html' in args.format:
            generate_html = True
        if 'pdf' in args.format:
            generate_pdf = True

    relaystory = RelayStory(args.input, args.output, generate_markdown,
                            generate_html, generate_pdf)
    relaystory.read_raw_story()
    relaystory.markdown_story()
    relaystory.html_story()
    relaystory.pdf_story()


if __name__ == '__main__':
    main()
